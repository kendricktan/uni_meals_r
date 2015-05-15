from django.conf.urls import include, url
from . import views

urlpatterns = [
    # Profile
    url(r'^/?$', views.profile_view, name='profile_view'),
    url(r'^edit/?$', views.profile_edit_view, name='profile_edit_view'),
    
    # Sign-up view
    url(r'^signup/?$', views.signup_view, name='signup_view'),
    
    # login view
    url(r'^login/?$', views.login_view, name='login_view'),
    
    # logout and redirects
    url(r'^logout/?$', views.logout_view, name='logout_view'),        
]