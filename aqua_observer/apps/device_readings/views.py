# for defining endpoints

import datetime
import json
import os

from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import DeviceReadings, UserThreshold, DeviceToken
from .serializers import ReadingSerializer, DeviceTokenSerializer

import requests
import google.auth.transport.requests
from google.oauth2 import service_account

# increments dateEnd so that the last day is also captured in a range ie. 2023-12-04 - 2023-12-06 (returns all data for 2023-12-06 till 23:59:59)
@csrf_exempt
def fixDBDateInterpretation(date):
    tempStart = date.split(':')[0]
    tempEnd = date.split(':')[1] + 'T23:59:59'
    dateObjStart = datetime.date.fromisoformat(tempStart)
    dateObjEnd = datetime.datetime.strptime(tempEnd, '%Y-%m-%dT%H:%M:%S')
    return [str(dateObjStart), str(dateObjEnd)]


# MWLD = Mean Water Level per Day
@csrf_exempt
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

@csrf_exempt
def _get_access_token():
    credentials = service_account.Credentials.from_service_account_file('firebase_config.json',
        scopes=[
            'https://www.googleapis.com/auth/firebase.messaging'
        ]
    )
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    return credentials.token

@csrf_exempt
def _send_notification_new_api(deviceToken: str, title: str = "Upozorenje", msg: str = "Dosegnuta kritična razina"):
    token = _get_access_token()
    url = 'https://fcm.googleapis.com/v1/projects/aquaobserver-49185/messages:send'
    headers = {
        'Authorization': 'Bearer ' + token,
    }
    body = {
        "message": {
            "token": deviceToken,
            "notification": {
                "body": msg,
                "title": title
            }
        }
    }
    response = requests.post(url, headers=headers, json=body)
    return response.json()

@csrf_exempt
def notifyDevices():
    getTokens = DeviceToken.objects.all()
    serializer = DeviceTokenSerializer(getTokens, many=True)
    for sd in serializer.data:
        _send_notification_new_api(str(dict(sd.items()).get('dToken')))

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
                extractedTime = dData.get('tstz').split('T')[1].split('+')[0]  # gets the time from string that represents DateTime object
                dataJSON["data"].append({"time": extractedTime, "waterLevel": dData.get('waterLevel')})
            return JsonResponse(dataJSON)
        else:
            retrievedReadings = DeviceReadings.objects.all()
            serializer = ReadingSerializer(retrievedReadings, many=True)
            return JsonResponse({"readings": serializer.data})
    # hardware is sending data
    if request.method == 'POST':
        serializer = ReadingSerializer(data=request.data)
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
@csrf_exempt
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

@csrf_exempt
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

@csrf_exempt
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
    
@api_view(['POST'])
@csrf_exempt
def registerDevice(request):
    req_token = json.loads(request.body).get('token')
    if (request.method == "POST"):
        print("QUERY: ", DeviceToken.objects.filter(Q(dToken=req_token)).query)
        doesExist = DeviceToken.objects.filter(Q(dToken=req_token))
        print("BLBALABLLBA: ", doesExist)
        if len(doesExist) > 0:
            if doesExist[0].dToken != req_token:
                tokenObject = DeviceToken.objects.create(dToken=req_token)
                tokenObject.save()
                return Response({"msg": "Token added"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"msg": "Token already exists"}, status=status.HTTP_302_FOUND)
        else:
            # The queryset is empty, create a new record
            tokenObject = DeviceToken.objects.create(dToken=req_token)
            tokenObject.save()
            return Response({"msg": "Token added"}, status=status.HTTP_201_CREATED)


