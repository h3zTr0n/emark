from django.shortcuts import render
from itemstuff.models import Item
from django.http import HttpResponse
from django.template import RequestContext, loader

# Create your views here.
def browseCategory(request, category):
	#categorypath = request.path.split("/")
	#category = categorypath[len(categorypath)-1]
	categories = {
		"jewelery": 1,
		"pottery": 2,
		"sewingweaving": 3,
		"clothing": 4,
		"art": 5,
	}
	items = Item.objects.filter(category=categories[category.strip("/").lower()])

	context = {
		"items": items,
	}
	template = loader.get_template('DbrowseCategory.html')
	return HttpResponse(template.render(RequestContext(request, context)))

def getItem(request, username, itemid):
	return HttpResponse("TODO")

def search(request, input):
	return HttpResponse("TODO")

#SERVER
def createItem(request):
	title = request.POST['title']
	details = request.POST['details']
	price = request.POST['price']
	description = request.POST['description']
	tags = request.POST['tags']
	category = request.POST['category']

	item = Item(user=request.user,title=title, details=details, price=price, description=description,tags=tags,category=category)
	item.save()
	return HttpResponse("Success! Created " + title + " for " + request.user.username)
def editItem(request):
	return HttpResponse("TODO")
