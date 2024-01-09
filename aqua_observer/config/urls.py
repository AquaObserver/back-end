from django.contrib import admin
from django.urls import path, include
from aqua_observer.apps.device_readings import views
import aqua_observer.broker as br

urlpatterns = [
    path('readings/', views.readingsList),
    path('readings/<str:dayDate>', views.readingsList),
    path('readingsRange/<str:dateRange>', views.readingsRange),
    path('dailyLatest/', views.getLatestDaily),  # POST method, expects this JSON {"date": YYYY-MM-DD}
    path('userThreshold/', views.userThreshold),
    path('getLatest/', views.lastReading),
    path('registerDevice/', views.registerDevice),
    path('calibrate/', views.startCalibration),
    path('test/', views.notifyDevices),
    path(r'jet/', include('jet.urls', 'jet')),
    path(r'jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('admin/', admin.site.urls),
]
