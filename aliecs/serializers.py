from rest_framework import serializers

from .models import HostIpSearchTask


class PostTaskSerializer(serializers.ModelSerializer):
    category = serializers.CharField(write_only=True, required=True)
    status = serializers.IntegerField(default=1)
    sdata = serializers.IPAddressField(write_only=True, required=False)
    allname = serializers.CharField(write_only=True, required=False)

    def validate(self, attrs):
        try:
            attrs['allip'] = attrs['sdata']
            del attrs['sdata']
        except Exception as e:
            pass
        del attrs['category']
        return attrs

    class Meta:
        model = HostIpSearchTask
        fields = ('allip', 'status', 'result', 'id', 'category', 'sdata', 'allname')


class GetTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostIpSearchTask
        fields = ('result', 'status')

