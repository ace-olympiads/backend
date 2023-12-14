from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer,AccountsSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import Account

class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomAccountCreate(APIView):


    def post(self, request, *args, **kwargs):
        
        print(request.data)
        serializer=AccountsSerializer(data=request.data)
        if serializer.is_valid():
            accounts = serializer.save()
            if accounts:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        mail = request.query_params.get('email')
        print(mail)
        user=Account.objects.get(email=mail)
        serializer= AccountsSerializer(user)
        if user is not None:
                last_viewed_questions = user.last_viewed_questions.all().values()
                last_viewed_videos = user.last_viewed_concept_videos.all().values()
                question_details = list(last_viewed_questions)
                video_details = list(last_viewed_videos)
                serialized_data = serializer.data
                serialized_data['last_viewed_questions'] = question_details
                serialized_data['last_viewed_concept_videos'] = video_details
                return Response(serialized_data, status=status.HTTP_201_CREATED)
        return Response({"error": "User does not exisits"})
        

class AccountUpdateView(APIView):
    def patch(self, request, *args, **kwargs):
        mail = request.query_params.get('email')
        user = Account.objects.get(email=mail)
        
        if user is not None:
            profile_image_url = request.data.get('profile_image_url')

            if profile_image_url:
                user.image = profile_image_url
                user.save()
                
                return Response({"message": "Profile image URL updated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "No profile image URL provided"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)