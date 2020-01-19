from rest_framework import serializers

from tools.models import Upload


class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = ['id', 'username', 'file', 'filename', 'filepath', 'archive', 'type', 'size', 'create_time']
