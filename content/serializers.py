from rest_framework import serializers

from .models import KnowledgeBase


class KnowledgeBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = KnowledgeBase
        fields = ["id", "topic", "title", "grade", "content"]

    def validate_content(self, value):
        if not value.name.endswith('.txt'):
            raise serializers.ValidationError("Only .txt files are allowed.")
        return value

    def create(self, validated_data):
        return KnowledgeBase.objects.create(**validated_data)
