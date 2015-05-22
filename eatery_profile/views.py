from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template.context_processors import csrf
from datetime import datetime
from user_profile.models import *
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

# View eatery page
def eatery_view(request, eatery_id):
    # Variable list
    _u = None
    _eatery = None
    user_id = -1    
    
    # Checks if user is authenticated
    if request.user.is_authenticated():
        _u = request.user
        user_id = _u.id          
    
    # Trys to get eatery via id, if not *will* returns 404 page
    try:
        _eatery = eatery_profile.objects.get(id=int(eatery_id))
        
    except Exception as e:
        return HttpResponse('Eatery not found!')        

    # Check if user liked the specials
    _specials_list = _eatery.specials_set.all()    
    _specials_return = []
    
    for _specials in _specials_list:      
        _specials_return.append((_specials, _specials.specials_hearts.all().filter(user_profile=_u)))
        
    # Check if user liked the food
    _food_list = _eatery.food_set.all()    
    _food_return = []
    
    for _food in _food_list:   
        print food        
        _food_return.append((_food, _food.food_hearts.all().filter(user_profile=_u)))

    # Check if user upvoted/downvoted eatery
    _eatery_voted = _eatery.user_votes_set.all().filter(user_profile=_u)
    
    # Upvoted % 
    _eatery_votes_all = get_eatery_upvotes(_eatery)
        
    # Our variable list
    variables = {
        'USER': _u,
        'EATERY': _eatery,
        'EATERY_VOTED': _eatery_voted,
        'EATERY_UPVOTE_ALL': _eatery_votes_all,
        'SPECIALS_LIST': _specials_return,
        'FOOD_LIST': _food_return,        
    }
    
    # Check if eatery is opened now
    for opening_hours in _eatery.opening_hours_set.all():
        if opening_hours.is_opened_now:
            variables['OPEN_NOW'] = opening_hours                
            break   
    
    # Add review
    if request.method == 'POST':
        try:
            # add review to eatery
            review_text = request.POST['id_review_text']
            _user_review = reviews(user_profile=_u, review_text=review_text, eatery_profile=_eatery)
            _user_review.save()
            
        except Exception as e:
            pass
        
        # Refreshes page so won't POST again
        return HttpResponseRedirect(request.get_full_path())
        
    # Returns response
    return render(request, 'eatery.html', variables)