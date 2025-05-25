import firebase_admin
from firebase_admin import credentials, auth
import os
from pathlib import Path

# Get the base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Path to the service account key file
# You should place your Firebase service account key file in a secure location
# and reference it here
FIREBASE_SERVICE_ACCOUNT_KEY_PATH = os.path.join(BASE_DIR, 'firebase-service-account-key.json')

# Flag to track initialization status
firebase_initialized = False

def initialize_firebase():
    """Initialize the Firebase Admin SDK"""
    global firebase_initialized
    
    # Only initialize if not already initialized
    if not firebase_initialized:
        try:
            # Check if Firebase is already initialized
            try:
                # This will raise an exception if no app exists
                firebase_admin.get_app()
                print("Firebase Admin SDK already initialized")
                firebase_initialized = True
                return True
            except ValueError:
                # No app exists, so initialize
                cred = credentials.Certificate(FIREBASE_SERVICE_ACCOUNT_KEY_PATH)
                firebase_admin.initialize_app(cred)
                firebase_initialized = True
                print("Firebase Admin SDK initialized successfully")
                return True
        except Exception as e:
            print(f"Error initializing Firebase Admin SDK: {e}")
            return False
    return True

# Initialize Firebase when this module is imported
initialize_firebase()
