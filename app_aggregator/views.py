import datetime as dt

from django.shortcuts import render
from django.views.generic import TemplateView

from app_aggregator.models import Session


class SessionsList(TemplateView):
    template_name = 'app_aggregator/sessions_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        date_range = (
            dt.date.today() + dt.timedelta(hours=24),
            dt.date.today() + dt.timedelta(hours=48)
        )
        queryset = Session.objects.filter(datetime__range=date_range)\
            .order_by('movie_id', 'theater_id', 'datetime')

        # формируем json вида
        # [{"movie": movie_obj, "theaters": [{"theater": theater_obj, "sessions": [session1_obj, session2_obj]}]}]
        objects = []
        prev_movie_id = None
        prev_theater_id = None
        for session in queryset:
            if session.movie_id != prev_movie_id:
                prev_movie_id = session.movie_id
                prev_theater_id = None
                objects.append({'movie': session.movie, 'theaters': []})

            if session.theater_id != prev_theater_id:
                prev_theater_id = session.theater_id
                objects[-1]['theaters'].append({'theater': session.theater, 'sessions': []})

            objects[-1]['theaters'][-1]['sessions'].append(session)

        context['object_list'] = objects
        return context


