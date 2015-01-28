from django.conf.urls import patterns, url
from itemstuff import views

urlpatterns = patterns('',
	url(r'createItem/$', views.createItem, name='createItem'),
	url(r'^saveItem/(?P<itemid>.+)$', views.saveItem, name='saveItem'),
	url(r'^editItem/(?P<itemid>.+)$', views.editItem, name='editItem'),
	url(r'^deleteItem/(?P<itemid>.+)$', views.deleteItem, name='deleteItem'),
	url(r'^addRating/$',views.addRating, name='addRating'),
)
