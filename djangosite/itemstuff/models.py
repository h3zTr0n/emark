from django.db import models

# Create your models here.
class Item(models.Model):
	#user = models.ForeignKey('django.contrib.auth.User')
	user = models.TextField()
	title = models.TextField()
	details = models.TextField()
	price = models.FloatField()
	#profile_picture = models.FileField(upload_to="/pp/")
	description = models.TextField()
	category = models.IntegerField()
	tags = models.TextField(blank=True, null=True)
	time = models.DateTimeField(auto_now=True)