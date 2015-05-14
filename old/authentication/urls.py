from django.conf.urls import include, url
from . import views

urlpatterns = [
    # signup view
    url(r'^signup/?$', views.signup_view, name='signup_view'),
    url(r'^/?$', views.signup_view, name='signup_view'),
    
    # adding user to database via POST
    url(r'^signup/adduser/$', views.signup_adduser, name='signup_adduser'),
    
    # login view
    url(r'^login/?$', views.login, name='login'),
    
    # logout and redirects
    url(r'^logout/?$', views.logout, name='logout'),
]