import datetime as dt

from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views import View

from app_aggregator.models import Session


class SessionsList(View):
    def get(self, request):
        # дату по умолчанию берём текущую, город - Белгород
        req_date = request.GET.get('date', dt.date.today().strftime('%Y-%m-%d'))
        req_city = request.GET.get('city', 'Белгород')

        try:
            selected_date = dt.datetime.strptime(req_date, '%Y-%m-%d')
        except ValueError:
            return HttpResponseBadRequest('Invalid date format')

        date_range = (
            selected_date,
            selected_date + dt.timedelta(hours=24)
        )

        queryset = Session.objects.filter(datetime__range=date_range, theater__city=req_city)\
            .order_by('movie_id', 'theater_id', 'datetime')

        # формируем словарь сеансов вида
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

        # собираем список уже начавшихся сеансов
        current_time = dt.datetime.now()
        closed_sessions = []
        for session in queryset:
            if session.datetime < current_time:
                closed_sessions.append(session.id)

        # для селектора дат на неделю вперёд формируем словарь вида {dt.date: bool},
        # где значение элемента словаря - это доступность хотя бы одного сеанса в этот день
        date_range = (
            dt.date.today(),
            dt.date.today() + dt.timedelta(days=7)
        )
        avail_dates = Session.objects.values_list('datetime', flat=True)\
            .filter(datetime__range=date_range, theater__city=req_city)\
            .order_by('datetime')

        avail_dates = set([d.date() for d in avail_dates])
        avail_dates = {d: d in avail_dates for d in [dt.date.today() + dt.timedelta(days=i) for i in range(7)]}

        context = {
            'object_list': objects,
            'closed_sessions': closed_sessions,
            'avail_dates': avail_dates,
            'selected_date': selected_date.date(),
            'selected_city': req_city
        }

        return render(request, 'app_aggregator/sessions_list.html', context=context)
