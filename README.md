# django_build_guide
# Building a Simple Blog App with Django

A beginner-friendly, step-by-step guide for creating a small blog application using Django. By the end, students will have a working page that lists blog posts and links to individual post pages.

## Learning objectives

- Understand the difference between a Django project and an app.
- Create a Django project and app.
- Configure the app and database.
- Create a `Post` model and run migrations.
- Build views, URL routes, and HTML templates.
- Display a list of posts and a single post.
- Troubleshoot common beginner errors.

## 1. Requirements

Install Python and check it in your terminal:

```bash
python --version
```

Open a project folder in VS Code. Commands below use Linux.

## 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
python -m pip install django
python -m django --version
```

A virtual environment keeps project dependencies separate from other Python projects.

## 3. Create the project and app

Run these commands in your working folder:

```bash
django-admin startproject myproject
cd myproject
python manage.py startapp blogapp
```

- **Project (`myproject`)** contains configuration and the main URL file.
- **App (`blogapp`)** contains the blog's models, views, templates, and app URLs.

## 4. Register the app

Open `myproject/settings.py`. Add `"blogapp"` to the existing `INSTALLED_APPS` list. Do not remove Django's built-in apps.

```python
INSTALLED_APPS = [
    # Keep the existing Django apps here.
    "blogapp",
]
```

This is an illustration of the addition; preserve the other entries already in your file.

## 5. Create the Post model

In `blogapp/models.py`:

```python
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

- `title` stores the post title.
- `content` stores the post text.
- `created_at` records when the post was created.
- `__str__()` gives each post a readable name in the admin.

## 6. Create database tables

```bash
python manage.py makemigrations
python manage.py migrate
```

`makemigrations` creates migration files describing model changes. `migrate` applies those changes to the database.

If `createsuperuser` reports `no such table: auth_user`, first run `python manage.py migrate`, then try again.

## 7. Register the model in Django admin

In `blogapp/admin.py`:

```python
from django.contrib import admin
from .models import Post

admin.site.register(Post)
```

Create an administrator:

```bash
python manage.py createsuperuser
```

Start the server with `python manage.py runserver`, then visit `http://127.0.0.1:8000/admin/` and sign in. You can add posts through the admin site.

## 8. Create the views

In `blogapp/views.py`:

```python
from django.shortcuts import render, get_object_or_404
from .models import Post


def post_list(request):
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "blogapp/post_list.html", {"posts": posts})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "blogapp/post_detail.html", {"post": post})
```

A **view** receives a request, does the necessary work, and returns a response. `post_list` retrieves all posts and sends them to a template. `post_detail` retrieves one post by its ID.

Make sure the model name and fields match your own code.

## 9. Configure URLs

Create or edit `blogapp/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("post/<int:post_id>/", views.post_detail, name="post_detail"),
]
```

Now open `myproject/urls.py` and connect the app URLs:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blogapp.urls")),
]
```

## 10. Create the template folders

Inside the `blogapp` app, create this structure:

```text
blogapp/
├── templates/
│   └── blogapp/
│       ├── post_list.html
│       └── post_detail.html
├── admin.py
├── models.py
├── urls.py
└── views.py
```

The nested `templates/blogapp/` folder helps Django find the app's templates.

**Important:** The template path in `render()` must match the real filename. For `"blogapp/post_list.html"`, the file should be at `blogapp/templates/blogapp/post_list.html`.

## 11. Create `post_list.html`

Path: `blogapp/templates/blogapp/post_list.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Blog</title>
</head>
<body>
    <h1>Welcome to My Blog</h1>

    {% for post in posts %}
        <article>
            <h2>
                <a href="{% url 'post_detail' post.id %}">
                    {{ post.title }}
                </a>
            </h2>
            <p>{{ post.content|truncatewords:30 }}</p>
        </article>
    {% empty %}
        <p>No blog posts yet. Check back soon!</p>
    {% endfor %}
</body>
</html>
```

- `{% for post in posts %}` loops over the posts passed by the view.
- `{{ post.title }}` displays a post title.
- `truncatewords:30` displays up to 30 words of content.
- `{% empty %}` displays a message if there are no posts.
- `{% url 'post_detail' post.id %}` creates a link to the post detail route.

## 12. Create `post_detail.html`

Path: `blogapp/templates/blogapp/post_detail.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ post.title }}</title>
</head>
<body>
    <a href="{% url 'post_list' %}">Back to all posts</a>

    <h1>{{ post.title }}</h1>
    <p>{{ post.content|linebreaks }}</p>
    <small>Published: {{ post.created_at }}</small>
</body>
</html>
```

This page shows one post. The `linebreaks` filter makes line breaks in the content easier to read.

## 13. Run and test the app

From the directory containing `manage.py`:

```bash
python manage.py runserver
```

Open:
- Blog homepage: `http://127.0.0.1:8000/`
- Admin site: `http://127.0.0.1:8000/admin/`

Add a few posts through the admin site, refresh the homepage, and click a title to view its detail page.

## 14. Common errors

### `TemplateDoesNotExist: blogapp/post_list.html`

Check that the file exists at `blogapp/templates/blogapp/post_list.html`. Check spelling and capitalization. `post_list.html` and `post.html` are different filenames.

### `no such table: auth_user`

Run:

```bash
python manage.py migrate
```

### 404 Page Not Found

Check the browser URL and the route patterns in both `urls.py` files. Make sure the main project includes `blogapp.urls`.

### `NoReverseMatch`

The name used in `{% url 'post_detail' ... %}` must match the URL pattern's `name`. Supply required arguments such as `post.id`.

### Posts do not appear

Add posts through the admin site. Confirm the view passes `{"posts": posts}` and the template loops over `posts`.

## 15. Useful commands

| Command | Purpose |
|---|---|
| `python -m venv venv` | Creates a virtual environment |
| `source venv/bin/activate` | Activates it on Linux/macOS |
| `python -m pip install django` | Installs Django |
| `django-admin startproject myproject` | Creates the project |
| `python manage.py startapp blogapp` | Creates the app |
| `python manage.py makemigrations` | Creates migration files |
| `python manage.py migrate` | Applies migrations |
| `python manage.py createsuperuser` | Creates an admin account |
| `python manage.py runserver` | Starts the development server |

## 16. Student exercises

1. Change the homepage heading to include your name or class.
2. Add three blog posts using the Django admin site.
3. Add a `category` field to `Post`, then run the migration commands.
4. Display the creation date on the list page.
5. Add a link on the detail page that returns to the homepage.
6. Temporarily change the name `post_list.html`, observe the error, and then restore the correct name.

## 17. Check your understanding

1. What is the difference between a Django project and an app?
2. What is a model?
3. What is the difference between `makemigrations` and `migrate`?
4. What does a view do?
5. Why do we create a `templates` folder?
6. What does `{% for post in posts %}` do?
7. Why must the filename in `render()` match the actual template?
8. What is the purpose of `urls.py`?
9. How do you create an administrator account?
10. Which command starts the local development server?

## Final result

You have built the foundation of a Django blog:
- A database model for posts.
- Admin access for adding posts.
- A homepage listing posts.
- A detail page for one post.
- URL routing and HTML templates.

**Suggested next steps:** Add CSS styling, forms for creating posts, editing and deleting, user authentication, and automated tests.

> Teaching note written by Leonard Emelieze Backend Instructor Digital Fortress Ltd
