from celery import shared_task
import os
import json
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkslb.request.v20140515 import DescribeLoadBalancersRequest
import math
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AliyunCenter.settings')
from multiprocessing import Pool
from django.core import serializers

from django.core.cache import cache
from .utils import AliClient
from .models import AliUserAccessKey, HostIpSearchTask, OtherPlatforms


def ChangUserCache(allclient):
    totals = list()
    for client in allclient:
        TotalCount = dict()
        alirequest = DescribeInstancesRequest.DescribeInstancesRequest()
        alirequest.set_accept_format('json')
        alirequest.set_PageSize(100)
        response = client['client'].do_action_with_exception(alirequest)
        json_data = json.loads(str(response, encoding='utf-8'))
        cache.set(client['user'], json_data, 60 * 10)
        TotalCount['user'] = client['user']
        TotalCount['client'] = client['client']
        TotalCount['totalcount'] = json_data["TotalCount"]
        totals.append(TotalCount)
    return totals


def PageCache(pagesizes, totals):
    for total in totals:
        for pagesize in pagesizes:
            totalPages = math.ceil(total['totalcount'] / pagesize)
            for totalPage in range(1, int(totalPages)+1):
                alirequest = DescribeInstancesRequest.DescribeInstancesRequest()
                alirequest.set_accept_format('json')
                alirequest.set_PageNumber(totalPage)
                alirequest.set_PageSize(pagesize)
                response = total['client'].do_action_with_exception(alirequest)
                json_data = json.loads(str(response, encoding='utf-8'))
                key = total['user'] + str(totalPage) + str(pagesize)
                cache.set(key, json_data, 60 * 10)


def DefaultCache(allclient):
    defclient = allclient[0]['client']
    alirequest = DescribeInstancesRequest.DescribeInstancesRequest()
    alirequest.set_accept_format('json')
    alirequest.set_PageSize(100)
    response = defclient.do_action_with_exception(alirequest)
    json_data = json.loads(str(response, encoding='utf-8'))
    cache.set('Default_Index', json_data, 60 * 10)


def SlbCache(pagesizes, totals):
    for total in totals:
        for pagesize in pagesizes:
            totalPages = math.ceil(total['totalcount'] / pagesize)
            for totalPage in range(1, int(totalPages) + 1):
                try:
                    alirequest = DescribeLoadBalancersRequest.DescribeLoadBalancersRequest()
                    alirequest.set_accept_format('json')
                    alirequest.set_PageNumber(totalPage)
                    alirequest.set_PageSize(pagesize)
                    response = total['client'].do_action_with_exception(alirequest)
                    json_data = json.loads(str(response, encoding='utf-8'))
                    key = total['user'] + str(totalPage) + str(pagesize) + '_slb'
                    cache.set(key, json_data, 60 * 10)
                except Exception as e:
                    key = total['user'] + str(totalPage) + str(pagesize) + '_slb'
                    cache.set(key, '', 60 * 10)


@shared_task
def SetEcsCache():
    allclient = list()
    aliuserlist = AliUserAccessKey.objects.all()
    for aliuserobj in aliuserlist:
        dic = dict()
        ClientObj = AliClient(aliuserobj.AccessKey_ID, aliuserobj.Access_Key_Secret, aliuserobj.region_id)
        aliclient = ClientObj.client()
        dic['client'] = aliclient
        dic['user'] = aliuserobj.nickname
        allclient.append(dic)

    # default cache
    DefaultCache(allclient)

    # change user cache
    totals = ChangUserCache(allclient)

    # page cache
    pagesizes = [10, 50, 100]
    PageCache(pagesizes, totals)

    # slb cache
    SlbCache(pagesizes, totals)


# ----------------------------------------- 搜索------------------------------------------------------------------------


def searchPrivateIp(aliuser, ip, user_type):
    clientobj = AliClient(aliuser.AccessKey_ID, aliuser.Access_Key_Secret,
                          aliuser.region_id)
    client = clientobj.client()
    alirequest = DescribeInstancesRequest.DescribeInstancesRequest()
    alirequest.set_accept_format('json')
    alirequest.set_PageSize(100)
    alirequest.set_PrivateIpAddresses([ip])
    response = client.do_action_with_exception(alirequest)
    json_data = json.loads(str(response, encoding='utf-8'))
    if len(json_data['Instances']['Instance']) == 0:
        pass
    else:
        json_data['nickname'] = aliuser.nickname
        json_data['user_type'] = user_type
        return json_data


def searchPublicIp(aliuser, ip, user_type):
    clientobj = AliClient(aliuser.AccessKey_ID, aliuser.Access_Key_Secret,
                          aliuser.region_id)
    client = clientobj.client()
    alirequest = DescribeInstancesRequest.DescribeInstancesRequest()
    alirequest.set_accept_format('json')
    alirequest.set_PageSize(100)
    alirequest.set_PublicIpAddresses([ip])
    response = client.do_action_with_exception(alirequest)
    json_data = json.loads(str(response, encoding='utf-8'))
    if len(json_data['Instances']['Instance']) == 0:
        pass
    else:
        json_data['nickname'] = aliuser.nickname
        json_data['user_type'] = user_type
        return json_data


def searchEip(aliuser, ip, user_type):
    clientobj = AliClient(aliuser.AccessKey_ID, aliuser.Access_Key_Secret,
                          aliuser.region_id)
    client = clientobj.client()
    alirequest = DescribeInstancesRequest.DescribeInstancesRequest()
    alirequest.set_accept_format('json')
    alirequest.set_PageSize(100)
    alirequest.set_EipAddresses([ip])
    response = client.do_action_with_exception(alirequest)
    json_data = json.loads(str(response, encoding='utf-8'))
    if len(json_data['Instances']['Instance']) == 0:
        pass
    else:
        json_data['nickname'] = aliuser.nickname
        json_data['user_type'] = user_type
        return json_data


def searchOtherPublicIp(other_user, ip, user_type):
    query_data = other_user.hosts.filter(PublicIpAddress=ip)
    if query_data:
        json_data = serializers.serialize("json", query_data)
        json_data = json.loads(json_data)
        json_data_ = dict()
        json_data_['table_data'] = json_data
        json_data_['nickname'] = other_user.nickname
        json_data_['user_type'] = user_type
        return json_data_


def searchOtherPrivateIp(other_user, ip, user_type):
    query_data = other_user.hosts.filter(PrivateIpAddress=ip)
    if query_data:
        json_data = serializers.serialize("json", query_data)
        json_data = json.loads(json_data)
        json_data_ = dict()
        json_data_['table_data'] = json_data
        json_data_['nickname'] = other_user.nickname
        json_data_['user_type'] = user_type
        return json_data_


def searchSlbIp(aliuser, ip, user_type):
    try:
        clientobj = AliClient(aliuser.AccessKey_ID, aliuser.Access_Key_Secret,
                              aliuser.region_id)
        client = clientobj.client()
        alirequest = DescribeLoadBalancersRequest.DescribeLoadBalancersRequest()
        alirequest.set_accept_format('json')
        alirequest.set_PageSize(100)
        alirequest.set_Address(ip)
        response = client.do_action_with_exception(alirequest)
        json_data = json.loads(str(response, encoding='utf-8'))
        if len(json_data["LoadBalancers"]["LoadBalancer"]) == 0:
            pass
        else:
            json_data['nickname'] = aliuser.nickname
            json_data['user_type'] = user_type
            json_data['slb'] = 1
            return json_data
    except Exception as e:
        print(e)


@shared_task
def SearchHostIp(ip, id):
    pool = Pool(processes=3)
    return_dict = list()
    users = list()
    jobs = list()
    aliuserobj = AliUserAccessKey.objects.all()
    otheruserobj = OtherPlatforms.objects.all()
    for aliuser in aliuserobj:
        user = dict()
        user['user'] = aliuser
        user['user_type'] = 'aliuser'
        users.append(user)
    for other_user in otheruserobj:
        user = dict()
        user['user'] = other_user
        user['user_type'] = 'other_user'
        users.append(user)
    for user in users:
        if user['user_type'] == 'aliuser':
            r1 = pool.apply_async(searchPrivateIp, (user['user'], ip, user['user_type']))
            r2 = pool.apply_async(searchPublicIp, (user['user'], ip, user['user_type']))
            r3 = pool.apply_async(searchEip, (user['user'], ip, user['user_type']))
            r6 = pool.apply_async(searchSlbIp, (user['user'], ip, user['user_type']))
            jobs.append(r1)
            jobs.append(r2)
            jobs.append(r3)
            jobs.append(r6)
        elif user['user_type'] == 'other_user':
            r4 = pool.apply_async(searchOtherPrivateIp, (user['user'], ip, user['user_type']))
            r5 = pool.apply_async(searchOtherPublicIp, (user['user'], ip, user['user_type']))
            jobs.append(r4)
            jobs.append(r5)
    pool.close()
    pool.join()
    for job in jobs:
        return_dict.append(job.get())
    taskobj = HostIpSearchTask.objects.get(pk=id)
    taskobj.result = return_dict
    taskobj.status = 2
    taskobj.save()
    print('ok')
    return True


def searchEcsInstancename(aliuser, instancename, user_type):
    clientobj = AliClient(aliuser.AccessKey_ID, aliuser.Access_Key_Secret,
                          aliuser.region_id)
    client = clientobj.client()
    alirequest = DescribeInstancesRequest.DescribeInstancesRequest()
    alirequest.set_accept_format('json')
    alirequest.set_PageSize(100)
    alirequest.set_InstanceName('*%s*' % instancename)
    response = client.do_action_with_exception(alirequest)
    json_data = json.loads(str(response, encoding='utf-8'))
    if len(json_data['Instances']['Instance']) == 0:
        pass
    else:
        json_data['nickname'] = aliuser.nickname
        json_data['user_type'] = user_type
        return json_data


def searchOtherInstancename(other_user, instancename, user_type):
    query_data = other_user.hosts.filter(InstanceName__icontains=instancename)
    if query_data:
        json_data = serializers.serialize("json", query_data)
        json_data = json.loads(json_data)
        json_data_ = dict()
        json_data_['table_data'] = json_data
        json_data_['nickname'] = other_user.nickname
        json_data_['user_type'] = user_type
        return json_data_


def searchSlbInstancename(aliuser, instancename, user_type):
    pass


@shared_task
def SearchHostInstancename(instancename, id):
    pool = Pool(processes=3)
    return_dict = list()
    users = list()
    jobs = list()
    aliuserobj = AliUserAccessKey.objects.all()
    otheruserobj = OtherPlatforms.objects.all()
    for aliuser in aliuserobj:
        user = dict()
        user['user'] = aliuser
        user['user_type'] = 'aliuser'
        users.append(user)
    for other_user in otheruserobj:
        user = dict()
        user['user'] = other_user
        user['user_type'] = 'other_user'
        users.append(user)
    for user in users:
        if user['user_type'] == 'aliuser':
            r1 = pool.apply_async(searchEcsInstancename, (user['user'], instancename, user['user_type']))
            jobs.append(r1)
        elif user['user_type'] == 'other_user':
            r2 = pool.apply_async(searchOtherInstancename, (user['user'], instancename, user['user_type']))
            jobs.append(r2)
    pool.close()
    pool.join()
    for job in jobs:
        return_dict.append(job.get())
    taskobj = HostIpSearchTask.objects.get(pk=id)
    taskobj.result = return_dict
    taskobj.status = 2
    taskobj.save()
    print('ok')
    return True



