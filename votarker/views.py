from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django.contrib.auth.models import User
from permissions.services import APIPermissionClassFactory
from votarker.serializers import VotarkerSerializer

def evaluate(user, obj, request):
    return user.username == obj.username

class VotarkerViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = VotarkerSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='EventPermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'list': True,
                },
                'instance': {
                    'retrieve': evaluate,
                    'destroy': evaluate,
                    'update': evaluate,
                    'partial_update': evaluate,
                }
            }
        ),
    )

    def perform_create(self, serializer):
        user = user = User.objects.create_user(serializer.data['username'], serializer.data['email'], serializer.data['password'])
        user.first_name = serializer.data['first_name']
        user.last_name = serializer.data['last_name']
        user.save()
        return Response({})