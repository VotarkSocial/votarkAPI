from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from chat.models import Chat
from message.models import Message
from permissions.services import APIPermissionClassFactory
from chat.serializers import ChatSerializer
from message.serializers import MessageSerializer

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='EventPermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'list': False,
                },
                'instance': 
                    'retrieve': 'chat.view_chat',
                    'destroy': 'chat.admin_chat',
                    'update': 'chat.admin_chat',
                    'partial_update': 'chat.admin_chat',
                    'messages': 'chat.view_chat',
                    'add_admin': 'chat.admin_chat',
                    'add': 'chat.admin_chat
                }
              }
        ),
    )

    def perform_create(self, serializer):
        chat = serializer.save()
        user = self.request.user
        assign_perm('chat.view_chat', user, chat)
        assign_perm('chat.admin_chat', user, chat)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def messasges(self, request, pk=None):
        chat = self.get_object()
        response = []
        for message in Message.objects.filter(chat=chat).order_by('date'):
            response.append(MessageSerializer(message).data)
        return Response(response)    

    @action(detail=True, url_path='add', methods=['post'])
    def add(self, request, pk=None):
        try:
            chat = self.get_object()
            username = request.data['username']
            user = VotarkUser.objects.get(username=username)
            assign_perm('chat.view_chat', user, chat)
            return Response(serializer.data)
        except:
            return Response({'detail':'username is not valid'})

    @action(detail=True, url_path='add', methods=['post'])
    def add_admin(self, request, pk=None):
        try:
            chat = self.get_object()
            username = request.data['username']
            user = VotarkUser.objects.get(username=username
            assign_perm('chat.view_chat', user, chat)
            assign_perm('chat.admin_chat', user, chat)
            return Response(serializer.data)
        except:
            return Response({'detail':'username is not valid'})
