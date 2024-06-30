from rest_framework import serializers
from .models import Concept, Video

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'concept','description','title', 'youtube_url', 'thumbnail_url', 'author']

class ConceptSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True, read_only=True)

    class Meta:
        model = Concept
        fields = ['id', 'title', 'description', 'videos','category']
