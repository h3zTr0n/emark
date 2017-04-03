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
		"electronics": 1,
		"events": 2,
		"education": 3,
		"motor": 4,
		"service": 5,
		"jobs": 6,
		"boutiques & Fashion": 7,
		"home & garden": 8,
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
	"Electronics",
	"Events",
	"Education",
	"Motor",
	"Service",
	"Jobs",
	"Boutiques & Fashion",
	"Home & Garden",
	]
	itemCategory = categories[item.category-1]

	reviews = Review.objects.filter(item=item)
	reviews = list(reviews)
	for review in reviews:
		review.ratingp = review.rating * 20
		review.negratingp = (5-review.rating) * 20

	context = {
		"seller":seller,
		"sellerinfo":sellerinfo,
		"selleritems":selleritems,
		"item":item,
		"itemCategory":itemCategory,
		"reviews":reviews,
		"ratingp":item.averagerating * 20,
		"negratingp":(5 - item.averagerating) * 20
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
	item.tags = item.tags if item.tags else ""
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
		cata = ["cELECTRONICS" in request.GET, "cEVENTS" in request.GET, "cEDUCATION" in request.GET, "cMOTOR" in request.GET, "cCLOTHING" in request.GET, "cSERVICE" in request.GET, "cJOBS" in request.GET,  "cBOUTIQUESFASHION" in request.GET,  "cJOBS" in request.GET, "cHOMEGARDEN" in request.GET]
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
			if a.tags and term in a.tags:
				acount+=1
			if term in b.title:
				bcount+=1
			if term in b.details:
				bcount+=1
			if term in b.description:
				bcount+=1
			if b.tags and term in b.tags:
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
			"ELECTRONICS": cata[0],
			"EVENTS": cata[1],
			"EDUCATION": cata[2],
			"MOTOR": cata[3],
			"CLOTHING": cata[4],
			# "SERVICE": cata[5],
			# "JOBS": cata[6],
			# "BOUTIQUESFASHION": cata[7],
			# "JOBS": cata[8],
			# "HOMEGARDEN": cata[9],
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
	return HttpResponseRedirect("/user/" + request.user.username + "/" + item.itemid)

def deleteItem(request, itemid):
	item = Item.objects.filter(itemid=itemid)[0]
	item.delete()
	#return HttpResponse("deleted this item")
	return HttpResponseRedirect("/user/" + request.user.username + "/")

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

	return HttpResponseRedirect("/user/" + item.user.username + "/" + item.itemid)
	#return HttpResponse("success, created a review for " + item.title)


# views for handling cateegory models
from django.views import generic

from .forms import ElectronicsModelForm
from .forms import BoutiquesFashionModelForm
from .forms import MotorModelForm
from .forms import EventModelForm
from django.core.urlresolvers import reverse_lazy

from braces import views

class ElectronicFormView(generic.CreateView):
	form_class = ElectronicsModelForm
	template_name = "Delectronic.html"
	success_url = reverse_lazy("browseCategory")

	def form_valid(Self, form):
		form.instance.created_by = self.request.user
		return super(ElectronicFormView, self).form_valid(form)

class BoutiquesFashionFormView(generic.CreateView):
	form_class = BoutiquesFashionModelForm
	template_name = "boutiques_fashion.html"

	def form_valid(self, form):
		form.instance.created_by = self.request.user
		return super(BoutiquesFashionFormView, self).form_valid(form)

class MotorFormView(generic.CreateView):
	form_class = MotorModelForm
	template_name = "motor.html"

	def form_valid(self, form):
		form.instance.created_by = self.request.user
		return super(MotorFormView, self).form_valid(form)

class EventFormView(generic.CreateView):
	form_class = EventModelForm
	template_name = "event.html"
	success_url = reverse_lazy("home")


	def form_valid(self, form):
		form.instance.created_by = self.request.user
		return super(EventFormView, self).form_valid(form)
