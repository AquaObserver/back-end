from django.contrib import admin
from django.urls import path
from aqua_observer.apps.device_readings import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('readings/', views.readingsList),
]
