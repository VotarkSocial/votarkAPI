from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from hashtag.models import Hashtag
from topic.models import Topic
from permissions.services import APIPermissionClassFactory
from topic.serializers import TopicSerializer
from hashtag.serializers import HashtagSerializer
from post.models import Post
from post.serializers import PostSerializers

def evaluate(user, obj, request):
    return user.id == obj.creator.id

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='EventPermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'list': True,
                },
                'instance': 
                    'destroy': evaluate,
                    'partial_update': evaluate,
                    'retrieve': True,
                    'trending': True,
                    'update': evaluate,
                }
              }
        ),
    )

    @action(detail=True, methods=['get'])
    def hashtags(self, request, pk=None):
        topic = self.get_object()
        response = []
        for hashtag in Hashtag.objects.filter(topic=topic):
            response.append(HashtagSerializer(hashtag).data)
        return Response(response)    

    def getTrending(limit):
        for post in Post.objects.values('topic').annotate(count=Count('topic')).order_by('count'):
            if(limit>0):
                response.append(PostSerializer(post).data)
            limit-=1
        return Response(response) 

    @action(detail=False, url_path='trending', methods=['get'])
    def trending(self, request):
        return Response(getTrending(100))

    @action(detail=True, methods=['get'])
    def order(self, request, pk=None):
        topic = self.get_object()
        response = []
        for post in Post.objects.filter(topic=topic):
            response.append({ post.user.username : post.order })
        return Response(response)    
