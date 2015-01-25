from django.conf.urls import patterns, url
from messagestuff import views

urlpatterns = patterns('',
	#url(r'^$', views.main, name='main'),
	url(r'^(?P<username>[A-Za-z0-9]*)$', views.main, name='mainWithUser'),
	url(r'^info/$', views.allInfo, name='indexAll'),
	url(r'^pSendMessage/$', views.sendMessage, name='sendMessage'),
	url(r'^pViewMessages/$', views.viewMessages, name='viewMessages'),
)
