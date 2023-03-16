# Generated by Django 4.1.7 on 2023-02-23 19:17

from django.db import migrations
import calendar

all_ts = ['13:00', '13:40', '14:20', '14:40', '15:00', '15:40', '16:20', '17:00', '17:10', '18:00', '19:00/20:00']


def insert_custom_activities(apps, _):
    DayOfWeek = apps.get_model('schedule', 'DayOfWeek')
    TimeSlot = apps.get_model('schedule', 'TimeSlot')
    DailyActivity = apps.get_model('schedule', 'DailyActivity')
    ts0 = TimeSlot.objects.get(description='15:00')
    ts1 = TimeSlot.objects.get(description='15:40')
    ts2 = TimeSlot.objects.get(description='16:20')

    mon, tue, wed, thu, fri = [DayOfWeek.objects.get(name=d) for d in calendar.day_name[:5]]

    for dow in DayOfWeek.objects.all():
        DailyActivity(day_of_week=dow, time_slot=ts1, description='Ativ. Pedag.').save()

    DailyActivity(day_of_week=mon, time_slot=ts0, description='Ed. Fisica').save()
    DailyActivity(day_of_week=mon, time_slot=ts2, description='Ingles').save()
    DailyActivity(day_of_week=wed, time_slot=ts0, description='Ed. Fisica').save()
    DailyActivity(day_of_week=wed, time_slot=ts2, description='Ingles').save()

    DailyActivity(day_of_week=tue, time_slot=ts0, description='Jogos').save()
    DailyActivity(day_of_week=tue, time_slot=ts2, description='Japones').save()

    DailyActivity(day_of_week=thu, time_slot=ts0, description='Musica').save()
    DailyActivity(day_of_week=thu, time_slot=ts2, description='Japones').save()

    DailyActivity(day_of_week=fri, time_slot=ts0, description='Exp. Corporal').save()
    DailyActivity(day_of_week=fri, time_slot=ts2, description='Artes').save()


class Migration(migrations.Migration):
    dependencies = [
        ('schedule', '0002_auto_20230223_1227'),
    ]

    operations = [
        migrations.RunPython(insert_custom_activities),
    ]
