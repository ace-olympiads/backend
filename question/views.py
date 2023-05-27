from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.views import View
from django.shortcuts import get_object_or_404
from .models import Question
from .serializers import QuestionSerializer

class AddQuestionView(APIView):
    permission_classes = (IsAuthenticated, )
    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.save()
            return JsonResponse({'success': True, 'question_id': question.id})
        else:
            return JsonResponse({'success': False, 'errors': serializer.errors})


class QuestionDetailView(View):
    permission_classes = (IsAuthenticated, )
    
    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        serializer = QuestionSerializer(question)
        return JsonResponse(serializer.data)

class QuestionListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return JsonResponse(serializer.data, safe=False)