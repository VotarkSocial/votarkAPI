from rest_framework import serializers

from votarker.models import Votarker

class VotarkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Votarker
        fields = (
            'id',
            'first_name',
            'last_name',
            'username', 
            'password',
            'email',
            'bio',
            'birth_date',
            'location',
            'picture' 
        )