# College_Snaps-Upload_Event_Images
# CampusSnap 📸

A college event photo upload platform built with Django.  
Students upload event photos → Admin reviews and approves → Photos go live in the gallery → Social media club gets them.

---

## Features

- Student registration and login
- Upload photos tied to specific college events
- Admin review panel — approve or reject each upload
- Public gallery showing only approved photos
- Image preview before upload (drag & drop supported)
- Status tracking — students see pending / approved / rejected for each upload
- Built-in Django admin for full database management

---

## Tech Stack

| Layer     | Technology                        |
|-----------|-----------------------------------|
| Backend   | Django 4.2 (Python)               |
| Database  | SQLite (dev) / PostgreSQL (prod)  |
| Frontend  | HTML, CSS, vanilla JavaScript     |
| Images    | Pillow (file handling)            |
| Deploy    | Render / Railway (free tier)      |

---

## Project Structure

```
college_events/
├── college_events/         # Project config (settings, main urls)
│   ├── settings.py         # All Django settings
│   ├── urls.py             # Root URL dispatcher
│   └── wsgi.py             # WSGI entry point for deployment
│
├── events/                 # Our Django app
│   ├── models.py           # Event + EventImage database models
│   ├── views.py            # All page logic
│   ├── forms.py            # Upload form, registration form, review form
│   ├── urls.py             # App URL patterns
│   ├── admin.py            # Django admin configuration
│   ├── static/events/      # CSS + JS files
│   └── templates/events/   # HTML templates
│
├── media/                  # Uploaded images (git-ignored)
├── manage.py               # Django management commands
├── requirements.txt        # Python dependencies
└── .gitignore
```

---

## Local Setup

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/campussnap.git
cd campussnap
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
This creates `db.sqlite3` — your local database file.

### 5. Create an admin account
```bash
python manage.py createsuperuser
```
Enter a username, email, and password. This account gets access to the admin panel.

### 6. Start the dev server
```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000** — the site is live!

---

## How to Use

### As Admin
1. Go to `/admin-panel/` (or `/admin/` for Django's built-in admin)
2. Create events using the **+ New Event** button
3. Review student uploads — approve or reject each one
4. Approved photos appear instantly in the public gallery

### As a Student
1. Register at `/register/`
2. Log in and go to **Upload**
3. Select an event, choose a photo, add a caption
4. Track your upload status at **My Photos**

---

## Pages

| URL                  | Page                     | Access       |
|----------------------|--------------------------|--------------|
| `/`                  | Home — event listing     | Public       |
| `/event/<id>/`       | Event gallery            | Public       |
| `/upload/`           | Upload photo             | Logged in    |
| `/my-uploads/`       | My upload history        | Logged in    |
| `/admin-panel/`      | Review queue             | Admin only   |
| `/admin-panel/create-event/` | Create event     | Admin only   |
| `/admin/`            | Django built-in admin    | Superuser    |
| `/login/`            | Login                    | Public       |
| `/register/`         | Register                 | Public       |

---

## Key Concepts Learned

- **Django ORM** — Python classes that become database tables automatically
- **ModelForms** — forms that validate and save directly to a model
- **ForeignKey** — linking two tables (an image belongs to an event, an image belongs to a user)
- **@login_required** — protecting views so only logged-in users can access them
- **@user_passes_test** — protecting admin views from regular users
- **MEDIA_ROOT / MEDIA_URL** — how Django stores and serves uploaded files
- **Django messages framework** — showing one-time success/error notifications
- **Django template language** — `{% for %}`, `{% if %}`, `{{ variable }}` in HTML
- **CSRF protection** — `{% csrf_token %}` in every form prevents cross-site attacks

---

## Deployment (Render)

1. Push code to GitHub
2. Create account at [render.com](https://render.com)
3. New Web Service → connect your GitHub repo
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `gunicorn college_events.wsgi`
6. Add environment variable: `DJANGO_SETTINGS_MODULE=college_events.settings`

---

## Contributing

This is a learning/demo project. Feel free to fork and extend it!

Ideas to add next:
- Email notifications when an image is approved/rejected
- Bulk approve/reject in the admin panel
- Image compression before saving
- Export approved images as a ZIP for the social media club
- Deploy with PostgreSQL instead of SQLite

---

*Built as a practice project to learn Django — [Your Name], [Year]*
