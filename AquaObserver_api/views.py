#for defining endpoints

import datetime
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

#increments dateEnd so that the last day is also captured in a range ie. 2023-12-04 - 2023-12-06 (returns data for 2023-12-06)
def fixDBDateInterpretation(date):
    tempStart = date.split(':')[0]
    tempEnd = date.split(':')[1]
    dateObjStart = datetime.date.fromisoformat(tempStart)
    dateObjEnd = datetime.date.fromisoformat(tempEnd)
    return [str(dateObjStart), str(dateObjEnd + datetime.timedelta(days=1))]

#MWLD = Mean Water Level per Day
def calculateMWLD(serializedData):
    meanValue = dict()
    #populate dict with dates as keys and mean values of each day
    for sD in serializedData:   # goes through list of records and adds distinct date as a key in dictionary
        dateAsKey = dict(sD.items()).get('tstz').split('T')[0]
        if dateAsKey not in list(meanValue.keys()):
            tempValue = 0
            countedValues = 0
            for subData in serializedData:  #for each entry with same date as current key, calculate mean waterLevel for current date
                sameDate = dict(subData.items()).get('tstz').split('T')[0]
                if sameDate == dateAsKey:
                    tempValue += float(dict(subData.items()).get('waterLevel'))
                    countedValues += 1
            meanValue[str(dateAsKey)] = tempValue/countedValues
    return meanValue


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
    dataJSON = {"data":[]}
    if (request.method == 'GET'):
        dates = fixDBDateInterpretation(dateRange)
        dateStart = dates[0]
        dateEnd = dates[1]
        readingsInRange = DeviceReadings.objects.filter(Q(tstz__range=(dateStart, dateEnd)))
        serializer = ReadingSerializer(readingsInRange, many=True)
        calculatedvalues = calculateMWLD(serializer.data) 
        for dateKey in calculatedvalues.keys():
            dataJSON["data"].append({"date": dateKey, "meanValue": calculatedvalues.get(dateKey)})
        return JsonResponse(dataJSON)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)