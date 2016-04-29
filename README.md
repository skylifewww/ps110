<h3>How to install & run:</h3>

1. ./manage makemigrations

2. ./manage.py migrate

3. ./manage.py createsuperuser

4. ./manage.py runserver

<h3>Add Event to your existing Django project:</h3>

1. Add event.apps.EventConfig to INSTALLED_APPS in settings.py - DONE

2. Add url(r'^event/', include('event.urls')) to your project urls.py - DONE