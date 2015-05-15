from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template.context_processors import csrf
from datetime import datetime
from .models import *
from .forms import *
import json

def index_view(request):
    return HttpResponse("index")
    
def browse_view(request):
    return HttpResponse("browse")
    
def search_view(request):
    return HttpResponse("search")
    
def eatery_view(request):
    return HttpResponse("eatery")