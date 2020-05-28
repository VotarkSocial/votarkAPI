from django.contrib.auth.models import User
from follow.models import Follow
from follow.serializers import FollowSerializer
from guardian.shortcuts import assign_perm
from permissions.services import APIPermissionClassFactory
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

def evaluate(user, obj, request):
    return user.id == obj.follower.id

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='EventPermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'list': True,
                    'unfollow': True,
                },
                'instance': {
                    'destroy': evaluate,
                    'partial_update': False,
                    'retrieve': True,
                    'update': False,
                }
            }
        ),
    )

    def perform_create(self, serializer):
        follow = serializer
        user = serializer.validated_data['user']
        follower = serializer.validated_data['follower']
        if(user!=follower and len(Follow.objects.filter(user=user, follower=follower))==0):
            follow.save()
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def unfollow(self, request):
        try:
            user = self.request.user
            userid = request.data['id']
            follow = Follow.objects.filter(user=user,follower=userid)
            follow.delete()
            return Response({'status':'ok'})
        except:
            return Response({'detail':'id is not valid'})   