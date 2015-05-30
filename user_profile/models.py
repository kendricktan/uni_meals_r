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
    op_user_profile = models.ForeignKey(user_profile, null=True, related_name='op_user_profile')
    received_user_profile = models.ForeignKey(user_profile, null=True, related_name='received_user_profile')    
    title = models.CharField(max_length=255, null=True)
    text = models.CharField(max_length=32767)
    datetime_sent = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)    
    
    def __unicode__(self):
        return unicode(self.op_user_profile.get_username() + '\'s message to ' + self.received_user_profile.get_username() + ', id: ' + str(self.id))
        
    def get_datetime_sent(self):
        return self.datetime_sent.strftime('%d/%m/%y') + ' at ' + self.datetime_sent.strftime('%H:%M')
        
    def get_short_description(self):
        if self.message_reply_set.all().count() == 0:
            if len(self.text) >= 255:
                return unicode(self.text[0:255] + '...')
            return unicode(self.text)
        else:
            if len(self.message_reply_set.last().text) >= 255:
                return unicode(self.message_reply_set.last().text[0:255] + '...')
            else:
                return unicode(self.message_reply_set.last().text)
        
class message_reply(models.Model):
    op_user_profile = models.ForeignKey(user_profile, null=True)        
    text = models.CharField(max_length=32767)
    datetime_sent = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    message = models.ForeignKey(message)
    
    def get_datetime_sent(self):
        return self.datetime_sent.strftime('%d/%m/%y') + ' at ' + self.datetime_sent.strftime('%H:%M')
        
    def __unicode__(self):
        return unicode(self.op_user_profile.get_username() + '\'s reply, id: ' + str(self.id))

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