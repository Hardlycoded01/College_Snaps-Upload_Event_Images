"""
Models define the database structure.

Each class = one database table.
Each attribute = one column in that table.
Django's ORM turns these Python classes into SQL automatically.
"""

from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    """
    Represents a college event (e.g. Freshers Party, Tech Fest).
    
    Fields:
    - name: the event title
    - description: longer details
    - date: when it happens
    - created_by: which admin/user created this event entry
    - created_at: auto-filled timestamp when record is saved
    - is_active: toggle to show/hide without deleting
    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,   # if user deleted, keep the event
        null=True,
        related_name='events_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)  # set once on creation
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date']  # newest events first

    def __str__(self):
        # This is what shows in Django admin and shell
        return f"{self.name} ({self.date})"

    def approved_images(self):
        """Return only images that admin has approved."""
        return self.images.filter(status='approved')

    def pending_images(self):
        """Return images waiting for admin review."""
        return self.images.filter(status='pending')


class EventImage(models.Model):
    """
    An image uploaded by a student for a specific event.
    
    The image file is saved inside media/uploads/<year>/<month>/<day>/
    Django handles the folder creation automatically via upload_to.
    
    status field controls the admin review workflow:
    - pending  → just uploaded, not shown publicly yet
    - approved → admin said yes, visible in gallery
    - rejected → admin said no, hidden
    """

    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,   # delete images if event is deleted
        related_name='images'       # lets us do event.images.all()
    )
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_images'
    )

    # ImageField saves the file to disk and stores the path in the DB
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/')

    caption = models.CharField(max_length=300, blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_images'
    )

    admin_note = models.TextField(
        blank=True,
        help_text='Internal note from admin (not shown to student)'
    )

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Image by {self.uploaded_by} for {self.event.name}"