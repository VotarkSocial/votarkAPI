from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from searchedHashtag.models import SearchedHashtag
from permissions.services import APIPermissionClassFactory
from searchedHashtag.serializers import SearchedHashtagSerializer

class SearchedHashtagViewSet(viewsets.ModelViewSet):
    queryset = SearchedHashtag.objects.all()
    serializer_class = SearchedHashtagSerializer
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