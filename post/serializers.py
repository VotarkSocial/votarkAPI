from rest_framework import serializers

from post.models import Post

class PostSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    topicname = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id',
            'image',
            'video',
            'date',
            'description',
            'order',
            'topic',
            'user',
            'victories',
            'username',
            'topicname'
        )

    def get_username(self, obj):
        return obj.user.username

    def get_topicname(self, obj):
        return obj.topic.name
