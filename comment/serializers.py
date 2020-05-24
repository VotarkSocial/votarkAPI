from rest_framework import serializers

from comment.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            'id',
            'content',
            'date',
            'post',
            'user',
            'username',
            'versus',
        )

    def get_username(self, obj):
        return obj.user.username
