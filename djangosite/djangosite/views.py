from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext, loader
from accountstuff.models import UserInfo
from django.contrib.auth.models import User
from itemstuff.models import Item
import random
from functools import cmp_to_key

def home(request):
	context = {}
	if (request.user.is_authenticated()):
		context["user"] = request.user
		context["userinfo"] = UserInfo.objects.filter(user=request.user)[0]
		followings = context["userinfo"].following.all()
		followingInfos = []
		for following in followings:
			followingInfos.append(UserInfo.objects.filter(user=following)[0])
		context["followingInfos"] = followingInfos
		feedItems = []
		for item in Item.objects.all():
			for following in followings:
				if item.user == following:
					feedItems.append(item)
		context["feedItems"] = feedItems

	userinfos = UserInfo.objects.all()
	userinfos = sorted(userinfos, key=cmp_to_key(compareFollowers))
	userinfos.reverse()
	featureduserinfos=[]
	for i in range(0,4):
		featureduserinfos.append(userinfos[i])

	items = Item.objects.all()
	randInts3 = random.sample(range(len(items)),3)
	featureditems = []
	for rand in randInts3:
		featureditems.append(items[rand])
		
	randInts6 = random.sample(range(len(items)),6)
	featureditems2 = []
	for rand in randInts6:
		featureditems2.append(items[rand])

	context["featureduserinfos"] = featureduserinfos
	context["featureditems"] = featureditems
	context["featureditems2"] = featureditems2
	template = loader.get_template('Dhomepage.html')
	return HttpResponse(template.render(RequestContext(request, context)))

def compareFollowers(a,b):
	return len(a.followers.all()) - len(b.followers.all())
def about(request):
	context={}
	if (request.user.is_authenticated()):
		context["user"] = request.user
		context["userinfo"] = UserInfo.objects.filter(user=request.user)[0]
	template = loader.get_template('about.html')
	return HttpResponse(template.render(RequestContext(request, context)))

def error(request):
	context={}
	template = loader.get_template('error.html')
	return HttpResponse(template.render(RequestContext(request, context)))

def handler404(request):
    response = render_to_response('404.html', {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response
'''
def browseCategory(request):
	#items = Item.objects.filter(category=request.)
	return render_to_response('browseCategory.html', context_instance=RequestContext(request))
def browseTag(request):	 
	return render_to_response('browseTag.html', context_instance=RequestContext(request))
def itemListing(request):	 
	return render_to_response('itemListing.html', context_instance=RequestContext(request))
def search(request):	 
	return render_to_response('search.html', context_instance=RequestContext(request))
def shoppingCart(request):	 
	return render_to_response('shoppingcart.html', context_instance=RequestContext(request))
'''
