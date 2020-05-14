from django.urls import path, include
from rest_framework import routers

from .views import cm_gtm_and_cyt_iptables, create_shadowsocket, create_forward


router = routers.DefaultRouter(trailing_slash=False)

router.register(r'ali-ram-addr', cm_gtm_and_cyt_iptables.AliRamView, basename='ali_ram_addr')
router.register(r'_switch-gtm', cm_gtm_and_cyt_iptables.SwitchGtmView, basename='switch_gtm')
# router.register(r'_get-switch-status', cm_gtm_and_cyt_iptables.GetSwitchStatusView, basename='get_switch_status')
router.register(r'tmp-cyt-iptables', cm_gtm_and_cyt_iptables.TmpCytWhiteIpTablesView, basename='tmp_cyt_iptables')
router.register(r'create-shadowsocket', create_shadowsocket.CreateShadowSocketView,
                basename='create_shadowsocket_template')
router.register(r'create-shadowsocket-task', create_shadowsocket.CreateShadowSocketTaskView,
                basename='create_shadowsocket_task')
router.register(r'create-forward', create_forward.CreateForwardView, basename='create_forward_template')
router.register(r'create-forward-task', create_forward.CreateForwardTaskView, basename='create_forward_task')


app_name = 'ops'


urlpatterns = [
    # path('switch-gtm', views.SwitchGtm.as_view(), name='switch_gtm'),
    path('get-switch-status', cm_gtm_and_cyt_iptables.GetSwitchStatus.as_view(), name='get_switch_status'),
    path('get-domain-line', cm_gtm_and_cyt_iptables.CheckDomainLine, name='get_domain_line'),
    path('', include(router.urls)),
]
