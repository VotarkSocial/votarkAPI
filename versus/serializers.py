from rest_framework import serializers

from versus.models import Versus

class VersusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Versus
        fields = (
            'id',
            'date',
            'post1',
            'post2',
        )