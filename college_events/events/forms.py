"""
Forms handle:
1. Rendering HTML <form> elements
2. Validating submitted data
3. Saving to the database

ModelForm automatically creates a form from a Model class.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import EventImage, Event


class StudentRegistrationForm(UserCreationForm):
    """
    Extends Django's built-in registration form to add email and full name.
    UserCreationForm already handles username + password + password confirmation.
    """
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class ImageUploadForm(forms.ModelForm):
    """
    Form for students to upload images.
    We only expose 'event', 'image', and 'caption' to the student.
    'status', 'uploaded_by' etc. are set programmatically in the view.
    """
    class Meta:
        model = EventImage
        fields = ['event', 'image', 'caption']
        widgets = {
            'caption': forms.TextInput(attrs={
                'placeholder': 'Brief description of this photo (optional)'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show active events in the dropdown
        self.fields['event'].queryset = Event.objects.filter(is_active=True)
        self.fields['event'].empty_label = "— Select an event —"

    def clean_image(self):
        """
        Custom validation for the image field.
        This runs automatically when form.is_valid() is called.
        """
        image = self.cleaned_data.get('image')
        if image:
            # Limit file size to 10MB
            if image.size > 10 * 1024 * 1024:
                raise forms.ValidationError("Image file too large. Maximum size is 10MB.")
            # Check file type
            allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
            if image.content_type not in allowed_types:
                raise forms.ValidationError("Only JPEG, PNG, GIF, and WebP images are allowed.")
        return image


class AdminReviewForm(forms.ModelForm):
    """
    Form for admin to approve/reject an image with an optional note.
    """
    class Meta:
        model = EventImage
        fields = ['status', 'admin_note']
        widgets = {
            'admin_note': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional note to yourself'})
        }
