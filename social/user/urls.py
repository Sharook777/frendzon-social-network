
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name="register"),
    #url(r'^profile/$', views.profile, name="profile"),
    url(r'^(?P<member>\d+)/profile/$', views.profile, name="profile"),
    #url(r'^profile/delete/$', views.profile_del, name="profile_del"),
    url(r'^password/$', views.password, name="password"),
    url(r'^picture/$', views.pro_pic, name="pro_pic"),
    url(r'^status/$', views.status_change, name="status"),
    url(r'^settings/$', views.settings, name="settings"),
    url(r'^(?P<member>\d+)/gallery/$', views.gallery, name="gallery"),
    url(r'^(?P<member>\d+)/about/$', views.about, name="about"),
    url(r'^bug/$', views.bug, name="bug"),
    
]
