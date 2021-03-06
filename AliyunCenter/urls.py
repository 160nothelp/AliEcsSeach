"""AliyunCenter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/aliecs/', include('aliecs.urls', namespace='aliecs')),
    path('api/user/', include('user.urls', namespace='user')),
    path('api/ops/', include('ops.urls', namespace='ops')),
    path('api/workticket/', include('worktickets.urls', namespace='worktickets')),
    path('api/tools/', include('tools.urls', namespace='tools')),
    path('api/sso-wiki/', include('sso_wiki.urls', namespace='sso_wiki')),
    path('api/monitor/', include('monitor.urls', namespace='monitor')),
    path('api/audit/', include('audit.urls', namespace='audit')),
]
