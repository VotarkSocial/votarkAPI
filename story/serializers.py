from rest_framework import serializers

from story.models import Story

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = (
            'id',
            'content',
            'user',
        )