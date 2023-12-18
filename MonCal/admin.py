from django.contrib import admin
from .models import Booking_time,Suresubject,Event,Working_day,Subject_type,Cycle_type,Pause_type,Cycle_pause,Room

admin.site.register(Booking_time)
admin.site.register(Suresubject)
admin.site.register(Event)
admin.site.register(Working_day)
admin.site.register(Cycle_type)
admin.site.register(Cycle_pause)
admin.site.register(Pause_type)
admin.site.register(Subject_type)
admin.site.register(Room)