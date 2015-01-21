from django.shortcuts import render
from uploader.models import UploadForm,Upload
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# Create your views here.

def home(request):
	if(request.method=="POST"):
		img = UploadForm(request.POST,request.FILES)
		img.user=request.user
		if img.is_valid():
			img.save()
			return HttpResponseRedirect(reverse('imageupload'))
	else:
		img=UploadForm()
	images=Upload.objects.all()
	return render(request,'uploadstuff.html',{'form':img,'images':images})