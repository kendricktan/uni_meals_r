from django.contrib.auth import authenticate, logout, login as auth_login
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template.context_processors import csrf
from datetime import datetime
from .models import *
import json


# Requests index page
def index_view(request):
    _u = None
    if request.user.is_authenticated():
        _u = get_custom_model_user(request.user)
        
    return render(request, 'main/index.html', {'USER': _u})
    
# Requests sign up, login page
def signup_view(request):
    _u = None
    if request.user.is_authenticated():
        _u = get_custom_model_user(request.user)
        
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
    _u = None
    if request.user.is_authenticated():
        _u = get_custom_model_user(request.user)
        
    return render(request, 'main/login.html', {'USER': _u})
    
    # Logs user in
def login_loginuser(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        # Boolean var to see if we logged in correctly
        login_bool = login_user(username, email, password, request)
        
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
    
    # Logs user out
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')
    
# Browse, search
def browse_view(request):
    _u = None
    if request.user.is_authenticated():
        _u = get_custom_model_user(request.user)
        
    return render(request, 'main/browse.html', {'USER': _u})
    
def search_view(request):
    _u = None
    if request.user.is_authenticated():
        _u = get_custom_model_user(request.user)
        
    return render(request, 'main/search.html', {'USER': _u})
    
# Eatery
def eatery_view(request):
    _u = None
    if request.user.is_authenticated():
        _u = get_custom_model_user(request.user)
        
    return render(request, 'main/eatery.html', {'USER': _u})
    
# Profile
def profile_view(request, profile_id):
    #if request.user.is_authenticated():
    _u = get_custom_model_user(request.user)
                
    if _u is not None:
        return render(request, 'main/profile.html', {'USER': _u})
            
    return HttpResponse('Profile does not exist!') 
    
def profile_edit_view(request, profile_id):
    if request.user.is_authenticated():
        _u = get_custom_model_user(request.user)
        
        if _u is not None:
            # Only lets user edit profile if their ID is the same
            if _u.id == int(profile_id):
                return render(request, 'main/profile_edit.html', {'USER': _u})
    
    return HttpResponse('Please log in to access this function') 
    
def profile_edit_dp(request):
    if request.method == 'POST':
        img = request.FILES['image']
        
        response_data = {}

        if img is not None:
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
    return None
    
# Inbox, messages
def inbox_view(request):
    _u = None
    if request.user.is_authenticated():
        _u = get_custom_model_user(request.user)
        
    return render(request, 'main/inbox.html', {'USER': _u})
    
def message_view(request):
    _u = None
    if request.user.is_authenticated():
        _u = get_custom_model_user(request.user)
        
    return render(request, 'main/message.html', {'USER': _u})