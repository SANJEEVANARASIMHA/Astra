from django.urls import path
from . import views

app_name = 'energy'

urlpatterns = [
    path('energy', views.EnergyAPIView.as_view(), name='energy'),
    path('parking', views.VehicleTrackingAPIView.as_view(), name='vehicle'),
    path('passive/asset', views.PassiveAssetAPIView.as_view(), name='passive/asset'),

]
