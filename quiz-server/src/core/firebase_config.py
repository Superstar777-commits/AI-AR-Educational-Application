from fastapi import HTTPException
from src.core.config import settings
import firebase_admin
from firebase_admin import credentials, auth
import json

# Get the Firebase service account json from env variables
service_account_str = settings.FIREBASE_SERVICE_ACCOUNT
if not service_account_str:
    raise RuntimeError("FIREBASE_SERVICE_ACCOUNT env variable is not set. Please set it to the content of your service account JSON file.")

try:
    # Decode the JSON string into a dictionary
    service_account_info = json.loads(service_account_str)

    # initialize Firebase Admin SDK
    cred = credentials.Certificate(service_account_info)
    firebase_admin.initialize_app(cred)
    print("Firebase Admin SDK initialized successfully")
except Exception as e:
    raise RuntimeError(f"Failed to initialize Firebase Admin SDK: {e}")