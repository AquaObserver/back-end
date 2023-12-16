#for transforming python objects to JSON
from rest_framework import serializers
from .models import DeviceReadings


class ReadingSerializer(serializers.ModelSerializer):
    class Meta:     #metadata describing the model
        model = DeviceReadings
        fields = ['id', 'tstz', 'deviceId', 'waterLevel']