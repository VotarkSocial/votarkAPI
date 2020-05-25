from rest_framework import serializers

from searchedUser.models import SearchedUser
from votarkUser.serializers import VotarkUserSerializer

class SearchedUserSerializer(serializers.ModelSerializer):
    
    searched = serializers.SerializerMethodField()

    class Meta:
        model = SearchedUser
        fields = (
            'id',
            'date',
            'searched',
            'user',
        )

    
    def get_searched(self, obj):
        return VotarkUserSerializer(obj.searchedUser).data