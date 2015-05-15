from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template.context_processors import csrf
from datetime import datetime
from .models import *
from .forms import *
import json

# Views sign-up page
def signup_view(request):
    _u = None
    # Get page
    if request.method == 'GET':
        if request.user.is_authenticated():
            _u = request.user
            
        form = register_form()
        return render(request, 'signup.html', {'form': form, 'USER' : _u})
    
    # Forms post data
    if request.method == 'POST':
        # Creates new register_form object
        form = register_form(request.POST)
        
        # Generate response data
        response_data = {}        
        
        # Checks if username/email user inputted already exists
        response_data['error'] = form.check_exists(request)
        
        # Validates form
        if form.is_valid() and response_data['error'] is None:
        
            # Saves user
            form.save()
            # Informs client we've successfully added user
            response_data['username'] = form.cleaned_data['username']
                            
        
        # Returns response
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
            
def login_view(request):
    _u = None
    if request.user.is_authenticated():
        _u = request.user
        
    if request.method == 'GET':       
        form = login_form()
        return render(request, 'login.html', {'form' : form, 'USER' : _u})

    # Form data is posted and redirects to index page
    if request.method == 'POST':
        form = login_form(request.POST)
        
        # Generate our response data
        response_data = {}
        
        if form.is_valid():
            is_login = form.login(request)            

            if not is_login:    
                response_data['error'] = "Invalid details"
                
        else:
            response_data['error'] = form.errors
                                
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
        
        return HttpResponse('Unable to log in')          
            
def logout_view(request):
    auth_logout(request)
    return HttpResponseRedirect('/')
    
def profile_edit_view(request):
    _u = None
    if request.user.is_authenticated():
        _u = request.user
        
    return render(request, 'profile_edit.html', {'USER' : _u})
    
def profile_view(request):
    _u = None
    if request.user.is_authenticated():
        _u = request.user
        
    return render(request, 'profile.html', {'USER' : _u})            