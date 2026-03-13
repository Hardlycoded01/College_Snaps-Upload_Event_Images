"""
URL Configuration for college_events project.

Each URL pattern maps a URL path to a view function.
We also serve media files in development using static() helper.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),         # Django's built-in admin panel
    path('', include('events.urls')),        # All our app URLs
    path('accounts/', include('django.contrib.auth.urls')),  # login/logout/password
]

# In development, serve uploaded media files directly
# In production you'd use Nginx or a CDN instead
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
