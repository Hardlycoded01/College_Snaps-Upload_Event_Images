"""
URL patterns for the events app.

Each path() call maps:
  URL pattern → view function → name (used in templates with {% url 'name' %})
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # ── Public pages ──────────────────────────────────────────────
    path('', views.home, name='home'),
    path('event/<int:event_id>/', views.event_gallery, name='event_gallery'),

    # ── Student auth ──────────────────────────────────────────────
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='events/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # ── Student actions ───────────────────────────────────────────
    path('upload/', views.upload_image, name='upload_image'),
    path('my-uploads/', views.my_uploads, name='my_uploads'),

    # ── Admin panel ───────────────────────────────────────────────
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/review/<int:image_id>/', views.review_image, name='review_image'),
    path('admin-panel/create-event/', views.create_event, name='create_event'),
]
