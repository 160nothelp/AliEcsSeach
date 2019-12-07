from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest, DescribeInstanceAutoRenewAttributeRequest, \
    DescribeInstanceMonitorDataRequest
from aliyunsdkslb.request.v20140515 import DescribeLoadBalancersRequest
import json
import datetime
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from dwebsocket.decorators import accept_websocket, require_websocket
from django.core.paginator import Paginator
from django.core import serializers

from .models import AliUserAccessKey, OtherPlatforms, HostIpSearchTask
from .utils import AliClient, ECSList, ECSDetails, isIpV4AddrLegal, SlbList
from .tasks import SearchHostIp
from user.api_session import authenticate
from user.user_permission import HostsPermission


@accept_websocket
def GraphicsView(request):
    '''
    监控信息，websocket通道
    :param request:
    :return: websocket
    '''
    if not request.is_websocket():
        print('error')
    else:
        for message in request.websocket:
            payload = json.loads(message)
            ecsdata = AliUserAccessKey.objects.get(nickname=payload['aliuser'])
            clientobj = AliClient(ecsdata.AccessKey_ID, ecsdata.Access_Key_Secret,
                                  ecsdata.region_id)
            client = clientobj.client()
            alirequest = DescribeInstanceMonitorDataRequest.DescribeInstanceMonitorDataRequest()
            alirequest.set_accept_format('json')
            endTime = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'
            onehourago = datetime.datetime.utcnow() + datetime.timedelta(hours=-1)
            startTime = onehourago.replace(microsecond=0).isoformat() + 'Z'
            alirequest.set_EndTime(endTime)
            alirequest.set_StartTime(startTime)
            alirequest.set_InstanceId(payload['instanceid'])
            response = client.do_action_with_exception(alirequest)
            json_data = json.loads(str(response, encoding='utf-8'))
            request.websocket.send(json.dumps(json_data["MonitorData"]["InstanceMonitorData"]))


# API ------------------------------------------------------------------------------------------------------------------


class IndexBaseView(View):
    @method_decorator(authenticate)
    def get(self, request):
        username = request.user.username

        return JsonResponse({
            'username': username
        })


class HostListUserSelect(View):
    @method_decorator(authenticate)
    @method_decorator(HostsPermission)
    def get(self, request):
        userdata = AliUserAccessKey.objects.all()
        userdata_ = list()
        for userobj in userdata:
            user_nikename = dict()
            user_nikename['nickname'] = userobj.nickname
            userdata_.append(user_nikename)
        otheruserdata = OtherPlatforms.objects.all()
        for otheruser in otheruserdata:
            otheruser_nikename = dict()
            otheruser_nikename['nickname'] = otheruser.nickname
            otheruser_nikename['the_other'] = otheruser.the_other
            userdata_.append(otheruser_nikename)

        return JsonResponse({
            'userdata': userdata_
        })


class EcsHostTableView(View):
    @method_decorator(authenticate)
    @method_decorator(HostsPermission)
    def get(self, request):
        user = request.GET.get('user')
        page_size = request.GET.get('page_size')
        page_num = request.GET.get('page_num')
        key = user + str(page_num) + str(page_size)
        if cache.get(key) is not None:
            json_data = cache.get(key)
        else:
            ecsdata = AliUserAccessKey.objects.get(nickname=user)
            clientobj = AliClient(ecsdata.AccessKey_ID, ecsdata.Access_Key_Secret,
                                  ecsdata.region_id)
            client = clientobj.client()

            alirequest = DescribeInstancesRequest.DescribeInstancesRequest()
            alirequest.set_accept_format('json')
            alirequest.set_PageNumber(page_num)
            alirequest.set_PageSize(page_size)
            response = client.do_action_with_exception(alirequest)
            json_data = json.loads(str(response, encoding='utf-8'))
        ecslistobj = ECSList(json_data, user)
        index_data_ = ecslistobj.IndexList()

        return JsonResponse({
            'index_data_': index_data_
        })


class HostTableView(View):
    @method_decorator(authenticate)
    @method_decorator(HostsPermission)
    def get(self, request):
        other_user = request.GET.get('other_user')
        page_size = request.GET.get('page_size')
        page_num = request.GET.get('page_num')
        otheruserdata = OtherPlatforms.objects.get(nickname=other_user)
        hosts = otheruserdata.hosts.all()
        p = Paginator(hosts, int(page_size))
        totalpage = p.num_pages
        totalCount = p.count
        page = p.page(page_num)
        page_json = serializers.serialize("json", page)
        page_json = json.loads(page_json)

        return JsonResponse({
            'table': page_json,
            'nichname': other_user,
            'totalpage': totalpage,
            'TotalCount': totalCount
        })


class HostIpSearchView(View):
    @method_decorator(authenticate)
    @method_decorator(HostsPermission)
    def post(self, request):
        payload = json.loads(request.body)
        if payload['sdata'].strip() != '':
            if payload['category'] == 'AllIP':
                is_true = isIpV4AddrLegal(payload['sdata'])
                if is_true:
                    ip = payload['sdata'].strip()
                    searchobj = HostIpSearchTask(allip=ip, status=1, result='')
                    searchobj.save()
                    SearchHostIp.delay(ip, str(searchobj.id))
                    return JsonResponse({
                        'status': 'ok',
                        'task_id': str(searchobj.id)
                    })
                else:
                    return JsonResponse({
                        'status': 'pass'
                    })
        else:
            return JsonResponse({
                'status': 'pass'
            })


class GetHostIpSearch(View):
    def get(self, request):
        task_id = request.GET.get('task_id')
        taskobj = HostIpSearchTask.objects.get(pk=task_id)
        try:
            results = eval(taskobj.result)
        except Exception as e:
            return JsonResponse({
                'wait': 1
            })
        all_data = list()
        index_data = list()
        for result in results:
            if result is not None:
                if result['user_type'] == 'aliuser':
                    if result.get('slb'):
                        slbobj = SlbList(result)
                        slb_json = slbobj.indexlist()
                        slb_json['user_type'] = 'aliuser'
                        slb_json['slb'] = 1
                        all_data.append(slb_json)
                    else:
                        ecslistobj = ECSList(result, result['nickname'])
                        index_data_ = ecslistobj.IndexList()
                        for data in index_data_['index_data']:
                            index_data.append(data)
                        all_data.append({'PageNumber': 1, 'totalPages': 1, 'index_data': index_data, 'pagesize_off': True
                                         , 'user_type': 'aliuser'})
                if result['user_type'] == 'other_user':
                    all_data.append(result)
        return JsonResponse({
            'search_data': all_data,
            'status': taskobj.status
        })


class SlbListView(View):
    @method_decorator(authenticate)
    @method_decorator(HostsPermission)
    def get(self, request):
        user = request.GET.get('user')
        page_size = request.GET.get('page_size')
        page_num = request.GET.get('page_num')
        key = user + str(page_num) + str(page_size) + '_slb'
        if cache.get(key) is not None:
            json_data = cache.get(key)
        else:
            userdata = AliUserAccessKey.objects.get(nickname=user)
            clientobj = AliClient(userdata.AccessKey_ID, userdata.Access_Key_Secret,
                                  userdata.region_id)
            client = clientobj.client()
            alirequest = DescribeLoadBalancersRequest.DescribeLoadBalancersRequest()
            alirequest.set_accept_format('json')
            alirequest.set_PageSize(page_size)
            alirequest.set_PageNumber(page_num)
            response = client.do_action_with_exception(alirequest)
            json_data = json.loads(str(response, encoding='utf-8'))
        slbobj = SlbList(json_data)
        slb_json = slbobj.indexlist()
        return JsonResponse({
            'slb': slb_json
        })


class AliEcsDetailsView(View):
    '''
    详情页
    参数：用户，实例id
    模板
    '''
    @method_decorator(authenticate)
    @method_decorator(HostsPermission)
    def get(self, request):
        aliuser = request.GET.get('user')
        instanceid = request.GET.get('instanceid')
        ecsdata = AliUserAccessKey.objects.get(nickname=aliuser.strip())
        clientobj = AliClient(ecsdata.AccessKey_ID, ecsdata.Access_Key_Secret,
                              ecsdata.region_id)
        client = clientobj.client()
        alirequest = DescribeInstancesRequest.DescribeInstancesRequest()
        alirequest.set_accept_format('json')
        alirequest.set_InstanceIds([instanceid.strip()])
        response = client.do_action_with_exception(alirequest)
        json_data = json.loads(str(response, encoding='utf-8'))
        ecsdetailsobj = ECSDetails(json_data)
        ecsdetails = ecsdetailsobj.DetailList()
        ecsdetails['aliuser'] = aliuser
        try:
            alirequest = DescribeInstanceAutoRenewAttributeRequest.DescribeInstanceAutoRenewAttributeRequest()
            alirequest.set_accept_format('json')
            alirequest.set_InstanceId(instanceid.strip())
            response = client.do_action_with_exception(alirequest)
            json_data = json.loads(str(response, encoding='utf-8'))
            renew_data = json_data['InstanceRenewAttributes']['InstanceRenewAttribute'][0]
            ecsdetails['AutoRenewEnabled'] = renew_data['AutoRenewEnabled']
        except Exception as e:
            ecsdetails['AutoRenewEnabled'] = ''

        return JsonResponse({
            'ecsdetails': ecsdetails
        })

