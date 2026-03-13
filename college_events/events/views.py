"""
Views are Python functions (or classes) that:
1. Receive an HTTP request
2. Do some logic (query DB, process form, etc.)
3. Return an HTTP response (usually rendered HTML)

@login_required decorator = redirect to login page if not authenticated
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .models import Event, EventImage
from .forms import StudentRegistrationForm, ImageUploadForm, AdminReviewForm


# ─── Helper ────────────────────────────────────────────────────────────────────

def is_admin(user):
    """Check if user is a staff/superuser (admin)."""
    return user.is_staff or user.is_superuser


# ─── Public / Student Views ────────────────────────────────────────────────────

def home(request):
    """
    Home page — shows all active events with their approved image count.
    Anyone can visit this page (no login required).
    """
    events = Event.objects.filter(is_active=True)
    # Add approved image count to each event using annotate would be ideal,
    # but for simplicity we use a list comprehension here
    events_with_counts = []
    for event in events:
        events_with_counts.append({
            'event': event,
            'image_count': event.approved_images().count(),
        })
    return render(request, 'events/home.html', {
        'events_data': events_with_counts
    })


def event_gallery(request, event_id):
    """
    Shows approved images for a specific event.
    Anyone can view.
    """
    event = get_object_or_404(Event, id=event_id, is_active=True)
    images = event.approved_images()
    return render(request, 'events/gallery.html', {
        'event': event,
        'images': images,
    })


@login_required
def upload_image(request):
    """
    Students upload images here.
    
    GET request  → show empty form
    POST request → validate form, save image, redirect
    
    The @login_required decorator automatically redirects to /login/ 
    if the user is not logged in.
    """
    if request.method == 'POST':
        # request.FILES contains uploaded files
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form but don't commit to DB yet
            image_obj = form.save(commit=False)
            # Set fields that the student doesn't control
            image_obj.uploaded_by = request.user
            image_obj.status = 'pending'  # always starts as pending
            image_obj.save()

            messages.success(
                request,
                f'Your image has been uploaded successfully! '
                f'It will appear in the gallery after admin review.'
            )
            return redirect('my_uploads')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        # GET: show blank form
        form = ImageUploadForm()

    return render(request, 'events/upload.html', {'form': form})


@login_required
def my_uploads(request):
    """
    Shows the logged-in student their own upload history with status.
    """
    images = EventImage.objects.filter(uploaded_by=request.user)
    return render(request, 'events/my_uploads.html', {'images': images})


def register(request):
    """
    Student registration view.
    After successful registration, log them in automatically.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login after registration
            messages.success(request, f'Welcome, {user.first_name}! Your account is ready.')
            return redirect('home')
    else:
        form = StudentRegistrationForm()

    return render(request, 'events/register.html', {'form': form})


# ─── Admin Views ───────────────────────────────────────────────────────────────

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """
    Admin overview: pending images, event stats.
    @user_passes_test(is_admin) means only staff/superuser can access.
    """
    pending_images = EventImage.objects.filter(status='pending').select_related('event', 'uploaded_by')
    approved_images = EventImage.objects.filter(status='approved')
    rejected_images = EventImage.objects.filter(status='rejected')
    events = Event.objects.filter(is_active=True)

    return render(request, 'events/admin_dashboard.html', {
        'pending_images': pending_images,
        'pending_count': pending_images.count(),
        'approved_count': approved_images.count(),
        'rejected_count': rejected_images.count(),
        'events': events,
    })


@login_required
@user_passes_test(is_admin)
def review_image(request, image_id):
    """
    Admin approves or rejects a single image.
    """
    image = get_object_or_404(EventImage, id=image_id)

    if request.method == 'POST':
        form = AdminReviewForm(request.POST, instance=image)
        if form.is_valid():
            reviewed_image = form.save(commit=False)
            reviewed_image.reviewed_by = request.user
            reviewed_image.reviewed_at = timezone.now()
            reviewed_image.save()

            action = reviewed_image.get_status_display()
            messages.success(request, f'Image has been {action}.')
            return redirect('admin_dashboard')
    else:
        form = AdminReviewForm(instance=image)

    return render(request, 'events/review_image.html', {
        'image': image,
        'form': form,
    })


@login_required
@user_passes_test(is_admin)
def create_event(request):
    """
    Admin creates a new event that students can upload to.
    """
    from django import forms as django_forms
    from .models import Event

    class EventForm(django_forms.ModelForm):
        class Meta:
            model = Event
            fields = ['name', 'description', 'date']
            widgets = {'date': django_forms.DateInput(attrs={'type': 'date'})}

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(request, f'Event "{event.name}" created!')
            return redirect('admin_dashboard')
    else:
        form = EventForm()

    return render(request, 'events/create_event.html', {'form': form})
