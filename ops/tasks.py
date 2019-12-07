from celery import shared_task
import os
from aliyunsdkalidns.request.v20150109.OperateBatchDomainRequest import OperateBatchDomainRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.DeleteDomainRecordRequest import DeleteDomainRecordRequest
import json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AliyunCenter.settings')
from multiprocessing import Pool
import math

from .models import GtmCheckDomain


def setDomain(client, domains, value, id, rtype):
    task_id = list()
    for domain in domains:
        gtm_data = list()
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
def SwitchDomain(client, domains, value, id, rtype):
    pool = Pool(processes=2)
    return_dict = list()
    jobs = list()
    step = math.ceil(len(domains) / 2)
    domains = [domains[i:i + step] for i in range(0, len(domains), step)]
    if len(domains) < 2:
        r1 = pool.apply_async(setDomain, (client, domains[0], value, id, rtype))
        jobs.append(r1)
    else:
        r1 = pool.apply_async(setDomain, (client, domains[0], value, id, rtype))
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


