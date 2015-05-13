from django.conf.urls import include, url
from . import views

urlpatterns = [
    # signup
    url(r'^$', views.signup_view, name='signup_view'),
    url(r'^adduser/?$', views.signup_adduser, name='signup_adduser'),
    url(r'^login/?$', views.login, name='login'),
    url(r'^logout/?$', views.logout, name='logout'),
]