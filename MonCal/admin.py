from django.contrib import admin
from .models import Schedule,Suresubject,EventSchedule,Event,Working_day,Subject_type,Cycle_type

admin.site.register(Schedule)
admin.site.register(Suresubject)
admin.site.register(EventSchedule)
admin.site.register(Event)
admin.site.register(Working_day)
admin.site.register(Subject_type)
admin.site.register(Cycle_type)