# for defining endpoints

import datetime
import json

from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import DeviceReadings
from .models import UserThreshold
from .serializers import ReadingSerializer


# increments dateEnd so that the last day is also captured in a range ie. 2023-12-04 - 2023-12-06 (returns all data for 2023-12-06 till 23:59:59)
def fixDBDateInterpretation(date):
    tempStart = date.split(':')[0]
    tempEnd = date.split(':')[1] + 'T23:59:59'
    dateObjStart = datetime.date.fromisoformat(tempStart)
    dateObjEnd = datetime.datetime.strptime(tempEnd, '%Y-%m-%dT%H:%M:%S')
    return [str(dateObjStart), str(dateObjEnd)]


# MWLD = Mean Water Level per Day
def calculateMWLD(serializedData):
    meanValue = dict()
    # populate dict with dates as keys and mean values of each day
    for sD in serializedData:  # goes through list of records and adds distinct date as a key in dictionary
        dateAsKey = dict(sD.items()).get('tstz').split('T')[0]
        if dateAsKey not in list(meanValue.keys()):
            tempValue = 0
            countedValues = 0
            for subData in serializedData:  # for each entry with same date as current key, calculate mean waterLevel for current date
                sameDate = dict(subData.items()).get('tstz').split('T')[0]
                if sameDate == dateAsKey:
                    tempValue += float(dict(subData.items()).get('waterLevel'))
                    countedValues += 1
            meanValue[str(dateAsKey)] = tempValue / countedValues
    return meanValue


# defined readings endpoint aka readings/
@api_view(['GET', 'POST'])
def readingsList(request, dayDate=None):
    # front-end is retreiving data
    if request.method == 'GET':
        if (dayDate is not None):
            dataJSON = {
                "data": []
            }
            try:
                readingsOfTheDay = DeviceReadings.objects.filter(Q(tstz__startswith=dayDate))
                serializer = ReadingSerializer(readingsOfTheDay, many=True)
            except:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            for d in serializer.data:
                dData = dict(d.items())
                extractedTime = dData.get('tstz').split('T')[1].split('+')[
                    0]  # gets the time from string that represents DateTime object
                dataJSON["data"].append({"time": extractedTime, "waterLevel": dData.get('waterLevel')})
            # print(dataJSON)
            return JsonResponse(dataJSON)
        else:
            # get all the readings
            retrievedReadings = DeviceReadings.objects.all()
            # serialize readings
            serializer = ReadingSerializer(retrievedReadings, many=True)
            # return json
            return JsonResponse({"readings": serializer.data})
    # hardware is sending data
    if request.method == 'POST':
        print("NOW:", datetime.datetime.now())
        serializer = ReadingSerializer(data=request.data)
        #print("Serializer DATA: ", serializer)
        if serializer.is_valid():
            serializer.save()  # saves it to the DB
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# define latest daily reading endpoint aka dailyLatest/
@csrf_exempt
def getLatestDaily(request):
    if request.method == 'POST':
        requestedDate = json.loads(request.body).get('date')  # from JSON get value from filed "date":
        try:
            lastReading = DeviceReadings.objects.filter(Q(tstz__startswith=requestedDate)).latest(
                'tstz')  # would translate to query: Select * from DeviceReadings where tstz like "<requestedDate>%" and gets the latest reading
        except DeviceReadings.DoesNotExist:
            return JsonResponse({"waterLevel": -1})  # in case there is no record in database
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({"waterLevel": lastReading.waterLevel})


# defined userThreshold endpoint aka userThreshold/
@api_view(['GET', 'POST'])
def userThreshold(request):  # gets the application defined userThreshold
    if request.method == 'GET':
        try:
            rData = UserThreshold.objects.get()
        except UserThreshold.DoesNotExist:
            return JsonResponse({"threshold": -1})
        return JsonResponse({"threshold": rData.thresholdLevel})

    if request.method == 'POST':  # updates the application userThreshold
        newThrasholdValue = json.loads(request.body).get('thresholdLevel')
        try:
            rData = UserThreshold.objects.get()
        except UserThreshold.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)
        rData.thresholdLevel = newThrasholdValue
        rData.save()
        return Response(rData.thresholdLevel, status=status.HTTP_200_OK)


def readingsRange(request, dateRange):
    dataJSON = {"data": []}
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


def lastReading(request):
    if (request.method == 'GET'):
        try:
            lastCreatedReading = DeviceReadings.objects.last()
            serializer = ReadingSerializer(lastCreatedReading)
        except DeviceReadings.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return JsonResponse(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
