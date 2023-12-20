from datetime import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from pytz import timezone

class DeviceReadings(models.Model):
    tstz = models.DateTimeField(default=datetime.now)
    deviceId = models.IntegerField()
    waterLevel = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        localTime = self.tstz.astimezone(timezone("Europe/Zagreb"))
        return f"Reading: {self.tstz.date()}:{localTime.time().strftime('%H:%M:%S')}"


class UserThreshold(models.Model):
    thresholdLevel = models.IntegerField(default=10, validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return f"Threshold: {self.thresholdLevel}%"

class DeviceToken(models.Model):
    dToken = models.CharField(max_length = 200)

    def __str__(self):
        return f"Token: {self.dToken[0:10]}"


@receiver(post_save, sender=UserThreshold)
def user_threshold_post_save(sender, instance, created, **kwargs):
    from aqua_observer.broker import client
    client.publish("aqua1/critLvl", int(instance.thresholdLevel))

@receiver(post_save, sender=DeviceReadings)
def device_readings_post_save(sender, instance, created, **kwargs):
    #get treshold value if instance > treshold make post request to server
    threshold = UserThreshold.objects.get(id=1)
    from .views import notifyDevices
    if instance.waterLevel < threshold.thresholdLevel:
        notifyDevices()
        print("Water level is critical!")
        #request = requests.post('http://localhost:8000/api/notifications/', data={'message': 'Water level is critical!'})
        #print(request.text)