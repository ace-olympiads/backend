from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Question
from .serializers import QuestionSerializer
from rest_framework.permissions import IsAuthenticated

class QuestionListCreateView(APIView):
    serializer_class = QuestionSerializer

    def get(self, request):
        questions = Question.objects.all()
        serializer = self.serializer_class(questions, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        print(data)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestionRetrieveUpdateDestroyView(APIView):
    serializer_class = QuestionSerializer

    def get(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        serializer = self.serializer_class(question)
        return Response(serializer.data)

    def put(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        data = request.data
        data["author"] = request.user.id
        serializer = self.serializer_class(question, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class AddRecentlyVisitedQuestionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        question_id = request.data.get('question_id')
        user.add_recently_visited_question(question_id)
        return Response({'message': 'Recently visited question added'})
    
class RecentlyVisitedQuestionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        question_ids = user.recently_visited_questions
        questions = Question.objects.filter(id__in=question_ids)
        serialized_questions = [question.to_json() for question in questions]
        return Response({'recently_visited_questions': serialized_questions})