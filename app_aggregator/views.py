import datetime as dt

from django.shortcuts import render
from django.utils.timezone import make_aware
from django.views.generic import ListView

from app_aggregator.models import Session


class SessionsList(ListView):
    model = Session
    template_name = 'app_aggregator/sessions_list.html'
    queryset = Session.objects.filter(
        datetime__range=(dt.date.today() + dt.timedelta(hours=24), dt.date.today() + dt.timedelta(hours=48)))\
        .order_by('movie_id', 'theater_id', 'datetime')
