from rest_framework import serializers

from .models import Zones, ZoneTracking, WeeklyZoneTracking

""" Serializer for Zones Model """


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zones
        fields = "__all__"


""" Serializer for ZoneTracking Model """


class ZoneTrackingSerializer(serializers.Serializer):
    timestamp = serializers.CharField()
    count = serializers.IntegerField()


""" Serializer for Monthly and WeeklyTrackingData """


class WeeklyZoneTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyZoneTracking
        fields = "__all__"
