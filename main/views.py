from django.contrib.auth import authenticate, logout, login as auth_login
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template.context_processors import csrf
from datetime import datetime
from .models import *


# Requests index page
def index_view(request):
    return render(request, 'main/index.html')
    
# Requests sign up, login page
def signup_view(request):
    return render(request, 'main/signup.html')
    
def login_view(request):
    return render(request, 'main/login.html')
    
# Browse, search
def browse_view(request):
    return render(request, 'main/browse.html')
    
def search_view(request):
    return render(request, 'main/search.html')
    
# Eatery
def eatery_view(request):
    return render(request, 'main/eatery.html')
    
# Profile
def profile_view(request):
    return render(request, 'main/profile.html')
    
def profile_edit_view(request):
    return render(request, 'main/profile_edit.html')
    
# Inbox, messages
def inbox_view(request):
    return render(request, 'main/inbox.html')
    
def message_view(request):
    return render(request, 'main/message.html')