from django.views import generic

from studybuddy_app.models import MeetupSearch

class MeetupSearchListView(generic.ListView):
    model = MeetupSearch
    template_name = 'studybuddy_app/meetupsearch_list.html'
    context_object_name = 'meetup_list'
