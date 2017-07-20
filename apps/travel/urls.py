from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$', views.index, name='index'),
    url(r'^main$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^travels$', views.home, name='home'),
    url(r'^travels/add$', views.add, name='add'),
    url(r'^travels/addtrip$', views.addtrip, name='addtrip'),
    url(r'^join/(?P<id>[0-9]+)$', views.join, name='join'),
    url(r'^travels/destination/(?P<id>[0-9]+)$', views.trippage, name='trippage'),
]

