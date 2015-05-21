from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template.context_processors import csrf
from datetime import datetime
from .models import *
from eatery_profile.models import *
from .forms import *
import json

'''
    # Authentication
'''

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
        # Populate data from our post data into our form
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
  
# Logs user out and redirects to home page  
def logout_view(request):
    auth_logout(request)
    return HttpResponseRedirect('/')
    

'''
    # End Authentication
'''


'''
    # Profile
'''

# Request to view the profile page
def profile_view(request, profile_id):
    _u = None
    if request.user.is_authenticated():
        _u = request.user
        
    return render(request, 'profile.html', {'USER' : _u})   
        
# Request to view the profile editing page
def profile_edit_view(request, profile_id):
    _u = None
    if request.user.is_authenticated():
        _u = request.user
        
        # Only allows user to edit profile if they're the same person
        if request.method == 'GET' and _u.id == int(profile_id):
            form_dp = profile_edit_dp_form()
            form_info = profile_edit_info_form(initial={'new_location': _u.location, 'new_description': _u.description})
            form_password = profile_edit_password_form()       
            
            variables = {
                'USER' : _u,
                'form_dp' : form_dp,
                'form_info' : form_info,
                'form_password' : form_password,
            }
            
            return render(request, 'profile_edit.html', variables)
    
    return HttpResponse('you don\'t have permissions to view this page!')
  
# Edit description
def update_profile_info(request, profile_id):
    # Need user to be authenticated to view this page
    if request.user.is_authenticated():
        _u = request.user

        # only lets us edit the profile of the same person
        if request.method == 'POST' and _u.id == int(profile_id):
        
            # Populate data from our post data into our form
            new_location = request.POST['new_location']
            new_description = request.POST['new_description']                       
            
            # Updates info, if the fields are not null
            if new_location is not None:
                _u.location = new_location
                
            if new_description is not None:
                _u.description = new_description
             
            # Saves new user info
            _u.save()
            
            # Yay success
            return HttpResponseRedirect('/')
            
    else:
        return HttpResponse('You don\'t have permissions to view this!')
        
# Edit display picture
def update_profile_dp(request, profile_id):
    # Need user to be authenticated to view this page
    if request.user.is_authenticated():
        _u = request.user

        # only lets us edit the profile of the same person
        if request.method == 'POST' and _u.id == int(profile_id):
            form = profile_edit_dp_form(request.POST, request.FILES)
            
            if form.is_valid():
                new_dp = request.FILES['new_dp']                      
                _u.picture = new_dp
                _u.save()
                
                # Redirects to previous page
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
    else:
        return HttpResponse('You don\'t have permissions to view this!')
        
# Update password
def update_profile_password(request, profile_id):
    # Need user to be authenticated to view this page
    if request.user.is_authenticated():
        _u = request.user

        # only lets us edit the profile of the same person
        if request.method == 'POST' and _u.id == int(profile_id):
        
            # Populate data from our post data into our form
            new_password = request.POST['new_password']              
            
            # Updates user password            
            _u.set_password(new_password)
             
            # Saves new user info
            _u.save()
            
            # Yay success
            return HttpResponse('!')
            
    else:
        return HttpResponse('You don\'t have permissions to view this!')
   
'''
    # HEART UNHEART FOOD/SPECIALS
'''   

# Hearts specials
def profile_heart_special(request, specials_id):    
    _u = None
    response_data = {}    
    if request.user.is_authenticated():
        _u = request.user
        
        if request.method == 'POST':
            
            try:                                                               
                # Get the current specials
                _specials = specials.objects.get(id=int(specials_id))    

                # Checks if user don't have a heart class, if doesn't add one
                # Heart class basically checks the current special if user has liked it
                if _specials.specials_hearts.all().filter(user=_u).count() == 0:
                    _specials_hearts = specials_hearts(user=_u)
                    _specials_hearts.save()            
                    
                    # Adds user heart class to specials
                    _specials.specials_hearts.add(_specials_hearts)                                                                                 
                
            except Exception as e:
                #print e
                pass
                
        # Returns response
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )             
    
# Unhearts specials
def profile_unheart_special(request, specials_id):
    _u = None
    response_data = {}    
    if request.user.is_authenticated():
        _u = request.user
        
        if request.method == 'POST':
            
            try:
                # Get the current specials
                _specials = specials.objects.get(id=int(specials_id))    

                # Checks if user liked it, if they have then remove it                
                _specials.specials_hearts.all().get(user=_u).delete()
                
            except Exception:
                pass
                
    # Returns response
    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    ) 
    
# Hearts food
def profile_heart_food(request, food_id):    
    _u = None
    response_data = {}    
    if request.user.is_authenticated():
        _u = request.user
        
        if request.method == 'POST':            
            try:                                                               
                # Get the current specials
                _food = food.objects.get(id=int(food_id))    

                # Checks if user don't have a heart class, if doesn't add one
                # Heart class basically checks the current special if user has liked it
                if _food.food_hearts.all().filter(user=_u).count() == 0:
                    _food_hearts = food_hearts(user=_u)
                    _food_hearts.save()            
                    
                    # Adds user heart class to specials
                    _food.food_hearts.add(_food_hearts)                                                                                 
                
            except Exception as e:
                #print e
                pass
                
        # Returns response
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )   
        
# Unhearts food
def profile_unheart_food(request, food_id):
    _u = None
    response_data = {}    
    if request.user.is_authenticated():
        _u = request.user
        
        if request.method == 'POST':
            
            try:
                # Get the current specials
                _food = food.objects.get(id=int(food_id))    

                # Checks if user liked it, if they have then remove it   
                _food.food_hearts.all().get(user=_u).delete()
                
            except Exception:
                pass
                
    # Returns response
    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    ) 
        
'''
    # End Profile
'''    