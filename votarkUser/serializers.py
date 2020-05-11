from rest_framework import serializers

from votarkUser.models import VotarkUser

class VotarkUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = VotarkUser
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
        extra_kwargs = {'password': {'write_only': True}}
