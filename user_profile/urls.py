from django.conf.urls import include, url
from . import views

urlpatterns = [
    # User Profile
    url(r'^(?P<profile_id>[0-9]+)/$', views.profile_view, name='profile_view'),
    url(r'^edit/(?P<profile_id>[0-9]+)/$', views.profile_edit_view, name='profile_edit_view'),
    url(r'^edit/(?P<profile_id>[0-9]+)/update_info/$', views.update_profile_info, name='update_profile_info'),
    url(r'^edit/(?P<profile_id>[0-9]+)/update_password/$', views.update_profile_password, name='update_profile_password'),
    url(r'^edit/(?P<profile_id>[0-9]+)/update_dp/$', views.update_profile_dp, name='update_profile_dp'),
    
    # Heart and unhearts specials
    url(r'^heart/special/(?P<specials_id>[0-9]+)/$', views.profile_heart_special, name='profile_heart_special'),
    url(r'^unheart/special/(?P<specials_id>[0-9]+)/$', views.profile_unheart_special, name='profile_unheart_special'),
    url(r'^heart/food/(?P<food_id>[0-9]+)/$', views.profile_heart_food, name='profile_heart_food'),
    url(r'^unheart/food/(?P<food_id>[0-9]+)/$', views.profile_unheart_food, name='profile_unheart_food'),
    
    # Upvote/downvote eatery
    url(r'^upvote/eatery/(?P<eatery_id>[0-9]+)/$', views.profile_eatery_upvote, name='profile_eatery_upvote'),
    url(r'^downvote/eatery/(?P<eatery_id>[0-9]+)/$', views.profile_eatery_downvote, name='profile_eatery_downvote'),
    url(r'^clearvote/eatery/(?P<eatery_id>[0-9]+)/$', views.profile_eatery_clearvote, name='profile_eatery_clearvote'),
    
    # Inbox (depreciated) 
    #url(r'^inbox/$', views.inbox_view, name='inbox_view'),
    #url(r'^inbox/message/(?P<message_id>[0-9]+)/$', views.inbox_message_view, name='inbox_message_view'),
    #url(r'^inbox/message/new/$', views.inbox_message_new_view, name='inbox_message_new_view'),
    
    # Sign-up view
    url(r'^signup/$', views.signup_view, name='signup_view'),
    
    # login view
    url(r'^login/$', views.login_view, name='login_view'),
    
    # logout and redirects
    url(r'^logout/$', views.logout_view, name='logout_view'),                
]