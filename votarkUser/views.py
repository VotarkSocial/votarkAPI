from chat.models import Chat
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from email.message import EmailMessage
from follow.models import Follow
from guardian.shortcuts import assign_perm
from guardian.shortcuts import get_objects_for_user
from permissions.services import APIPermissionClassFactory
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from votarkUser.models import VotarkUser
from votarkUser.serializers import VotarkUserSerializer
from follow.serializers import FollowSerializer
from chat.serializers import ChatSerializer
from searchedHashtag.models import SearchedHashtag
from searchedHashtag.serializers import SearchedHashtagSerializer
from searchedUser.models import SearchedUser
from searchedUser.serializers import SearchedUserSerializer
from viewedStory.models import ViewedStory
from viewedStory.serializers import ViewedStorySerializer
import os 
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
                    'partial_update': evaluate,
                    'restore_password': True,
                    'retrieve': True,
                    'searh_history_post':evaluate,
                    'searh_history_user':evaluate,
                    'update': evaluate,
                    'stories': evaluate
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
    def searh_history_post(self, request, pk=None):
        user = self.get_object()
        response = []
        for searched in SearchedHashtag.objects.filter(user=user).order_by('-date'):
            response.append(SearchedHashtagSerializer(searched).data)
        return Response(response)

    @action(detail=True, methods=['get'])
    def searh_history_user(self, request, pk=None):
        user = self.get_object()
        response = []
        for searched in SearchedUser.objects.filter(searchedUser=user).order_by('-date'):
            response.append(SearchedUserSerializer(searched).data)
        return Response(response)

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
    
    