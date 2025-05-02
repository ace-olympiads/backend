from rest_framework import serializers
from users.models import ExamCard, NewUser,Account, NavbarButton, QuestionCard, VideoCard

class NavbarButtonSerializer(serializers.ModelSerializer):
    class Meta:
        model = NavbarButton
        fields = ['id', 'name', 'display_name', 'is_enabled', 'order']


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = NewUser
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
 
 
class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields ='__all__'

class VideoCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoCard
        fields = '__all__'
        
class ExamCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamCard
        fields = ['id', 'title', 'description', 'icon', 'width', 'height']
        
class QuestionCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionCard
        fields = ['id', 'question_text', 'question_subtext', 'image', 'tabs']
    
