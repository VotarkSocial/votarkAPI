from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm
from permissions.services import APIPermissionClassFactory
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from share.models import Share
from share.serializers import ShareSerializer

def evaluate(user, obj, request):
    return user.id == obj.user.id

class ShareViewSet(viewsets.ModelViewSet):
    queryset = Share.objects.all()
    serializer_class = ShareSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='EventPermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'list': True,
                },
                'instance': {
                    'destroy': False,
                    'partial_update': False,
                    'retrieve': True,
                    'update': False,
                }
            }
        ),
    )