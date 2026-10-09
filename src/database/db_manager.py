import sqlite3
import os
import secrets
import hashlib
import json
from contextlib import contextmanager
from typing import Dict, Any, Optional, Tuple

class DatabaseManager:
    """
    Thread-safe SQLite Database Manager for Cyber Fraud Shield.
    Handles user authentication (salted PBKDF2 SHA-256 password hashing),
    user personal profile records, and end-to-end data idempotency management
    for both backend operations and AI agents.
    """

    def __init__(self, db_path: str | None = None):
        if db_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_path = os.path.join(base_dir, "cyber_shield.db")
        
        self.db_path = db_path
        self.init_db()

    @contextmanager
    def _get_connection(self):
        """Establishes a database connection with PRAGMA foreign_keys enabled and ensures connection is closed on exit."""
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        try:
            yield conn
        finally:
            conn.close()

    def init_db(self):
        """Creates database tables if they do not exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Table 1: users (User accounts credentials)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

            # Table 2: user_profiles (User personal details)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id INTEGER PRIMARY KEY,
                full_name TEXT NOT NULL,
                age INTEGER NOT NULL,
                mobile_number TEXT NOT NULL,
                address TEXT DEFAULT "",
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """)

            # Table 3: idempotency_records (Data Idempotency cache for Backend & Agents)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS idempotency_records (
                idempotency_key TEXT PRIMARY KEY,
                request_hash TEXT NOT NULL,
                scope TEXT NOT NULL,
                response_json TEXT NOT NULL,
                status_code INTEGER DEFAULT 200,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

            # Table 4: idempotent_scan_history (Unique scan logs for incident deduplication)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS idempotent_scan_history (
                scan_hash TEXT PRIMARY KEY,
                scan_type TEXT NOT NULL,
                input_summary TEXT NOT NULL,
                result_json TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)
            conn.commit()

    def drop_all_tables(self) -> bool:
        """Drops all tables from the database."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("PRAGMA foreign_keys = OFF;")
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
                tables = [row["name"] for row in cursor.fetchall()]
                for table in tables:
                    cursor.execute(f"DROP TABLE IF EXISTS {table};")
                conn.commit()
                return True
        except Exception as e:
            print(f"[DatabaseManager] Error dropping tables: {e}")
            return False

    def generate_idempotency_key(self, payload: Any, prefix: str = "") -> str:
        """
        Generates a deterministic SHA-256 idempotency key for any string, bytes, or dict payload.
        """
        if isinstance(payload, bytes):
            data_bytes = payload
        elif isinstance(payload, dict):
            data_bytes = json.dumps(payload, sort_keys=True).encode("utf-8")
        else:
            data_bytes = str(payload).strip().encode("utf-8")
        
        digest = hashlib.sha256(data_bytes).hexdigest()
        return f"{prefix}:{digest}" if prefix else digest

    def get_idempotent_record(self, idempotency_key: str, scope: str = "") -> Optional[Dict[str, Any]]:
        """
        Retrieves cached response dict for an idempotency key if available.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if scope:
                cursor.execute(
                    "SELECT response_json, created_at FROM idempotency_records WHERE idempotency_key = ? AND scope = ?",
                    (idempotency_key, scope)
                )
            else:
                cursor.execute(
                    "SELECT response_json, created_at FROM idempotency_records WHERE idempotency_key = ?",
                    (idempotency_key,)
                )
            
            row = cursor.fetchone()
            if row:
                try:
                    data = json.loads(row["response_json"])
                    data["idempotent_hit"] = True
                    data["idempotency_key"] = idempotency_key
                    data["cached_at"] = row["created_at"]
                    return data
                except Exception:
                    pass
        return None

    def save_idempotent_record(
        self,
        idempotency_key: str,
        request_hash: str,
        scope: str,
        response_data: Dict[str, Any],
        status_code: int = 200
    ) -> bool:
        """
        Stores an operation response idempotently. Uses INSERT OR REPLACE for atomicity.
        """
        try:
            # Ensure idempotent flags in stored data
            data_to_store = dict(response_data)
            data_to_store.pop("idempotent_hit", None)
            
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO idempotency_records (idempotency_key, request_hash, scope, response_json, status_code)
                    VALUES (?, ?, ?, ?, ?)
                """, (idempotency_key, request_hash, scope, json.dumps(data_to_store), status_code))
                conn.commit()
                return True
        except Exception as e:
            print(f"[DatabaseManager] Failed to save idempotency record: {e}")
            return False

    def clear_idempotency_cache(self, scope: Optional[str] = None) -> Tuple[bool, str]:
        """Purges cached idempotency records from database."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                if scope:
                    cursor.execute("DELETE FROM idempotency_records WHERE scope = ?", (scope,))
                else:
                    cursor.execute("DELETE FROM idempotency_records;")
                deleted_count = cursor.rowcount
                conn.commit()
                return True, f"Purged {deleted_count} idempotency cache records."
        except Exception as e:
            return False, f"Failed to clear cache: {e}"

    def get_idempotency_stats(self) -> Dict[str, Any]:
        """Returns statistics on active idempotency cache records across scopes."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT scope, COUNT(*) as count FROM idempotency_records GROUP BY scope")
            rows = cursor.fetchall()
            stats_by_scope = {row["scope"]: row["count"] for row in rows}
            
            cursor.execute("SELECT COUNT(*) as total FROM idempotency_records")
            total = cursor.fetchone()["total"]
            return {"total_records": total, "by_scope": stats_by_scope}

    def _hash_password(self, password: str, salt: bytes | None = None) -> Tuple[str, str]:
        """Hashes password using PBKDF2-HMAC-SHA256 with 100,000 iterations."""
        if salt is None:
            salt = secrets.token_bytes(16)
        
        pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return pwd_hash.hex(), salt.hex()

    def _verify_password(self, password: str, password_hash_hex: str, salt_hex: str) -> bool:
        """Verifies candidate password against stored salt and hash."""
        salt = bytes.fromhex(salt_hex)
        pwd_hash_hex, _ = self._hash_password(password, salt)
        return secrets.compare_digest(pwd_hash_hex, password_hash_hex)

    def register_user(
        self,
        username: str,
        email: str,
        password: str,
        full_name: str,
        age: int,
        mobile_number: str,
        address: str = ""
    ) -> Tuple[bool, str]:
        """
        Registers a new user idempotently inside a single SQL transaction.
        If identical details are submitted multiple times, returns an idempotent success message.
        """
        username = username.strip()
        email = email.strip().lower()
        full_name = full_name.strip()
        mobile_number = mobile_number.strip()

        if not username or not email or not password or not full_name or not mobile_number:
            return False, "All required fields (username, email, password, full name, mobile number) must be filled."

        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Check for existing username or email
                cursor.execute("""
                    SELECT u.id, u.username, u.email, u.password_hash, u.salt, p.full_name, p.mobile_number
                    FROM users u
                    LEFT JOIN user_profiles p ON u.id = p.user_id
                    WHERE LOWER(u.username) = ? OR LOWER(u.email) = ?
                """, (username.lower(), email))
                
                existing = cursor.fetchone()
                if existing:
                    # Idempotency check: if credentials match, return idempotent success
                    if self._verify_password(password, existing["password_hash"], existing["salt"]):
                        return True, "Account is already registered (Idempotent response). Please log in."
                    return False, "Username or Email is already registered with different credentials."

                # New User insertion
                pwd_hash, salt_hex = self._hash_password(password)
                cursor.execute(
                    "INSERT INTO users (username, email, password_hash, salt) VALUES (?, ?, ?, ?)",
                    (username, email, pwd_hash, salt_hex)
                )
                user_id = cursor.lastrowid

                # Insert into user_profiles table
                cursor.execute(
                    "INSERT INTO user_profiles (user_id, full_name, age, mobile_number, address) VALUES (?, ?, ?, ?, ?)",
                    (user_id, full_name, age, mobile_number, address)
                )
                conn.commit()
                return True, "Account registered successfully! Please log in."
        except sqlite3.IntegrityError as e:
            return False, f"Database Integrity Error: {e}"
        except Exception as e:
            return False, f"Registration failed: {e}"

    def authenticate_user(self, username_or_email: str, password: str) -> Tuple[Optional[Dict[str, Any]], str]:
        """
        Authenticates user by username or email.
        Returns (user_dict_or_None, status_message).
        """
        identifier = username_or_email.strip().lower()
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.id, u.username, u.email, u.password_hash, u.salt,
                       p.full_name, p.age, p.mobile_number, p.address
                FROM users u
                JOIN user_profiles p ON u.id = p.user_id
                WHERE LOWER(u.username) = ? OR LOWER(u.email) = ?
            """, (identifier, identifier))
            
            row = cursor.fetchone()
            if not row:
                return None, "Invalid Username/Email or Password."

            if self._verify_password(password, row["password_hash"], row["salt"]):
                user_data = {
                    "user_id": row["id"],
                    "username": row["username"],
                    "email": row["email"],
                    "full_name": row["full_name"],
                    "age": row["age"],
                    "mobile_number": row["mobile_number"],
                    "address": row["address"]
                }
                return user_data, "Login successful!"

            return None, "Invalid Username/Email or Password."

    def get_user_profile(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves user profile by user_id."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.id, u.username, u.email, u.created_at,
                       p.full_name, p.age, p.mobile_number, p.address, p.updated_at
                FROM users u
                JOIN user_profiles p ON u.id = p.user_id
                WHERE u.id = ?
            """, (user_id,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None

    def update_user_profile(
        self,
        user_id: int,
        full_name: str,
        age: int,
        mobile_number: str,
        address: str
    ) -> Tuple[bool, str]:
        """
        Updates personal details in user_profiles table idempotently.
        If data is unchanged, returns an idempotent success message without mutating database timestamps.
        """
        try:
            clean_name = full_name.strip()
            clean_mobile = mobile_number.strip()
            clean_address = address.strip()

            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT full_name, age, mobile_number, address FROM user_profiles WHERE user_id = ?", (user_id,))
                current = cursor.fetchone()
                
                if current:
                    if (
                        current["full_name"] == clean_name and
                        current["age"] == age and
                        current["mobile_number"] == clean_mobile and
                        (current["address"] or "") == clean_address
                    ):
                        return True, "Profile is already up to date (Idempotent response)."

                cursor.execute("""
                    UPDATE user_profiles
                    SET full_name = ?, age = ?, mobile_number = ?, address = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                """, (clean_name, age, clean_mobile, clean_address, user_id))
                conn.commit()
                return True, "Profile updated successfully!"
        except Exception as e:
            return False, f"Failed to update profile: {e}"

