from django.contrib import admin

from aqua_observer.broker import client
from .models import DeviceReadings, UserThreshold, DeviceToken


class DeviceReadingsAdmin(admin.ModelAdmin):

    # Define your custom action function
    def custom_action(self, request, queryset):
        client.publish("aqua1/calibrate")

    custom_action.short_description = "Custom Action"  # Action name displayed in the dropdown
    actions = ['custom_action']


admin.site.register(DeviceReadings, DeviceReadingsAdmin)
admin.site.register(UserThreshold)
admin.site.register(DeviceToken)