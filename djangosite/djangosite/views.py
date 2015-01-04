from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext, loader

def home_out(request):
	 return render_to_response('HomepageOut.html', context_instance=RequestContext(request))