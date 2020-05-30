from chat.models import Chat
from chat.serializers import ChatSerializer
from votarkUser.models import VotarkUser
from guardian.shortcuts import assign_perm
from message.models import Message
from message.serializers import MessageSerializer
from permissions.services import APIPermissionClassFactory
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='EventPermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'list': True,
                },
                'instance': {
                    'add_admin': 'chat.admin_chat',
                    'add': 'chat.change_chat',
                    'destroy': 'chat.change_chat',
                    'messages': 'chat.view_chat',
                    'partial_update': 'chat.change_chat',
                    'retrieve': 'chat.view_chat',
                    'update': 'chat.change_chat',
                }
            }
        ),
    )

    def perform_create(self, serializer):
        chat = serializer.save()
        user = self.request.user
        assign_perm('chat.view_chat', user, chat)
        assign_perm('chat.change_chat', user, chat)
        print(serializer)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        chat = self.get_object()
        response = []
        for message in Message.objects.filter(chat=chat).order_by('date'):
            response.append(MessageSerializer(message).data)
        return Response(response)    

    @action(detail=True, url_path='add', methods=['post'])
    def add(self, request, pk=None):
        try:
            chat = self.get_object()
            userid = request.data['id']
            user = VotarkUser.objects.get(id=userid)
            assign_perm('chat.view_chat', user, chat)
            return Response({'status':'ok'})
        except Exception as e:
            print(e)
            return Response({'detail':'id is not valid'})

    @action(detail=True, url_path='add', methods=['post'])
    def add_admin(self, request, pk=None):
        try:
            chat = self.get_object()
            userid = request.data['id']
            user = VotarkUser.objects.get(username=userid)
            assign_perm('chat.view_chat', user, chat)
            assign_perm('chat.change_chat', user, chat)
            return Response({'status':'ok'})
        except:
            return Response({'detail':'id is not valid'})
