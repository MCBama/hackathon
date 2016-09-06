"""triage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

import triageWeb.views.map as maps
import triageWeb.views.helper_views as helpers
import triageWeb.views.login as login
import triageWeb.views.report as report

urlpatterns = [
    url(r'^$', maps.map_view),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'admin/login.html'}),
    url(r'^login_mobile/',login.login_mobile),
    url(r'^map_view/', maps.map_view),
    url(r'^report/$', report.report),
    url(r'^mobile_report/', report.mobile_report),
    url(r'^report_create/', report.report_create),
    url(r'^report/list/', report.report_list),
    url(r'^report/person/(?P<id>\d+)/edit/', report.report_person_edit),
    url(r'^report/(?P<report_type>\w+)/(?P<id>\d+)/update/', report.report_update),
    url(r'^report/person/(?P<id>\d+)/$', report.report_personnel_view),
    url(r'^report/person/(?P<id>\d+)/delete$', report.report_personnel_delete),
    url(r'^report/structure/(?P<id>\d+)/$', report.report_structure_view),
    url(r'^report/structure/(?P<id>\d+)/edit/', report.report_structure_edit),
    url(r'^report/structure/(?P<id>\d+)/delete$', report.report_structure_delete),
    url(r'^(?P<state>\w+)/(?P<lat>-?\d+\.\d+)/(?P<lon>-?\d+\.\d+)', report.mobile_post_report),
    url(r'^parse_json/', helpers.parse_json)
]
