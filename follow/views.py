from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from follow.models import Follow
from permissions.services import APIPermissionClassFactory
from follow.serializers import FollowSerializer

def evaluate(user, obj, request):
    return user.id == obj.follower.id

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='EventPermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'list': True,
                },
                'instance': 
                    'retrieve': True,
                    'destroy': evaluate,
                    'update': False,
                    'partial_update': False,
                }
              }
        ),
    )