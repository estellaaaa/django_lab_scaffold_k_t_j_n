from django.views import generic

from studybuddy_app.models import MeetupSearch

class MeetupSearchDetailView(generic.DetailView):
    model = MeetupSearch
    template_name = 'studybuddy_app/meetupsearch_detail.html'
    context_object_name = 'meetup'
