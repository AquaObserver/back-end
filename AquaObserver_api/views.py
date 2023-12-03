#for defining endpoints

from django.http import JsonResponse
from .models import DeviceReadings
from .serializers import ReadingSerializer

#defined readings endpoint aka /readings/
def readingsList(request):
    #get all the readings
    retrievedReadings = DeviceReadings.objects.all()
    #serialize readings
    serializer = ReadingSerializer(retrievedReadings, many=True)
    #return json
    return JsonResponse({"readings": serializer.data})