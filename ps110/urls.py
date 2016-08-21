"""ps110 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include

, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include


from django.contrib import admin
from . import views
from event.models import Event
from event.models import Classroom

from rest_framework import routers, serializers, viewsets
from django.views.generic.base import RedirectView

from rest_framework_jwt.views import obtain_jwt_token

from django.contrib.auth.models import User

import django_filters
from rest_framework import filters

from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from django.db.models import Q

from datetime import datetime

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class classroomSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = Classroom
		fields = ['id','name', 'teacher_name', 'teacher_email']

class ClassroomViewSet(viewsets.ModelViewSet):
	queryset = Classroom.objects.all()
	serializer_class = classroomSerializer

	@detail_route(methods=['get'])
	def subscribe(self, request, pk=None):
		obj = self.get_object()
		user = request.user
		if user.is_anonymous():
			raise PermissionDenied
		if user in obj.subscribers.all():
			print "already"
		else:
			obj.subscribers.add(user)

		member = True
		return Response({'member': member})	

	@detail_route(methods=['get'])
	def unsubscribe(self, request, pk=None):
		obj = self.get_object()
		user = request.user
		if user.is_anonymous():
			raise PermissionDenied
		if user in obj.subscribers.all():
			obj.subscribers.remove(user)
		else:
			print "nothing"
		member = False
		return Response({'member': member})	

class eventSerializer(serializers.HyperlinkedModelSerializer):
	classroom = serializers.SlugRelatedField(
	    many=True,
	    read_only=True,
	    slug_field='name'
	)
	class Meta:
		model = Event
		fields = ['month_name','day_number','day_name','title', 'description', 'location', 'start_date', 'end_date', 'event_duration', 'classroom']



class EventViewSet(viewsets.ModelViewSet):
	queryset = Event.objects.all()
	serializer_class = eventSerializer

	def get_queryset(self):
	    user = self.request.user
	    print 'user'
	    print user
	    subscriptions = Classroom.objects.filter(subscribers__in=[user.id])
	    print 'subscriptions'
	    print subscriptions
	    #events = Event.objects.filter(classroom__in=subscriptions)
	    now = datetime.now()
	    events = Event.objects.filter(Q(classroom__in=subscriptions,start_date=now.date())|Q(classroom__in=subscriptions,start_date__gt=now.date())).order_by('start_date')
	    print 'events'
	    print events
	    return events

router = routers.DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'classrooms', ClassroomViewSet)




urlpatterns = [

	url(r'^api/register', 'ps110.views.create_auth'),
	url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),
	url(r'^resetpassword/passwordsent/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
	url(r'^$', views.home, name='home'),
    url(r'^admin/', admin.site.urls),
	url(r'^api/facebook_auth', 'ps110.views.facebook_auth'),
	url(r'^home/', 'ps110.views.home', name='home'),
	url('', include('social.apps.django_app.urls', namespace='social')),
	url('', include('django.contrib.auth.urls', namespace='auth')),
	url(r'^api/', include(router.urls)),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	url(r'^api-token-auth/', obtain_jwt_token),
	url('', include('event.urls', namespace='event')),
]
