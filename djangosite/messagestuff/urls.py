from django.conf.urls import patterns, url
from messagestuff import views

urlpatterns = patterns('',
	url(r'^$', views.allInfo, name='indexAll'),
	url(r'^sendMessage/$', views.sendMessage, name='sendMessage'),
	url(r'^viewMessages/$', views.viewMessages, name='viewMessages'),
)
