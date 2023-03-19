from django.db import models


# Create your models here.

class TimeSlot(models.Model):
    description = models.CharField(max_length=255)
    lunch_time_slot = models.BooleanField()

    def __str__(self):
        return self.description


class DayOfWeek(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class DailyActivity(models.Model):
    day_of_week = models.ForeignKey(DayOfWeek, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    description = models.CharField(max_length=1500)

    def __str__(self):
        return '{} at {}: {}'.format(str(self.day_of_week), str(self.time_slot), self.description)


class MenuEntry(models.Model):
    entry_date = models.DateField('date of the entry')
    entry_time = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    entry = models.CharField(max_length=1500)

    def __str__(self):
        return f'{self.entry_date.isoformat()} - {self.entry_time.description}: {self.entry}'
