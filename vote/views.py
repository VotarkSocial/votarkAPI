from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from vote.models import Vote
from permissions.services import APIPermissionClassFactory
from vote.serializers import VoteSerializer

def evaluate(user, obj, request):
    return user.id == obj.user.id

class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
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
                    'destroy': False,
                    'update': False,
                    'partial_update': False,
                }
              }
        ),
    )