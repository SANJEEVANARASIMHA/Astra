from django.urls import path
from . import views


urlpatterns = [
    path('vehicle/tracking', views.VehicleTRackingAPI.as_view())
]