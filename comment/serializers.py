from rest_framework import serializers

from comment.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'id',
            'content',
            'date',
            'post',
            'user',
            'versus',
        )