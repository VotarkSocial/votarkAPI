from rest_framework import serializers

from searchedHashtag.models import SearchedHashtag

class SearchedHashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchedHashtag
        fields = (
            'id',
            'date',
            'hashtag',
            'user',
        )
