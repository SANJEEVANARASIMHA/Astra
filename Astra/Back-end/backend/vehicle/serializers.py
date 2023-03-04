from rest_framework import serializers
from .models import VehicleTracking


class VehicleTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleTracking
        fields = '__all__'
