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
    # Inbox
'''
# Depreciated
'''
def inbox_view(request):
    _u = None
    variables = {}
    
    if request.user.is_authenticated():
        _u = request.user        
        variables['USER'] = _u
        
        if request.method == 'GET':            
            
            # Gets messages received
            _message_all = []
            for _message_ in message.objects.all():
                if _message_.op_user_profile == _u or _message_.received_user_profile == _u:
                    _message_all.append(_message_)
            _message_all_unread = message.objects.all().filter(received_user_profile=_u, is_read=False)
            
            # Gets sent message
            _message_all_sent = message.objects.all().filter(op_user_profile=_u)
            
            variables['MESSAGE_ALL'] = _message_all
            variables['MESSAGE_ALL_UNREAD'] = _message_all_unread
            variables['MESSAGE_ALL_SENT'] = _message_all_sent
            
        
        return render(request, 'inbox.html', variables)
    
    else:
        return HttpResponseRedirect('/profile/signup/')

def inbox_message_view(request, message_id):
    _u = None
    variables = {}
    
    if request.user.is_authenticated():
        _u = request.user
        variables['USER'] = _u
        
        _message = message.objects.get(id=int(message_id))        
        
        if request.method == 'GET':            
            
            # If this message is related to user then we can allow them to view it
            if _message.op_user_profile == _u or _message.received_user_profile == _u:                
                
                variables['MESSAGE'] = _message
                variables['MESSAGE_REPLIES'] = _message.message_reply_set.all()
            
                return render(request, 'message.html', variables)
                
        if request.method == 'POST':
            _message.is_read = False
            _message.save()
            _message_reply_text = request.POST['id_msg_reply_textarea']
            _message_reply = message_reply(op_user_profile=_u, text=_message_reply_text, message=_message)
            _message_reply.save()
            
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
    return HttpResponseRedirect('/')
        
        
# Generate new mail
def inbox_message_new_view(request):
    _u = None
    variables = {}
    
    if request.user.is_authenticated():
        _u = request.user
        variables['USER'] = _u
        
        if request.method == 'POST':
            # user just click message button
            try:
                _receiver = user_profile.objects.get(id=int(request.POST['id_target_user']))
                variables['USER_TARGET'] = _receiver
                
            except Exception:
                pass
    
            # user pressed send button
            try:
                _receiver = user_profile.objects.get(id=int(request.POST['id_user_target_id']))                
                _message_text = request.POST['id_msg_textarea']
                _message_title = request.POST['id_msg_title']
                _m = message(op_user_profile=_u, received_user_profile=_receiver, title=_message_title, text=_message_text)
                _m.save()
                
                return HttpResponseRedirect('/profile/inbox/')
                
            except Exception:
                pass
            
            
    return render(request, 'new_message.html', variables)
'''
'''
    # End inbox
'''

'''
    # Profile
'''

# Request to view the profile page
def profile_view(request, profile_id):
    _u = None
    variables = {}
    
    if request.user.is_authenticated():
        _u = request.user
        variables['USER'] = _u
        
    # tries to get current profile viewing, if can't get that profile then redirects to homepage
    try:
        _u_target = user_profile.objects.get(id=int(profile_id))
        variables['USER_TARGET'] = _u_target
        
        # Compile reviews, vote, specials_hearts, and food_hearted
        _timeline_return = []
        
        # format = (identifier, title, time-title, text, eatery_id, datetime)
        
        # votes
        for _vote in _u_target.user_votes_set.all():
            _vote_title = ('Upvoted ' if _vote.is_upvoted else 'Downvoted ') + _vote.eatery_profile.name
            _vote_text = _u_target.username + (' upvoted ' if _vote.is_upvoted else ' downvoted ') + _vote.eatery_profile.name
            _timeline_return.append(('uv' if _vote.is_upvoted else 'dv', _vote_title, _vote.get_datetime_voted(), _vote_text, _vote.eatery_profile.id, _vote.datetime_voted))
            
        # Reviews
        for _review in _u_target.reviews_set.all():  
            _review_title = 'Reviewed ' + _review.eatery_profile.name
            _review_text = '\''+ _review.review_text +'\''
            _timeline_return.append(('r', _review_title, _review.get_datetime_pub(), _review_text, _review.eatery_profile.id, _review.datetime_pub))
            
        # Specials hearts
        for _sh in _u_target.specials_hearts_set.all():
            _sh_title = 'Hearted'
            _sh_text = 'Hearted ' + _sh.specials_set.first().eatery_profile.name + '\'s ' + _sh.specials_set.first().name
            _timeline_return.append(('sh', _sh_title, _sh.get_datetime_hearted(), _sh_text, _sh.specials_set.first().eatery_profile.id, _sh.datetime_hearted))
            
        # food hearts
        for _fh in _u_target.food_hearts_set.all():
            _fh_title = 'Hearted'
            _fh_text = 'Hearted ' + _fh.food_set.first().eatery_profile.name + '\'s ' + _fh.food_set.first().name
            _timeline_return.append(('sh', _fh_title, _fh.get_datetime_hearted(), _fh_text, _fh.food_set.first().eatery_profile.id, _fh.datetime_hearted))
            
        # Sort it 
        _timeline_return = sorted(_timeline_return, key=lambda _timeline_return_lambda: _timeline_return_lambda[5], reverse=True)
    
        variables['TIMELINE'] = _timeline_return
        
    except Exception:
        return HttpResponseRedirect('/')        
          
        
    return render(request, 'profile.html', variables)   
        
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
    # Heart/Unheart specials
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
                if _specials.specials_hearts.all().filter(user_profile=_u).count() == 0:
                    _specials_hearts = specials_hearts(user_profile=_u)
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
                _specials.specials_hearts.all().get(user_profile=_u).delete()
                
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
                if _food.food_hearts.all().filter(user_profile=_u).count() == 0:
                    _food_hearts = food_hearts(user_profile=_u)
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
                _food.food_hearts.all().get(user_profile=_u).delete()
                
            except Exception:
                pass
                
    # Returns response
    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    ) 

        
'''
    # Upvote/Downvote Eatery
'''    

# Upvote eatery
def profile_eatery_upvote(request, eatery_id):
    _u = None
    response_data = {}
    if request.user.is_authenticated():
        _u = request.user
        
        if request.method == 'POST':
            try:
                _eatery = eatery_profile.objects.get(id=int(eatery_id))
                
                # Checks if user has already voted, if not
                if _eatery.user_votes_set.all().filter(user_profile=_u).count() == 0:
                    # Creates a vote and associates it with the user
                    _user_votes = user_votes(user_profile=_u, is_upvoted=True, eatery_profile=_eatery)
                    _user_votes.save()                     
                
                # Returns back eatery_id to JS so it enables the JS to 
                # recreate buttons that corresponds to the eatery_id
                response_data['eatery_id'] = int(eatery_id)
                
                # Upvoted % 
                response_data['eatery_upvote_all'] = get_eatery_upvotes(_eatery)
            
            except Exception:
                pass                        
                        
    return HttpResponse(
        json.dumps(response_data),
        content_type='application/json'
    )        
    
# Downvote eatery
def profile_eatery_downvote(request, eatery_id):
    _u = None
    response_data = {}
    if request.user.is_authenticated():
        _u = request.user
        
        if request.method == 'POST':
            try:
                _eatery = eatery_profile.objects.get(id=int(eatery_id))
                
                # Checks if user has already voted, if not
                if _eatery.user_votes_set.all().filter(user_profile=_u).count() == 0:
                    # Creates a vote and associates it with the user
                    _user_votes = user_votes(user_profile=_u, is_upvoted=False, eatery_profile=_eatery)
                    _user_votes.save()                     
                    
                # Returns back eatery_id to JS so it enables the JS to 
                # recreate buttons that corresponds to the eatery_id
                response_data['eatery_id'] = int(eatery_id)
                
                # Upvoted % 
                response_data['eatery_upvote_all'] = get_eatery_upvotes(_eatery)
                
            except Exception as e:
                print e
                
    return HttpResponse(
        json.dumps(response_data),
        content_type='application/json'
    )
    
# Clear eatery vote
def profile_eatery_clearvote(request, eatery_id):
    _u = None
    response_data = {}
    if request.user.is_authenticated():
        _u = request.user
        
        if request.method == 'POST':
            try:
                # Returns back eatery_id to JS so it enables the JS to 
                # recreate buttons that corresponds to the eatery_id
                response_data['eatery_id'] = int(eatery_id)                               
                
                _eatery = eatery_profile.objects.get(id=int(eatery_id))                
                _eatery.user_votes_set.get(user_profile=_u).delete()                               
                
                # Upvoted % 
                response_data['eatery_upvote_all'] = get_eatery_upvotes(_eatery)
            
            except Exception:
                pass
                
    return HttpResponse(
        json.dumps(response_data),
        content_type='application/json'
    )    
    
'''
    # End Profile
'''    