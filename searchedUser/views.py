from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from searchedUser.models import SearchedUser
from permissions.services import APIPermissionClassFactory
from searchedUser.serializers import SearchedUserSerializer

class SearchedUserViewSet(viewsets.ModelViewSet):
    queryset = SearchedUser.objects.all()
    serializer_class = SearchedUserSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='EventPermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'list': False,
                },
                'instance': 
                    'retrieve': False,
                    'destroy': False,
                    'update': False,
                    'partial_update': False,
                }
              }
        ),
    )