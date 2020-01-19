from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'search', views.AliSearchView, basename='search')
router.register(r'get_search', views.AliSearchGetStatusView, basename='get_search')
router.register(r'userdata-select', views.HostListUserSelectView, basename='get_select_user')
router.register(r'ecs-host-table', views.EcsHostTableView, basename='ecs_host_table')
router.register(r'host-table', views.OtherHostTableView, basename='host_table')
router.register(r'slb-table', views.SlbListView, basename='slb_table')
router.register(r'details', views.AliEcsDetailsView, basename='details_view')

app_name = 'aliecs'

urlpatterns = [
    path('', include(router.urls)),
    path('graphics-view', views.GraphicsView, name='graphics_view'),
]
