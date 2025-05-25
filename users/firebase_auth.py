import firebase_admin
from firebase_admin import auth
from rest_framework import status
from rest_framework.response import Response
from .models import Account
from django.conf import settings
import requests
import json

def verify_firebase_token(id_token):
    """
    Verify the Firebase ID token and return the decoded token
    """
    try:
        # Ensure Firebase is initialized
        from .firebase_config import initialize_firebase
        if not initialize_firebase():
            print("Failed to initialize Firebase before token verification")
            return None
            
        # Verify the ID token with Firebase Admin SDK
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        print(f"Firebase token verification error: {str(e)}")
        # Check if token is in correct format
        if not id_token or not isinstance(id_token, str):
            print(f"Invalid token format: {type(id_token)}")
        elif len(id_token) < 20:  # Simple length check
            print(f"Token seems too short: {id_token}")
        return None

def get_firebase_user_info(firebase_uid):
    """
    Get user information from Firebase using the UID
    """
    try:
        user = auth.get_user(firebase_uid)
        return user
    except Exception as e:
        return None

def create_or_update_user(decoded_token, provider='firebase'):
    """
    Create or update a user in the database based on Firebase authentication
    """
    try:
        firebase_uid = decoded_token['uid']
        email = decoded_token.get('email', '')
        name = decoded_token.get('name', '')
        if not name:
            name = email.split('@')[0]  # Use part of email as name if not provided
        
        picture = decoded_token.get('picture', '')
        
        # Check if user already exists with this Firebase UID
        try:
            user = Account.objects.get(firebase_uid=firebase_uid)
            # Update existing user
            user.email = email
            user.username = name
            user.image = picture
            user.provider = provider
            user.save()
        except Account.DoesNotExist:
            # Check if user exists with this email
            try:
                user = Account.objects.get(email=email)
                # Update existing user with Firebase UID
                user.firebase_uid = firebase_uid
                user.username = name
                user.image = picture
                user.provider = provider
                user.save()
            except Account.DoesNotExist:
                # Create new user
                user = Account.objects.create(
                    email=email,
                    username=name,
                    firebase_uid=firebase_uid,
                    image=picture,
                    provider=provider,
                    role='common'  # Default role
                )
        
        return user
    except Exception as e:
        print(f"Error creating/updating user: {e}")
        return None

def exchange_token_with_firebase(auth_code):
    """
    Exchange authorization code for Firebase tokens
    Used for OAuth flows
    """
    try:
        api_key = settings.FIREBASE_WEB_API_KEY
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithIdp?key={api_key}"
        
        payload = {
            "postBody": f"id_token={auth_code}&providerId=google.com",
            "requestUri": "http://localhost:3000",
            "returnIdpCredential": True,
            "returnSecureToken": True
        }
        
        response = requests.post(url, data=json.dumps(payload))
        return response.json()
    except Exception as e:
        print(f"Error exchanging token: {e}")
        return None

def sign_in_with_email_password(email, password):
    """
    Sign in with email and password using Firebase REST API
    """
    try:
        api_key = settings.FIREBASE_WEB_API_KEY
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
        
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        
        response = requests.post(url, data=json.dumps(payload))
        return response.json()
    except Exception as e:
        print(f"Error signing in with email/password: {e}")
        return None

def create_user_with_email_password(email, password):
    """
    Create a new user with email and password using Firebase REST API
    """
    try:
        api_key = "AIzaSyByt-cG289YqD95Ps5GO3JpqOC8W88I3HU"
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}"
        
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        
        response = requests.post(url, data=json.dumps(payload))
        result = response.json()
        
        # Log detailed information about the response
        if not response.ok:
            error_message = result.get('error', {}).get('message', 'Unknown error')
            print(f"Firebase user creation failed: {error_message}")
            print(f"Full response: {result}")
            
            # Return the error details for better debugging
            return {
                'error': error_message,
                'details': result.get('error', {}),
                'status_code': response.status_code
            }
            
        return result
    except Exception as e:
        print(f"Error creating user with email/password: {e}")
        return None
