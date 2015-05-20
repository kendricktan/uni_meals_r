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
    
    # Trys to get eatery, if not *will* returns 404 page
    try:
        _eatery = eatery_profile.objects.get(id=int(eatery_id))
        
    except Exception as e:
        return HttpResponse('Eatery not found!')
        
    # Gets restaurant pricing
    _price_loop = [i+1 for i in range(_eatery.pricing)]
    _price_loop_end = [i+1 for i in range(5-_eatery.pricing+1,5)]
    
    # Checks if user liked the specific specials or not
    if request.user.is_authenticated():
        for specials in _eatery.specials_set.all():
            try:
                # if this passes the check then the user has already liked it
                _u.timeline.specials_hearted_set.get(specials_id=specials.id)                
                specials.user_liked = True
                
            except Exception:
                specials.user_liked = False
                pass
             
            specials.save()
    
    # Our variable list
    variables = {
        'USER': _u,
        'EATERY': _eatery,
        'PRICE_LOOP': _price_loop,
        'PRICE_LOOP_END': _price_loop_end,
    }
    
    # Check if eatery is opened now
    for opening_hours in _eatery.opening_hours_set.all():
        if opening_hours.is_opened_now:
            variables['OPEN_NOW'] = opening_hours                
            break   

    # Checks if user reviewed eatery
    if request.user.is_authenticated():
        try:
            request.user.user_has_reviewed_eatery(int(eatery_id))
            variables['USER_REVIEWED'] = True
            
        except Exception:
            pass
    
    # Add review
    if request.method == 'POST':
        try:
            # add review to eatery
            review_text = request.POST['id_review_text']
            _eatery = eatery_profile.objects.get(id=int(eatery_id))
            review = reviews(user_id=user_id, review_text=review_text, eatery_profile=_eatery)
            review.save()                                    
            
            # if existing + logged in user added reviews
            # add eatery review (er) to user's history
            if request.user.is_authenticated():                     
                _er = eatery_reviewed(eatery_id=int(eatery_id), review_text=review_text, timeline=_u.timeline)
                _er.save()            
            
        except Exception as e:
            pass
        
        # Refreshes page so won't POST again
        return HttpResponseRedirect(request.get_full_path())
        
    # Returns response
    return render(request, 'eatery.html', variables)