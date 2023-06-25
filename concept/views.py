from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.models import Account
from .models import Concept, Video
from .serializers import ConceptSerializer, VideoSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

class ConceptListCreateView(APIView):
    def get(self, request):
        concepts = Concept.objects.all()
        serializer = ConceptSerializer(concepts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ConceptSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConceptRetrieveUpdateDestroyView(APIView):
    def get(self, request, concept_id):
        concept = get_object_or_404(Concept, pk=concept_id)
        serializer = ConceptSerializer(concept)
        return Response(serializer.data)

    def put(self, request, concept_id):
        concept = get_object_or_404(Concept, pk=concept_id)
        serializer = ConceptSerializer(concept, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, concept_id):
        concept = get_object_or_404(Concept, pk=concept_id)
        concept.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class VideoListCreateView(APIView):
    def get(self, request, concept_id):
        concept = get_object_or_404(Concept, pk=concept_id)
        videos = concept.videos.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)

    def post(self, request, concept_id):
        data=request.data
        data["concept"] = concept_id
        serializer = VideoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VideoRetrieveUpdateDestroyView(APIView):
    def get_video(self, concept_id, video_id):
        concept = get_object_or_404(Concept, pk=concept_id)
        video = get_object_or_404(Video, pk=video_id, concept=concept)
        return video

    def get(self, request, concept_id, video_id):
        video = self.get_video(concept_id, video_id)
        serializer = VideoSerializer(video)
        email = request.data.get('email')
        if email:
            user = get_object_or_404(Account, email=email)
            user.last_viewed_concept_videos.add(video)
            if user.last_viewed_concept_videos.count() > 10:
                user.last_viewed_concept_videos.remove(
                    user.last_viewed_concept_videos.earliest('created_at')
                )
        return Response(serializer.data)

    def put(self, request, concept_id, video_id):
        video = self.get_video(concept_id, video_id)
        data=request.data
        data["concept"] = concept_id
        serializer = VideoSerializer(video, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, concept_id, video_id):
        video = self.get_video(concept_id, video_id)
        video.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)