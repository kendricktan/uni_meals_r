from django.conf.urls import include, url
from . import views

urlpatterns = [        
    # Index
    url(r'^/?$', views.index_view, name='index_view'),
    
    # Browse
    url(r'^browse/?$', views.browse_view, name='browse_view'),
    
    # Search
    url(r'^search/?$', views.search_view, name='search_view'),
    
    # Eatery Profile
    url(r'^eatery/?$', views.eatery_view, name='eatery_view'),
]