from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer,AccountsSerializer, ExamCardSerializer, QuestionCardSerializer, VideoCardSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import Account, ExamCard, NavbarButton, QuestionCard, VideoCard

class NavbarConfigView(APIView):
    """API endpoint to fetch navbar configuration"""
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        buttons = NavbarButton.objects.filter(is_enabled=True).order_by('order')
        
        # Structure the data to match the navbar hierarchy
        nav_structure = []
        button_dict = {}
        
        # First pass: collect all buttons
        for button in buttons:
            button_data = {
                'id': button.id,
                'name': button.name,
                'display_name': button.display_name,
                'children': []
            }
            button_dict[button.id] = button_data
            
            # Add top-level buttons
            if not button.parent:
                nav_structure.append(button_data)
        
        # Second pass: add children
        for button in buttons:
            if button.parent and button.parent.id in button_dict:
                parent = button_dict[button.parent.id]
                parent['children'].append(button_dict[button.id])
        
        return Response({
            'navbar_items': nav_structure
        }, status=status.HTTP_200_OK)
        
        

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
        
class VideoCardList(APIView):
    def get(self, request):
        data = {}
        for tab in ['Newest', 'Popular', 'Active']:
            cards = VideoCard.objects.filter(tab=tab)
            serializer = VideoCardSerializer(cards, many=True)
            data[tab] = serializer.data
        return Response(data)
    
class ExamCardListCreate(APIView):
    """List all exam cards or create a new one."""
    def get(self, request):
        cards = ExamCard.objects.all()
        serializer = ExamCardSerializer(cards, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExamCardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestionCardListCreate(APIView):
    """List all question cards or create a new one."""
    def get(self, request):
        cards = QuestionCard.objects.all()
        serializer = QuestionCardSerializer(cards, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = QuestionCardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)