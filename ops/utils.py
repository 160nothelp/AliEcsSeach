from aliyunsdkalidns.request.v20150109.OperateBatchDomainRequest import OperateBatchDomainRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.DeleteDomainRecordRequest import DeleteDomainRecordRequest
import json


def del_existings(client, domains, domains_obj):
    RecordIdLists = list()
    for domain in domains:
        gtm_data = list()
        for limit in domain:
            request = DescribeDomainRecordsRequest()
            request.set_accept_format('json')
            request.set_DomainName(limit)
            response = client.do_action_with_exception(request)
            json_data = json.loads(str(response, encoding='utf-8'))
            RecordIdList_ = list()
            for RecordId in json_data['DomainRecords']['Record']:
                RecordIdList_.append(RecordId['RecordId'])
            RecordIdLists.append(RecordIdList_)
            for RecordIdList in RecordIdLists:
                for RecordId in RecordIdList:
                    request = DeleteDomainRecordRequest()
                    request.set_accept_format('json')
                    request.set_RecordId(RecordId)
                    response = client.do_action_with_exception(request)

            data = dict()
            data['Dimain'] = limit
            data['Rr'] = '*'
            data['Value'] = domains_obj.gtm_cname
            data['Type'] = 'CNAME'
            gtm_data.append(data)


def gte_cname(client, gtm_data):
    request = OperateBatchDomainRequest()
    request.set_accept_format('json')
    request.set_Type("RR_ADD")
    request.set_DomainRecordInfos(gtm_data)
    response = client.do_action_with_exception(request)
    json_data = json.loads(str(response, encoding='utf-8'))
    return json_data['TaskId']


def default_line(client, default_data):
    request = OperateBatchDomainRequest()
    request.set_accept_format('json')
    request.set_Type("RR_ADD")
    request.set_DomainRecordInfos(default_data)
    response = client.do_action_with_exception(request)
    json_data = json.loads(str(response, encoding='utf-8'))
    return json_data['TaskId']


