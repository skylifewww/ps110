from django.contrib import admin
from django import forms
from django.utils import timezone
from django.contrib.admin import widgets
from .models import Event
from .models import Classroom

class EventForm(forms.ModelForm):
	
	# start_date = forms.DateTimeField(required=True)
	# end_date = forms.DateTimeField(required=True)

	classroom = forms.ModelMultipleChoiceField(
	    queryset=Classroom.objects.all(),
	    widget=forms.CheckboxSelectMultiple)

	class Meta:
	    model = Event
	    exclude = []

	def __init__(self, *args, **kwargs):
		super(EventForm, self).__init__(*args, **kwargs)
		self.fields['start_date'].widget = widgets.AdminSplitDateTime()
		self.fields['end_date'].widget = widgets.AdminSplitDateTime()

class EventAdmin(admin.ModelAdmin):
	form = EventForm
	def save_m2m(self):
	    opts = self.cleaned_data['options'].split('\n')
	    for opt in opts:
	        self._instance.polloption_set.create(text=opt.strip())

admin.site.register(Event,EventAdmin)

admin.site.register(Classroom)