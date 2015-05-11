from django.db import models
from django.contrib.auth.models import User

'''
    #### USER ####
'''  

# user model
class user(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to="text", blank=True, null=True)
    location = models.CharField(max_length=20)
    
    def __unicode__(self):
        return unicode(self.user.get_username())       
       
# Creates a new user       
def create_new_user(username, email, password, location):
    # Checks if username or email exists
    if User.objects.filter(username=username).count() > 0 or User.objects.filter(email=email).count() > 0:
        return None
        
    else:
        # Creates a new user model
        _U = User(username=username, email=email)
        _U.set_password(password)
        _U.save()
        
        _u = user(user=_U, location=location)
        _u.save()
        
        return _u
  
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