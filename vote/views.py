from django.contrib.auth.models import User
from django.db.models import Q
from follow.models import Follow
from guardian.shortcuts import assign_perm
from like.models import Like
from permissions.services import APIPermissionClassFactory
from post.models import Post
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from share.models import Share
from versus.models import Versus
from vote.models import Vote
from vote.serializers import VoteSerializer
import random

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
                'instance': {
                    'destroy': False,
                    'partial_update': False,
                    'retrieve': True,
                    'update': False,
                }
            }
        ),
    )

    def getWinner(versus):
        if(versus.winner):
            return versus.post1
        else:
            return versus.post2

    def perform_create(self, serializer):
        vote = serializer.save()
        post = getWinner(vote.versus)
        post.victories += 1
        post.save()
        hasToChangedOrder = True

        """We have to update de order that the post has in the topic
            There is a hiearchy to order:
                Victories
                SecondaryVictories
                Followers obtained because of the poston the Post
                Shares of versus where post is
                Likes on versus where post is
                Random Pick by system
        """

        while(hasToChangedOrder):                                                                                   #hierarchy:
            currentPost = Post.objects.filter(topic=post.topic, order=post.order-1)
            if(currentPost.victories>post.victories):                                                                   #Victories
                hasToChangedOrder = False
            elif(currentPost.victories<post.victories):
                currentPost.order-=1
                post.order+=1
                currentPost.save()
                post.save()
            else:
                secondaryVictories_post = 0
                for versus in Versus.objects.filter(post1=post):                                                        #Secondary Victories 
                    for vote_ in Vote.objects.filter(versus=versus, winner=True):
                        secondaryVictories_post += versus.post2.victories
                for versus in Versus.objects.filter(post2=post):
                    for vote_ in Vote.objects.filter(versus=versus, winner=False):
                        secondaryVictories_post += versus.post1.victories
                secondaryVictories_current = 0
                for versus in Versus.objects.filter(post1=currentPost):
                    for vote_ in Vote.objects.filter(versus=versus, winner=True):
                        secondaryVictories_current += versus.post2.victories
                for versus in Versus.objects.filter(post2=currentPost):
                    for vote_ in Vote.objects.filter(versus=versus, winner=False):
                        secondaryVictories_current += versus.post1.victories
                if(secondaryVictories_current>secondaryVictories_post):
                    hasToChangedOrder = False
                elif(secondaryVictories_current<secondaryVictories_post):
                    currentPost.order-=1
                    post.order+=1
                    currentPost.save()
                    post.save()
                else:
                    followerOnPost = 0
                    for versus in Versus.objects.filter(Q(post1=post) | Q(post2=post)):                  #Followers because of the Post
                        followerOnPost += Follow.objects.filter(onVersus=versus).Count()
                    followerOnCurrent = 0
                    for versus in Versus.objects.filter(Q(post1=post) | Q(post2=post)):
                        followerOnCurrent += Follow.objects.filter(onVersus=versus).Count()
                    if(followerOnCurrent>followerOnPost):
                        hasToChangedOrder = False
                    elif(followerOnCurrent<followerOnPost):
                        currentPost.order-=1
                        post.order+=1
                        currentPost.save()
                        post.save()
                    else:
                        shareOnPost = 0
                        for versus in Versus.objects.filter(Q(post1=post) | Q(post2=post)):                  #shares because of the Post
                            shareOnPost += Share.objects.filter(versus=versus).Count()
                        shareOnCurrent = 0
                        for versus in Versus.objects.filter(Q(post1=post) | Q(post2=post)):
                            shareOnCurrent += Share.objects.filter(versus=versus).Count()
                        if(shareOnCurrent>shareOnPost):
                            hasToChangedOrder = False
                        elif(shareOnCurrent<shareOnPost):
                            currentPost.order-=1
                            post.order+=1
                            currentPost.save()
                            post.save()
                        else:
                            likeOnPost = 0
                            for versus in Versus.objects.filter(Q(post1=post) | Q(post2=post)):               #Likes because of the Post
                                likeOnPost += Like.objects.filter(versus=versus).Count()
                            likeOnCurrent = 0
                            for versus in Versus.objects.filter(Q(post1=post) | Q(post2=post)):
                                likeOnCurrent += Like.objects.filter(versus=versus).Count()
                            if(likeOnCurrent>likeOnPost):
                                hasToChangedOrder = False
                            elif(likeOnCurrent<likeOnPost):
                                currentPost.order-=1
                                post.order+=1
                                currentPost.save()
                                post.save()
                            else:
                                if(likeOnCurrent>likeOnPost):
                                    hasToChangedOrder = False
                                elif(likeOnCurrent<likeOnPost):
                                    currentPost.order-=1
                                    post.order+=1
                                    currentPost.save()
                                    post.save()
                                else:
                                    pick = random.randit(0,1)                                                                  #Random 
                                    if(pick==0):
                                        hasToChangedOrder = False
                                    elif(pick==1):
                                        currentPost.order-=1
                                        post.order+=1
                                        currentPost.save()
                                        post.save()
                                    hasToChangedOrder = False                  
        return Response(serializer.data)
