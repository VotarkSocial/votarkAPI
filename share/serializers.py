from rest_framework import serializers

from share.models import Share

class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Share
        fields = (
            'id',
            'date',
            'post',
            'versus',
        )