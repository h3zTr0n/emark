from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext, loader
from accountstuff.models import UserInfo
from django.contrib.auth.models import User
from itemstuff.models import Item
import random

def home(request):
	context = {}
	if (request.user.is_authenticated()):
		context["user"] = request.user
		context["userinfo"] = UserInfo.objects.filter(user=request.user)[0]
	
	userinfos = UserInfo.objects.all()
	randInts3 = random.sample(range(len(userinfos)),3)
	featureduserinfos = []
	for rand in randInts3:
		featureduserinfos.append(userinfos[rand])

	items = Item.objects.all()
	randInts4 = random.sample(range(len(items)),4)
	featureditems = []
	for rand in randInts4:
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
