from .models import PermissionGroup


class ManyGroupPermissionCheck:

    def __init__(self, group_querySet):
        self.group_querySet = group_querySet
        self.pr = {
            'gtm_permission': False,
            'hosts_permission': False,
            'cyt_iptables_permission': False,
            'create_shadowsocket_permission': False,
            'create_forward_permission': False,
            'worktickets_permission': False,
            'wiki_permission': False,
        }

    def permission_check(self):
        for group_obj in self.group_querySet:
            if self.pr['gtm_permission'] or group_obj.gtm_permission:
                self.pr['gtm_permission'] = True
            else:
                self.pr['gtm_permission'] = False
            if self.pr['hosts_permission'] or group_obj.hosts_permission:
                self.pr['hosts_permission'] = True
            else:
                self.pr['hosts_permission'] = False
            if self.pr['cyt_iptables_permission'] or group_obj.cyt_iptables_permission:
                self.pr['cyt_iptables_permission'] = True
            else:
                self.pr['cyt_iptables_permission'] = False
            if self.pr['create_shadowsocket_permission'] or group_obj.create_shadowsocket_permission:
                self.pr['create_shadowsocket_permission'] = True
            else:
                self.pr['create_shadowsocket_permission'] = False
            if self.pr['create_forward_permission'] or group_obj.create_forward_permission:
                self.pr['create_forward_permission'] = True
            else:
                self.pr['create_forward_permission'] = False
            if self.pr['worktickets_permission'] or group_obj.worktickets_permission:
                self.pr['worktickets_permission'] = True
            else:
                self.pr['worktickets_permission'] = False
            if self.pr['wiki_permission'] or group_obj.wiki_permission:
                self.pr['wiki_permission'] = True
            else:
                self.pr['wiki_permission'] = False

        return self.pr
