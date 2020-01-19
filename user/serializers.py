from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import User


class UserPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("hosts_permission", "gtm_permission")


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    check_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs["new_password"] == attrs["check_password"]:
            return attrs
        else:
            raise serializers.ValidationError("新密码不一致")




