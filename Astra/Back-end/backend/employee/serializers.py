from rest_framework import serializers

from .models import EmployeeRegistration, DistanceCalculation, EmployeeHistory

""" Serializer for EmployeeRegistration Model """


class EmployeeRegistrationSerializer(serializers.ModelSerializer):
    # tagid = EmployeeTagSerializer()

    class Meta:
        model = EmployeeRegistration
        fields = "__all__"


""" Serializer for DistanceCalculation Model """


class DistanceCalculationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistanceCalculation
        fields = "__all__"


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class SaveFileSerializer(serializers.Serializer):
    class Meta:
        model = EmployeeRegistration
        fields = "__all__"



class EmpHistorySerializer(serializers.ModelSerializer):
    # tagid = EmployeeTagSerializer()

    class Meta:
        model = EmployeeHistory
        fields = "__all__"




class EmployeeHistorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    x = serializers.FloatField()
    y = serializers.FloatField()
    battery = serializers.FloatField()
    lastseen = serializers.DateTimeField()
