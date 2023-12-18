from django.contrib import admin
from django.urls import path
from aqua_observer.apps.device_readings import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('readings/', views.readingsList),
    path('readings/<str:dayDate>', views.readingsList),
    path('readingsRange/<str:dateRange>', views.readingsRange),
    path('dailyLatest/', views.getLatestDaily),  # POST method, expects this JSON {"date": YYYY-MM-DD}
    path('userThreshold/', views.userThreshold),
    path('getLatest/', views.lastReading)
]
