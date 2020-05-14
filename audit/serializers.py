from rest_framework import serializers

from .models import CeleryTaskAudit
from user.models import User


class CeleryTaskAuditSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = CeleryTaskAudit
        fields = ('user', 'task', 'create_time')
