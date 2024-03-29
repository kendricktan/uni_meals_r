from django.contrib.auth import authenticate, logout, login as auth_login
from django.db import models
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models_functions import *

'''
    #### USER ####
'''  

# user model
class user(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to=generate_directory_user, blank=True, null=True)
    location = models.CharField(max_length=20)
    description = models.CharField(max_length=255)
    
    def __unicode__(self):
        return unicode(self.user.get_username())   

    def get_username(self):
        return unicode(self.user.get_username())
       
# Creates a new user       
def create_new_user(username, email, password):
    # Checks if username or email exists
    if User.objects.filter(username=username).count() > 0:
        return None, 'Username'
        
    elif User.objects.filter(email=email).count() > 0:
        return None, 'Email'
        
    else:
        # Creates a new user model
        _U = User(username=username, email=email)
        _U.set_password(password)
        _U.save()
        
        _u = user(user=_U)
        _u.save()
        
        return _u, None
        
    # Logins user
def login_user(username, email, password, request):    
    # _U = django's user model
    # _u = custom user model extended django's user model
    
    # Assuming its an username at first
    _username = username
    
    # If logging in via email
    if email:    
        # Gets user email
        try:
            # Gets user via email
            _U = User.objects.get(email=email)
            if _U is not None:
                # Get's user's email
                _username = _U.username
                
        except Exception as e:
            return False
    
    # Authenticate
    _U = authenticate(username=_username, password=password)
    
    # Our custom database is what stores the users, not Django's defualt user database
    try: 
        _u = _U.user
        auth_login(request, _U)
        return True
    
    except Exception as e:
        return False

# Change user dp
def change_user_dp(user, request):
    return None
  
# Gets custom model's user
def get_custom_model_user(_U):
    try:
        _u = _U.user
        return _u
    except Exception as e:
        return None
  
'''
    #### USER'S WALL ####
'''  
# User's wall
class wall(models.Model):
    user = models.OneToOneField(user)
    
    def __unicode__(self):
        return unicode((unicode(self.user) + '\'s wall'))
        

# Wall post on the wall
class wall_post(models.Model):
    op_id = models.IntegerField()
    text = models.CharField(max_length=999)
    datetime_pub = models.DateTimeField(auto_now_add=True)
    wall = models.ForeignKey(wall)
    
    
    def __unicode__(self):
        return unicode(self.text)
        
# Wall post comments
class wall_post_comment(models.Model):
    op_id = models.IntegerField()
    wall_post = models.ForeignKey(wall_post)
    text = models.CharField(max_length=999)
    datetime_pub = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return unicode(self.text)

'''
    #### END USER'S WALL ####
'''  

'''
    #### USER'S TIMELINE ####
'''  
class timeline(models.Model):
    user = models.OneToOneField(user)
    
    def __unicode__(self):
        return unicode((unicode(self.user) + '\'s timeline'))
    
class food_hearted(models.Model):
    food_id = models.IntegerField()
    datetime_hearted = models.DateTimeField(auto_now_add=True)
    timeline = models.ForeignKey(timeline)
    
    def __unicode__(self):
        return unicode(self.food_id)
        
class eatery_reviewed(models.Model):
    eatery_id = models.IntegerField()
    review_stars = models.IntegerField()
    review_text = models.CharField(max_length=255)
    datetime_reviewed = models.DateTimeField(auto_now_add=True)
    timeline = models.ForeignKey(timeline)
    
    def __unicode__(self):
        return unicode(self.eatery_id)
        
class vote_given(models.Model):
    eatery_id = models.IntegerField()
    is_upvoted = models.BooleanField()
    timeline = models.ForeignKey(timeline)
    
    def __unicode__(self):
        return unicode(self.eatery_id)
    
'''
    #### END USER'S TIMELINE ####
'''  


'''
    #### USER'S MESSAGES ####
'''  
class message(models.Model):
    op_id = models.IntegerField()
    title = models.CharField(max_length=50)
    text = models.CharField(max_length=32767)
    datetime_sent = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(user)
    
    def __unicode__(self):
        return unicode(self.title)
        
class message_reply(models.Model):
    op_id = models.IntegerField()
    text = models.CharField(max_length=32767)
    datetime_sent = models.DateTimeField(auto_now_add=True)
    message = models.ForeignKey(message)
    
    def __unicode__(self):
        return unicode(self.text)
    
'''
    #### END USER'S MESSAGES ####
'''  