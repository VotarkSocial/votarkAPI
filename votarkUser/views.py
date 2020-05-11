from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from votarkUser.models import VotarkUser
from permissions.services import APIPermissionClassFactory
from votarkUser.serializers import VotarkUserSerializer

def evaluate(user, obj, request):
    return user.username == obj.username

class VotarkUserViewSet(viewsets.ModelViewSet):
    queryset = VotarkUser.objects.all()
    serializer_class = VotarkUserSerializer
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
