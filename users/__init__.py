# Import Firebase configuration to initialize the SDK
try:
    from .firebase_config import initialize_firebase
    # This will ensure Firebase is initialized when the app starts
except Exception as e:
    print(f"Error importing Firebase configuration: {e}")