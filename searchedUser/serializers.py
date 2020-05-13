from rest_framework import serializers

from searchedUser.models import SearchedUser

class SearchedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchedUser
        fields = (
            'id',
            'date',
            'searchedUser',
            'user',
        )