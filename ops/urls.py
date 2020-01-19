from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter(trailing_slash=False)

router.register(r'ali-ram-addr', views.AliRamView, basename='ali_ram_addr')
router.register(r'_switch-gtm', views.SwitchGtmView, basename='switch_gtm')
router.register(r'_get-switch-status', views.GetSwitchStatusView, basename='get_switch_status')


app_name = 'ops'


urlpatterns = [
    path('switch-gtm', views.SwitchGtm.as_view(), name='switch_gtm'),
    path('get-switch-status', views.GetSwitchStatus.as_view(), name='get_switch_status'),
    path('get-domain-line', views.CheckDomainLine, name='get_domain_line'),
    path('', include(router.urls)),
]
