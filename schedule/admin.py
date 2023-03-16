from django.contrib import admin
from .models import TimeSlot, DailyActivity, MenuEntry

# Register your models here.
admin.site.register(TimeSlot)
admin.site.register(DailyActivity)
admin.site.register(MenuEntry)
