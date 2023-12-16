from django.db import models
from pytz import timezone


# defining a model of data that will be stored in the database aka. defining the table


class DeviceReadings(models.Model):
    tstz = models.DateTimeField(
        auto_now=True)  # timestamp timezone aka YYYY-MM-DD HH:MM:SS.SSS for then the reading was taken
    deviceId = models.IntegerField()  # ID of the device that took the readings
    waterLevel = models.FloatField()  # level of the water measured from the device

    def __str__(self):
        localTime = self.tstz.astimezone(timezone("Europe/Zagreb"))
        return f"Reading: {self.tstz.date()}:{localTime.time().strftime('%H:%M:%S')}"
