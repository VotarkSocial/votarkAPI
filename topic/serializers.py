from rest_framework import serializers

from topic.models import Topic
from hashtag.models import Hashtag
from hashtag.serializers import HashtagSerializer

class TopicSerializer(serializers.ModelSerializer):
    hashtags = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = (
            'id',
            'name',
            'privacity',
            'creator',
            'hashtags'
        )


    def get_hashtags(self, obj):
        response = []
        for hashtag in Hashtag.objects.filter(topic=obj.id):
            response.append(HashtagSerializer(hashtag).data)
        return response