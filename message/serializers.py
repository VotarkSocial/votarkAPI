from rest_framework import serializers

from message.models import Message

class MessageSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = (
            'id',
            'chat',
            'content',
            'date',
            'user',
            'username',
        )

    def get_username(self, obj):
        return obj.user.username

    
