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
	teacher_name = models.CharField(max_length=200)
	teacher_email = models.EmailField(max_length=120)
	def __str__(self):
		return self.teacher_email
		
class Event(models.Model):

	title = models.CharField(max_length=200)
	description = models.TextField(max_length=2200)
	location = models.CharField(max_length=200)
	event_date = models.DateTimeField(default=timezone.now())
	event_length = models.IntegerField(max_length=200)
	classroom = models.ManyToManyField(Classroom)

	@property
	def month_name(self):
	    return self.event_date.strftime("%B")
	def day_number(self):
	    return self.event_date.strftime("%d")
	def day_name(self):
	    return self.event_date.strftime("%A")

	def __str__(self):
		return self.title



class Parent(models.Model):

	name = models.CharField(max_length=200)
	phone = models.CharField(max_length=200)
	child_name = models.CharField(max_length=200)
	classrooms = models.CharField(max_length=200)
	created = models.DateTimeField(default=timezone.now())
	def __str__(self):
		return self.created

class Activity(models.Model):

	user = models.IntegerField(max_length=200)
	created = models.DateTimeField(default=timezone.now())
	event = models.CharField(max_length=200)
	def __str__(self):
		return self.event

class ActivityForm(forms.ModelForm):

	class Meta:
		model = Activity
		fields = ['user', 'created', 'event']

class ParentForm(forms.ModelForm):

	class Meta:
		model = Parent
		fields = ['name', 'phone', 'child_name', 'classrooms', 'created']

class ClassroomForm(forms.ModelForm):

	class Meta:
		model = Classroom
		fields = ['name', 'teacher_name', 'teacher_email']

class EventForm(forms.ModelForm):

	class Meta:
		model = Event
		fields = ['title', 'description', 'location', 'event_date', 'event_length', 'classroom']
