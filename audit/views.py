from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import CeleryTaskAudit
from .serializers import CeleryTaskAuditSerializer


class CeleryTaskAuditView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CeleryTaskAuditSerializer
    queryset = CeleryTaskAudit.objects.all().order_by('-create_time')[:10]
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

