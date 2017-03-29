from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = (
	(0, "electronics"),
	(5, "events"),
	(10, "education"),
	(15, "motor"),
	(20, "service"),
	(25, "jobs"),
	(30, "boutiques & Fashion"),
	(35, "home & garden"),
)
# Create your models here.

class Item(models.Model):
	user = models.ForeignKey(User)
	#user = models.TextField()
	title = models.TextField()
	details = models.TextField()
	price = models.FloatField()
	picture = models.FileField(upload_to="items/",null=True,blank=True)
	description = models.TextField()
	category = models.IntegerField(choices=CATEGORY_CHOICES)
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
