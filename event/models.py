from __future__ import unicode_literals
from django.db import models
from django import forms
from jsonfield import JSONField
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
<<<<<<< HEAD
#from datetime import datetime
import datetime
=======
from datetime import datetime
>>>>>>> 34e4f98733716ee54053c290f8aba7c0fc56189b

"""
Create a new token when a user is created
"""

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)









"""
Classroom Model
"""

class Classroom(models.Model):

	name = models.CharField(max_length=200)
	teacher_name = models.CharField(max_length=200, null=True, blank=True, verbose_name=(u"Teacher Name (Optional)"))
	teacher_email = models.EmailField(max_length=120, null=True, blank=True, verbose_name=(u"Teacher Email (Optional)"))

	subscribers = models.ManyToManyField(User, verbose_name=(u"subscribers"), blank=True, null=True)

	def __str__(self):
		return self.name

"""
Classroom Form
"""

class ClassroomForm(forms.ModelForm):

	class Meta:
		model = Classroom
		fields = ['name', 'teacher_name', 'teacher_email']










"""
Event Model
"""

class Event(models.Model):

	title = models.CharField(max_length=200)
	description = models.TextField(max_length=2200)
	location = models.CharField(max_length=200, null=True, blank=True, verbose_name=(u"Where is this taking place? (Optional)"))

<<<<<<< HEAD
	# where we pulled this from
	source = models.CharField(max_length=200,null=True, blank=True, default='pta')

=======
>>>>>>> 34e4f98733716ee54053c290f8aba7c0fc56189b
	start_date = models.DateTimeField(default=timezone.now())
	end_date = models.DateTimeField(default="", null=True, blank=True, verbose_name=(u"End Date (Optional)"))

	classroom = models.ManyToManyField(Classroom)

<<<<<<< HEAD
	# def days_hours_and_minutes(self):
	# 	a = self.start_date
	# 	b = self.end_date
	# 	td = b - a
	# 	return td.days, td.seconds // 3600, (td.seconds // 60) % 60

	def days_hours_and_minutes(self):
		#print "str(self.start_date)", str(self.start_date)
		try:
			a = datetime.datetime.strptime(str(self.start_date).replace('+00:00',''), '%Y-%m-%dT%H:%M:%S') - datetime.timedelta(days=1)
		except ValueError:
			try:
				a = datetime.datetime.strptime(str(self.start_date).replace('+00:00',''), '%Y-%m-%d %H:%M:%S') - datetime.timedelta(days=1)
			except ValueError:
				print "SUPER ERROR\tXXX\tXXXX\n\n"
				a = None
		try:
			b = datetime.datetime.strptime(str(self.end_date).replace('+00:00',''), '%Y-%m-%dT%H:%M:%S') - datetime.timedelta(days=1)
		except ValueError:
			try:
				b = datetime.datetime.strptime(str(self.end_date).replace('+00:00',''), '%Y-%m-%d %H:%M:%S') - datetime.timedelta(days=1)
			except ValueError:
				b = None

		if b and a:
			td = b - a
			return td.days, td.seconds // 3600, (td.seconds // 60) % 60
		else:
			return None
=======
	def days_hours_and_minutes(self):
		a = self.start_date
		b = self.end_date
		td = b - a
		return td.days, td.seconds // 3600, (td.seconds // 60) % 60
>>>>>>> 34e4f98733716ee54053c290f8aba7c0fc56189b

	def start_time(self):
		return self.start_date.strftime("%I:%M %p")

<<<<<<< HEAD
	# def today(self):
	# 	return datetime.today()

=======
>>>>>>> 34e4f98733716ee54053c290f8aba7c0fc56189b
	def end_time(self):
		return self.end_date.strftime("%I:%M %p")

	def event_duration(self):
		return None

	@property
	def month_name(self):
	    return self.start_date.strftime("%B")
	def day_number(self):
	    return self.start_date.strftime("%d")
	def day_name(self):
	    return self.start_date.strftime("%A")

	def __str__(self):
<<<<<<< HEAD
		return str(self.title) + ' - ' + str(self.start_date) + ' - ' + str(self.end_date)
=======
		return self.title
>>>>>>> 34e4f98733716ee54053c290f8aba7c0fc56189b

"""
Event Form
"""

class EventForm(forms.ModelForm):

	class Meta:
		model = Event
		fields = ['title', 'description', 'location', 'end_date', 'start_date', 'classroom']

	def __init__(self, *args, **kwargs):
		self.fields["classroom"].widget = forms.widgets.CheckboxSelectMultiple()
		self.fields["classroom"].help_text = "Class room subscribers"
		self.fields["classroom"].queryset = Classroom.objects.all()
