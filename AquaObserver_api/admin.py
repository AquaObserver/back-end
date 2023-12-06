from django.contrib import admin
from .models import DeviceReadings
from .models import UserThreshold

admin.site.register(DeviceReadings)
admin.site.register(UserThreshold)