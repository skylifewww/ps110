from __future__ import unicode_literals

from django.db import models
from django import forms
from jsonfield import JSONField
from django.utils import timezone

# Create your models here.
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)

class Classroom(models.Model):

	name = models.CharField(max_length=200)
	teacher_name = models.CharField(max_length=200, null=True, blank=True, verbose_name=(u"Teacher Name (Optional)"))
	teacher_email = models.EmailField(max_length=120, null=True, blank=True, verbose_name=(u"Teacher Email (Optional)"))

	subscribers = models.ManyToManyField(User, verbose_name=(u"subscribers"), blank=True, null=True)

	def __str__(self):
		return self.name

class ClassroomForm(forms.ModelForm):

	class Meta:
		model = Classroom
		fields = ['name', 'teacher_name', 'teacher_email']

		
class Event(models.Model):

	title = models.CharField(max_length=200)
	description = models.TextField(max_length=2200)
	location = models.CharField(max_length=200, null=True, blank=True, verbose_name=(u"Where is this taking place? (Optional)"))

	start_date = models.DateTimeField(default=timezone.now())
	end_date = models.DateTimeField(default="", null=True, blank=True, verbose_name=(u"End Date (Optional)"))
	event_duration = models.CharField(max_length=200, null=True, blank=True,verbose_name='Duration (optional)')


	classroom = models.ManyToManyField(Classroom)
	
	@property
	def month_name(self):
	    return self.start_date.strftime("%B")
	def day_number(self):
	    return self.start_date.strftime("%d")
	def day_name(self):
	    return self.start_date.strftime("%A")

	def __str__(self):
		return self.title



class EventForm(forms.ModelForm):

	class Meta:
		model = Event
		fields = ['title', 'description', 'location', 'end_date', 'start_date', 'event_duration', 'classroom']

	def __init__(self, *args, **kwargs):
		self.fields["classroom"].widget = forms.widgets.CheckboxSelectMultiple()
		self.fields["classroom"].help_text = "Class room subscribers"
		self.fields["classroom"].queryset = Classroom.objects.all()
