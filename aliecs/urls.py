from django.urls import path
from . import views

app_name = 'aliecs'

urlpatterns = [

    # API
    path('index-base', views.IndexBaseView.as_view(), name='index_base_data'),
    path('userdata-select', views.HostListUserSelect.as_view(), name='userdata_select'),
    path('host-table', views.HostTableView.as_view(), name='host_table'),
    path('host-ip-search', views.HostIpSearchView.as_view(), name='host_ip_search'),
    path('get-host-ip-result', views.GetHostIpSearch.as_view(), name='get_host_ip_result'),
    path('slb-table', views.SlbListView.as_view(), name='slb_table'),
    path('ecs-host-table', views.EcsHostTableView.as_view(), name='ecs_host_table'),
    path('details', views.AliEcsDetailsView.as_view(), name='details_view'),
    path('graphics-view', views.GraphicsView, name='graphics_view'),
]
