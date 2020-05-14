from rest_framework import viewsets
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from tools.models import Upload, FileUpload
from tools.serializers import UploadSerializer, FileUploadSerializer


class UploadViewSet(viewsets.ModelViewSet):
    queryset = Upload.objects.all().order_by("-create_time")
    serializer_class = UploadSerializer
    filter_fields = ('username', 'type',)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)


class FileUploadViewSet(viewsets.ModelViewSet):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)


