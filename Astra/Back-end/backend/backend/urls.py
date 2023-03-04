from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path(r'api/', include('common.urls')),
    path(r'api/', include('gateway.urls')),    
    path(r'api/', include('sensor.urls')),
    path(r'api/', include('signalrepeator.urls')),
    path(r'api/', include('employee.urls')),
    path(r'api/', include('alert.urls')),
    path(r'api/', include('zones.urls')),
    path(r'api/', include('vehicle.urls')),
    path(r'api/', include('energy.urls')),
    path(r'api/', include('weightscale.urls')),
    #path(r'api/', include('attendance.urls')),
    path('admin/', admin.site.urls),
]






