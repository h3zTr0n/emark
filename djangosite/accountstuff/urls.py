from django.conf.urls import patterns, url
#from accountstuff import views
from accountstuff import views

urlpatterns = patterns('',
	url(r'^$', views.main, name='signup'),
	url(r'^info/$', views.info, name='info'),
	url(r'^pSignin/$', views.signin, name='signin'),
	url(r'^signout/$', views.signout, name='signout'),
	url(r'^pRegister/$', views.register, name='register'),
    url(r'^settings/$', views.settings, name="settings2"),
    #url(r'^settings2/$', views.settingsOld, name="settings"),
	url(r'^pUpdate/$', views.updateSettings, name='modifySettings'),
)
