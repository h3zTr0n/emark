from django.conf.urls import patterns, url
from messagestuff import views

urlpatterns = [
	#url(r'^$', views.main, name='main'),
	url(r'^info/$', views.allInfo, name='indexAll'),
	url(r'^pSendMessage/$', views.sendMessage, name='sendMessage'),
	url(r'^pViewMessages/$', views.viewMessages, name='viewMessages'),
	url(r'^pUnreadMessages/$', views.unreadMessages, name='unreadMessages'),
	url(r'^(?P<username>[A-Za-z0-9]*)$', views.main, name='mainWithUser'),
]
