from django.conf.urls import include, url
from . import views

urlpatterns = [        
    # Index
    url(r'^/?$', views.index_view, name='index_view'),
    
    # Browse
    url(r'^browse/$', views.browse_view, name='browse_view'),
    
    # Search
    url(r'^search/$', views.search_view, name='search_view'),
    
    # Eatery Profile
    url(r'^eatery/(?P<eatery_id>[0-9]+)/$', views.eatery_view, name='eatery_view'),    
    url(r'^eatery/(?P<eatery_id>[0-9]+)/clear_review/$', views.eatery_clear_review, name='eatery_clear_review'),
    url(r'^eatery/(?P<eatery_id>[0-9]+)/add_review/$', views.eatery_add_review, name='eatery_add_review'),
]