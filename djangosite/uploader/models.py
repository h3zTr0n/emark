from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

class Upload(models.Model):
	pic = models.FileField("Image",upload_to="images/")
	upload_date=models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.pic.url

#FileUpload form class
class UploadForm(ModelForm):
	class Meta:
		model = Upload