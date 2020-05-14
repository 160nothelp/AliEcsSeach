from django.http import HttpResponse
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest, DescribeInstanceAutoRenewAttributeRequest, \
    DescribeInstanceMonitorDataRequest
from aliyunsdkslb.request.v20140515 import DescribeLoadBalancersRequest
import json
import datetime
from django.core.cache import cache
from django.utils.decorators import method_decorator
from dwebsocket.decorators import accept_websocket, require_websocket
from django.core.paginator import Paginator
from django.core import serializers
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import PostTaskSerializer, GetTaskSerializer
from .models import AliUserAccessKey, OtherPlatforms, HostIpSearchTask
from .utils import AliClient, ECSList, ECSDetails, isIpV4AddrLegal, SlbList
from .tasks import SearchHostIp, SearchHostInstancename
from user.user_permission import HostsPermission, ProjectPermissions
from audit.addlog import add_tasks_log


@accept_websocket
def GraphicsView(request):
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


class HostListUserSelectView(viewsets.GenericViewSet, mixins.ListModelMixin):
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    @method_decorator(HostsPermission)
    def list(self, request, *args, **kwargs):
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
        return Response({
            'userdata': userdata_
        })


class EcsHostTableView(viewsets.GenericViewSet, mixins.ListModelMixin):
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    @method_decorator(HostsPermission)
    @method_decorator(ProjectPermissions)
    def list(self, request, *args, **kwargs):
        user = request.query_params.get('user')
        page_size = request.query_params.get('page_size')
        page_num = request.query_params.get('page_num')
        key = user + str(page_num) + str(page_size)
        if cache.get(key) is not None:
            json_data = cache.get(key)
        else:
            try:
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
            except Exception as e:
                print(e)
                return HttpResponse(status=404)
        ecslistobj = ECSList(json_data, user)
        index_data_ = ecslistobj.IndexList()

        return Response({
            'index_data_': index_data_
        })


class OtherHostTableView(viewsets.GenericViewSet, mixins.ListModelMixin):
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    @method_decorator(HostsPermission)
    def list(self, request, *args, **kwargs):
        other_user = request.query_params.get('other_user')
        page_size = request.query_params.get('page_size')
        page_num = request.query_params.get('page_num')
        otheruserdata = OtherPlatforms.objects.get(nickname=other_user)
        hosts = otheruserdata.hosts.all()
        p = Paginator(hosts, int(page_size))
        totalpage = p.num_pages
        totalCount = p.count
        page = p.page(page_num)
        page_json = serializers.serialize("json", page)
        page_json = json.loads(page_json)

        return Response({
            'table': page_json,
            'nichname': other_user,
            'totalpage': totalpage,
            'TotalCount': totalCount
        })


class SlbListView(viewsets.GenericViewSet, mixins.ListModelMixin):
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    @method_decorator(HostsPermission)
    @method_decorator(ProjectPermissions)
    def list(self, request, *args, **kwargs):
        user = request.query_params.get('user')
        page_size = request.query_params.get('page_size')
        page_num = request.query_params.get('page_num')
        key = user + str(page_num) + str(page_size) + '_slb'
        if cache.get(key) is not None:
            json_data = cache.get(key)
        else:
            try:
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
            except Exception as e:
                print(e)
                return HttpResponse(status=404)
        slbobj = SlbList(json_data)
        slb_json = slbobj.indexlist()
        return Response({
            'slb': slb_json
        })


class AliEcsDetailsView(viewsets.GenericViewSet, mixins.ListModelMixin):
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    @method_decorator(HostsPermission)
    def list(self, request, *args, **kwargs):
        aliuser = request.query_params.get('user')
        instanceid = request.query_params.get('instanceid')
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

        return Response({
            'ecsdetails': ecsdetails
        })


class AliSearchView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = PostTaskSerializer
    queryset = HostIpSearchTask.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    @method_decorator(add_tasks_log('主机搜索'))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        if request.data['category'] == 'AllIP':
            SearchHostIp.delay(request.data['sdata'], serializer.data['id'], request.user.username)
        elif request.data['category'] == 'AllName':
            SearchHostInstancename.delay(request.data['allname'], serializer.data['id'], request.user.username)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AliSearchGetStatusView(mixins.ListModelMixin, viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    serializer_class = GetTaskSerializer
    queryset = HostIpSearchTask.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        try:
            results = eval(serializer.data['result'])
        except Exception as e:
            print(e)
            return Response({
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
        return Response({
            'search_data': all_data,
            'status': serializer.data['status']
        })

