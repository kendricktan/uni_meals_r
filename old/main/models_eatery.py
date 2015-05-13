from django.db import models
from .models_functions import *

'''
    #### EATERY ####
'''

class eatery(models.Model):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=14)
    picture = models.ImageField(upload_to=generate_directory_eatery, blank=True, null=True)
    description = models.CharField(max_length=255)
    pricing = models.IntegerField(null=True, blank=True)
    gmaps_url = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    absolute_coordinates = models.CharField(max_length=255, null=True, blank=True)
    
    def __unicode__(self):
        return unicode(self.name)
        
'''
    #### FOOD & SPECIALS ####
'''
class food(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=500)
    picture = models.ImageField(upload_to=generate_directory_food, blank=True, null=True)
    eatery = models.ForeignKey(eatery)
    
    def __unicode__(self):
        return unicode(self.name)
        
class specials(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    normal_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=500)
    picture = models.ImageField(upload_to=generate_directory_specials, blank=True, null=True)
    date_valid_from = models.DateField()
    date_valid_to = models.DateField()
    hour_valid_from = models.TimeField()
    hour_valid_to = models.TimeField()
    eatery = models.ForeignKey(eatery)
    
    def __unicode__(self):
        return unicode(self.name)
    
'''
    #### END FOOD & SPECIALS ####
'''
  
'''
    #### REVIEWS ####
'''
class reviews(models.Model):
    user_id = models.IntegerField()
    stars_given = models.IntegerField()
    review_text = models.CharField(max_length=500)
    useful_no = models.IntegerField()
    not_useful_no = models.IntegerField()
    eatery = models.ForeignKey(eatery)
    
    def __unicode__(self):
        return unicode(self.review_text)
    
'''
    #### END REVIEWS ####
'''

'''
    #### VOTES ####
'''
class votes(models.Model):
    eatery = models.OneToOneField(eatery)
    
    def __unicode__(self):
        return unicode(self.eatery.name + '\'s votes!')
        
class upvoted(models.Model):
    date_voted = models.DateField(auto_now_add=True)
    votes = models.ForeignKey(votes)
    
    def __unicode__(self):
        return unicode(self.votes.eatery.name + '\'s upvotes!')
        
class downvoted(models.Model):
    date_voted = models.DateField(auto_now_add=True)
    votes = models.ForeignKey(votes)
    
    def __unicode__(self):
        return unicode(self.votes.eatery.name + '\'s downvotes!')
        
'''
    #### END VOTES ####
'''

  
'''
    #### OPENING HOURS AND SPECIAL DAYS ####
'''
DAYS = [
    (1, ("Monday")),
    (2, ("Tuesday")),
    (3, ("Wednesday")),
    (4, ("Thursday")),
    (5, ("Friday")),
    (6, ("Saturday")),
    (7, ("Sunday")),
]

class opening_hours(models.Model):
    day_from = models.IntegerField(choices=DAYS)
    day_to = models.IntegerField(choices=DAYS)
    hour_from = models.TimeField()
    hour_to = models.TimeField()
    eatery = models.ForeignKey(eatery)
    
    def __unicode__(self):
        return unicode(self.eatery.name + self.get_operational_time())
        
    def get_operational_time(self):
        str_day_from = ''
        str_day_to = ''
        if(len(str(self.hour_from)) > 5):
            str_day_from = str(self.hour_from)[:-3]
        else:
            str_day_from = str(self.hour_from)
            
        if(len(str(self.hour_to)) > 5):
            str_day_to = str(self.hour_to)[:-3]
        else:
            str_day_to = str(self.hour_to)
        
        return unicode(self.get_day_from_display() + ' - ' + self.get_day_to_display() + ' (' + str_day_from + ' - ' + str_day_to + ')')
    
    def get_day_from_display(self):
        return DAYS[self.day_from]
        
    def get_day_to_display(self):
        return DAYS[self.day_to]
    
class special_days(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateField()
    opened = models.BooleanField()
    hour_from = models.TimeField(null=True, blank=True)
    hour_to = models.TimeField(null=True, blank=True)
    eatery = models.ForeignKey(eatery)
    
    def __unicode__(self):
        return unicode(self.name)
        
    def get_check(self):
        output = str(self.date)
        
        str_day_from = ''
        str_day_to = ''
        if(len(str(self.hour_from)) > 5):
            str_day_from = str(self.hour_from)[:-3]
        else:
            str_day_from = str(self.hour_from)
            
        if(len(str(self.hour_to)) > 5):
            str_day_to = str(self.hour_to)[:-3]
        else:
            str_day_to = str(self.hour_to)
            
        if self.opened is True:
            output += (' (' + str_day_from + ' - ' + str_day_to + ')')
        else:
            output += ' (closed)'
        return unicode(output)
    
    def get_day_hour_from(self):
        if self.opened is True:
            return self.hour_from
        return str('Closed!')
        
    def get_day_hour_to(self):
        if self.opened  is True:
            return self.hour_to
        return str('Closed!')
'''
    #### END OPENING HOURS AND SPECIAL DAYS ####
'''
        
'''
    #### TAGS & SPECIAL TAGS ####
'''
# Tags to identify restaurant genre such as "Japanese, Chinese, Malaysian, etc"
class tags(models.Model):
    keyword = models.CharField(max_length=50)
    eatery = models.ManyToManyField(eatery)
    
    def __unicode__(self):
        return unicode(self.keyword)
    
# Special tags to identify additional info such as "Glutten free, vegetarian, Kid-friendly, smoker friendly" etc
class special_tags(models.Model):
    keyword = models.CharField(max_length=50)
    eatery = models.ManyToManyField(eatery)
    
    def __unicode__(self):
        return unicode(self.keyword)
'''
    #### END TAGS & SPECIAL TAGS ####
'''