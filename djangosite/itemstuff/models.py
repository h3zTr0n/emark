from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

CATEGORY_CHOICES = (
	("electronics", (
			("laptops", "laptops"),
			("phones", "phones"),
		),
	),
	("events", (
			("wedding", "clothing"),
			("kitchen_party", "kitchen_party"),
		),
	),
	("education", (
		("learning_materials", "learning_materials"),
		("other"),
		),
	),
	("motor", (
			("toyota", "toyota"),
			("benz", "benz"),
		),
	),
	("service", (
		("carpenter", "carpenter"),
		("plumber", "plumber"),
		),
	),
	("jobs", (
		("searching", "searching"),
		("employing", "employing"),
		),
	),
	("boutiques_&_Fashion", (
			("clothing", "clothing"),
		),
	),
	("home_&_garden", (
			("house utensils"),
		),
	  ),
    )



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
		help_text=_("Your full name here."),
		max_length=255
	)
	email = models.EmailField(
		help_text=_("Enter your email address.")
	)
	phone = models.CharField(
		help_text=_("Enter your phone number here"),
		max_length=50
	)
	model_type = models.CharField(
		max_length=255,
		choices=CATEGORY_CHOICES
	)
	description = models.TextField(
		help_text = _("please enter as much KEY details as u can about the item.")
	)
	image = models.ImageField(
		help_text = _("place the product' image here"),
		upload_to="items/electronics/%Y/%m/%d/",null=True,blank=True
	)
	province = models.CharField(
		help_text=_("Select your province here."),
		max_length=255,
		choices=PROVINCE_CHOICES
	)
	Location = models.CharField(
		help_text=_("Please enter name of your town."),
		max_length=255
	)

	class Meta:
		verbose_name_plural = "Electronics"
		verbose_name = "Electronic"

	def __unicode__(self):
		return self.name

class Events(models.Model):
	pass

class Education(models.Model):
	pass

class Motor(models.Model):
	pass

class Service(models.Model):
	pass

class Jobs(models.Model):
	pass

class BoutiquesFashion(models.Model):
	pass

class HomeGarden(models.Model):
	pass
# Create your models here.

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

	def __str__(self):
		return self.text
