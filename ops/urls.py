from django.urls import path
from . import views


app_name = 'ops'


urlpatterns = [
    path('switch-gtm', views.SwitchGtm.as_view(), name='switch_gtm'),
    path('get-switch-status', views.GetSwitchStatus.as_view(), name='get_switch_status'),
    path('get-domain-line', views.CheckDomainLine, name='get_domain_line'),
]
