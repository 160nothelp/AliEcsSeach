from celery import shared_task
import os
from aliyunsdkalidns.request.v20150109.OperateBatchDomainRequest import OperateBatchDomainRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.DeleteDomainRecordRequest import DeleteDomainRecordRequest
import time
import traceback
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException, ServerException
from aliyunsdkecs.request.v20140526.RunInstancesRequest import RunInstancesRequest
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526.AuthorizeSecurityGroupRequest import AuthorizeSecurityGroupRequest
import json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AliyunCenter.settings')
from multiprocessing import Pool
import math
import paramiko

from .models import GtmCheckDomain, TmpCytMerchNginx, TmpCytWhiteIpTables, CreateShadowSocketTask, \
    CreateForwardTask


def setDomain(client, domains, value, id, rtype, special_domain=None):
    task_id = list()
    gtm_data = list()
    special_list = list()
    if special_domain is not None:
        for limit in special_domain:
            request = DescribeDomainRecordsRequest()
            request.set_accept_format('json')
            request.set_DomainName(limit)
            response = client.do_action_with_exception(request)
            json_data = json.loads(str(response, encoding='utf-8'))
            RecordIdList_ = list()
            for RecordId in json_data['DomainRecords']['Record']:
                if RecordId['RR'] == 'api':
                    RecordIdList_.append(RecordId['RecordId'])
            special_list.append(RecordIdList_)
            data = dict()
            data['Domain'] = limit
            data['Rr'] = 'api'
            data['Value'] = value
            data['Type'] = rtype
            gtm_data.append(data)

    if special_domain is not None:
        for RecordIdList in special_list:
            for RecordId in RecordIdList:
                request = DeleteDomainRecordRequest()
                request.set_accept_format('json')
                request.set_RecordId(RecordId)
                response = client.do_action_with_exception(request)

    for domain in domains:
        RecordIdLists = list()
        for limit in domain:
            # 当前二级列表里的域名的解析id
            request = DescribeDomainRecordsRequest()
            request.set_accept_format('json')
            request.set_DomainName(limit)
            response = client.do_action_with_exception(request)
            json_data = json.loads(str(response, encoding='utf-8'))
            RecordIdList_ = list()
            for RecordId in json_data['DomainRecords']['Record']:
                RecordIdList_.append(RecordId['RecordId'])
            RecordIdLists.append(RecordIdList_)
            # 当前二级列表里的域名 组合的批量信息
            data = dict()
            data['Domain'] = limit
            data['Rr'] = '*'
            data['Value'] = value
            data['Type'] = rtype
            gtm_data.append(data)

        for RecordIdList in RecordIdLists:
            for RecordId in RecordIdList:
                request = DeleteDomainRecordRequest()
                request.set_accept_format('json')
                request.set_RecordId(RecordId)
                response = client.do_action_with_exception(request)

        request = OperateBatchDomainRequest()
        request.set_accept_format('json')
        request.set_Type("RR_ADD")
        request.set_DomainRecordInfos(gtm_data)
        response = client.do_action_with_exception(request)
        json_data = json.loads(str(response, encoding='utf-8'))
        task_id.append(json_data['TaskId'])
    return task_id


@shared_task
def SwitchDomain(client, domains, value, id, rtype, special_domain):
    pool = Pool(processes=2)
    return_dict = list()
    jobs = list()
    step = math.ceil(len(domains) / 2)
    domains = [domains[i:i + step] for i in range(0, len(domains), step)]
    if len(domains) < 2:
        r1 = pool.apply_async(setDomain, (client, domains[0], value, id, rtype, special_domain))
        jobs.append(r1)
    else:
        r1 = pool.apply_async(setDomain, (client, domains[0], value, id, rtype, special_domain))
        r2 = pool.apply_async(setDomain, (client, domains[1], value, id, rtype))
        jobs.append(r1)
        jobs.append(r2)
    pool.close()
    pool.join()
    for job in jobs:
        return_dict.append(job.get())

    obj = GtmCheckDomain.objects.get(pk=id)
    obj.task_id = return_dict
    obj.save()


# -------------------------------------------------------------------------临时cyt防火墙------------------------------------------------------------------------


def check_iptables_ip(white_ip, nginx_ip):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(nginx_ip, 22, 'root', timeout=10)
    cmd = "iptables -nvL |awk '{print $8 }' |grep -w %s" % white_ip
    stdin, stdout, stderr = client.exec_command(cmd)
    result = stdout.read()
    error = stderr.read()
    if not error:
        if result:
            client.close()
            return 'existed'
        else:
            client.close()
            return 'do not exist'
    else:
        client.close()
        return False


def add_iptables(white_ip, nginx_ip):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(nginx_ip, 22, 'root', timeout=10)
    cmd = 'iptables -I INPUT -s %s -p tcp --dport 443 -j ACCEPT && iptables -I INPUT -s %s -p tcp --dport 80 -j ACCEPT' % (white_ip, white_ip)
    stdin, stdout, stderr = client.exec_command(cmd)
    result = stdout.read()
    error = stderr.read()
    if not error:
        client.close()
        return True
    else:
        client.close()
        return False



@shared_task
def tmpCytIptables(id):
    white_ipobj = TmpCytWhiteIpTables.objects.get(pk=id)
    white_ip = white_ipobj.white_ip
    nginx_ipobj = TmpCytMerchNginx.objects.all()
    results = list()
    for ip_obj in nginx_ipobj:
        nginx_ip = ip_obj.hosts_name
        result = check_iptables_ip(white_ip, nginx_ip)
        if result == 'do not exist':
            add_result = add_iptables(white_ip, nginx_ip)
            if add_result:
                results.append('添加成功')
            else:
                results.append('添加失败')
        elif result == 'existed':
            results.append('记录已存在')
        else:
            results.append('未知错误')
    white_ipobj.result = results
    white_ipobj.status = 2
    white_ipobj.save()


# -------------------------------------------------- shadowsocket -------------------------------------


RUNNING_STATUS = 'Running'
CHECK_INTERVAL = 3
CHECK_TIMEOUT = 180


class AliyunRunShadowSocketInstances(object):

    def __init__(self, access_id, access_secret, region_id, image_id, security_group_id, vswitch_id, key_pair_name,
                 instance_charge_type, post_user, task_obj, admin_security_id, admin_security_access_id,
                 admin_security_access_secret, admin_security_region_id):
        self.access_id = access_id
        self.access_secret = access_secret

        # 是否只预检此次请求。true：发送检查请求，不会创建实例，也不会产生费用；false：发送正常请求，通过检查后直接创建实例，并直接产生费用
        self.dry_run = False
        # 实例所属的地域ID
        self.region_id = region_id
        # 实例的资源规格
        self.instance_type = 'ecs.xn4.small'
        # 实例的计费方式
        self.instance_charge_type = instance_charge_type
        # 镜像ID
        self.image_id = image_id
        # 指定新创建实例所属于的安全组ID
        self.security_group_id = security_group_id
        # 购买资源的时长
        self.period = 1
        # 购买资源的时长单位
        self.period_unit = 'Month'
        # 实例所属的可用区编号
        # self.zone_id = 'cn-shenzhen-a'
        # 网络计费类型
        self.internet_charge_type = 'PayByTraffic'
        # 虚拟交换机ID
        self.vswitch_id = vswitch_id
        # 实例名称
        self.instance_name = 'cmdb_create_vpn-%s-%s' % (post_user, time.strftime('%y%m%d-%H%M',
                                                                             time.localtime(time.time())))
        # 指定创建ECS实例的数量
        self.amount = 1
        # 公网出带宽最大值
        self.internet_max_bandwidth_out = 100
        # 是否为I/O优化实例
        self.io_optimized = 'optimized'
        # 密钥对名称
        self.key_pair_name = key_pair_name
        # 系统盘大小
        self.system_disk_size = '40'
        # 系统盘的磁盘种类
        self.system_disk_category = 'cloud_efficiency'
        self.task_obj = task_obj
        self.admin_security_id = admin_security_id
        self.admin_security_access_id = admin_security_access_id
        self.admin_security_access_secret = admin_security_access_secret
        self.admin_security_region_id = admin_security_region_id

        self.client = AcsClient(self.access_id, self.access_secret, self.region_id)
        self.admin_security_client = ''

    def run(self, amount, cout):
        try:
            ids = self.run_instances(amount, cout)
            ip = self._check_instances_status(ids, amount, cout)
            return ip
        except ClientException as e:
            print('Fail. Something with your connection with Aliyun go incorrect.'
                  ' Code: {code}, Message: {msg}'
                  .format(code=e.error_code, msg=e.message))
            self.task_obj._false = ('Fail. Something with your connection with Aliyun go incorrect.'
                                    ' Code: {code}, Message: {msg}'
                                    .format(code=e.error_code, msg=e.message))
        except ServerException as e:
            print('Fail. Business error.'
                  ' Code: {code}, Message: {msg}'
                  .format(code=e.error_code, msg=e.message))
            self.task_obj._false = ('Fail. Business error.'
                                    ' Code: {code}, Message: {msg}'
                                    .format(code=e.error_code, msg=e.message))
        except Exception:
            print('Unhandled error')
            print(traceback.format_exc())
            self.task_obj._false = 'Unhandled error', traceback.format_exc()

    def run_instances(self, amount, cout):
        """
        调用创建实例的API，得到实例ID后继续查询实例状态
        :return:instance_ids 需要检查的实例ID
        """
        request = RunInstancesRequest()

        request.set_DryRun(self.dry_run)

        request.set_InstanceType(self.instance_type)
        request.set_InstanceChargeType(self.instance_charge_type)
        request.set_ImageId(self.image_id)
        request.set_SecurityGroupId(self.security_group_id)
        request.set_Period(self.period)
        request.set_PeriodUnit(self.period_unit)
        # request.set_ZoneId(self.zone_id)
        request.set_InternetChargeType(self.internet_charge_type)
        request.set_VSwitchId(self.vswitch_id)
        request.set_InstanceName(self.instance_name)
        request.set_Amount(self.amount)
        request.set_InternetMaxBandwidthOut(self.internet_max_bandwidth_out)
        request.set_IoOptimized(self.io_optimized)
        request.set_KeyPairName(self.key_pair_name)
        request.set_SystemDiskSize(self.system_disk_size)
        request.set_SystemDiskCategory(self.system_disk_category)

        body = self.client.do_action_with_exception(request)
        data = json.loads(body)
        instance_ids = data['InstanceIdSets']['InstanceIdSet']
        self.task_obj.result = math.ceil(cout / amount * 1 / 3 * 100)
        self.task_obj.save()
        print('Success. Instance creation succeed. InstanceIds: {}'.format(', '.join(instance_ids)))
        return instance_ids

    def add_securitygroup(self, port, vpn_ip):
        self.admin_security_client = AcsClient(self.admin_security_access_id, self.admin_security_access_secret,
                                               self.admin_security_region_id)
        request = AuthorizeSecurityGroupRequest()
        request.set_IpProtocol("tcp")
        request.set_PortRange('%s/%s' % (port, port))
        request.set_SourceCidrIp(vpn_ip)
        request.set_Description("vpn")
        request.set_SecurityGroupId(self.admin_security_id)
        body = self.admin_security_client.do_action_with_exception(request)
        data = json.loads(body)
        RequestId = data['RequestId']
        print('Success, security add succeed. RequestId: {}'.format(','.join(RequestId)))

    def _check_instances_status(self, instance_ids, amount, cout):
        """
        每3秒中检查一次实例的状态，超时时间设为3分钟。
        :param instance_ids 需要检查的实例ID
        :return:
        """
        start = time.time()
        ip = ''
        while True:
            request = DescribeInstancesRequest()
            request.set_InstanceIds(json.dumps(instance_ids))
            body = self.client.do_action_with_exception(request)
            data = json.loads(body)
            for instance in data['Instances']['Instance']:

                if RUNNING_STATUS in instance['Status']:
                    instance_ids.remove(instance['InstanceId'])
                    print('Instance boot successfully: {}'.format(instance['InstanceId']))
                    print(instance["PublicIpAddress"]["IpAddress"][0])
                    if self.admin_security_id and self.admin_security_access_id:
                        try:
                            self.add_securitygroup(80, instance["PublicIpAddress"]["IpAddress"][0])
                            self.add_securitygroup(443, instance["PublicIpAddress"]["IpAddress"][0])
                        except ClientException as e:
                            print('Fail. Something with your connection with Aliyun go incorrect.'
                                  ' Code: {code}, Message: {msg}'
                                  .format(code=e.error_code, msg=e.message))
                            self.task_obj._false = ('Fail. Something with your connection with Aliyun go incorrect.'
                                                    ' Code: {code}, Message: {msg}'
                                                    .format(code=e.error_code, msg=e.message))
                        except ServerException as e:
                            print('Fail. Business error.'
                                  ' Code: {code}, Message: {msg}'
                                  .format(code=e.error_code, msg=e.message))
                            self.task_obj._false = ('Fail. Business error.'
                                                    ' Code: {code}, Message: {msg}'
                                                    .format(code=e.error_code, msg=e.message))
                        except Exception:
                            print('Unhandled error')
                            print(traceback.format_exc())
                            self.task_obj._false = 'Unhandled error', traceback.format_exc()

                    self.task_obj.result = math.ceil(cout / amount * 2 / 3 * 100)
                    self.task_obj.save()
                    ip = instance["PublicIpAddress"]["IpAddress"][0]

            if not instance_ids:
                print('Instances all boot successfully')
                self.task_obj.result = cout / amount * 100
                self.task_obj.save()
                break

            if time.time() - start > CHECK_TIMEOUT:
                print('Instances boot failed within {timeout}s: {ids}'
                      .format(timeout=CHECK_TIMEOUT, ids=', '.join(instance_ids)))
                self.task_obj.result = 'false'
                self.task_obj.save()
                break
            time.sleep(CHECK_INTERVAL)
        return ip


@shared_task
def createshadowsocket(id):
    task_obj = CreateShadowSocketTask.objects.get(pk=id)
    access_id = task_obj.vpn_template.project.AccessKey_ID
    access_secret = task_obj.vpn_template.project.Access_Key_Secret
    region_id = task_obj.vpn_template.project.region_id
    image_id = task_obj.vpn_template.img_id
    security_group_id = task_obj.vpn_template.security_id
    vswitch_id = task_obj.vpn_template.vswitch_id
    key_pair_name = task_obj.vpn_template.secret_key
    instance_charge_type = task_obj.vpn_template.InstanceChargeType
    post_user = task_obj.user.username
    admin_security_id = task_obj.vpn_template.admin_security_id
    amount = task_obj.amount
    if task_obj.vpn_template.admmin_security_alikey:
        admin_security_access_id = task_obj.vpn_template.admmin_security_alikey.AccessKey_ID
        admin_security_access_secret = task_obj.vpn_template.admmin_security_alikey.Access_Key_Secret
        admin_security_region_id = task_obj.vpn_template.admmin_security_alikey.region_id
    else:
        admin_security_access_id = None
        admin_security_access_secret = None
        admin_security_region_id = None

    ecs_obj = AliyunRunShadowSocketInstances(access_id, access_secret, region_id, image_id, security_group_id,
                                             vswitch_id, key_pair_name, instance_charge_type, post_user, task_obj,
                                             admin_security_id, admin_security_access_id, admin_security_access_secret,
                                             admin_security_region_id)
    vpn_ips = ''
    for i in range(amount):
        ip = ecs_obj.run(int(amount), int(i)+1)
        vpn_ips += str(ip) + '\n'
    task_obj.vpn_ip = vpn_ips
    task_obj.status = 2
    task_obj.save()


# -------------------------------------------------- forward 懒得继承 -------------------------------------


class AliyunRunForwardInstances(object):

    def __init__(self, access_id, access_secret, region_id, image_id, security_group_id, vswitch_id, key_pair_name,
                 instance_charge_type, post_user, task_obj):
        self.access_id = access_id
        self.access_secret = access_secret

        # 是否只预检此次请求。true：发送检查请求，不会创建实例，也不会产生费用；false：发送正常请求，通过检查后直接创建实例，并直接产生费用
        self.dry_run = False
        # 实例所属的地域ID
        self.region_id = region_id
        # 实例的资源规格
        self.instance_type = 'ecs.xn4.small'
        # 实例的计费方式
        self.instance_charge_type = instance_charge_type
        # 镜像ID
        self.image_id = image_id
        # 指定新创建实例所属于的安全组ID
        self.security_group_id = security_group_id
        # 购买资源的时长
        self.period = 1
        # 购买资源的时长单位
        self.period_unit = 'Month'
        # 实例所属的可用区编号
        # self.zone_id = 'cn-shenzhen-a'
        # 网络计费类型
        self.internet_charge_type = 'PayByTraffic'
        # 虚拟交换机ID
        self.vswitch_id = vswitch_id
        # 实例名称
        self.instance_name = 'cmdb_create_forward-%s-%s' % (post_user, time.strftime('%y%m%d-%H%M',
                                                                                     time.localtime(time.time())))
        # 指定创建ECS实例的数量
        self.amount = 1
        # 公网出带宽最大值
        self.internet_max_bandwidth_out = 100
        # 是否为I/O优化实例
        self.io_optimized = 'optimized'
        # 密钥对名称
        self.key_pair_name = 'cm_jumper01'
        # 系统盘大小
        self.system_disk_size = '40'
        # 系统盘的磁盘种类
        self.system_disk_category = 'cloud_efficiency'
        self.task_obj = task_obj

        self.client = AcsClient(self.access_id, self.access_secret, self.region_id)

    def run(self, amount, cout):
        try:
            ids = self.run_instances(amount, cout)
            ips = self._check_instances_status(ids, amount, cout)
            return ips
        except ClientException as e:
            print('Fail. Something with your connection with Aliyun go incorrect.'
                  ' Code: {code}, Message: {msg}'
                  .format(code=e.error_code, msg=e.message))
            self.task_obj._false = ('Fail. Something with your connection with Aliyun go incorrect.'
                                    ' Code: {code}, Message: {msg}'
                                    .format(code=e.error_code, msg=e.message))
        except ServerException as e:
            print('Fail. Business error.'
                  ' Code: {code}, Message: {msg}'
                  .format(code=e.error_code, msg=e.message))
            self.task_obj._false = ('Fail. Business error.'
                                    ' Code: {code}, Message: {msg}'
                                    .format(code=e.error_code, msg=e.message))
        except Exception:
            print('Unhandled error')
            print(traceback.format_exc())
            self.task_obj._false = 'Unhandled error', traceback.format_exc()

    def run_instances(self, amount, cout):
        """
        调用创建实例的API，得到实例ID后继续查询实例状态
        :return:instance_ids 需要检查的实例ID
        """
        request = RunInstancesRequest()

        request.set_DryRun(self.dry_run)

        request.set_InstanceType(self.instance_type)
        request.set_InstanceChargeType(self.instance_charge_type)
        request.set_ImageId(self.image_id)
        request.set_SecurityGroupId(self.security_group_id)
        request.set_Period(self.period)
        request.set_PeriodUnit(self.period_unit)
        # request.set_ZoneId(self.zone_id)
        request.set_InternetChargeType(self.internet_charge_type)
        request.set_VSwitchId(self.vswitch_id)
        request.set_InstanceName(self.instance_name)
        request.set_Amount(self.amount)
        request.set_InternetMaxBandwidthOut(self.internet_max_bandwidth_out)
        request.set_IoOptimized(self.io_optimized)
        request.set_KeyPairName(self.key_pair_name)
        request.set_SystemDiskSize(self.system_disk_size)
        request.set_SystemDiskCategory(self.system_disk_category)

        body = self.client.do_action_with_exception(request)
        data = json.loads(body)
        instance_ids = data['InstanceIdSets']['InstanceIdSet']
        print('Success. Instance creation succeed. InstanceIds: {}'.format(', '.join(instance_ids)))
        self.task_obj.result = math.ceil(cout / amount * 1 / 2 * 100)
        self.task_obj.save()
        return instance_ids

    def _check_instances_status(self, instance_ids, amount, cout):
        """
        每3秒中检查一次实例的状态，超时时间设为3分钟。
        :param instance_ids 需要检查的实例ID
        :return:
        """
        start = time.time()
        while True:
            request = DescribeInstancesRequest()
            request.set_InstanceIds(json.dumps(instance_ids))
            body = self.client.do_action_with_exception(request)
            data = json.loads(body)
            pip = ''
            iip = ''
            for instance in data['Instances']['Instance']:
                if RUNNING_STATUS in instance['Status']:
                    instance_ids.remove(instance['InstanceId'])
                    print('Instance boot successfully: {}'.format(instance['InstanceId']))
                    pip = instance["PublicIpAddress"]["IpAddress"][0]
                    iip = instance["VpcAttributes"]["PrivateIpAddress"]["IpAddress"][0]

            if not instance_ids:
                print('Instances all boot successfully')
                self.task_obj.result = cout / amount * 100
                self.task_obj.save()
                break

            if time.time() - start > CHECK_TIMEOUT:
                print('Instances boot failed within {timeout}s: {ids}'
                      .format(timeout=CHECK_TIMEOUT, ids=', '.join(instance_ids)))
                break

            time.sleep(CHECK_INTERVAL)
        return [pip, iip]


@shared_task
def createforward(id):
    task_obj = CreateForwardTask.objects.get(pk=id)
    access_id = task_obj.forward_template.project.AccessKey_ID
    access_secret = task_obj.forward_template.project.Access_Key_Secret
    region_id = task_obj.forward_template.project.region_id
    image_id = task_obj.forward_template.img_id
    security_group_id = task_obj.forward_template.security_id
    vswitch_id = task_obj.forward_template.vswitch_id
    key_pair_name = task_obj.forward_template.secret_key
    instance_charge_type = task_obj.forward_template.InstanceChargeType
    post_user = task_obj.user.username
    amount = task_obj.amount

    ecs_obj = AliyunRunForwardInstances(access_id, access_secret, region_id, image_id, security_group_id,
                                        vswitch_id, key_pair_name, instance_charge_type, post_user, task_obj)

    forward_pip = ''
    forward_iip = ''
    for i in range(amount):
        ips = ecs_obj.run(int(amount), int(i)+1)
        forward_pip += str(ips[0]) + '\n'
        forward_iip += str(ips[1]) + '\n'

    task_obj.forward_pip = forward_pip
    task_obj.forward_iip = forward_iip
    task_obj.status = 2
    task_obj.save()
