from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm
from message.models import Message
from message.serializers import MessageSerializer
from permissions.services import APIPermissionClassFactory
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

def evaluate(user, obj, request):
    return user.id == obj.user.id

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
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
                    'update': evaluate,
                    'partial_update': evaluate,
                }
            }
        ),
    )