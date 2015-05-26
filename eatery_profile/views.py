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
    
#### Return list of eateries for search
def _search_eateries(query_list, location_list, is_nearby, max_price):
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
        for query in shlex.split(query_list):
            if eatery.description.lower().find(query.lower()) != -1 or eatery.name.lower().find(query.lower()) != -1:
                contains_query = True
                    
        _specials_list = eatery.specials_set.all()
        _food_list = eatery.food_set.all()
        _tags_list = eatery.tags_set.all()
        _special_tag_list = eatery.special_tags_set.all()
        
        # Checks eatery's specials, food, tags, and specials_tag
        
        # Specials
        if contains_query is False:     
            for query in shlex.split(query_list):
                if _specials_list.filter(name__icontains=query).count() != 0 or _specials_list.filter(description__icontains=query).count() != 0:
                    contains_query = True
        
        # Food
        if contains_query is False:   
            for query in shlex.split(query_list):
                if _food_list.filter(name__icontains=query).count() != 0 or _food_list.filter(description__icontains=query).count() != 0:
                    contains_query = True  

        # Tags
        if contains_query is False:    
            for query in shlex.split(query_list):
                if _tags_list.filter(keyword__icontains=query).count() != 0:
                    contains_query = True 
                
        # Special tags
        if contains_query is False:   
            for query in shlex.split(query_list):
                if _special_tag_list.filter(keyword__icontains=query).count() != 0:
                    contains_query = True                                     
        
        # If eatery contains any instance of the query then it'll be added to the list, with the default sorting algorithm applied to it
        if contains_query is True:
            # Checks if Eatery price is within user search
            if eatery.within_price_range(max_price):            
                # Checks if location is nearby    
                if is_nearby:
                    if eatery.location.is_nearby(location_list) is True:                       
                        _eatery_upvotes = eatery.user_votes_set.all().filter(is_upvoted=True).count()
                        _eatery_downvotes = eatery.user_votes_set.all().filter(is_upvoted=False).count()
                        _eatery_total_votes = eatery.user_votes_set.all().count()                                
                                                
                        _eatery_return.append((eatery, _confidence_best(_eatery_upvotes, _eatery_downvotes), _eatery_upvotes, _eatery_total_votes, eatery.pricing_bold(), eatery.pricing_rest()))
                        
                elif is_nearby is False:
                    _eatery_upvotes = eatery.user_votes_set.all().filter(is_upvoted=True).count()
                    _eatery_downvotes = eatery.user_votes_set.all().filter(is_upvoted=False).count()
                    _eatery_total_votes = eatery.user_votes_set.all().count()                                
                                            
                    _eatery_return.append((eatery, _confidence_best(_eatery_upvotes, _eatery_downvotes), _eatery_upvotes, _eatery_total_votes, eatery.pricing_bold(), eatery.pricing_rest()))
                    
    return _eatery_return
    
'''
    #### End Ranking algorithm
'''

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
    
# Returns search results
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
        query_list = request.POST['query']
        location_list = request.POST['location']               
        
        _eatery_return = []
        _eatery_return = _search_eateries(query_list, location_list, True, 4)
            
        # Sort best
        _eatery_return = sorted(_eatery_return, key=lambda _eatery_return_lambda: _eatery_return_lambda[1], reverse=True)
        
        variables['SEARCH_QUERY'] = query_list
        variables['LOCATION'] = location_list
        variables['EATERIES'] = _eatery_return
        variables['EATERIES_COUNT'] = len(_eatery_return)
            
        return render(request, 'search.html', variables)

# Returns search results via ajax
def search_ajax(request):
    response_data = {}
    if request.method == 'GET':
        return HttpResponseRedirect('/')
    
    if request.method == 'POST':
        query_list = request.POST['search_query']
        location_list = request.POST['location_query']                           
        
        # Gets price moderation
        max_price = 3        
        for ENUM_PRICE in PRICING_ENUM:
            if ENUM_PRICE[1] == request.POST['max_pricing_val']:
                max_price = ENUM_PRICE[0]
        
        # Checks if request is nearby
        is_nearby = (request.POST['location_val'].lower()=='nearby')
        
        # Gets eatery return
        _eatery_return = _search_eateries(query_list, location_list, is_nearby, max_price)
        
        # Sort by...
        sort_by_val = request.POST['sort_by_val']               
            
        # Sort by ...
        if sort_by_val == 'Best':
            _eatery_return = sorted(_eatery_return, key=lambda _eatery_return_lambda: _eatery_return_lambda[1], reverse=True)            
        
        # Ajax response_data
        response_data['SEARCH_QUERY'] = query_list
        response_data['LOCATION'] = location_list
        response_data['EATERIES_COUNT'] = len(_eatery_return)
                        
        # Initialize our return list
        response_data['EATERY_ID'] = []
        response_data['EATERY_NAME'] = []
        response_data['EATERY_TAGS'] = []
        response_data['EATERY_LOCATION_SUBURB'] = []
        response_data['EATERY_UPVOTES'] = []
        response_data['EATERY_TOTAL_VOTES'] = []
        response_data['EATERY_PRICING_BOLD'] = []
        response_data['EATERY_PRICING_REST'] = []
        
        # Slice this section for ajax scroll results
        for x in range(0, len(_eatery_return)):
            response_data['EATERY_ID'].append(_eatery_return[x][0].id)
            response_data['EATERY_NAME'].append(_eatery_return[x][0].name)
            tags_list = [str(tags) for tags in _eatery_return[x][0].tags_set.all()]
            response_data['EATERY_TAGS'].append(tags_list)
            #response_data['EATERY_TAGS'].append()
            response_data['EATERY_LOCATION_SUBURB'].append(_eatery_return[x][0].location.suburb)
            response_data['EATERY_UPVOTES'].append(_eatery_return[x][2])
            response_data['EATERY_TOTAL_VOTES'].append(_eatery_return[x][3])
            response_data['EATERY_PRICING_BOLD'].append(len(_eatery_return[x][4]))
            response_data['EATERY_PRICING_REST'].append(len(_eatery_return[x][5])) 
        
        return HttpResponse(
            json.dumps(response_data),
            content_type='application/json'
        )
        
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
    