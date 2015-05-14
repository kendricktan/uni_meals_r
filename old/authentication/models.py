from django.db import models
from django.contrib.auth.models import User, AbstractUser

# User model
class user_profile(AbstractUser):
    picture = models.ImageField(upload_to='text', null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=40, null=True, blank=True)
    
    def __unicode__(self):
        return unicode(self.get_username())