from rest_framework import serializers

from .models import User


class UserPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("hosts_permission", "gtm_permission", 'cyt_iptables_permission', 'create_shadowsocket_permission',
                  'create_forward_permission', 'wiki_permission',
                  'worktickets_permission')


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    check_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs["new_password"] == attrs["check_password"]:
            return attrs
        else:
            raise serializers.ValidationError("新密码不一致")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'id')


