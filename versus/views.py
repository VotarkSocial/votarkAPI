from comment.models import Comment
from comment.serializers import CommentSerializer
from django.contrib.auth.models import User
from django.db.models import Q
from guardian.shortcuts import assign_perm
from like.models import Like
from like.serializers import LikeSerializer
from permissions.services import APIPermissionClassFactory
from post.models import Post
from post.serializers import Post
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from share.models import Share
from share.serializers import ShareSerializer
from versus.models import Versus
from versus.serializers import VersusSerializer
import random

def get_element_random(elements,order):                                                               #With a list of valid elements and an order
    valid_elements = []                                                                            #It will return a element
    for key in order:                                                                              #choosing a post randomly
        valid_post.append(elements[key])                                                           #going through all the elements in the orden given
    n=len(valid_elements)                                                                          #choosing if that post will be returned
    index = 0                                                                                      #with a 20% of probability, if randomly it 
    n=len(valid_elements)                                                                          #chooses it, it returns it, elsewhere
    index = 0                                                                                      #he continues throught the next element
    while index<n:
        if(random.randint(0,5)==0):
            return (valid_elements[index])
        index+=1
        if(index==n):
            return (valid_elements[0])                                                              #If goes through all given elements, returns the first on list
    return None

def pick_by_like(topic):
    posts = Post.objects.filter(topic=topic)
    order = {}
    index = 0
    for valid_post in posts:
        versus = Versus.objects.filter(Q(post1=valid_post) | Q(post2=valid_post))
        if(Vote.objects.filter(versus=versus).Count()==0):
            order[index] = Like.objects.filter(versus=versus).Count()
            index += 1
    order = {k: v for k, v in sorted(x.items(), key=lambda item: item[1])}                          #Sorting by ammount of likes
    return get_element_random(posts,order)

def pick_by_date(post):
    posts = Post.objects.filter(topic=post.topic).order('-date')
    index = 0
    order = {}
    valid_posts = []
    for valid_post in posts:
        versus = Versus.objects.filter(Q(post1=valid_post) | Q(post2=valid_post))
        if(Vote.objects.filter(versus=versus).Count()==0):
            order[index] = index
    return get_element_random(posts,order)

def pick_by_comment(topic):
    posts = Post.objects.filter(topic=topic)
    order = {}
    index = 0
    for valid_post in posts:
        versus = Versus.objects.filter(Q(post1=valid_post) | Q(post2=valid_post))
        if(Vote.objects.filter(versus=versus).Count()==0):
            order[index] = Comment.objects.filter(Q(versus=versus) | Q(post=valid_post)).Count()
            index += 1
    order = {k: v for k, v in sorted(x.items(), key=lambda item: item[1])}                          #Sorting by ammount of comments
    return get_element_random(posts,order)

def pick_by_follow(topic):
    posts = Post.objects.filter(topic=topic)
    order = {}
    index = 0
    for valid_post in posts:
        versus = Versus.objects.filter(Q(post1=valid_post) | Q(post2=valid_post))
        if(Vote.objects.filter(versus=versus).Count()==0):
            order[index] = Follow.objects.filter(onVersus=versus).Count()
            index += 1
    order = {k: v for k, v in sorted(x.items(), key=lambda item: item[1])}                          #Sorting by ammount of followers obtained by that post
    return get_element_random(posts,order)

def pick_by_share(topic):
    posts = Post.objects.filter(topic=topic)
    order = {}
    index = 0
    for valid_post in posts:
        versus = Versus.objects.filter(Q(post1=valid_post) | Q(post2=valid_post))
        if(Vote.objects.filter(versus=versus).Count()==0):
            order[index] = Share.objects.filter(versus=versus).Count()
            index += 1
    order = {k: v for k, v in sorted(x.items(), key=lambda item: item[1])}                          #Sorting by ammount of shares
    return get_element_random(posts,order)

def pick_post(topic):                                                                 #With a given topic it returns a post
    newPost = None
    while(newPost==None):
        choose = random.randint(0,100)
        if(choose<25):                                                                  #25% of the times it will choose a post based on likes
            newPost = pick_by_like(topic)
        elif(choose>=25 and choose<40):                                                 #15% of the times it will choose new posts
            newPost = pick_by_date(topic)
        elif(choose>=40 and choose<60):                                                 #20% of the times it will choose a post based on comments
            newPost = pick_by_comment(topic)
        elif(choose>=60 and choose<90):                                                 #30% of the times it will choose a post similar to those where the user followed the votarker
            newPost = pick_by_follow(topic)
        elif(choose>=90 and choose<100):                                                #10% of the times it will choose a post based on shares   
            newPost = pick_by_share(topic)

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
                'instance': {
                    'comments': True,
                    'destroy': False,
                    'likes': True,
                    'partial_update': False,
                    'pick': True,
                    'retrieve': True,
                    'shares': True,
                    'update': False,
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

    @action(detail=False, url_path='pick', methods=['post'])
    def pick(self, request, pk=None):
        try:
            postid= request.data['postid']
            post = Post.objects.get(id=postid)
            newPost = pick_post(post.topic)
            if (Versus.objects.filter(post1=post, post2=newPost).Count()==0):
                versus = Versus.create(post1=post, post2=pick_post(post.topic))
                versus.save()
                return Response(VersusSerializer(versus).data)
            return Response(VersusSerializer(Versus.objects.filter(post1=post, post2=newPost)[0]).data)
        except:
            return Response({'detail':'postid is not valid'})

    
