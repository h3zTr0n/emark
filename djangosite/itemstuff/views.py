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
	categories = {
		"jewelry": 1,
		"pottery": 2,
		"sewingweaving": 3,
		"clothing": 4,
		"art": 5,
	}
	browsecata = category.strip("/").lower()
	if(browsecata in categories):
		items = Item.objects.filter(category=categories[browsecata])		
	else:
		items = None

	context = {
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
	selleritems = Item.objects.filter(user=seller)[:4]

	item = Item.objects.filter(itemid=itemid)[0]
	categories = [
		"Jewelry",
		"Pottery",
		"Sewing & Weaving",
		"Clothing",
		"Art",
	]
	itemCategory = categories[item.category-1]

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
		sellerFollowers = sellerinfo.followers.all()
		for follower in sellerFollowers:
			if follower == request.user:
				context["followed"] = True
				break
	template = loader.get_template('DitemListing.html')
	return HttpResponse(template.render(RequestContext(request, context)))

def editItem(request, itemid):
	item = Item.objects.filter(itemid=itemid)[0]
	context={
		"item":item,
	}
	if (request.user.is_authenticated()):
		context["user"] = request.user
		context["userinfo"] = UserInfo.objects.filter(user=request.user)[0]
	template = loader.get_template('editItem.html')
	return HttpResponse(template.render(RequestContext(request, context)))

def createItem(request):
	template = loader.get_template('editItem.html')
	context={}
	if (request.user.is_authenticated()):
		context["user"] = request.user
		context["userinfo"] = UserInfo.objects.filter(user=request.user)[0]
	return HttpResponse(template.render(RequestContext(request, context)))

def comparePrice(a, b):
	return a.price - b.price

def compareTime(a,b):
	return (a.time - b.time).total_seconds()

def search(request):
	#categories = ["jewelry","pottery","sewingweaving","clothing","art"]
	terms = request.GET["q"].split(' ')
	sortby = "relevancy"
	if "sort" in request.GET:
		sortby = request.GET['sort']
	cata = [True, True, True, True, True]
	if (len(request.GET) > 1):
		cata = ["cjewelry" in request.GET, "cpottery" in request.GET, "csewingweaving" in request.GET, "cclothing" in request.GET, "cart" in request.GET]
	minPrice = None
	maxPrice = None
	if ("minPrice" in request.GET and request.GET["minPrice"]):
		minPrice = float(request.GET["minPrice"])
	if ("maxPrice" in request.GET and request.GET["maxPrice"]):
		maxPrice = float(request.GET["maxPrice"])
	#
	items = []
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

	#filtering options
	categoryFilteredItems = []
	categoryPriceFilteredItems = []

	for item in items:
		if (cata[item.category-1] == True):
			categoryFilteredItems.append(item)
	for item in categoryFilteredItems:
		if(minPrice == None and maxPrice == None):
			categoryPriceFilteredItems.append(item)
		if(minPrice and maxPrice == None):
			if(item.price > minPrice):
				categoryPriceFilteredItems.append(item)
		if(maxPrice and minPrice == None):
			if(item.price < maxPrice):
				categoryPriceFilteredItems.append(item)
		if(minPrice and maxPrice):
			if(item.price > minPrice and item.price < maxPrice):
				categoryPriceFilteredItems.append(item)

	items = categoryPriceFilteredItems

	context = {
		"search": request.GET["q"],
		"items": items,	
		"sortby": sortby,
		"cata": {
			"jewelry": cata[0],
			"pottery": cata[1],
			"sewingweaving": cata[2],
			"clothing": cata[3],
			"art": cata[4],
		},
		"minPrice": minPrice,
		"maxPrice": maxPrice,
	}
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
		picture = request.FILES['pic']
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