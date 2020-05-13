from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from post.models import Post
from permissions.services import APIPermissionClassFactory
from post.serializers import PostSerializer

def evaluate(user, obj, request):
    return user.id == obj.user.id

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
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
                    'update': evaluate,
                    'partial_update': evaluate,
                }
              }
        ),
    )
