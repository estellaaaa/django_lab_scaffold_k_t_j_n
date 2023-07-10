from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Meetup, MeetupSearch


# admin.site.register(Meetup)

class MeetupAdmin(admin.ModelAdmin):
    # fields = ["location", "title", "start_time", "end_time"]
    
    fieldsets = [
        ("What?", {"fields": ["title", "topic", "course"]}),
        ("When?", {"fields": ["start_time", "duration"]}),
        ("Where?", {"fields": ["location"]}),
    ]
    list_display = ["title", "start_time"]


admin.site.register(Meetup, MeetupAdmin)

admin.site.register(MeetupSearch)

