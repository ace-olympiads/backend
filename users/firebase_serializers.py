from rest_framework import serializers
from .models import Account

class FirebaseAuthSerializer(serializers.Serializer):
    """Serializer for Firebase ID token authentication"""
    id_token = serializers.CharField(max_length=2400)

class GoogleAuthSerializer(serializers.Serializer):
    """Serializer for Google OAuth authentication"""
    auth_code = serializers.CharField()
    
class EmailPasswordAuthSerializer(serializers.Serializer):
    """Serializer for email/password authentication"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
class EmailPasswordRegisterSerializer(serializers.Serializer):
    """Serializer for email/password registration"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField()
    
class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile data"""
    class Meta:
        model = Account
        fields = ['id', 'email', 'username', 'role', 'image', 'contact_no', 'created_at', 'provider']
        read_only_fields = ['id', 'email', 'created_at', 'provider']
        
class UserRoleUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user roles"""
    class Meta:
        model = Account
        fields = ['role']
