from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm
from permissions.services import APIPermissionClassFactory
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from viewedStory.models import ViewedStory
from viewedStory.serializers import ViewedStorySerializer

class ViewedStoryViewSet(viewsets.ModelViewSet):
    queryset = ViewedStory.objects.all()
    serializer_class = ViewedStorySerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='EventPermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'list': False,
                },
                'instance': {
                    'destroy': False,
                    'partial_update': False,
                    'retrieve': False,
                    'update': False,
                }
            }
        ),
    )