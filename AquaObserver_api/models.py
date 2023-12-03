from django.db import models

#defining a model of data that will be stored in the database aka. defining the table
class DeviceReadings(models.Model):
    # no need to ad entry ID, it is added automaticaly
    tstz = models.DateTimeField()       #timestamp timezone aka. YYYY-MM-DD HH:MM:SS.SSS for then the reading was taken
    deviceId = models.IntegerField()    #ID of the device that took the readings
    waterLevel = models.FloatField()    #level of the water measured from the device