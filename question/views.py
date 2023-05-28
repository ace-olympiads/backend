from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Question
from .serializers import QuestionSerializer

class QuestionListCreateView(APIView):
    serializer_class = QuestionSerializer

    def get(self, request):
        questions = Question.objects.all()
        serializer = self.serializer_class(questions, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        data["author"] = request.user.id
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