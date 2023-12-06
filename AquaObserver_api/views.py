#for defining endpoints
import json
from django.db.models import Q
from django.http import JsonResponse
from .models import DeviceReadings
from .models import UserThreshold
from .serializers import ReadingSerializer
from .serializers import ThresholdSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

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

#define latest daily reading endpoint aka dailyLatest/
@csrf_exempt
def getLatestDaily(request):
    if request.method == 'POST':
        requestedDate = json.loads(request.body).get('date')    #from JSON get value from filed "data":
        try:
            lastReading = DeviceReadings.objects.filter(Q(tstz__startswith=requestedDate)).latest('tstz')   #would translate to query: Select * from DeviceReadings where tstz like "<requestedDate>%" and gets the latest reading
        except DeviceReadings.DoesNotExist:
            return JsonResponse({"waterLevel": -1}) #in case there is no record in database
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({"waterLevel": lastReading.waterLevel})

#defined userThreshold endpoint aka userThreshold/ or userThreshold/<int:userID>
@api_view(['GET', 'POST', 'PUT'])
def userThreshold(request, userID=None):
    if request.method == 'GET':
        try:
            user = UserThreshold.objects.get(userId=userID)
        except UserThreshold.DoesNotExist:
            return JsonResponse({"user": None, "threshold": -1})
        return JsonResponse({"user": user.userId, "threshold": user.thresholdLevel})

    if request.method == 'POST':
        serializer = ThresholdSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    if request.method == 'PUT':
        try:
            user = UserThreshold.objects.get(userId=userID)
            user.delete()
        except UserThreshold.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = ThresholdSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)