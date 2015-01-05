from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext, loader

def home(request):
	 return render_to_response('homepage.html', context_instance=RequestContext(request))
def browseCategory(request):	 
	return render_to_response('browseCategory.html', context_instance=RequestContext(request))
def browseTag(request):	 
	return render_to_response('browseTag.html', context_instance=RequestContext(request))
def itemListing(request):	 
	return render_to_response('itemListing.html', context_instance=RequestContext(request))
def search(request):	 
	return render_to_response('search.html', context_instance=RequestContext(request))
def shoppingCart(request):	 
	return render_to_response('shoppingcart.html', context_instance=RequestContext(request))