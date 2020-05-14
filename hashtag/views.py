from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm
from hashtag.models import Hashtag
from hashtag.serializers import HashtagSerializer
from permissions.services import APIPermissionClassFactory
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

def evaluate(user, obj, request):
    return user.id == obj.topic.creator.id

class HashtagViewSet(viewsets.ModelViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
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
                    'destroy': False,
                    'update': evaluate,
                    'partial_update': evaluate,
                }
            }
        ),
    )