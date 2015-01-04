from django.conf.urls import patterns, url
from accountstuff import views

urlpatterns = patterns('',
	url(r'^$', views.info, name='info'),
	url(r'^profile/$', views.profile, name='profile'),
   	url(r'^settings/$', views.settings, name='settings'),
	url(r'^signin/$', views.signin, name='signin'),
	url(r'^signout/$', views.signout, name='signout'),
	url(r'^register/$', views.register, name='register'),
)
