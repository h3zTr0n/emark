from django.shortcuts import render
from itemstuff.models import Item, Review
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from accountstuff.models import UserInfo
import random
from functools import cmp_to_key

# Create your views here.
def browseCategory(request, category):
	#categorypath = request.path.split("/")
	#category = categorypath[len(categorypath)-1]
	categories = {
		"jewelry": 1,
		"pottery": 2,
		"sewingweaving": 3,
		"clothing": 4,
		"art": 5,
	}
	items = Item.objects.filter(category=categories[category.strip("/").lower()])

	context = {
		"cnum": categories[category.strip("/").lower()],
		"category": category.strip("/").lower(),
		"items": items,
	}
	if (request.user.is_authenticated()):
		context["user"] = request.user
		context["userinfo"] = UserInfo.objects.filter(user=request.user)[0]
	template = loader.get_template('DbrowseCategory.html')
	return HttpResponse(template.render(RequestContext(request, context)))

def getItem(request, username, itemid):
	seller = User.objects.filter(username=username)[0]
	sellerinfo = UserInfo.objects.filter(user = seller)[0]
	selleritems = Item.objects.filter(user=seller)

	item = Item.objects.filter(itemid=itemid)[0]
	categories = [
		"Jewelry",
		"Pottery",
		"Sewing & Weaving",
		"Clothing",
		"Art",
	]
	itemCategory = categories[item.category]

	reviews = Review.objects.filter(item=item)

	context = {
		"seller":seller,
		"sellerinfo":sellerinfo,
		"selleritems":selleritems,
		"item":item,
		"itemCategory":itemCategory,
		"reviews":reviews,
	}
	if (request.user.is_authenticated()):
		context["user"] = request.user
		context["userinfo"] = UserInfo.objects.filter(user=request.user)[0]
	template = loader.get_template('DitemListing.html')
	return HttpResponse(template.render(RequestContext(request, context)))

def editItem(request, itemid):
	item = Item.objects.filter(itemid=itemid)[0]
	context={
		"item":item,
	}
	template = loader.get_template('editItem.html')
	return HttpResponse(template.render(RequestContext(request, context)))

def createItem(request):
	template = loader.get_template('editItem.html')
	context={}
	return HttpResponse(template.render(RequestContext(request, context)))

'''
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
'''

def comparePrice(a, b):
	return a.price - b.price

def compareTime(a,b):
	return (a.time - b.time).total_seconds()

def searchnew(request):
	categories = ["jewelry","pottery","sewingweaving","clothing","art"]
	#
	terms = request.GET["q"].split(' ')
	sortby = "relevancy"
	if "sort" in request.GET:
		sortby = request.GET['sort']
	cata = [True, True, True, True, True]
	if (len(request.GET) > 1):
		cata = ["cjewelry" in request.GET, "cpottery" in request.GET, "csewingweaving" in request.GET, "cclothing" in request.GET, "cart" in request.GET]
	minPrice
	maxPrice

def search(request):
	categories = [
		"jewelry",
		"pottery",
		"sewingweaving",
		"clothing",
		"art",
	]

	items = []
	terms = request.GET["q"].split(' ')
	sortby = "relevancy"
	cata = {}
	if (len(request.GET) > 1):
		cata["jewelry"] = "cjewelry" in request.GET
		cata["pottery"] = "cpottery" in request.GET
		cata["sewingweaving"] = "csewingweaving" in request.GET
		cata["clothing"] = "cclothing" in request.GET
		cata["art"] = "cart" in request.GET
	else:
		cata["jewelry"] = True
		cata["pottery"] = True
		cata["sewingweaving"] = True
		cata["clothing"] = True
		cata["art"] = True
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
	items = list(items)
	for item in items:
		if (cata[categories[item.category-1]] == False):
			items.remove(item)
	context = {
		"search": request.GET["q"],
		"items": items,	
		"sortby": sortby,
		"cata": cata,
	}
	if ("minPrice" in request.GET and request.GET["minPrice"]):
		context["minPrice"] = float(request.GET["minPrice"])
		for item in items:
			if (item.price < float(request.GET["minPrice"])):
				items.remove(item)
	if ("maxPrice" in request.GET and request.GET["maxPrice"]):
		context["maxPrice"] = float(request.GET["maxPrice"])
		for item in items:
			if (item.price > float(request.GET["maxPrice"])):
				items.remove(item)
	
	if (request.user.is_authenticated()):
		context["user"] = request.user
		context["userinfo"] = UserInfo.objects.filter(user=request.user)[0]
	template = loader.get_template('Dsearch.html')
	return HttpResponse(template.render(RequestContext(request, context)))

#SERVER
def saveItem(request, itemid):
	title = details = price = desciprtion = tags = category = None

	if('title' in request.POST and request.POST['title']):
		title = request.POST['title']
	if('details' in request.POST and request.POST['details']):
		details = request.POST['details']
	if('price' in request.POST and request.POST['price']):
		price = request.POST['price']
	if('description' in request.POST and request.POST['description']):
		description = request.POST['description']
	if('tags' in request.POST and request.POST['tags']):
		tags = request.POST['tags']
	if('category' in request.POST and request.POST['category']):
		category = request.POST['category']

	if(itemid == 'new'):
		picture = None
		itemid = request.POST['title'].replace(" ", "").lower() + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9))
		item = Item(user=request.user,title=title, details=details, price=price, picture=picture,description=description,tags=tags,category=category, itemid = itemid)
	else:
		itemid = itemid
		item = Item.objects.filter(itemid=itemid)[0]
		item.title = title
		item.details = details
		item. price = price
		item.description = description
		item.tags = tags
		item.category = category
		if('pic' in request.FILES and request.FILES['pic']):
			item.picture = request.FILES['pic']

	item.save()
	return HttpResponse("Success! editted/Created " + title + " for " + request.user.username)

def deleteItem(request, itemid):
	item = Item.objects.filter(itemid=itemid)[0]
	item.delete()
	return HttpResponse("deleted this item")

def addRating(request):
	user = request.user
	ratingnumber = request.POST['rating']
	ratingmessage = request.POST['review-message']
	itemid = request.POST['itemid']
	
	item = Item.objects.filter(itemid = itemid)[0]	
	numRatings = len(Review.objects.filter(item=item))
	totalRatings = (item.averagerating)*numRatings
	newRating = (totalRatings + float(ratingnumber))/(numRatings + 1)
	item.averagerating = newRating
	item.save()

	rating = Review(user = user, item = item, rating = ratingnumber, text = ratingmessage)
	rating.save()
	
	return HttpResponse("success, created a review for " + item.title)