from django.db import models
from django.contrib.auth.models import User
from itemstuff.models import Item
# Create your models here.

class ShoppingCartItem(models.Model):
	user = models.ForeignKey(User)
	item = models.ForeignKey(Item)
	quantity = models.IntegerField()
	def __str__(self):
		return self.item.title