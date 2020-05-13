from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from comment.models import Comment
from permissions.services import APIPermissionClassFactory
from comment.serializers import CommentSerializer

def evaluate(user, obj, request):
    return user.id == obj.user.id

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='EventPermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'list': False,
                },
                'instance': 
                    'retrieve': evaluate,
                    'destroy': evaluate,
                    'update': evaluate,
                    'partial_update': evaluate,
                }
              }
        ),
    )