from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template.context_processors import csrf
from datetime import datetime
from .models import *
from .forms import *
import json

def index_view(request):
    _u = None
    if request.user.is_authenticated():
        _u = request.user
        
    if request.method == 'GET':
        form = search_form()
        variables = {
            'USER': _u,
            'form': form,
        }
        return render(request, 'index.html', variables)           
    
def browse_view(request):
    _u = None
    if request.user.is_authenticated():
        _u = request.user
        
    if request.method == 'GET':        
        variables = {
            'USER': _u,           
        }
        return render(request, 'browse.html', variables)
    
def search_view(request):
    _u = None
    if request.user.is_authenticated():
        _u = request.user
        
    if request.method == 'GET':        
        variables = {
            'USER': _u,           
        }
        return render(request, 'search.html', variables)
        
    if request.method == 'POST':
        
        query = request.POST['query']
        nearby = request.POST['nearby']
        
        variables = {
            'USER': _u,           
        }       
        
        # Algorithm to find eatery, chuck here
            
        return render(request, 'search.html', variables)
        
def eatery_view(request, eatery_id):
    _u = None
    if request.user.is_authenticated():
        _u = request.user
        
    if request.method == 'GET':
        _eatery = None
        
        # Trys to get eatery, if not *will* returns 404 page
        try:
            _eatery = eatery_profile.objects.get(id=int(eatery_id))
            
        except Exception as e:
            return HttpResponse('Eatery not found!')
            
        _price_loop = [i+1 for i in range(_eatery.pricing)]
        _price_loop_end = [i+1 for i in range(5-_eatery.pricing+1,5)]
        
        variables = {
            'USER': _u,
            'EATERY': _eatery,
            'PRICE_LOOP': _price_loop,
            'PRICE_LOOP_END': _price_loop_end,
        }
        
        for opening_hours in _eatery.opening_hours_set.all():
            if opening_hours.is_opened_now:
                variables['OPEN_NOW'] = opening_hours                
                break
        
        return render(request, 'eatery.html', variables)