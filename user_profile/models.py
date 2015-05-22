from django.db import models
from django.contrib.auth.models import User, AbstractUser

'''
    # FUNCTIONS
'''
def generate_directory_user(self, filename):
    id = self.id
    if id == None:
        id = max(map(lambda a:a.id,Theme.objects.all())) + 1    
    url = "user/%s/%s" % (str(id), filename)
    return url
    
'''
    # USER
'''
class user_profile(AbstractUser):
    picture = models.ImageField(upload_to=generate_directory_user, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=40, null=True, blank=True)
    
    def __unicode__(self):
        return unicode(self.get_username())        
     
    def user_has_picture(self):
        return bool(self.picture)
        
    def user_has_reviewed_eatery(self, eatery_id):
        if self.timeline.eatery_reviewed_set.filter(eatery_id=int(eatery_id)).count() > 0:
            return True
        return None
'''
    # MESSAGE
'''   
class message(models.Model):
    op_id = models.IntegerField()
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=32767)
    datetime_sent = models.DateTimeField(auto_now_add=True)
    user_profile = models.ForeignKey(user_profile)
    
    def __unicode__(self):
        return unicode(self.user_profile.get_username() + '\'s message, id: ' + self.id)
        
class message_reply(models.Model):
    op_id = models.IntegerField()
    text = models.CharField(max_length=32767)
    datetime_sent = models.DateTimeField(auto_now_add=True)
    message = models.ForeignKey(message)
    
    def __unicode__(self):
        return unicode(self.message.title() + '\'s message reply, id: ' + self.id)
  
'''
    # WALL
'''
class wall(models.Model):
    user_profile = models.OneToOneField(user_profile)
    
    def __unicode__(self):
        return unicode(self.user_profile.get_username() + '\'s wall')
        
class wall_post(models.Model):
    op_id = models.IntegerField()
    text = models.CharField(max_length=255)
    datetime_pub = models.DateTimeField(auto_now_add=True)
    wall = models.ForeignKey(wall)
    
    def __unicode__(self):
        return unicode(self.wall.id)
        
class wall_post_comment(models.Model):
    op_id = models.IntegerField()
    text = models.CharField(max_length=255)
    datetime_pub = models.DateTimeField(auto_now_add=True)
    wall_post = models.ForeignKey(wall_post)
        
    def __unicode__(self):
        return unicode(self.wall_post.id)        