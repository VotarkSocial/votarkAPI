from rest_framework import serializers

from hashtag.models import Hashtag

class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = (
            'id',
            'content',
            'topic',
        )
