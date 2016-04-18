from __future__ import unicode_literals

from django.db import models


from jsonfield import JSONField
from django.utils import timezone

# Create your models here.

class Activity(models.Model):

	user = models.IntegerField(max_length=200)
	created = models.DateTimeField(default=timezone.now())
	event = models.CharField(max_length=200)
	def __str__(self):
		return self.event




