from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template.context_processors import csrf
from datetime import datetime
from .models import *
from .forms import *
import json

# Create your views here.
def signup_view(request):
    form = register_form()
    return render(request, 'authentication/form.html', {'form': form})
    
def signup_adduser(request):
    if request.method == 'POST':
        form = register_form(request.POST)
        
        if form.is_valid():
            form.save()
            return HttpResponse('yay!')
        else:
            return HttpResponse('boo!')
    
def login(request):
    if request.method == 'POST':
        form = login_form(request.POST)
        
        if form.is_valid():
            is_login = form.login(request)
            
            if is_login:            
                return HttpResponse('yay')
        
        return HttpResponse('nay')
    else:       
        if request.user.is_authenticated():
            return HttpResponse('Log out to log in!')
        else:
            form = login_form()
            return render(request, 'authentication/login.html', {'form' : form})
            
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')