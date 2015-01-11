from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Item(models.Model):
	#user = models.ForeignKey(User, default=User.objects.filter(username="youngguo")[0])
	user = models.TextField()
	title = models.TextField()
	details = models.TextField()
	price = models.FloatField()
	#profile_picture = models.FileField(upload_to="/pp/")
	description = models.TextField()
	category = models.IntegerField()
	tags = models.TextField(blank=True, null=True)
	time = models.DateTimeField(auto_now=True)