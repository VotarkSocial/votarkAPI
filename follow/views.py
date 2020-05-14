from django.contrib.auth.models import User
from follow.models import Follow
from follow.serializers import FollowSerializer
from guardian.shortcuts import assign_perm
from permissions.services import APIPermissionClassFactory
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

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
                'instance': {
                    'destroy': evaluate,
                    'partial_update': False,
                    'retrieve': True,
                    'update': False,
                }
            }
        ),
    )