import unittest
import os
import shutil
import tempfile
import sys

# Ensure src module is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.database.db_manager import DatabaseManager
from src.agents.text_agent import TextScamDetectorAgent
from src.agents.speech_agent import SpeechAnalysisAgent
from src.agents.bot_agent import CyberShieldBotAgent
from src.agents.orchestrator import FreeAgentOrchestrator

class TestEndToEndDataIdempotency(unittest.TestCase):

    def setUp(self):
        """Set up an isolated temporary database for idempotency testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_idempotency.db")
        self.db = DatabaseManager(db_path=self.db_path)
        self.orchestrator = FreeAgentOrchestrator(db_manager=self.db)

    def tearDown(self):
        """Clean up temporary test database directory."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_backend_user_registration_idempotency(self):
        """Verify user registration returns idempotent success on retry with matching credentials."""
        # First Registration
        ok1, msg1 = self.db.register_user(
            username="testuser",
            email="testuser@example.com",
            password="SecurePassword123!",
            full_name="Test User",
            age=30,
            mobile_number="+91 9999988888",
            address="123 Security St"
        )
        self.assertTrue(ok1, f"First registration failed: {msg1}")
        self.assertIn("registered successfully", msg1)

        # Duplicate Registration (Identical details & credentials)
        ok2, msg2 = self.db.register_user(
            username="testuser",
            email="testuser@example.com",
            password="SecurePassword123!",
            full_name="Test User",
            age=30,
            mobile_number="+91 9999988888",
            address="123 Security St"
        )
        self.assertTrue(ok2, "Duplicate registration should succeed idempotently")
        self.assertIn("already registered (Idempotent response)", msg2)

    def test_backend_user_profile_update_idempotency(self):
        """Verify updating profile with identical data returns idempotent success."""
        ok, msg = self.db.register_user(
            username="profileuser",
            email="profileuser@example.com",
            password="SecurePassword123!",
            full_name="Profile User",
            age=28,
            mobile_number="+91 9876543210"
        )
        self.assertTrue(ok)

        user_data, login_msg = self.db.authenticate_user("profileuser", "SecurePassword123!")
        self.assertIsNotNone(user_data)
        user_id = user_data["user_id"]

        # Update 1: Change profile
        ok_up1, msg_up1 = self.db.update_user_profile(user_id, "Updated Name", 29, "+91 9876543210", "New Address")
        self.assertTrue(ok_up1)
        self.assertIn("updated successfully", msg_up1)

        # Update 2: Re-submit identical profile data
        ok_up2, msg_up2 = self.db.update_user_profile(user_id, "Updated Name", 29, "+91 9876543210", "New Address")
        self.assertTrue(ok_up2)
        self.assertIn("already up to date (Idempotent response)", msg_up2)

    def test_text_agent_idempotency(self):
        """Verify TextScamDetectorAgent caches and returns idempotent scan results."""
        sample_text = "URGENT: Your bank account is locked! Click http://fake-bank-verify.com now to avoid suspension."

        # Scan 1: Compute fresh analysis
        res1 = self.orchestrator.text_agent.analyze(sample_text)
        self.assertFalse(res1.get("idempotent_hit", True), "First scan must not be a cache hit")
        self.assertIn("risk_score", res1)

        # Scan 2: Duplicate scan with identical text
        res2 = self.orchestrator.text_agent.analyze(sample_text)
        self.assertTrue(res2.get("idempotent_hit", False), "Second scan MUST be an idempotent cache hit")
        self.assertEqual(res1["risk_score"], res2["risk_score"])
        self.assertEqual(res1["scam_type"], res2["scam_type"])

    def test_speech_agent_idempotency(self):
        """Verify SpeechAnalysisAgent caches and returns idempotent audio scan results."""
        sample_audio = b"SIMULATED_AUDIO_STREAM_FOR_IDEMPOTENCY_TESTING_BYTES"
        filename = "test_audio.wav"

        # Scan 1: Process audio clip
        res1 = self.orchestrator.speech_agent.analyze_audio(sample_audio, filename)
        self.assertFalse(res1.get("idempotent_hit", True), "First audio scan must not be a cache hit")
        self.assertIn("overall_voice_risk_score", res1)

        # Scan 2: Re-process identical audio clip
        res2 = self.orchestrator.speech_agent.analyze_audio(sample_audio, filename)
        self.assertTrue(res2.get("idempotent_hit", False), "Second audio scan MUST be an idempotent cache hit")
        self.assertEqual(res1["overall_voice_risk_score"], res2["overall_voice_risk_score"])
        self.assertEqual(res1["transcription"], res2["transcription"])

    def test_bot_agent_idempotency(self):
        """Verify CyberShieldBotAgent caches and returns idempotent responses for identical prompts."""
        prompt = "I shared my bank OTP with a fake caller!"

        # Query 1: Initial emergency advice
        reply1 = self.orchestrator.bot_agent.respond(prompt)
        self.assertIsNotNone(reply1)

        # Query 2: Re-query identical emergency advice
        reply2 = self.orchestrator.bot_agent.respond(prompt)
        self.assertTrue("Idempotent" in reply2 or reply1 in reply2, "Second bot query must return idempotent cached advice")

    def test_idempotency_cache_purge(self):
        """Verify clearing idempotency cache purges database records."""
        # Populate cache
        self.orchestrator.text_agent.analyze("Test message for cache purge test")
        stats_before = self.db.get_idempotency_stats()
        self.assertGreater(stats_before["total_records"], 0)

        # Clear cache
        ok, msg = self.db.clear_idempotency_cache()
        self.assertTrue(ok)
        
        stats_after = self.db.get_idempotency_stats()
        self.assertEqual(stats_after["total_records"], 0)


if __name__ == "__main__":
    unittest.main()
