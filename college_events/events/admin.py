"""
Register models with Django's built-in admin site.
This gives you a full CRUD interface at /admin/ for free.
"""

from django.contrib import admin
from .models import Event, EventImage


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'is_active', 'created_by', 'created_at')
    list_filter = ('is_active', 'date')
    search_fields = ('name', 'description')
    list_editable = ('is_active',)


@admin.register(EventImage)
class EventImageAdmin(admin.ModelAdmin):
    list_display = ('event', 'uploaded_by', 'status', 'uploaded_at', 'reviewed_by')
    list_filter = ('status', 'event')
    search_fields = ('caption', 'uploaded_by__username')
    list_editable = ('status',)
    readonly_fields = ('uploaded_at', 'reviewed_at')

    # Group fields nicely in the detail view
    fieldsets = (
        ('Image Info', {
            'fields': ('event', 'image', 'caption', 'uploaded_by', 'uploaded_at')
        }),
        ('Review', {
            'fields': ('status', 'admin_note', 'reviewed_by', 'reviewed_at')
        }),
    )
