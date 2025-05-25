from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .firebase_serializers import (
    FirebaseAuthSerializer, 
    GoogleAuthSerializer, 
    EmailPasswordAuthSerializer, 
    EmailPasswordRegisterSerializer,
    UserProfileSerializer,
    UserRoleUpdateSerializer
)
from .firebase_auth import (
    verify_firebase_token, 
    create_or_update_user, 
    exchange_token_with_firebase,
    sign_in_with_email_password,
    create_user_with_email_password
)
from .models import Account
from django.shortcuts import get_object_or_404

class FirebaseTokenAuthView(APIView):
    """
    Authenticate a user with a Firebase ID token
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = FirebaseAuthSerializer(data=request.data)
        if serializer.is_valid():
            id_token = serializer.validated_data['id_token']
            
            # Verify the token with Firebase
            decoded_token = verify_firebase_token(id_token)
            if not decoded_token:
                return Response(
                    {"error": "Invalid Firebase token"}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # Create or update user in our database
            user = create_or_update_user(decoded_token)
            if not user:
                return Response(
                    {"error": "Failed to create or update user"}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserProfileSerializer(user).data
            }, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GoogleAuthView(APIView):
    """
    Authenticate a user with Google OAuth
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        if serializer.is_valid():
            auth_code = serializer.validated_data['auth_code']
            
            # Exchange the auth code for Firebase tokens
            firebase_data = exchange_token_with_firebase(auth_code)
            if not firebase_data or 'idToken' not in firebase_data:
                return Response(
                    {"error": "Failed to authenticate with Google"}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # Verify the token with Firebase
            id_token = firebase_data['idToken']
            decoded_token = verify_firebase_token(id_token)
            if not decoded_token:
                return Response(
                    {"error": "Invalid Firebase token"}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # Create or update user in our database
            user = create_or_update_user(decoded_token, provider='google')
            if not user:
                return Response(
                    {"error": "Failed to create or update user"}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserProfileSerializer(user).data
            }, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmailPasswordLoginView(APIView):
    """
    Login with email and password
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Print the raw request data for debugging
        print(f"Request data: {request.data}")
        
        # Check if id_token is in the request data
        if 'id_token' not in request.data:
            print("Warning: id_token not found in request data")
            print(f"Available keys: {request.data.keys()}")
            
            # Check if idToken is used instead (camelCase vs snake_case)
            if 'idToken' in request.data:
                request.data['id_token'] = request.data['idToken']
                print("Found idToken, converting to id_token")
        
        serializer = FirebaseAuthSerializer(data=request.data)
        if serializer.is_valid():
            id_token = serializer.validated_data['id_token']
            print(f"Token length: {len(id_token)}")
            print(f"Token prefix: {id_token[:20]}...")
            
            # Verify the token with Firebase
            decoded_token = verify_firebase_token(id_token)
            if not decoded_token:
                print("Token verification failed")
                return Response(
                    {"error": "Invalid Firebase token"}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # Create or update user in our database
            user = create_or_update_user(decoded_token, provider='password')
            if not user:
                return Response(
                    {"error": "Failed to create or update user"}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserProfileSerializer(user).data
            }, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmailPasswordRegisterView(APIView):
    """
    Register with email and password
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Print the raw request data for debugging
        print(f"Register request data: {request.data}")
        
        # Check if id_token is in the request data
        if 'id_token' not in request.data and 'idToken' in request.data:
            request.data['id_token'] = request.data['idToken']
            print("Found idToken, converting to id_token for registration")
            
        serializer = EmailPasswordRegisterSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            id_token = request.data.get('id_token')
            
            # Check if user already exists
            if Account.objects.filter(email=email).exists():
                return Response(
                    {"error": "User with this email already exists"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Verify the token with Firebase
            if not id_token:
                print("No ID token provided for registration")
                return Response(
                    {"error": "Firebase ID token is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            print(f"Registration token length: {len(id_token)}")
            print(f"Registration token prefix: {id_token[:20]}...")
                
            decoded_token = verify_firebase_token(id_token)
            if not decoded_token:
                print("Registration token verification failed")
                return Response(
                    {"error": "Invalid Firebase token"}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # Create user in our database
            firebase_uid = decoded_token['uid']
            user = Account.objects.create(
                email=email,
                username=username,
                firebase_uid=firebase_uid,
                provider='password',
                role='common'  # Default role
            )
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserProfileSerializer(user).data
            }, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    """
    Get or update user profile
    No authentication required - completely open access
    """
    permission_classes = [AllowAny]
    
    def get(self, request, user_id=None):
        email = request.query_params.get('email')
        
        if user_id:
            # Get specific user by ID
            user = get_object_or_404(Account, id=user_id)
        elif email:
            # Get specific user by email
            user = get_object_or_404(Account, email=email)
        else:
            # List all users if no specific user requested
            users = Account.objects.all()
            serializer = UserProfileSerializer(users, many=True)
            return Response(serializer.data)
        
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    
    def put(self, request, user_id=None):
        email = request.query_params.get('email')
        
        if user_id:
            # Update specific user by ID
            user = get_object_or_404(Account, id=user_id)
        elif email:
            # Update specific user by email
            user = get_object_or_404(Account, email=email)
        else:
            return Response(
                {"error": "Either user_id or email parameter is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRoleUpdateView(APIView):
    """
    Update user role (admin only)
    """
    permission_classes = [AllowAny]  # As per client's request to not restrict any API
    
    def put(self, request, user_id):
        user = get_object_or_404(Account, id=user_id)
        serializer = UserRoleUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
