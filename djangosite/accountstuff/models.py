from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserInfo(models.Model):
	user = models.OneToOneField(User)
	#user = models.TextField()
	profile_picture = models.FileField(upload_to="users/",null=True,blank=True)
	bio = models.TextField(null=True,blank=True)
	gender = models.NullBooleanField()
	birthday = models.DateField()
	phonenumber = models.CharField(max_length=20)
	followers = models.ManyToManyField(User, related_name = "slaves", blank = True, null = True)
	following = models.ManyToManyField(User, related_name = "masters", blank = True, null = True)
	def __str__(self):
		return self.user.username