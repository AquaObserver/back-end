"""
URL configuration for AquaObserver_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from AquaObserver_api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('readings/', views.readingsList),  #can be GET or POST, GET retrieves all data in DB, POST expects this JSON {"tstz": "YYYY-MM-DDTHH:MM:SS", "deviceId": <integer>, "waterLevel": <float value>}
    path('readings/<str:dayDate>', views.readingsList), #GET; if there is a date specified in URL, like readings/YYYY-MM-DD, then all readings since 00:00:00 till 23:58:00 of that day are retrieved
    path('readingsRange/<str:dateRange>', views.readingsRange), #dateRange should be in format readingsRange/dateStart:dateEnd
    path('dailyLatest/', views.getLatestDaily), # POST method, expects this JSON {"date": YYYY-MM-DD}
    path('userThreshold/', views.userThreshold) #depends on method is it GET or POST, but same route for GET and POST calls, POST body expects this JSON {"thresholdLevel": <float value>}
]
