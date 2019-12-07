from django.http import JsonResponse
from django.views import View
from aliyunsdkcore.client import AcsClient
from aliyunsdkalidns.request.v20150109.DescribeBatchResultCountRequest import DescribeBatchResultCountRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
import json
from django.utils.decorators import method_decorator
from dwebsocket.decorators import accept_websocket, require_websocket

from .models import GtmCheckDomain
from .tasks import SwitchDomain
from user.api_session import authenticate
from user.user_permission import GtmPermission
from aliecs.utils import isIpV4AddrLegal


class SwitchGtm(View):
    @method_decorator(authenticate)
    @method_decorator(GtmPermission)
    def post(self, request):
        payload = json.loads(request.body)
        type = payload['type']
        domains_obj = GtmCheckDomain.objects.first()
        donamins = domains_obj.domain_list.strip().split()
        step = 20
        donamins = [donamins[i:i + step] for i in range(0, len(donamins), step)]
        domains_obj.task_id = None
        domains_obj.save()
        client = AcsClient(domains_obj.AccessKey_ID, domains_obj.Access_Key_Secret, domains_obj.region_id)
        if type == 'gtm':
            rtype = 'CNAME'
            SwitchDomain.delay(client, donamins, domains_obj.gtm_cname, domains_obj.id, rtype)
        if type == 'default':
            rtype = 'A'
            SwitchDomain.delay(client, donamins, domains_obj.default_line, domains_obj.id, rtype)

        return JsonResponse({
            'status': 'complete'
        })


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
                    result_ = '已完成，有错误，错误数量：%s' % json_data.get('FailedCount')
                if json_data['Status'] == 0:
                    result_ = '执行中'
                if json_data['Status'] == -1:
                    result_ = '有域名不对'

            result.append(result_)
        index = [i for i, a in enumerate(result) if a == '执行中' or a == '有域名不对']
        if len(index) == 0:
            status = 'all'
        else:
            status = 'no'
        return JsonResponse({
            'result': result,
            'status': status
        })


# class CheckDomainLine(View):
#     @method_decorator(authenticate)
#     @method_decorator(GtmPermission)
@accept_websocket
def CheckDomainLine(request):
    for message in request.websocket:
        domains_obj = GtmCheckDomain.objects.first()
        domains = domains_obj.domain_list.strip().split()
        total = len(domains)
        counter = 0
        for domain in domains:
            client = AcsClient(domains_obj.AccessKey_ID, domains_obj.Access_Key_Secret, domains_obj.region_id)
            alirequest = DescribeDomainRecordsRequest()
            alirequest.set_accept_format('json')
            alirequest.set_DomainName(domain)
            response = client.do_action_with_exception(alirequest)
            json_data = json.loads(str(response, encoding='utf-8'))
            line = 'default'
            for RecordId in json_data['DomainRecords']['Record']:
                is_true = isIpV4AddrLegal(RecordId['Value'])
                if not is_true:
                    line = 'gtm'
            if line == 'default':
                counter += 1
        other = total - counter
        request.websocket.send(json.dumps({'total': total, 'counter': counter, 'other': other}))
    # return JsonResponse({
    #     'total': total,
    #     'counter': counter
    # })

