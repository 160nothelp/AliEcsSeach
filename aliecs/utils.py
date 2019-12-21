from aliyunsdkcore.client import AcsClient
from datetime import datetime, timedelta
import math
import json
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest


class AliClient(object):
    def __init__(self, AccessKey_ID, Access_Key_Secret, region_id):
        self.AccessKey_ID = AccessKey_ID
        self.Access_Key_Secret = Access_Key_Secret
        self.region_id = region_id

    def client(self):
        client = AcsClient(self.AccessKey_ID, self.Access_Key_Secret, self.region_id)
        return client


class ECSList(object):
    def __init__(self, json_data, nickname=None):
        self.json_data = json_data
        self.nickname = nickname

    def IndexList(self):
        try:
            PageNumber = self.json_data['PageNumber']
            totalPages = math.ceil(self.json_data["TotalCount"]/self.json_data["PageSize"])
            index_data = list()
            for ecs_data in self.json_data["Instances"]["Instance"]:
                ecs = dict()
                ecs["Cpu"] = ecs_data["Cpu"]
                ecs["Memory"] = int(ecs_data["Memory"] / 1024)
                ecs["InstanceType"] = ecs_data["InstanceType"]
                ecs["InternetMaxBandwidthOut"] = ecs_data["InternetMaxBandwidthOut"]
                ecs["IoOptimized"] = ecs_data["IoOptimized"]
                ecstime = datetime.strptime(ecs_data["ExpiredTime"].replace('T', ' ').replace('Z', ''),
                                            '%Y-%m-%d %H:%M') + timedelta(hours=8)
                ecs["ExpiredTime"] = ecstime.strftime('%Y-%m-%d %H:%M')
                ecsctime = datetime.strptime(ecs_data["CreationTime"].replace('T', ' ').replace('Z', ''),
                                             '%Y-%m-%d %H:%M') + timedelta(hours=8)
                ecs["CreationTime"] = ecsctime.strftime('%Y-%m-%d %H:%M')
                ecs["InstanceId"] = ecs_data["InstanceId"]
                ecs["InstanceName"] = ecs_data["InstanceName"]
                ecs["OSType"] = ecs_data["OSType"]
                ecs["IoOptimized"] = ecs_data["IoOptimized"]
                ecs["PublicIpAddress"] = str(ecs_data["PublicIpAddress"]["IpAddress"]).replace('[', '').replace(']', '').replace("'", "")
                ecs["PrivateIpAddress"] = str(ecs_data["VpcAttributes"]["PrivateIpAddress"]["IpAddress"]).replace('[', '').replace(']', '').replace("'", "")
                ecs["EipAddress"] = str(ecs_data["EipAddress"]["IpAddress"]).replace('[', '').replace(']', '').replace("'", "")
                ecs["Bandwidth"] = ecs_data["EipAddress"].get("Bandwidth")
                ecs["ZoneId"] = ecs_data["ZoneId"]
                ecs["Status"] = ecs_data["Status"]
                ecs["InstanceChargeType"] = ecs_data["InstanceChargeType"]
                ecs["InstanceNetworkType"] = ecs_data["InstanceNetworkType"]
                ecs['nickname'] = self.nickname
                ecs['user_type'] = 'aliuser'

                index_data.append(ecs)
        except Exception as e:
            return 'error'
        index_data_ = dict()
        index_data_["PageNumber"] = PageNumber
        index_data_["totalPages"] = totalPages
        index_data_["index_data"] = index_data
        index_data_['TotalCount'] = self.json_data["TotalCount"]

        return index_data_


class ECSDetails(object):
    def __init__(self, json_data):
        self.json_data = json_data

    def DetailList(self):
        ecs_data = self.json_data["Instances"]["Instance"][0]
        ecs = dict()
        ecs["Cpu"] = ecs_data["Cpu"]
        ecs["Memory"] = int(ecs_data["Memory"] / 1024)
        ecs["InstanceType"] = ecs_data["InstanceType"]
        ecs["InternetMaxBandwidthOut"] = ecs_data["InternetMaxBandwidthOut"]
        ecs["IoOptimized"] = ecs_data["IoOptimized"]
        ecstime = datetime.strptime(ecs_data["ExpiredTime"].replace('T', ' ').replace('Z', ''),
                                    '%Y-%m-%d %H:%M') + timedelta(hours=8)
        ecs["ExpiredTime"] = ecstime.strftime('%Y-%m-%d %H:%M')
        ecsctime = datetime.strptime(ecs_data["CreationTime"].replace('T', ' ').replace('Z', ''),
                                     '%Y-%m-%d %H:%M') + timedelta(hours=8)
        ecs["CreationTime"] = ecsctime.strftime('%Y-%m-%d %H:%M')
        ecs["InstanceId"] = ecs_data["InstanceId"]
        ecs["InstanceName"] = ecs_data["InstanceName"]
        ecs["OSType"] = ecs_data["OSType"]
        ecs["IoOptimized"] = ecs_data["IoOptimized"]
        ecs["PublicIpAddress"] = str(ecs_data["PublicIpAddress"]["IpAddress"]).replace('[', '').replace(']',
                                                                                                        '').replace("'",
                                                                                                                    "")
        ecs["PrivateIpAddress"] = str(ecs_data["VpcAttributes"]["PrivateIpAddress"]["IpAddress"]).replace('[',
                                                                                                          '').replace(
            ']', '').replace("'", "")
        ecs["EipAddress"] = str(ecs_data["EipAddress"]["IpAddress"]).replace('[', '').replace(']', '').replace("'", "")
        ecs["Bandwidth"] = ecs_data["EipAddress"].get("Bandwidth")
        ecs["ZoneId"] = ecs_data["ZoneId"]
        ecs["Status"] = ecs_data["Status"]
        ecs["InstanceChargeType"] = ecs_data["InstanceChargeType"]
        ecs["InstanceNetworkType"] = ecs_data["InstanceNetworkType"]
        ecs['DeletionProtection'] = ecs_data['DeletionProtection']
        ecs['ClusterId'] = ecs_data['ClusterId']
        ecs['VpcId'] = ecs_data['VpcAttributes']['VpcId']
        ecs['VSwitchId'] = ecs_data['VpcAttributes']['VSwitchId']
        ecs['Description'] = ecs_data['Description']
        ecs['InstanceTypeFamily'] = ecs_data['InstanceTypeFamily']
        ecs['ImageId'] = ecs_data['ImageId']
        ecs['KeyPairName'] = ecs_data.get('KeyPairName', '')
        # ecs['TagValue'] = ecs_data.get('Tags', {}).get('Tag', {}).get('TagValue', '')
        # ecs['TagValue'] = [x for x in ecs_data.get('Tags', {}).get('Tag', {})]
        # ecs['TagKey'] = ecs_data.get('Tags', {}).get('Tag', {}).get('TagKey', '')
        ecs['TagKey'] = [x for x in ecs_data.get('Tags', {}).get('Tag', {})]
        ecs['OSNameEn'] = ecs_data['OSNameEn']
        ecs['NetworkInterfaceId'] = ecs_data['NetworkInterfaces']['NetworkInterface'][0]['NetworkInterfaceId']
        ecs['InternetChargeType'] = ecs_data['InternetChargeType']
        ecs['AutoReleaseTime'] = ecs_data['AutoReleaseTime']
        ecs['DeletionProtection'] = ecs_data['DeletionProtection']

        return ecs


def isIpV4AddrLegal(ipStr):
    # 切割IP地址为一个列表
    ip_split_list = ipStr.strip().split('.')
    # 切割后列表必须有4个元素
    if 4 != len(ip_split_list):
        return False
    for i in range(4):
        try:
            # 每个元素必须为数字
            ip_split_list[i] = int(ip_split_list[i])
        except:
            print("IP invalid:" + ipStr)
            return False
    for i in range(4):
        # 每个元素值必须在0-255之间
        if ip_split_list[i] <= 255 and ip_split_list[i] >= 0:
            pass
        else:
            print("IP invalid:" + ipStr)
            return False
    return True


class SlbList:
    def __init__(self, json_data):
        self.json_data = json_data

    def indexlist(self):
        PageNumber = self.json_data['PageNumber']
        totalPages = math.ceil(self.json_data["TotalCount"] / self.json_data["PageSize"])
        index_data = list()
        for ecs_data in self.json_data["LoadBalancers"]["LoadBalancer"]:
            ecs = dict()
            ecs["Address"] = ecs_data["Address"]
            ecs["InstanceName"] = ecs_data['LoadBalancerName']
            ecs["LoadBalancerId"] = ecs_data["LoadBalancerId"]
            ecs['MasterZoneId'] = ecs_data['MasterZoneId']
            ecs["LoadBalancerStatus"] = ecs_data["LoadBalancerStatus"]
            ecs["Address"] = ecs_data["Address"]
            ecs["NetworkType"] = ecs_data["NetworkType"]
            ecs['PayType'] = ecs_data['PayType']
            ecsctime = datetime.strptime(ecs_data["CreateTime"].replace('T', ' ').replace('Z', ''),
                                         '%Y-%m-%d %H:%M') + timedelta(hours=8)
            ecs["CreateTime"] = ecsctime.strftime('%Y-%m-%d %H:%M')
            ecs['user_type'] = 'alislb'
            index_data.append(ecs)
        index_data_ = dict()
        index_data_["PageNumber"] = PageNumber
        index_data_["totalPages"] = totalPages
        index_data_["index_data"] = index_data
        index_data_['TotalCount'] = self.json_data["TotalCount"]
        return index_data_


