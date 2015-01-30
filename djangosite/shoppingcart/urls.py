from django.conf.urls import patterns, url
from shoppingcart import views

urlpatterns = patterns('',
		url(r'^$', views.displayCart,  name = 'shoppingCart'),
		url(r'^addItem/(?P<itemid>[A-Za-z0-9 ]+)/(?P<quantity>[0-9]+)$', views.addItemToUser, name = 'addItemToUser'),
		url(r'^remove/(?P<scitemid>[A-za-z0-9]+)$', views.removeItem, name = 'removeItem'),
		url(r'^checkout/$', views.checkout, name = 'checkout'),
		url(r'^checkout/pShipping/$', views.shipping, name = 'shipping'),
		url(r'^checkout/pPayment/$', views.payment, name = 'payment'),
		url(r'^checkout/pSubmitOrder/$', views.submitOrder, name = 'submitOrder'),
		url(r'^checkout/clearOrder/$', views.clearOrder, name = 'clearOrder'),
		url(r'^shoppingitem/(?P<cartitemid>[A-Za-z0-9]+)/$', views.receivedItem, name = 'receivedItem'),
		url(r'^removeitem/(?P<cartitemid>[A-Za-z0-9]+)/$', views.removeFinishedItem, name = 'removeFinishedItem')
	)	