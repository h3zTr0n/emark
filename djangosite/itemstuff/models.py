# -*- coding: UTF-8 -*-
# __author__: Alison Mukoma
# Database tables for service CATEGORY_CHOICES

from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone



# CATEGORY_CHOICES = (
# 	("electronics", (
# 			("laptops", "laptops"),
# 			("phones", "phones"),
# 		),
# 	),
# 	("events", (
# 			("wedding", "clothing"),
# 			("kitchen_party", "kitchen_party"),
# 		),
# 	),
# 	("education", (
# 		("learning_materials", "learning_materials"),
# 		("other"),
# 		),
# 	),
# 	("motor", (
# 			("toyota", "toyota"),
# 			("benz", "benz"),
# 		),
# 	),
# 	("service", (
# 		("carpenter", "carpenter"),
# 		("plumber", "plumber"),
# 		),
# 	),
# 	("jobs", (
# 		("searching", "searching"),
# 		("employing", "employing"),
# 		),
# 	),
# 	("boutiques_&_Fashion", (
# 			("clothing", "clothing"),
# 		),
# 	),
# 	("home_&_garden", (
# 			("house utensils"),
# 		),
# 	  ),
#     )
#
#

PROVINCE_CHOICES = (
	("central", "Central Province"),
	("southern", "Southern Province"),
	("nothern", "Northern Province"),
	("western", "western Province"),
	("estern", "Estern Province"),
	("southwestern", "South-Western Province"),
	("nothWester", "Noth-Western Province"),
)

class Electronics(models.Model):
	name = models.CharField(
		_("Name of the product"),
		help_text=_("Type of electronic device ie(laptop)."),
		max_length=255
	)
	description = models.TextField(
		help_text=_("Enter item description.")
	)
	image = models.ImageField(
		_("Image of the product"),
		help_text=_("Upload item image here"),
		upload_to="items/electronics/%Y/%m/%d/",null=True,blank=True
	)
	province = models.CharField(
		_("Province of the advertiser"),
		max_length=255,
		choices=PROVINCE_CHOICES
	)
	town = models.CharField(
		_("Town of the advertiser"),
		help_text=_("Enter your town's name here."),
		max_length=255
	)
	location = models.CharField(
		_("Location of the advertiser"),
		help_text=_("Enter your location here."),
		max_length=255
	)
	Advertisers_name = models.CharField(
		_("Advertiser's name"),
		help_text=_("Provide the name of the advertiser."),
		max_length=255
	)
	Advertisers_number = models.CharField(
		_("Advertiser's phone number"),
		help_text=_("Enter phone number of the advertiser."),
		max_length=255
	)
	created = models.DateTimeField(default=timezone.now,
								editable=False)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		verbose_name_plural = "Electronics"
		verbose_name = "Electronic"

	def __str__(self):
		return self.name

# Boutiques and Fashions model
class BoutiquesFashion(models.Model):
	service_Type = models.CharField(
		_("Type of service"),
		help_text=_("Enter type of service."),
		max_length=255
	)
	details = models.TextField(
		help_text=_("Enter item details.")
	)
	image = models.ImageField(
		_("Image of the product"),
		help_text=_("Upload item image here"),
		upload_to="items/boutiques_fashion/%Y/%m/%d/",null=True,blank=True
	)
	town = models.CharField(
		_("Town of the advertiser"),
		help_text=_("Enter your town's name here."),
		max_length=255
	)
	location = models.CharField(
		_("Location of the advertiser"),
		help_text=_("Enter your location here."),
		max_length=255
	)
	Advertisers_name = models.CharField(
		_("Advertiser's name"),
		help_text=_("Provide the name of the advertiser."),
		max_length=255,
	)
	Advertisers_number = models.CharField(
		help_text=_("Enter phone number of the advertiser."),
		max_length=255
	)
	created = models.DateTimeField(default=timezone.now,
								editable=False)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		verbose_name_plural = "Boutiques and Fashions"
		verbose_name = "Boutique and Fashion"


STEERING_CHOICES = (
	("L", "Left hand drive"),
	("R", "Right hand drive"),
)

# Motor model
class Motor(models.Model):
	make_model = models.CharField(
		_("Make or Model"),
		max_length=255,
		help_text=_("Provide the make or the model of the motor")
	)
	year = models.DateField(
		_("Date of publishing this advert"),
		max_length=255,
		auto_now_add=False
	)
	body_type = models.CharField(
		_("Body type"),
		help_text = _("Body type of motor i.e (minibus)"),
		max_length=255
	)
	transmission = models.IntegerField(
		_("Transmission"),
		help_text=_("Provide transmission of the motor ie for vehicle it could be 123400075")
	)
	steering = models.CharField(
		_("Steering Type"),
		help_text=_("Choose type of steering ie left or right"),
		choices = STEERING_CHOICES,
		max_length=255
	)
	engine_capacity = models.CharField(
		_("Engine capacity"),
		help_text=_("Ie 245 litres"),
		max_length=255
	)
	mileage = models.IntegerField(
		_("Mileage"),
		help_text=_("provide mileage ie 12300")
	)
	price = models.CharField(
		_("Price"),
		help_text=_("Enter selling price of the vehicle"),
		max_length=255
	)

	Fuel_type = models.CharField(
		_("Fuel Type"),
		help_text =_("Fuel type could be 'petrol', 'diesel' etc "),
		max_length=255
	)
	# transmission = models.IntegerField()
	details = models.TextField(
		help_text=_("Enter item details.")
	)
	image = models.ImageField(
		_("Image of the product"),
		help_text=_("Upload item image here"),
		upload_to="items/boutiques_fashion/%Y/%m/%d/",null=True,blank=True
	)
	town = models.CharField(
		_("Town of the advertiser"),
		help_text=_("Enter your town's name here."),
		max_length=255
	)
	location = models.CharField(
		_("Location of the advertiser"),
		help_text=_("Enter your location here."),
		max_length=255
	)
	Advertisers_name = models.CharField(
		_("Advertiser's name"),
		help_text=_("Provide the name of the advertiser."),
		max_length=255,
	)
	Advertisers_number = models.CharField(
		help_text=_("Enter phone number of the advertiser."),
		max_length=255
	)
	created = models.DateTimeField(default=timezone.now,
								editable=False)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		verbose_name_plural = "Motors"
		verbose_name = "Motor"
		ordering = ["-created"]

	def __unicode__(self):
		return self.make_model

# Events model

class Event(models.Model):
	name = models.CharField(
		_("Name of the event"),
		max_length=255
	)

	advertisers_name = models.CharField(
		_("Name of event advertiser"),
		help_text = _("Enter the event advertiser's name"),
		max_length=255
	)
	description = models.TextField(
		_("Describe the event"),
		max_length=255
	)
	created = models.DateTimeField(default=timezone.now,
								editable=False
								)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		verbose_name_plural = "Events"
		verbose_name = "Event"
		ordering = ["-created"]

	def __unicode__(self):
		return self.name


#
#
#
# class Education(models.Model):
# 	pass
#
# class Motor(models.Model):
# 	pass
#
# class Service(models.Model):
# 	pass
#
# class Jobs(models.Model):
# 	pass
#
#
# class HomeGarden(models.Model):
# 	pass

class Item(models.Model):
	user = models.ForeignKey(User)
	#user = models.TextField()
	title = models.TextField()
	details = models.TextField()
	price = models.FloatField()
	picture = models.FileField(upload_to="items/",null=True,blank=True)
	description = models.TextField()
	category = models.IntegerField()
	# category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
	tags = models.TextField(blank=True, null=True)
	time = models.DateTimeField(auto_now=True)
	itemid = models.TextField()
	averagerating = models.FloatField(default=0)

	def __str__(self):
		return self.title


class Review(models.Model):
	user = models.ForeignKey(User)
	item = models.ForeignKey(Item, default=0)
	rating = models.IntegerField()
	text = models.TextField(blank = True, null = True)
#
# 	def __str__(self):
# 		return self.text
#
#
# class Services(models.Model):
# 	name = models.CharField(
# 		max_length=255,
# 		help_text=_("Please provice us with your product name"),
# 		default = _("Default name")
# 	)
#
# 	created_at = models.DateTimeField(default=timezone.now)
#
# 	class Meta:
# 		verbose_name_plural = "Services"
#
# 	def __unicode__(Self):
# 		return "Welcome "+ str(self.user)
#
# GENDER_CHOICES =(
# 	("M", "Male"),
# 	("F", "Female"),
# 	("O", "Other"),
# )
#
# STATUS_CHOICES = (
# 	("S", "Single"),
# 	("M", "Married"),
# 	("D", "Divorced"),
# )
