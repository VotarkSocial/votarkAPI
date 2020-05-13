from rest_framework import serializers

from vote.models import Vote

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = (
            'id',
            'date',
            'user',
            'versus',
            'winner',
        )