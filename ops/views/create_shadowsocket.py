from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.utils.decorators import method_decorator

from ops.serializers import CreateShadowSocketTemplateSerializer, CreateShadowSocketTaskSerializer
from ops.models import CreateShadowSocketTemplate, CreateShadowSocketTask
from audit.addlog import add_tasks_log


class CreateShadowSocketView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = CreateShadowSocketTemplateSerializer
    queryset = CreateShadowSocketTemplate.objects.all().order_by('-create_time')
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)


@method_decorator(add_tasks_log('创建shadowsocket_vpn'), name='create')
class CreateShadowSocketTaskView(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = CreateShadowSocketTaskSerializer
    queryset = CreateShadowSocketTask.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

