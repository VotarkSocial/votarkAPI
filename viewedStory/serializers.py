from rest_framework import serializers

from viewedStory.models import ViewedStory

class ViewedStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewedStory
        fields = (
            'id',
            'story',
            'user',
        )