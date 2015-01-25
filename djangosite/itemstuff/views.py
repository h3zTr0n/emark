from django.shortcuts import render
from itemstuff.models import Item
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.models import User
import random

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
		"category": category.strip("/").lower(),
		"items": items,
	}
	template = loader.get_template('DbrowseCategory.html')
	return HttpResponse(template.render(RequestContext(request, context)))

def getItem(request, username, itemid):
	seller = User.objects.filter(username=username)[0]
	item = Item.objects.filter(itemid=itemid)[0]

	context = {
		"seller":seller,
		"item":item,
	}
	template = loader.get_template('DitemListing.html')
	return HttpResponse(template.render(RequestContext(request, context)))

def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K

def comparePrice(a, b):
	return a.price - b.price

def compareTime(a,b):
	return (a.time - b.time).total_seconds()

def search(request):
	items = []
	terms = request.GET["q"].split(' ')
	sortby = "relevancy"
	if "sort" in request.GET:
		sortby = request.GET['sort'] 
	for term in terms:
		for item in Item.objects.filter(title__icontains=term):
			if item not in items:
				items.append(item)
		for item in Item.objects.filter(details__icontains=term):
			if item not in items:
				items.append(item) 
		for item in Item.objects.filter(description__icontains=term):
			if item not in items:
				items.append(item)
		for item in Item.objects.filter(tags__icontains=term):
			if item not in items:
				items.append(item)

	def compareRelevancy(a,b):
		acount = bcount = 0
		for term in terms:
			if term in a.title:
				acount+=1
			if term in a.details:
				acount+=1
			if term in a.description:
				acount+=1
			if term in a.tags:
				acount+=1
			if term in b.title:
				bcount+=1
			if term in b.details:
				bcount+=1
			if term in b.description:
				bcount+=1
			if term in b.tags:
				bcount+=1
		return acount - bcount

	if sortby == "lowtohigh":
		items = sorted(items, key=cmp_to_key(comparePrice))
	if sortby == "hightolow":
		items = sorted(items, key=cmp_to_key(comparePrice))
		items.reverse()
	if sortby == "recent":
		items = sorted(items, key=cmp_to_key(compareTime))
		items.reverse()
	if sortby == "relevancy":
		items = sorted(items, key=cmp_to_key(compareRelevancy))
		items.reverse()
	context = {
		"search": request.GET["q"],
		"items": items,	
		"sortby": sortby,
	}
	
	template = loader.get_template('Dsearch.html')
	return HttpResponse(template.render(RequestContext(request, context)))

#SERVER
def createItem(request):
	itemid = request.POST['title'].replace(" ", "").lower() + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9))
	title = request.POST['title']
	details = request.POST['details']
	price = request.POST['price']
	description = request.POST['description']
	tags = request.POST['tags']
	category = request.POST['category']

	item = Item(user=request.user,title=title, details=details, price=price, description=description,tags=tags,category=category, itemid = itemid)
	item.save()
	return HttpResponse("Success! Created " + title + " for " + request.user.username)
def editItem(request):
	return HttpResponse("TODO")
