from chat.models import Chat
from chat.serializers import ChatSerializer
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from email.message import EmailMessage
from follow.models import Follow
from follow.serializers import FollowSerializer
from guardian.shortcuts import assign_perm
from guardian.shortcuts import get_objects_for_user
from permissions.services import APIPermissionClassFactory
from post.models import Post
from post.serializers import PostSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from searchedHashtag.models import SearchedHashtag
from searchedHashtag.serializers import SearchedHashtagSerializer
from searchedUser.models import SearchedUser
from searchedUser.serializers import SearchedUserSerializer
from topic.views import getTrending
from versus.models import Versus
from versus.serializers import VersusSerializer
from versus.views import get_element_random, pick_post
from viewedStory.models import ViewedStory
from viewedStory.serializers import ViewedStorySerializer
from votarkUser.models import VotarkUser
from votarkUser.serializers import VotarkUserSerializer
import os 
import random
import smtplib
import uuid

EMAIL_ADRESS = ''
EMAIL_PASSWORD = ''

def evaluate(user, obj, request):
    return user.username == obj.username

class VotarkUserViewSet(viewsets.ModelViewSet):
    queryset = VotarkUser.objects.all()
    serializer_class = VotarkUserSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='EventPermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'list': True,
                },
                'instance': {
                    'chats':evaluate,
                    'destroy': evaluate,
                    'followers': True,
                    'following': True,
                    'mystories':evaluate,
                    'partial_update': evaluate,
                    'pick': evaluate,
                    'posts': True,
                    'restore_password': True,
                    'retrieve': True,
                    'search_history_hashtag':evaluate,
                    'search_history_user':evaluate,
                    'searchHastag': True,
                    'searchUser': True,
                    'stories': evaluate,
                    'update': evaluate,
                }
            }
        ),
    )

    def perform_create(self, serializer):
        user = serializer.save()
        user.password = make_password(serializer.validated_data['password'])
        user.save()
        return Response(serializer.data)


    @action(detail=False, url_path='restore', methods=['post'])
    def restore_password(self, request):
        try:
            email = request.data['email']
            user = VotarkUser.objects.get(email=email)
            user.password = str(uuid.uuid1())
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_ADRESS,EMAIL_PASSWORD)
                msg = EmailMessage()
                msg['Subject'] = 'Password has been changed'
                msg['From'] = EMAIL_ADRESS
                msg['To'] = email
                msg.set_content('Hi! ' + user.first_name + ' ' + user.last_name + ' your password has been restored\n email: ' + email + '\npassword: ' + user.password + '\n THE TEAM OF VOTARK')
                smtp.send_message(msg)
            return Response(request.data)
        except:
            return Response({'detail':'email is not valid'})
                

    @action(detail=True, methods=['get'])
    def followers(self, request, pk=None):
        user = self.get_object()
        response = []
        for follower in Follow.objects.filter(user=user):
            response.append(FollowSerializer(follower).data)
        return Response(response)    

    @action(detail=True, methods=['get'])
    def following(self, request, pk=None):
        user = self.get_object()
        response = []
        for follower in Follow.objects.filter(follower=user):
            response.append(FollowSerializer(follower).data)
        return Response(response)

    @action(detail=True, methods=['get'])
    def chats(self, request, pk=None):
        user = self.get_object()
        response = []
        for chat in get_objects_for_user(joe, 'chat.view_chat').order_by('-date'):
            response.append(ChatSerializer(chat).data)
        return Response(response)

    @action(detail=True, methods=['get'])
    def search_history_hashtag(self, request, pk=None):
        user = self.get_object()
        response = []
        for searched in SearchedHashtag.objects.filter(user=user).order_by('-date'):
            response.append(SearchedHashtagSerializer(searched).data)
        return Response(response)

    @action(detail=True, methods=['get'])
    def search_history_user(self, request, pk=None):
        user = self.get_object()
        response = []
        for searched in SearchedUser.objects.filter(searchedUser=user).order_by('-date'):
            response.append(SearchedUserSerializer(searched).data)
        return Response(response)

    
    @action(detail=True, methods=['post'])
    def search_user(self, request):
        user = self.get_object()
        try:
            query = request.data['query']
            users = VotarkUser.objects.filter(username__contains=query)
            response=[]
            limit=5
            for votarker in users:
                if(limit>0):
                    SearchedUser.objects.create(user=user, searchedUser=votarker)
                    response.append(SearchedUserSerializer(votarker).data)
                limit-=1
            return Response(response)
        except:
            return Response({'detail':'query is not valid'})

    @action(detail=True, methods=['post'])
    def search_hastag(self, request):
        user = self.get_object()
        try:
            query = request.data['query']
            hashtags = Hashtag.objects.filter(content__contains=query)
            response=[]
            limit=5
            for Hashtag in hashtags:
                if(limit>0):
                    SearchedHashtag.objects.create(Hashtag=Hashtag, user=user)
                    response.append(SearchedUserSerializer(Hashtag).data)
                limit-=1
            return Response(response)
        except:
            return Response({'detail':'query is not valid'})

    @action(detail=True, methods=['get'])
    def stories(self, request, pk=None):
        user = self.get_object()
        index = 0
        order = {}
        current_response = []
        for following in Follow.objects.filter(follower=user).order_by('-date'):
            subresponse = {}
            value = index
            if Story.objects.filter(user=following).Count()!=0:
                subresponse['user'] = following                                                          #Order them by user
                stories = []
                for story in Story.objects.filter(user=following).order_by('-date'):                     
                    story = {}           
                    story['story'] = stories.append(StorySerializer(story).data)                              
                    if(ViewedStory.objects.filter(story=story, user=user).Count()==0):                  #Check if the user has not seen the story
                        story['viewed'] = False
                    else:
                        value+=100                                                                      #This will make it go to the end of the order
                        story['viewed'] = True
                    stories.append(story)
                if(SearchesUser.objects.filter(searchedUser=following, user=user).Count()==0):          #User has not searched him
                    value+=30
                else:
                    value-=5*SearchesUser.objects.filter(searchedUser=following, user=user).Count()     #THis will make users with more searches come first
                subresponse['stories'] = stories
                order[index] = value
                current_response.append(subresponse)
            index+=1
        order = {k: v for k, v in sorted(x.items(), key=lambda item: item[1])}                          #Sorting by value
        response = []
        for key in order:
            response.append(current_response[key])                                                      #Returning them in the specified order
        return Response(response)
    
    @action(detail=True, methods=['get'])
    def mystories(self, request, pk=None):
        user = self.get_object()
        response = []
        for story in Story.objects.filter(user=user).order_by('-date'):
            response.append(StorySerializer(story).data)
        return Response(response)

    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        user = self.get_object()
        response = []
        for post in Post.objects.filter(user=user).order_by('-date'):
            response.append(PostSerializer(post).data)
        return Response(response)

    @action(detail=True, methods=['get'])
    def pick(self, request, pk=None):
        post = None
        while(post==None):
            choose = random.randint(0,10)
            if(choose<6):                                                                  #60% of the times it will choose from the followed users
                user = self.get_object()
                index = 0
                order = {}
                valid_posts = []
                orderby = '-date'                                                           #75% new posts will be returned
                if(random.randint(0,4)==0):
                    order_by = '-order'                                                     #25% trending will be returned
                for post in Post.objects.order_by(orderby):
                    for following in Follow.objects.filter(follower=user).order():
                        if(post.user==following):
                            value = index
                            if(SearchesUser.objects.filter(searchedUser=following, user=user).Count()==0):          #User has not searched him
                                value+=10
                            else:
                                value-=5*SearchesUser.objects.filter(searchedUser=following, user=user).Count()     #This will make users with more searches come first
                            valid_posts.append(post)
                            order[index] = value
                    index+=1
                post=get_element_random(valid_posts,order)
            elif(choose>=6 and choose<10):                                                 #40% of the times it will choose from trending
                trending = getTrending(20)
                trend = random.choice(trending)
                topic = Topic.objects.filter(name=trend.topic)
                post = pick_post(topic)
        newPost = pick_post(post.topic)
        if (Versus.objects.filter(post1=post, post2=newPost).Count()==0):
            versus = Versus.create(post1=post, post2=pick_post(post.topic))
            versus.save()
            return Response(VersusSerializer(versus).data)
        return Response(VersusSerializer(Versus.objects.filter(post1=post, post2=newPost)[0]).data)