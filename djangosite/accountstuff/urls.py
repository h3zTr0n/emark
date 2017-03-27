from django.conf.urls import patterns, url
#from accountstuff import views
from accountstuff import views

urlpatterns = [
	url(r'^$', views.main, name='signup'),
	url(r'^info/$', views.info, name='info'),
	url(r'^pSignin/$', views.signin, name='signin'),
	url(r'^signout/$', views.signout, name='signout'),
	url(r'^pRegister/$', views.register, name='register'),
    url(r'^settings/$', views.settings, name="settings2"),
    #url(r'^settings2/$', views.settingsOld, name="settings"),
	url(r'^pUpdate/$', views.updateSettings, name='modifySettings'),
	url(r'^changeAddress/$', views.updateAddress, name = 'updateAddress'),
	url(r'^changeCCInfo/$', views.updateCC, name = 'updateCC'),
	url(r'^purchaseHistory/$', views.purchaseHistory, name ='purchaseHistory'),
	url(r'^shoppingitem/(?P<cartitemid>[A-Za-z0-9]+)/$', views.receivedItem, name = 'receivedItem'),
	url(r'^isEmailTaken/$', views.isEmailTaken, name='isEmailTaken'),
]
