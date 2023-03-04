from rest_framework import serializers

from energy.models import EnergyTracking, PassiveAsset, VehicleTracking


class EnergySerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergyTracking
        fields = "__all__"


class PassiveAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassiveAsset
        fields = "__all__"


class VehicleTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleTracking
        fields = "__all__"


class ParkingSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    tag = serializers.CharField(max_length=200)
