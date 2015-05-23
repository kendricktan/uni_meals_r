import datetime
from user_profile.models import *
from django.db import models

'''
    # FUNCTIONS
'''
def generate_directory_eatery_food(self, filename):
    id = self.eatery_profile.id
    if id == None:
        id = max(map(lambda a:a.id,Theme.objects.all())) + 1    
    url = "eatery_profile/%s/food/%s" % (str(id), filename)
    return url
    
def generate_directory_eatery_specials(self, filename):
    id = self.eatery_profile.id
    if id == None:
        id = max(map(lambda a:a.id,Theme.objects.all())) + 1    
    url = "eatery_profile/%s/specials/%s" % (str(id), filename)
    return url
    
def get_eatery_upvotes(_eatery):
    _eatery_upvotes = _eatery.user_votes_set.all().filter(is_upvoted=True).count()
    _eatery_downvotes = _eatery.user_votes_set.all().filter(is_upvoted=False).count()
    _eatery_total_votes = _eatery.user_votes_set.all().count()    
                
    # Don't wanna divide by zero
    _eatery_upvotes = _eatery_upvotes if _eatery_upvotes > 0 else 1    
    
    _eatery_votes_percentage = (_eatery_upvotes*100)/(_eatery_total_votes if _eatery_total_votes > 0 else 1) 

    # Some exceptions
    if _eatery.user_votes_set.all().filter(is_upvoted=True).count() == 0 and _eatery_total_votes > 0:
        _eatery_votes_percentage = '0'
        
    if _eatery_total_votes == 0:
        _eatery_votes_percentage = '--'
    
    _eatery_votes_all = []
    _eatery_votes_all.append((_eatery_votes_percentage, _eatery_total_votes))       
    
    return _eatery_votes_all
    
'''
    # EATERY
'''

PRICING_ENUM = [
    (1, ('Cheap')),
    (2, ('Affortable')),
    (3, ('Moderate')),
    (4, ('Expensive')),
    (5, ('Very Expensive')),    
]

class eatery_profile(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    description = models.CharField(max_length=500)
    pricing = models.IntegerField(choices=PRICING_ENUM)
    
    def __unicode__(self):
        return unicode(self.name);
   
    # Pricing for template style $$$/$$
    def pricing_bold(self):
        return [i+1 for i in range(self.pricing)]
        
    def pricing_rest(self):
        return [i+1 for i in range(self.pricing, 5)]

'''
    # LOCATION
'''

class location(models.Model):
    address = models.CharField(max_length=120)
    country_long = models.CharField(max_length=30)
    country_short = models.CharField(max_length=5)
    state_long = models.CharField(max_length=30)
    state_short = models.CharField(max_length=5)
    city = models.CharField(max_length=30)
    suburb = models.CharField(max_length=30)
    postal_code = models.IntegerField()
    coordinates_latitude = models.DecimalField(max_digits=8, decimal_places=3)
    coordinates_longitude = models.DecimalField(max_digits=8, decimal_places=3)
    eatery_profile = models.OneToOneField(eatery_profile)
    
    def __unicode__(self):
        return unicode(self.eatery_profile.name + '\'s location')
        

'''
    # OPERATIONAL INFO
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
    eatery_profile = models.ForeignKey(eatery_profile)
    
    def __unicode__(self):
        return unicode(self.eatery_profile.name + '\'s opening hours')
        
    def is_opened_now(self):
        cur_day = datetime.datetime.today().weekday()
        
        # If its open today
        if cur_day >= self.day_from-1 and cur_day <= self.day_to-1:
            
            cur_time = datetime.datetime.today().strftime("%H:%M")
            
            # We don't want
            hour_from = self.hour_from.strftime("%H:%M")
            hour_to = self.hour_to.strftime("%H:%M")
            
            # If its open 
            if cur_time > hour_from and cur_time < hour_to:
                return True
        
        return False
        
    def get_operational_time(self):
        hour_from = self.hour_from.strftime("%H:%M")
        hour_to = self.hour_to.strftime("%H:%M")        
        
        return unicode(self.get_day_from_display() + ' - ' + self.get_day_to_display() + ' (' + hour_from + ' - ' + hour_to + ')')
    
    def get_day_from_display(self):
        return DAYS[self.day_from-1][1]
        
    def get_day_to_display(self):
        return DAYS[self.day_to-1][1]
    
class special_days(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateField()
    opened = models.BooleanField()
    hour_from = models.TimeField(null=True, blank=True)
    hour_to = models.TimeField(null=True, blank=True)
    eatery_profile = models.ForeignKey(eatery_profile)
    
    def __unicode__(self):
        return unicode(self.name)
        
    def get_check(self):
        output = unicode(self.date)
        
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
        return unicode('Closed!')
        
    def get_day_hour_to(self):
        if self.opened  is True:
            return self.hour_to
        return unicode('Closed!')
        
'''
    # TAGS & SPECIAL TAGS ####
'''
# Tags to identify restaurant genre such as "Japanese, Chinese, Malaysian, etc"
class tags(models.Model):
    keyword = models.CharField(primary_key=True, max_length=50)
    eatery_profile = models.ManyToManyField(eatery_profile)
    
    def __unicode__(self):
        return unicode(self.keyword)
    
# Special tags to identify additional info such as "Glutten free, vegetarian, Kid-friendly, smoker friendly" etc
class special_tags(models.Model):
    keyword = models.CharField(primary_key=True, max_length=50)
    eatery_profile = models.ManyToManyField(eatery_profile)
    
    def __unicode__(self):
        return unicode(self.keyword)

        
'''
    # FOOD & SPECIALS
'''
class food_hearts(models.Model):    
    user_profile = models.ForeignKey(user_profile)
    date_hearted = models.DateTimeField(auto_now_add=True)
    
class food(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.CharField(max_length=255)
    picture = models.ImageField(upload_to=generate_directory_eatery_food, null=True, blank=True)
    food_hearts = models.ManyToManyField(food_hearts, null=True, blank=True)
    eatery_profile = models.ForeignKey(eatery_profile)
    
    def __unicode__(self):
        return unicode(self.name)
        
class specials_hearts(models.Model):    
    user_profile = models.ForeignKey(user_profile)
    date_hearted = models.DateTimeField(auto_now_add=True)    
    
    def __unicode__(self):
        return unicode(self.user_profile.get_username())
        
class specials(models.Model):
    name = models.CharField(max_length=50)
    normal_price = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.CharField(max_length=255)
    picture = models.ImageField(upload_to=generate_directory_eatery_specials, null=True, blank=True)
    date_valid_from = models.DateField()
    date_valid_to = models.DateField()
    hour_valid_from = models.TimeField(null=True, blank=True)
    hour_valid_to = models.TimeField(null=True, blank=True)    
    specials_hearts = models.ManyToManyField(specials_hearts, null=True, blank=True)
    eatery_profile = models.ForeignKey(eatery_profile)    
    
    def __unicode__(self):
        return unicode(self.name)
    
'''
    # REVIEWS
'''
class reviews(models.Model):
    user_profile = models.ForeignKey(user_profile)    
    review_text = models.CharField(max_length=255)
    useful_count = models.IntegerField(null=True, blank=True)
    not_useful_count = models.IntegerField(null=True, blank=True)
    eatery_profile = models.ForeignKey(eatery_profile)
    
    def __unicode__(self):
        return unicode(self.eatery_profile.name + '\'s reviews')        
        
    def user_picture_location(self):
        if self.user_profile.picture:
            return self.user_profile.picture
        return 'img/profile/blank.png'
        
    def user_username(self):
        return self.user_profile.get_username()
    
'''
    # VOTES 
'''
class user_votes(models.Model):
    user_profile = models.ForeignKey(user_profile)    
    datetime_voted = models.DateField(auto_now_add=True)
    is_upvoted = models.BooleanField()
    eatery_profile = models.ForeignKey(eatery_profile)
    
    def __unicode__(self):
        if self.is_upvoted is True:
            return unicode(self.user_profile.get_username() + '\'s upvotes!')              
        return unicode(self.user_profile.get_username() + '\'s downvotes')
        