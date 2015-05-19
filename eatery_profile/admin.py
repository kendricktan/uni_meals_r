from django.contrib import admin
from .models import *

class location_inline(admin.StackedInline):
    model = location
    
class opening_hours_inline(admin.StackedInline):
    model = opening_hours
    extra = 0
    
class special_days_inline(admin.StackedInline):
    model = special_days
    extra = 0
    
class tags_inline(admin.StackedInline):
    model = tags.eatery_profile.through
    
class special_tags_inline(admin.StackedInline):
    model = special_tags.eatery_profile.through
    
class food_inline(admin.StackedInline):
    model = food
    extra = 0
    
class specials_inline(admin.StackedInline):
    model = specials
    extra = 0
    
class reviews_inline(admin.StackedInline):
    model = reviews
    extra = 0
    
class eatery_profile_page(admin.ModelAdmin):
    inlines = [location_inline, opening_hours_inline, special_days_inline, food_inline, specials_inline, tags_inline, special_tags_inline, reviews_inline]

# Register your models here.
admin.site.register(eatery_profile, eatery_profile_page)
admin.site.register(tags)
admin.site.register(special_tags)