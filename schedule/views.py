from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import loader
from datetime import datetime, timezone, timedelta
from .models import DailyActivity, MenuEntry, DayOfWeek
import calendar
from django.utils import timezone as dtz

from bisect import bisect_left

zone = timezone(timedelta(hours=-3))
dtz.activate(zone)

datetime_format = '%d-%m-%Y %H:%M'

def detail(request, date):
    print(date)
    now = datetime.strptime(date, datetime_format).astimezone(zone)
    tomorrow = (now + timedelta(days=1)).strftime(datetime_format)
    yesterday = (now - timedelta(days=1)).strftime(datetime_format)
    weekday = calendar.day_name[now.weekday()]
    day_of_week = DayOfWeek.objects.get(name=weekday)
    activity_list = sorted(DailyActivity.objects.filter(day_of_week=day_of_week),
                           key=lambda da: da.time_slot.description)
    tss = [da.time_slot.description for da in activity_list ]
    i = bisect_left(tss, now.strftime('%H:%m'))
    current = tss[i-1] if i > 0 else None
    template = loader.get_template('schedule/index.html')

    context = {
        'today': now.strftime('%d-%m-%Y %H:%m'),
        'day_of_week': day_of_week.name,
        'activity_list': activity_list,
        'current': current,
        'tomorrow': tomorrow,
        'yesterday': yesterday
    }
    return HttpResponse(template.render(context, request))


def index(request):
    now = dtz.now().astimezone(zone).strftime(datetime_format)
    return detail(request, now)

    # dtz.activate(zone)
    # now = dtz.now().astimezone(zone)
    # weekday = calendar.day_name[datetime.today().weekday()]
    # day_of_week = DayOfWeek.objects.get(name=weekday)
    # activity_list = sorted(DailyActivity.objects.filter(day_of_week=day_of_week),
    #                        key=lambda da: da.time_slot.description)
    # tss = [da.time_slot.description for da in activity_list ]
    # i = bisect_left(tss, now.strftime('%H:%m'))
    # current = tss[i-1] if i > 0 else None
    # template = loader.get_template('schedule/index.html')
    #
    # context = {
    #     'today': now.strftime('%d-%m-%Y %H:%m'),
    #     'day_of_week': day_of_week.name,
    #     'activity_list': activity_list,
    #     'current': current
    # }
    # return HttpResponse(template.render(context, request))
