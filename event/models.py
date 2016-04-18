from __future__ import unicode_literals

from django.db import models


from jsonfield import JSONField
from django.utils import timezone

# Create your models here.

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




