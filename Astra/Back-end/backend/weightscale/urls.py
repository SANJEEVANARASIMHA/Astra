from django.urls import path

from . import views

app_name = 'sensor'
urlpatterns = [
    # path('sensor/report', views.SensorReadingView.as_view()),
    path('sensor/report', views.SensorsAPIView.as_view()),
    # path('report/graph', views.SensorGraphAPI.as_view()),
    path('report/graph', views.NewSensorGraphAPI.as_view()),
    # path('weight/sensor/graph', views.NewSensorGraphAPI.as_view())
]

