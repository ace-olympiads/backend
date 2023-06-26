from rest_framework import serializers

from users.models import Account
from .models import Question,Comment, Tag
from users.serializers import AccountsSerializer
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = '__all__'

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        question = Question.objects.create(**validated_data)
        tags = []
        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(name=tag_data['name'])
            question.tags.add(tag)
            tags.append(tag)
        return question

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', [])
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        tags = []
        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(name=tag_data['name'])
            instance.tags.add(tag)
            tags.append(tag)
        return instance



class CommentSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()
    commenter = AccountsSerializer()
    class Meta:
        model= Comment
        fields = '__all__'


class CommentPostSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    commenter = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())

    class Meta:
        model = Comment
        fields = ['question', 'commenter', 'email', 'content', 'status']