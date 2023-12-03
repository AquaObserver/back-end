#for defining endpoints

from django.http import JsonResponse
from .models import DeviceReadings
from .serializers import ReadingSerializer

#defined readings endpoint aka. /readings
def readings(request):
    #get all the readings
    readingsList = DeviceReadings.objects.all()
    #serialize readings
    serializer = ReadingSerializer(readingsList, many=True)
    #return json
    return JsonResponse(serializer.data)