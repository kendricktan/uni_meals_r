from django.conf.urls import include, url
from . import views

urlpatterns = [
    # User Profile
    url(r'^(?P<profile_id>[0-9]+)/$', views.profile_view, name='profile_view'),
    url(r'^edit/(?P<profile_id>[0-9]+)/$', views.profile_edit_view, name='profile_edit_view'),
    url(r'^edit/(?P<profile_id>[0-9]+)/update_info/$', views.update_profile_info, name='update_profile_info'),
    url(r'^edit/(?P<profile_id>[0-9]+)/update_password/$', views.update_profile_password, name='update_profile_password'),
    url(r'^edit/(?P<profile_id>[0-9]+)/update_dp/$', views.update_profile_dp, name='update_profile_dp'),
    
    # Sign-up view
    url(r'^signup/$', views.signup_view, name='signup_view'),
    
    # login view
    url(r'^login/$', views.login_view, name='login_view'),
    
    # logout and redirects
    url(r'^logout/$', views.logout_view, name='logout_view'),        
]