from django.db import models

'''
    #### EATERY ####
'''

class eatery(models.Model):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=14)
    description = models.CharField(max_length=255)
    pricing = models.IntegerField()
    gmaps_url = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    absolute_coordinates = models.CharField(max_length=255)
    
    def __unicode__(self):
        return unicode(self.name)
        
'''
    #### TAGS ####
'''
'''
    #### END TAGS ####
'''