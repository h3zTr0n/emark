from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Message(models.Model):
	sender = models.ForeignKey(User, related_name="sender")
	recipient = models.ForeignKey(User, related_name="recipient")
	timestamp = models.DateTimeField(auto_now=True)
	body = models.TextField()
	status = models.IntegerField(default=1)
