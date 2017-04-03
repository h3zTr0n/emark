from django.conf.urls import patterns, url
from itemstuff import views

urlpatterns = [
	url(r'createItem/$', views.createItem, name='createItem'),
	url(r'^saveItem/(?P<itemid>.+)$', views.saveItem, name='saveItem'),
	url(r'^editItem/(?P<itemid>.+)$', views.editItem, name='editItem'),
	url(r'^deleteItem/(?P<itemid>.+)$', views.deleteItem, name='deleteItem'),
	url(r'^addRating/$',views.addRating, name='addRating'),

	# category view routings
	url(r'^electronics/$', views.ElectronicFormView.as_view(), name="electronic"),
	url(r'^boutiques_fashion/$', views.BoutiquesFashionFormView.as_view(), name="boutiques_fashion"),
	url(r'^motor/$', views.MotorFormView.as_view(), name="motor"),
	url(r'^event/$', views.EventFormView.as_view(), name="event"),
	url(r'^job/$', views.JobFormView.as_view(), name="job"),
	url(r'^service/$', views.ServiceFormView.as_view(), name="service"),
	url(r'^education/$', views.EducationFormView.as_view(), name="education"),
	url(r'^homegarden/$', views.HomeGardenFormView.as_view(), name="home_garden"),
	
]
