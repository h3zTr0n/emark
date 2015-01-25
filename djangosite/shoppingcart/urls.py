from django.conf.urls import patterns, url
from shoppingcart import views

urlpatterns = patterns('',
		url(r'^$', views.displayCart,  name = 'shoppingCart'),
		url(r'^addItem/(?P<itemid>[A-Za-z0-9 ]+)/(?P<quantity>[0-9]+)$', views.addItemToUser, name = 'addItemToUser'),
		url(r'^remove/(?P<scitemid>[A-za-z0-9]+)$', views.removeItem, name = 'removeItem')
	)