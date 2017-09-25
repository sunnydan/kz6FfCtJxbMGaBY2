from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main),
    url(r'^main/$', views.main),
    url(r'^travels/$', views.travels),
    url(r'^travels/destination/(\d+)/$', views.destination),
    url(r'^travels/join/(\d+)/$', views.join),
    url(r'^travels/add/$', views.add),
    url(r'^travels/processadd/$', views.processadd),
    url(r'^login/$', views.processlogin),
    url(r'^logout/$', views.processlogout),
    url(r'^register/$', views.register),
]