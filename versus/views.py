from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from comment.models import Comment
from comment.serializers import CommentSerializer
from django.contrib.auth.models import User
from like.models import Like
from like.serializers import LikeSerializer
from permissions.services import APIPermissionClassFactory
from rest_framework.response import Response
from versus.models import Versus
from versus.serializers import VersusSerializer
from share.models import Share
from share.serializers import ShareSerializer

class VersusViewSet(viewsets.ModelViewSet):
    queryset = Versus.objects.all()
    serializer_class = VersusSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='EventPermission',
            permission_configuration={
                'base': {
                    'create': False,
                    'list': True,
                },
                'instance': 
                    'retrieve': True,
                    'destroy': False,
                    'update': False,
                    'partial_update': False,
                    'comments': True,
                    'likes': True,
                    'shares': True
                }
              }
        ),
    )

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        versus = self.get_object()
        response = []
        for comment in Comment.objects.filter(versus=versus):
            response.append(CommentSerializer(comment).data)
        for comment in Comment.objects.filter(post=versus.post1):
            response.append(CommentSerializer(comment).data)
        for comment in Comment.objects.filter(post=versus.post2):
            response.append(CommentSerializer(comment).data)
        return Response(response)    

    @action(detail=True, methods=['get'])
    def likes(self, request, pk=None):
        versus = self.get_object()
        response = []
        for like in Like.objects.filter(versus=versus):
            response.append(LikeSerializer(like).data)
        return Response(response)    

    @action(detail=True, methods=['get'])
    def shares(self, request, pk=None):
        versus = self.get_object()
        response = []
        for share in Share.objects.filter(versus=versus):
            response.append(ShareSerializer(share).data)
        return Response(response)    
