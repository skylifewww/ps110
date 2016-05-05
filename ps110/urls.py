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
from event.models import Parent
from event.models import Activity
from rest_framework import routers, serializers, viewsets
from rest_framework_jwt.views import obtain_jwt_token


class eventSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Event
		fields = ['title', 'description', 'location', 'event_date', 'event_length', 'classroom']



class EventViewSet(viewsets.ModelViewSet):
	queryset = Event.objects.all()
	serializer_class = eventSerializer


class classroomSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Classroom
		fields = ['name', 'teacher_name', 'teacher_email']



class ClassroomViewSet(viewsets.ModelViewSet):
	queryset = Classroom.objects.all()
	serializer_class = classroomSerializer


class parentSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Parent
		fields = ['name', 'phone', 'child_name', 'classrooms', 'created']



class ParentViewSet(viewsets.ModelViewSet):
	queryset = Parent.objects.all()
	serializer_class = parentSerializer


class activitySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Activity
		fields = ['user', 'created', 'event']



class ActivityViewSet(viewsets.ModelViewSet):
	queryset = Activity.objects.all()
	serializer_class = activitySerializer

router = routers.DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'classrooms', ClassroomViewSet)
router.register(r'parents', ParentViewSet)
router.register(r'activitys', ActivityViewSet)




urlpatterns = [
	url(r'^resetpassword/passwordsent/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
	url(r'^$', views.home, name='home'),
    url(r'^admin/', admin.site.urls),
	url(r'^home/', 'ps110.views.home', name='home'),
	url('', include('social.apps.django_app.urls', namespace='social')),
	url('', include('django.contrib.auth.urls', namespace='auth')),
	url(r'^api/', include(router.urls)),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	url(r'^api-token-auth/', obtain_jwt_token),
	url('', include('event.urls', namespace='event')),
]
