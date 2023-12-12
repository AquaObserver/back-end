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
def readingsList(request, dayDate = None):
    #front-end is retreiving data
    if request.method == 'GET':
        if (dayDate is not None):
            dataJSON = {
                "data":[]
            }
            try:
                readingsOfTheDay = DeviceReadings.objects.filter(Q(tstz__startswith=dayDate))
                serializer = ReadingSerializer(readingsOfTheDay, many = True)
            except:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            for d in serializer.data:
                dData = dict(d.items())
                extractedTime = dData.get('tstz').split('T')[1].split('+')[0]    #gets the time from string that represents DateTime object
                dataJSON["data"].append({"time": extractedTime, "waterLevel": dData.get('waterLevel')})
            #print(dataJSON)
            return JsonResponse(dataJSON)
        else:
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
        requestedDate = json.loads(request.body).get('date')    #from JSON get value from filed "date":
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
        

def readingsRange(request, dateRange):
    if (request.method == 'GET'):
        #print(dateRange)
        dateStart = dateRange.split(':')[0]
        dateEnd = dateRange.split(':')[1]
        print("QUErYYYY:", DeviceReadings.objects.filter(Q(tstz__range=(dateStart, dateEnd))).query)
        readingsInRange = DeviceReadings.objects.filter(Q(tstz__range=(dateStart, dateEnd)))
        serializer = ReadingSerializer(readingsInRange, many=True)
        print("DATAAAAA: ", serializer.data)