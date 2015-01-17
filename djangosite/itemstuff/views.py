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
	return (a.time - b.time).total_seconds() * 1000000

def search(request, input):
	items = []
	terms = input.split(' ')
	sortby = "relevancy"
	if "sortby" in request.POST:
		sortby = request.POST['sortby'] 
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
	if sortby == "lowtohigh":
		items = sorted(items, key=cmp_to_key(comparePrice))
	if sortby == "hightolow":
		items = sorted(items, key=cmp_to_key(comparePrice))
		items.reverse()
	if sortby == "recent":
		items = sorted(items, key=cmp_to_key(compareTime))
		items.reverse()
	context = {
		"items": items,	
		"sortby": sortby,
	}
	
	template = loader.get_template('Dsearch.html')
	return HttpResponse(template.render(RequestContext(request, context)))

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
