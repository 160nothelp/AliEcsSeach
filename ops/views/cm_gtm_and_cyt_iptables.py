from django.http import JsonResponse
from django.views import View
from aliyunsdkcore.client import AcsClient
from aliyunsdkalidns.request.v20150109.DescribeBatchResultCountRequest import DescribeBatchResultCountRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
import json
from django.utils.decorators import method_decorator
from dwebsocket.decorators import accept_websocket, require_websocket
from datetime import datetime
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from ops.serializers import PostTaskSerializer, AliRamSerializer, GetSwitchStatusSerializer, TmpCytWhiteIpTablesSerializer
from ops.models import GtmCheckDomain, AliRamLink, GtmDefaultLine, TmpCytWhiteIpTables
from ops.tasks import SwitchDomain, tmpCytIptables
from user.user_permission import GtmPermission, CytIptablesPermission
from aliecs.utils import isIpV4AddrLegal
from audit.addlog import add_tasks_log


# class SwitchGtm(View):
#     @method_decorator(GtmPermission)
#     def post(self, request):
#         payload = json.loads(request.body)
#         type = payload['type']
#         domains_obj = GtmCheckDomain.objects.first()
#         donamins = domains_obj.domain_list.strip().split()
#         special_domain = domains_obj.special_domain.strip().split()
#         step = 20
#         donamins = [donamins[i:i + step] for i in range(0, len(donamins), step)]
#         domains_obj.task_id = None
#         domains_obj.save()
#         client = AcsClient(domains_obj.AccessKey_ID, domains_obj.Access_Key_Secret, domains_obj.region_id)
#         if type == 'gtm':
#             rtype = 'CNAME'
#             SwitchDomain.delay(client, donamins, domains_obj.gtm_cname, domains_obj.id, rtype, special_domain)
#         if type == 'default':
#             rtype = 'A'
#             SwitchDomain.delay(client, donamins, domains_obj.default_line, domains_obj.id, rtype, special_domain)
#
#         return JsonResponse({
#             'status': 'complete'
#         })


class SwitchGtmView(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = PostTaskSerializer
    queryset = GtmDefaultLine.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    @method_decorator(add_tasks_log('批量更换cm域名解析'))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({
            'status': 'complete'
        }, status=status.HTTP_201_CREATED)


class GetSwitchStatus(View):
    def get(self, request):
        domains_obj = GtmCheckDomain.objects.first()
        client = AcsClient(domains_obj.AccessKey_ID, domains_obj.Access_Key_Secret, domains_obj.region_id)
        result = list()
        try:
            task_id_obj = eval(domains_obj.task_id)
        except Exception as e:
            return JsonResponse({
                'result': 1,
                'status': 'pass'
            })
        for task_ids in task_id_obj:
            result_ = ''
            for task_id in task_ids:
                request_ = DescribeBatchResultCountRequest()
                request_.set_accept_format('json')
                request_.set_TaskId(task_id)
                response = client.do_action_with_exception(request_)
                json_data = json.loads(str(response, encoding='utf-8'))
                if json_data['Status'] == 1:
                    result_ = '已完成'
                if json_data['Status'] == 2:
                    result_ = '已完成'
                    result.append('有错误，错误数量：%s' % json_data.get('FailedCount'))
                if json_data['Status'] == 0:
                    result_ = '执行中'
                if json_data['Status'] == -1:
                    result_ = '已完成'
                    result.append('有域名不属于阿里云的管控')

            result.append(result_)
        index = [i for i, a in enumerate(result) if a == '执行中']
        if len(index) == 0:
            status = 'all'
        else:
            status = 'no'
        return JsonResponse({
            'result': result,
            'status': status
        })


class GetSwitchStatusView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = GetSwitchStatusSerializer
    queryset = GtmCheckDomain.objects.all()

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     serializer = self.get_serializer(queryset, many=True)
    #     try:
    #         task_id_obj = eval(serializer.data['task_id'])
    #     except Exception as e:
    #         return Response({
    #             'result': 1,
    #             'status': 'pass'
    #         })
    #     client = AcsClient(serializer.AccessKey_ID, serializer.Access_Key_Secret, serializer.region_id)
    #     result = list()
    #     for task_ids in task_id_obj:
    #         result_ = ''
    #         for task_id in task_ids:
    #             request_ = DescribeBatchResultCountRequest()
    #             request_.set_accept_format('json')
    #             request_.set_TaskId(task_id)
    #             response = client.do_action_with_exception(request_)
    #             json_data = json.loads(str(response, encoding='utf-8'))
    #             if json_data['Status'] == 1:
    #                 result_ = '已完成'
    #             if json_data['Status'] == 2:
    #                 result_ = '已完成'
    #                 result.append('有错误，错误数量：%s' % json_data.get('FailedCount'))
    #             if json_data['Status'] == 0:
    #                 result_ = '执行中'
    #             if json_data['Status'] == -1:
    #                 result_ = '已完成'
    #                 result.append('有域名不属于阿里云的管控')
    #
    #         result.append(result_)
    #     index = [i for i, a in enumerate(result) if a == '执行中']
    #     if len(index) == 0:
    #         status = 'all'
    #     else:
    #         status = 'no'
    #     return Response({
    #         'result': result,
    #         'status': status
    #     })


@accept_websocket
def CheckDomainLine(request):
    for message in request.websocket:
        domains_obj = GtmCheckDomain.objects.first()
        domains = domains_obj.domain_list.strip().split()
        total = len(domains)
        counter = 0
        null = 0
        for domain in domains:
            client = AcsClient(domains_obj.AccessKey_ID, domains_obj.Access_Key_Secret, domains_obj.region_id)
            alirequest = DescribeDomainRecordsRequest()
            alirequest.set_accept_format('json')
            alirequest.set_DomainName(domain)
            response = client.do_action_with_exception(alirequest)
            json_data = json.loads(str(response, encoding='utf-8'))
            line = 'default'
            for RecordId in json_data['DomainRecords']['Record']:
                try:
                    if RecordId['Value'] is not None:
                        is_true = isIpV4AddrLegal(RecordId['Value'])
                        if not is_true:
                            line = 'gtm'
                    else:
                        line = 'null'
                except Exception as e:
                    line = 'null'
            if line == 'default':
                counter += 1
            if line == 'null':
                null += 1
        other = total - counter - null
        now = datetime.now()
        cday = now.strftime('%Y-%m-%d %H:%M:%S')
        request.websocket.send(json.dumps({'total': total, 'counter': counter, 'other': other, 'time': cday, 'null': null}))


class AliRamView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = AliRamSerializer
    queryset = AliRamLink.objects.all()


class TmpCytWhiteIpTablesView(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = TmpCytWhiteIpTablesSerializer
    queryset = TmpCytWhiteIpTables.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    @method_decorator(CytIptablesPermission)
    @method_decorator(add_tasks_log('添加cyt_iptables'))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        tmpCytIptables.delay(serializer.data['id'])
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


