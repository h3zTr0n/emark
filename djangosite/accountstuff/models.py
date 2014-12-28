from django.db import models
#from django.contrib.auth.models import User

# Create your models here.
class UserInfo(models.Model):
	#user = models.OneToOneField(User)
	user = models.TextField()
	#profile_picture = models.FileField(upload_to="/pp/")
	bio = models.TextField()
	gender = models.NullBooleanField()
	birthday = models.DateField()
	phonenumber = models.CharField(max_length=20)
