from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm
from like.models import Like
from like.serializers import LikeSerializer
from permissions.services import APIPermissionClassFactory
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

def evaluate(user, obj, request):
    return user.id == obj.user.id

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='EventPermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'list': True,
                },
                'instance': {
                    'retrieve': True,
                    'destroy': evaluate,
                    'update': False,
                    'partial_update': False,
                }
            }
        ),
    )