from django.contrib.auth import authenticate, logout, login as auth_login
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template.context_processors import csrf
from datetime import datetime
from .models import *
import json


# Requests index page
def index_view(request):
    return render(request, 'main/index.html')
    
# Requests sign up, login page
def signup_view(request):
    return render(request, 'main/signup.html')
    
    # Signs user up
def signup_adduser(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
    
        # creates a user
        _u, error = create_new_user(username, email, password)
        
        # Creates our response data object
        response_data = {}
        
        if _u:
            response_data['username'] = _u.get_username()                        
            
        elif _u is None:
            response_data['error'] = error;
            
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    
def login_view(request):    
    return render(request, 'main/login.html')
    
    # Logs user in
def login_loginuser(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        # Boolean var to see if we logged in correctly
        login_bool = login_user(username, email, password)
        
        # Response data
        response_data = {}
        
        if login_bool is True:
            response_data['success'] = True
            
        else:
            response_data['error'] = True
        
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    
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