from rest_framework import serializers

from .models import Upload, FileUpload


class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = ['id', 'username', 'file', 'filename', 'filepath', 'archive', 'type', 'size', 'create_time']


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ['id', 'file']
