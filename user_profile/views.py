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
    if request.user.is_authenticated():
        _u = request.user
        
    form = register_form()
    return render(request, 'signup.html', {'form': form, 'USER' : _u})
    
# Signs user up
def signup_adduser(request):       
    # Checks if request is post
    if request.method == 'POST':
        # Creates new register_form object
        form = register_form(request.POST)
        
        # Generate response data
        response_data = {}
        
        # Validates form
        if form.is_valid():
            form.save()
            response_data['username'] = form.cleaned_data['username']
            
        else:
            response_data['error'] = form.errors
            
        return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
            
def login_view(request):
    _u = None
    if request.user.is_authenticated():
        _u = request.user

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
    else:       
        form = login_form()
        return render(request, 'login.html', {'form' : form, 'USER' : _u})
            
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