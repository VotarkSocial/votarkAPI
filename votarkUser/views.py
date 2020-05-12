from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from votarkUser.models import VotarkUser
from permissions.services import APIPermissionClassFactory
from votarkUser.serializers import VotarkUserSerializer
from django.contrib.auth.hashers import make_password
from email.message import EmailMessage
import uuid
import os 
import smtplib

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
                    'retrieve': True,
                    'destroy': evaluate,
                    'update': evaluate,
                    'partial_update': evaluate,
                    'restore_password': True
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
                