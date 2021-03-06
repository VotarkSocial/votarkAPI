from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm
from permissions.services import APIPermissionClassFactory
from post.models import Post
from post.serializers import PostSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from versus.views import get_element_random, pick_post, getComments
from versus.models import Versus
from follow.models import Follow
from like.models import Like
from versus.serializers import VersusSerializer

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
                'instance': {
                    'retrieve': True,
                    'destroy': evaluate,
                    'update': evaluate,
                    'partial_update': evaluate,
                }
            }
        ),
    )

    def perform_create(self, serializer):
        post = serializer.save()
        post.order = len(Post.objects.filter(topic=post.topic))
        post.save()
        return Response(serializer.data)