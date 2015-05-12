from django.conf.urls import url
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Index
    url(r'^$', views.index_view, name='index_view'),
    
    # Sign up, login
    url(r'^signup/?$', views.signup_view, name='signup_view'),
    url(r'^login/?$', views.login_view, name='login_view'),
    
    # Browse, search
    url(r'^browse/?$', views.browse_view, name='browse_view'),
    url(r'^search/?$', views.search_view, name='search_view'),
    
    # Eatery
    url(r'^eatery/?$', views.eatery_view, name='eatery_view'),
    
    # Profile
    url(r'profile/?$', views.profile_view, name='profile_view'),
    url(r'profile/edit/?$', views.profile_edit_view, name='profile_edit_view'),
    
    # Inbox, messages
    url(r'inbox/?$', views.inbox_view, name='inbox_view'),
    url(r'inbox/message/?$', views.message_view, name='message_view'),
] 