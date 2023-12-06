#for defining endpoints

from django.http import JsonResponse
from .models import DeviceReadings
from .serializers import ReadingSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

#defined readings endpoint aka readings/
@api_view(['GET','POST'])
def readingsList(request):

    #front-end is retreiving data
    if request.method == 'GET':
        #get all the readings
        retrievedReadings = DeviceReadings.objects.all()
        #serialize readings
        serializer = ReadingSerializer(retrievedReadings, many=True)
        #return json
        return JsonResponse({"readings": serializer.data})
    #hardware is sending data
    if request.method == 'POST':
        serializer = ReadingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()       #saves it to the DB
            return Response(serializer.data, status=status.HTTP_201_CREATED)

#define daily readings endpoint aka daily/
def getDailyValues(request):
    return