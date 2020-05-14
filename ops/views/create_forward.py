from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.utils.decorators import method_decorator

from ops.models import CreateForwardTask, CreateForwardTemplate
from ops.serializers import CreateForwardTemplateSerializer, CreateForwardTaskSerializer
from audit.addlog import add_tasks_log


class CreateForwardView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = CreateForwardTemplateSerializer
    queryset = CreateForwardTemplate.objects.all().order_by('-create_time')
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)


@method_decorator(add_tasks_log('创建forward'), name='create')
class CreateForwardTaskView(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = CreateForwardTaskSerializer
    queryset = CreateForwardTask.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

