from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer,AccountsSerializer
from rest_framework.permissions import AllowAny
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
        print(request.data)
        mail=request.data["email"]
        print(mail)
        user=Account.objects.get(email=mail)
        serializer= AccountsSerializer(user)
        if user is not None:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": "User doesnot exisits"})
        
        