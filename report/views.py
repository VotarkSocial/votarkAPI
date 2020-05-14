from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm
from permissions.services import APIPermissionClassFactory
from report.models import Report
from report.serializers import ReportSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
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
                    'destroy': False,
                    'update': False,
                    'partial_update': False,
                }
            }
        ),
    )