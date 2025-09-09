import pytest
import requests

BASE_URL = "http://localhost:8000"

@pytest.fixture(scope="session")
def student_user_client():
    """
        This fixture sets up a test client for a student user.
    """
    headers = {"X-User-Type": "student"}

    # simulate getting the student user's profile
    response = requests.get(f"{BASE_URL}/profile", headers=headers)