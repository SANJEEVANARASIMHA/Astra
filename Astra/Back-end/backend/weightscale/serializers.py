from rest_framework import serializers

from weightscale.models import SensorReading, Sensors


class SensorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensors
        fields = ['id', 'tagid']


class SensorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensors
        fields = ['id','timestamp', 'currentDiff', 'battery']