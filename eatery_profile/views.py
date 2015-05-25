from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template.context_processors import csrf
from datetime import datetime, timedelta
from math import log, sqrt
from user_profile.models import *
from .models import *
from .forms import *
import json

'''
    # Ranking Algorithm
'''

#### Sort by: Best
def _confidence_best(ups, downs):
    n = ups + downs
    
    if n == 0:
        return 0
        
    z = 1.0 #1.0 = 85%, 1.6 = 95%
    phat = float(ups)/n
    
    return sqrt(phat+z*z/(2*n)-z*((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n)
    
'''
    # HttpResponse
'''

def index_view(request):
    _u = None
    variables = {}
    if request.user.is_authenticated():
        _u = request.user
        
    if request.method == 'GET':
        _form = search_form()
        
        variables['USER'] = _u
        variables['FORM'] = _form

        return render(request, 'index.html', variables)           
    
def browse_view(request):
    _u = None
    variables = {}
    if request.user.is_authenticated():
        _u = request.user
        variables['USER'] = _u
        
    if request.method == 'GET':    
    
        # Best ranking algorithm
        _eatery_list = eatery_profile.objects.all()
        _eatery_return = []
        
        for eatery in _eatery_list:
            _eatery_upvotes = eatery.user_votes_set.all().filter(is_upvoted=True).count()
            _eatery_downvotes = eatery.user_votes_set.all().filter(is_upvoted=False).count()
            _eatery_total_votes = eatery.user_votes_set.all().count()
            
            _eatery_return.append((eatery, _confidence_best(_eatery_upvotes, _eatery_downvotes), _eatery_upvotes, _eatery_total_votes, eatery.pricing_bold(), eatery.pricing_rest()))
            
        # Sort from descending points (most popular -> not popular)
        _eatery_return = sorted(_eatery_return, key=lambda _eatery_return_lambda: _eatery_return_lambda[1], reverse=True)
        
        variables['EATERIES'] = _eatery_return
        
        # Prints 1st item
        #print _eatery_return[0:1]
        
    if request.method == 'POST':
        _eatery_return = []       
        
    return render(request, 'browse.html', variables)
    
def search_view(request):
    _u = None
    variables = {}
    
    _form = search_form()
    variables['FORM'] = _form
    
    if request.user.is_authenticated():
        _u = request.user
        variables['USER'] = _u
        
    if request.method == 'GET':                           
        return HttpResponseRedirect('/')
        
    if request.method == 'POST':        
        query = request.POST['query']
        nearby = request.POST['nearby']               
        
        if nearby.lower() == 'current location':
            # Default search:
                # Pricing: Moderate
                # Location: nearby
                # Sort by: Best
                
            # Algorithm to find eatery, chuck here
            # Best ranking algorithm
            
            # Search through restaurant description, name, 
                # specials, food, 
                    # name
                    # description                    
                # tags, special_tags
                    # Keywords
            
            
            _eatery_list = eatery_profile.objects.all()
            _eatery_return = []
            
            for eatery in _eatery_list:
                # Boolean var to check if eatery contains query
                contains_query = False
                
                # Checks eatery description + name
                if eatery.description.find(query) != -1 or eatery.name.find(query) != -1:
                    contains_query = True
                            
                _specials_list = eatery.specials_set.all()
                _food_list = eatery.food_set.all()
                _tags_list = eatery.tags_set.all()
                _special_tag_list = eatery.special_tags_set.all()
                
                # Checks eatery's specials, food, tags, and specials_tag
                
                # Specials
                if contains_query is False:                    
                    if _specials_list.filter(name__contains=query).count() != 0 or _specials_list.filter(description__contains=query).count() != 0:
                        contains_query = True
                
                # Food
                if contains_query is False:                    
                    if _food_list.filter(name__contains=query).count() != 0 or _food_list.filter(description__contains=query).count() != 0:
                        contains_query = True  

                # Tags
                if contains_query is False:                    
                    if _tags_list.filter(keyword__contains=query).count() != 0:
                        contains_query = True 
                        
                # Special tags
                if contains_query is False:                    
                    if _special_tag_list.filter(keyword__contains=query).count() != 0:
                        contains_query = True                                     
                
                if contains_query is True:
                    _eatery_upvotes = eatery.user_votes_set.all().filter(is_upvoted=True).count()
                    _eatery_downvotes = eatery.user_votes_set.all().filter(is_upvoted=False).count()
                    _eatery_total_votes = eatery.user_votes_set.all().count()
                    
                    _eatery_return.append((eatery, _confidence_best(_eatery_upvotes, _eatery_downvotes), _eatery_upvotes, _eatery_total_votes, eatery.pricing_bold(), eatery.pricing_rest()))
                
            # Sort from descending points (most popular -> not popular)
            _eatery_return = sorted(_eatery_return, key=lambda _eatery_return_lambda: _eatery_return_lambda[1], reverse=True)
            
            variables['EATERIES'] = _eatery_return
            
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
        #print food        
        _food_return.append((_food, _food.food_hearts.all().filter(user_profile=_u)))

    # Check if user upvoted/downvoted eatery
    _eatery_voted = _eatery.user_votes_set.all().filter(user_profile=_u)
    
    # Upvoted % 
    _eatery_votes_all = get_eatery_upvotes(_eatery) 

    # Check is user has reviewed xx or yy's review
    _reviews_list = _eatery.reviews_set.all()
    _reviews_return = []
    
    for _review in _reviews_list:
        _reviews_return.append((_review, _review.reviews_usefulness_set.all().filter(user_profile=_u)))
        
    # Our variable list
    variables = {
        'USER': _u,
        'EATERY': _eatery,
        'EATERY_VOTED': _eatery_voted,
        'EATERY_UPVOTE_ALL': _eatery_votes_all,
        'SPECIALS_LIST': _specials_return,
        'FOOD_LIST': _food_return,   
        'REVIEW_LIST': _reviews_return,
    }
    
    # Check if eatery is opened now
    for opening_hours in _eatery.opening_hours_set.all():
        if opening_hours.is_opened_now:
            variables['OPEN_NOW'] = opening_hours                
            break   
            
    # Check if user has reviewed    
    if request.user.is_authenticated():
        try:
            variables['EATERY_REVIEWED'] = _eatery.reviews_set.all().filter(user_profile=_u).count()
            #print variables['EATERY_REVIEWED']
            
        except Exception as e:
            pass    
        
    # Returns response
    return render(request, 'eatery.html', variables)
  
# Add user eatery review
def eatery_add_review(request, eatery_id):
    _u = None
    response_data = {}
    if request.user.is_authenticated():
        _u = request.user
        
        if request.method == 'POST':
            try:                
                review_text = request.POST['id_review_text']
                
                _eatery = eatery_profile.objects.get(id=int(eatery_id))
                
                if _eatery.reviews_set.all().filter(user_profile=_u).count() == 0:            
                    _user_review = reviews(user_profile=_u, review_text=review_text, eatery_profile=_eatery)
                    _user_review.save()
                
            except Exception as e:
                pass
                
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
  
# Removes user eatery review
def eatery_clear_review(request, eatery_id):
    _u = None
    response_data = {}
    if request.user.is_authenticated():
        _u = request.user      
        
        try:
            _eatery = eatery_profile.objects.get(id=int(eatery_id))
            _user_reviews = _eatery.reviews_set.all().filter(user_profile=_u)
            for _user_review in _user_reviews:
                _user_review.delete()
                
        except Exception as e:
            pass
            
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
# Reviews usefulness of review
def eatery_review_usefulness(request, eatery_id, review_id):
    _u = None
    response_data = {}
    if request.user.is_authenticated():
        _u = request.user
        
        if request.method == 'POST':
            try:
                # Gets eatery
                _eatery = eatery_profile.objects.get(id=int(eatery_id))
                
                # Gets POST data about usefulness
                is_useful = request.POST['is_useful'] 

                # Gets current review
                _reviews = _eatery.reviews_set.get(id=int(review_id))
                    
                # Checks if use already has made a review for this review
                # If doesn't then adds his/her opinion into it
                if _reviews.reviews_usefulness_set.all().filter(user_profile=_u).count() == 0:
                    _reviews_usefullness = reviews_usefulness(user_profile=_u, is_useful=is_useful, reviews=_reviews)
                    _reviews_usefullness.save()                
                
            except Exception as e:
                pass
                
            response_data['eatery_id'] = int(eatery_id)
            response_data['review_id'] = int(review_id)
                
    return HttpResponse(
        json.dumps(response_data),
        content_type='application/json'
    )

# Reviews use opinion on review usefulness
def eatery_review_usefulness_clear(request, eatery_id, review_id):
    _u = None
    response_data = {}
    if request.user.is_authenticated():
        _u = request.user
        
        if request.method == 'POST':
            try:
                # Gets eatery
                _eatery = eatery_profile.objects.get(id=int(eatery_id))

                # Gets current review
                _reviews = _eatery.reviews_set.get(id=int(review_id))
                    
                # Removes usereview
                for _user_review_usefullness in _reviews.reviews_usefulness_set.all().filter(user_profile=_u):
                    _user_review_usefullness.delete()
                
            except Exception as e:
                pass
                
            response_data['eatery_id'] = int(eatery_id)
            response_data['review_id'] = int(review_id)
                
    return HttpResponse(
        json.dumps(response_data),
        content_type='application/json'
    )
    