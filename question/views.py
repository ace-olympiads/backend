import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import boto3
from django.shortcuts import get_object_or_404
from django.conf import settings
from users.models import Account
from .models import Examination, Question, Comment, Tag
from .serializers import CommentPostSerializer, ExaminationSerializer, QuestionSerializer, CommentSerializer, TagSerializer, ImageUploadSerializer
from django.db.models import Q

class ImageUploadView(APIView):
    serializer_class = ImageUploadSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data["file"]

            # Initialize the S3 client using boto3
            s3 = boto3.client(
                "s3",
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME,
            )

            # Generate a unique filename for the uploaded file
            file_extension = file.name.split(".")[-1]
            filename = f"{uuid.uuid4()}.{file_extension}"
            key = f"uploads/{filename}"

            try:
                # Upload the file to S3 with public-read ACL
                s3.upload_fileobj(
                    file,
                    settings.AWS_S3_BUCKET_NAME,
                    key,
                    ExtraArgs={
                        "ACL": "public-read",
                        "ContentType": file.content_type,
                    },
                )
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Construct the public URL for the uploaded file
            file_url = f"https://{settings.AWS_S3_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{key}"
            return Response({"fileUrl": file_url}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class QuestionListCreateView(APIView):
    serializer_class = QuestionSerializer

    def get(self, request):
        questions = Question.objects.all()
        serializer = self.serializer_class(questions, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        print(data)
        email = data.get('email')
        
        if not email:
            return Response(
                {"error": "Author email is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            account = Account.objects.get(email=email)
            if account.role != 'manager':
                return Response(
                    {"error": "Only managers can create questions"},
                    status=status.HTTP_403_FORBIDDEN
                )
        except Account.DoesNotExist:
            return Response(
                {"error": "Account not found"},
                status=status.HTTP_404_NOT_FOUND
            )
            
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            question = serializer.save(author=account)
            serialized_data = serializer.data
            serialized_data['tags'] = list(
                question.tags.values_list('name', flat=True))
            return Response(serialized_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionRetrieveUpdateDestroyView(APIView):
    serializer_class = QuestionSerializer

    def get(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        serializer = self.serializer_class(question)
        email = request.data.get('email')
        if email:
            user = get_object_or_404(Account, email=email)
            user.last_viewed_questions.add(question)

            if user.last_viewed_questions.count() > 10:
                user.last_viewed_questions.remove(
                    user.last_viewed_questions.earliest('created_at')
                )
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

class UserCommentsView(APIView):
    serializer_class = CommentSerializer

    def get(self, request, email):
        comments = Comment.objects.select_related('commenter').filter(email=email)
        serializer = self.serializer_class(comments, many=True)
        return Response(serializer.data)
    

class CommentsView(APIView):
    serializer_class = CommentSerializer

    def get(self, request, id):
        comments = Comment.objects.select_related(
            'commenter').all().filter(question=id).order_by('id')
        serializer = self.serializer_class(comments, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = CommentPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        comment = get_object_or_404(Comment, pk=id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TagListAPIView(APIView):
    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)


class QuestionByTagView(APIView):
    def get(self, request, tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            return Response({"error": "Tag not found"}, status=404)

        questions = Question.objects.filter(tags=tag)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


class SearchAPIView(APIView):
    def get(self, request):
        query = request.query_params.get('query', '')
        results = self.search(query)
        return Response(results)

    def search(self, query):
        results = []
        if query:
            search_results = Question.objects.filter(
                Q(question_text__icontains=query) | Q(
                    text_solution__icontains=query) | Q(
                    text_solution_latex__icontains=query) | Q(
                    question_text_latex__icontains=query)
            )
            for question in search_results:
                result = {
                    'id': question.id,
                    'title': question.question_text,
                    'question_latex': question.question_text_latex,
                    'solution': question.text_solution,
                    'solution_latex': question.text_solution_latex
                }
                results.append(result)
        return results

class ExaminationListAPIView(APIView):
    def get(self, request):
        examinations = Examination.objects.all()
        serializer = ExaminationSerializer(examinations, many=True)
        return Response(serializer.data)

class QuestionByExaminationView(APIView):
    def get(self, request, examination_id):
        try:
            examination = Examination.objects.get(id=examination_id)
        except Examination.DoesNotExist:
            return Response({"error": "Examination not found"}, status=404)

        questions = Question.objects.filter(examinations=examination)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)