from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from src.database.db_manager import DatabaseManager

app = FastAPI(
    title="Cyber Fraud Shield User API",
    description="FastAPI REST service for user registration, authentication, and profile table management.",
    version="1.0.0",
)

db_manager = DatabaseManager()


class UserRegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    full_name: str
    age: int = 25
    mobile_number: str
    address: Optional[str] = ""


class UserLoginRequest(BaseModel):
    username_or_email: str
    password: str


@app.post("/api/users/register")
def register_user(req: UserRegisterRequest):
    """
    Registers a new user and creates their personal profile record in SQLite database tables.
    """
    success, message = db_manager.register_user(
        username=req.username,
        email=req.email,
        password=req.password,
        full_name=req.full_name,
        age=req.age,
        mobile_number=req.mobile_number,
        address=req.address or "",
    )
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    # Auto authenticate to return profile
    user_data, _ = db_manager.authenticate_user(req.username, req.password)
    return {
        "status": "success",
        "message": message,
        "user": user_data,
    }


@app.post("/api/users/login")
def login_user(req: UserLoginRequest):
    """
    Authenticates user against SQLite database tables using PBKDF2 salted hash.
    """
    user_data, message = db_manager.authenticate_user(req.username_or_email, req.password)
    if not user_data:
        raise HTTPException(status_code=401, detail=message)
    
    return {
        "status": "success",
        "message": message,
        "user": user_data,
    }


@app.get("/api/users/profile/{user_id}")
def get_profile(user_id: int):
    """
    Retrieves user personal details from SQLite user_profiles table.
    """
    profile = db_manager.get_user_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found.")
    
    return {
        "status": "success",
        "profile": dict(profile),
    }
