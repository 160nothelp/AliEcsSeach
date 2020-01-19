from rest_framework import serializers
from aliyunsdkcore.client import AcsClient

from .models import GtmCheckDomain, AliRamLink
from .tasks import SwitchDomain


class PostTaskSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=64, write_only=True, required=True)

    def validate_type(self, type):
        domains_obj = GtmCheckDomain.objects.first()
        donamins = domains_obj.domain_list.strip().split()
        special_domain = domains_obj.special_domain.strip().split()
        step = 20
        donamins = [donamins[i:i + step] for i in range(0, len(donamins), step)]
        domains_obj.task_id = None
        domains_obj.save()
        client = AcsClient(domains_obj.AccessKey_ID, domains_obj.Access_Key_Secret, domains_obj.region_id)
        if type == 'gtm':
            rtype = 'CNAME'
            SwitchDomain.delay(client, donamins, domains_obj.gtm_cname, domains_obj.id, rtype, special_domain)
        elif type == 'default':
            rtype = 'A'
            SwitchDomain.delay(client, donamins, domains_obj.default_line, domains_obj.id, rtype, special_domain)
        else:
            raise serializers.ValidationError('提交参数错误')

        return type


class GetSwitchStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = GtmCheckDomain
        fields = ('task_id', 'AccessKey_ID', 'Access_Key_Secret', 'region_id')


class AliRamSerializer(serializers.ModelSerializer):
    class Meta:
        model = AliRamLink
        fields = ('project_name', 'ali_link')


