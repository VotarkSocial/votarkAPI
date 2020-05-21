from rest_framework import serializers

from versus.models import Versus
from post.serializers import PostSerializer
from votarkUser.serializers import VotarkUserSerializer

class VersusSerializer(serializers.ModelSerializer):
    user1 = serializers.SerializerMethodField()
    user2 = serializers.SerializerMethodField()
    content1 = serializers.SerializerMethodField()
    content2 = serializers.SerializerMethodField()
    

    class Meta:
        model = Versus
        fields = (
            'id',
            'date',
            'post1',
            'post2',
            'user1',
            'user2',
            'content1',
            'content2',
        )

    def get_user1(self, obj):
        return VotarkUserSerializer(obj.post1.user).data

    def get_user2(self, obj):
        return VotarkUserSerializer(obj.post2.user).data

    def get_content1(self, obj):
        return PostSerializer(obj.post1).data

    def get_content2(self, obj):
        return PostSerializer(obj.post2).data
