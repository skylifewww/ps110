from django.contrib import admin

# Register your models here.
from .models import Event
admin.site.register(Event)
from .models import Classroom
admin.site.register(Classroom)
from .models import Parent
admin.site.register(Parent)
from .models import Activity
admin.site.register(Activity)
