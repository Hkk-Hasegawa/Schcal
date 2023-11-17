from django.contrib import admin

from .models import Schedule,Suresubject,Person,Cycle,Excludeday

admin.site.register(Schedule)
admin.site.register(Suresubject)
admin.site.register(Person)
admin.site.register(Cycle)
admin.site.register(Excludeday)