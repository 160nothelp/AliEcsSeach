from rest_framework import serializers
from aliyunsdkcore.client import AcsClient

from .models import GtmCheckDomain, AliRamLink, GtmDefaultLine, TmpCytWhiteIpTables, TmpCytMerchNginx, \
    CreateShadowSocketTemplate, CreateShadowSocketTask, CreateForwardTemplate, CreateForwardTask
from aliecs.models import AliUserAccessKey
from user.models import User
from .tasks import SwitchDomain, createshadowsocket, createforward


class PostTaskSerializer(serializers.ModelSerializer):
    type = serializers.CharField(max_length=64, write_only=True, required=True)
    domain = serializers.SlugRelatedField(queryset=GtmCheckDomain.objects.all(), slug_field='id', read_only=True)
    host_name = serializers.CharField(max_length=128, read_only=True)
    default_line = serializers.IPAddressField()

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
            SwitchDomain.delay(client, donamins, self.initial_data['default_line'], domains_obj.id, rtype, special_domain)
        else:
            raise serializers.ValidationError('提交参数错误')
    
    def validate(self, attrs):
        
        del attrs['type']
        del attrs['default_line']
        return attrs
    
    class Meta:
        model = GtmDefaultLine
        fields = ('type', 'domain', 'default_line', 'host_name')


class GetSwitchStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = GtmCheckDomain
        fields = ('task_id', 'AccessKey_ID', 'Access_Key_Secret', 'region_id')


class AliRamSerializer(serializers.ModelSerializer):
    class Meta:
        model = AliRamLink
        fields = ('project_name', 'ali_link')


class TmpCytWhiteIpTablesSerializer(serializers.ModelSerializer):
    result = serializers.CharField(read_only=True)
    status = serializers.DecimalField(max_digits=1, decimal_places=0, read_only=True)
    
    class Meta:
        model = TmpCytWhiteIpTables
        fields = ('id', 'white_ip', 'result', 'status')


# class AliUserAccessKeySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AliUserAccessKey
#         fields = ('nickname', 'region_id')


class CreateShadowSocketTemplateSerializer(serializers.ModelSerializer):
    # project = AliUserAccessKeySerializer(many=True)
    project = serializers.SlugRelatedField(queryset=AliUserAccessKey.objects.all(), slug_field='nickname')

    class Meta:
        model = CreateShadowSocketTemplate
        fields = ('id', 'version', 'project', 'vpn_password', 'vpn_port', 'create_time')


class CreateShadowSocketTaskSerializer(serializers.ModelSerializer):
    vpn_template = serializers.SlugRelatedField(queryset=CreateShadowSocketTemplate.objects.all(), slug_field='id')
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    result = serializers.CharField(read_only=True)
    vpn_ip = serializers.CharField(read_only=True)
    status = serializers.DecimalField(max_digits=1, decimal_places=0, read_only=True)

    def create(self, validated_data):
        cst_obj = CreateShadowSocketTask.objects.create(**validated_data)
        createshadowsocket.delay(cst_obj.id)
        return cst_obj

    class Meta:
        model = CreateShadowSocketTask
        fields = ('id', 'vpn_template', 'user', 'amount', 'status', 'vpn_ip', 'result', '_false')


class CreateForwardTemplateSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(queryset=AliUserAccessKey.objects.all(), slug_field='nickname')

    class Meta:
        model = CreateForwardTemplate
        fields = ('id', 'version', 'project', 'forward_port', 'create_time')


class CreateForwardTaskSerializer(serializers.ModelSerializer):
    forward_template = serializers.SlugRelatedField(queryset=CreateForwardTemplate.objects.all(), slug_field='id')
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    status = serializers.DecimalField(max_digits=1, decimal_places=0, read_only=True)

    def create(self, validated_data):
        cft_obj = CreateForwardTask.objects.create(**validated_data)
        createforward.delay(cft_obj.id)
        return cft_obj

    class Meta:
        model = CreateForwardTask
        fields = ('id', 'forward_template', 'user', 'amount', 'status', 'forward_pip', 'forward_iip', 'result',
                  '_false')
