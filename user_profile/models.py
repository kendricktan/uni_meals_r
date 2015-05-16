from django.db import models
from django.contrib.auth.models import User, AbstractUser

def generate_directory_user(self, filename):
    id = self.id
    if id == None:
        id = max(map(lambda a:a.id,Theme.objects.all())) + 1    
    url = "user/%s/%s" % (str(id), filename)
    return url
    
# User model
class user_profile(AbstractUser):
    picture = models.ImageField(upload_to=generate_directory_user, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=40, null=True, blank=True)
    
    def __unicode__(self):
        return unicode(self.get_username())