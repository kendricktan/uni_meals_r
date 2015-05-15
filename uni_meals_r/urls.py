from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

urlpatterns = [
    # Admin
    url(r'^admin/', include(admin.site.urls)),
    
    # user_profile app
    url(r'^profile/', include('user_profile.urls')),
    
    # eatery_profile app
    url(r'^/?', include('eatery_profile.urls')),
    
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
