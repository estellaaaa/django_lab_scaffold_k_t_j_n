
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.contrib import messages
from ..forms import MeetupForm
from ..models import Meetup
from studybuddy_app.common.date import date_from_form
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from ..forms import ResourceForm 


class MeetupListView(LoginRequiredMixin, generic.ListView):
    model = Meetup
    
    def get_queryset(self):
        if self.request.GET.get('meetups') == 'all':
            return Meetup.objects.all()
            
        return Meetup.objects.filter(
            start_time__gte=timezone.now())
    
    def get_context_data(self, **kwargs):
        context = super(MeetupListView, self).get_context_data(**kwargs)
        if self.request.GET.get('meetups') == 'all':
            context['all_meetups'] = True
        return context

    def post(self, request, *args, **kwargs):
        return _create(request)


class MeetupDetailView(LoginRequiredMixin, generic.DetailView):
    model = Meetup

    def get_context_data(self, **kwargs):
        context = super(MeetupDetailView, self).get_context_data(**kwargs)
        meetup = self.get_object()
        participants = meetup.participants.all()
        context['participants'] = participants

        return context

    def post(self, request, *args, **kwargs):
        meetup = self.get_object()
        return _update(request, meetup)


@login_required
def new(request):
    meetup = Meetup()
    meetup_form = MeetupForm(instance=meetup)
    return _render_meetup_form(request, form=meetup_form,  title='Create new', button='Create')

@login_required
def edit(request, pk):
    meetup = get_object_or_404(Meetup, pk=pk)
    meetup_form = MeetupForm(instance=meetup)
    return _render_meetup_form(request, form=meetup_form, pk=pk)


def _render_meetup_form(request, form, pk=None, title='Edit', button='Save'):
    if pk is None:
        action_url = reverse('studybuddy_app:meetup.list')
    else:
        action_url = reverse(
            'studybuddy_app:meetup.detail',
            args=[pk])

    context = {"http_method": 'POST',
               "meetup_form": form,
               "action_url": action_url,
               "title_text": title,
               "button_text": button}
    return render(request, "studybuddy_app/meetup_form.html", context)


def _create(request):
    meetup_form = MeetupForm(request.POST, request.FILES)
    return _save_meetup(request, meetup_form=meetup_form)


def _update(request, meetup):
    meetup_form = MeetupForm(request.POST, instance=meetup)
    return _save_meetup(request, meetup_form=meetup_form, pk=meetup.pk)


def _save_meetup(request, meetup_form, pk=None):
    if not meetup_form.is_valid():
        messages.error(request, 'Error saving form')
        return _render_meetup_form(request, form=meetup_form, pk=pk)
    meetup = meetup_form.save(commit=False)
    meetup.start_time = date_from_form(meetup.start_time)
    meetup.save()
    messages.success(request, ('Your meetup was successfully saved!'))
    url = reverse("studybuddy_app:meetup.detail", args=(meetup.pk,))
    return HttpResponseRedirect(url)


@login_required
def delete(request, pk):
    meetup = get_object_or_404(Meetup, pk=pk)
    meetup.delete()
    return HttpResponseRedirect(
        reverse("studybuddy_app:meetup.list"))


@login_required
def rsvp(request, pk):
    if request.user.is_authenticated:
        meetup = Meetup.objects.get(pk=pk)
        meetup.participants.add(request.user)
    return HttpResponseRedirect(
        reverse("studybuddy_app:meetup.detail",
                args=[meetup.id]))

@login_required
def cancel_participation(request, pk):
    if request.user.is_authenticated:
        meetup = Meetup.objects.get(pk=pk)
        meetup.participants.remove(request.user)
    return HttpResponseRedirect(
        reverse("studybuddy_app:meetup.detail",
                args=[meetup.id]))

@login_required
def resource_edit(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    context = {
        "resource": resource,
        "http_method": 'POST',
        "action_url": reverse('studybuddy_app:resource.detail', args=(pk,)),
        "button_text": 'Save'
    }
    return render(request, "studybuddy_app/resource_form.html", context)
