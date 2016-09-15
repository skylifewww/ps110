<img height="250" src="https://raw.githubusercontent.com/discobeta/PS110Mobile/master/www/img/event.png"></td>
<br>
<a href="https://play.google.com/store/apps/details?id=com.les.ps110"><img width="110" src="http://ps110.org/static/img/googleplay.svg"></a>
<br>
<a href="https://itunes.apple.com/us/app/ps-110-events/id1146904301" target="_blank"><img width="110" src="https://raw.githubusercontent.com/discobeta/ps110/master/ps110/static/img/appstore.png" target="_blank"></a>

<br>
<h2> ps110.org Web & API Service </h2>

<h3> Dev Guide - How to install & run:</h3>

1. ./manage makemigrations

2. ./manage.py migrate

3. ./manage.py createsuperuser

3. export MYSQL_HOST="127.0.0.1"

5. export DJANGO_DEBUG=False (For print messages)

4. ./manage.py runserver

<h3> Dev Guide - Add Event to your existing Django project: </h3>

1. Add event.apps.EventConfig to INSTALLED_APPS in settings.py - DONE

2. Add url(r'^event/', include('event.urls')) to your project urls.py - DONE

<h3> Dev Guide - API Authentication</h3>

To authenticate with the API one must first obtain a Token by authenticating with your username and password and later use that Token in the header:

1. curl --header "Content-Type: application/x-www-form-urlencoded" --header "Accept: application/json; indent=4" --request POST --data "username=YOURUSERNAME&password=YOURPASSWORD" http://localhost:8000/api-token-auth/

2. curl -X GET http://localhost:8000/api/events/ -H 'Authorization: JWT token-received-in-previous-step'

<h3> User Guide - Managing Events and Classrooms </h3>

To manage your data login to your admin account on <a href="http://ps110.org/admin">ps110.org/admin</a>.

<h3> Google Calendar </h3>

A Django Admin Command is executed via cron to fetch events from the PS 110 PTA Google Calendar. The script is executed every day at midnight, EST.
