from rest_framework import serializers

from .models import Alert
from employee.serializers import EmployeeRegistrationSerializer


class AlertSerializer(serializers.ModelSerializer):
    asset = EmployeeRegistrationSerializer()

    class Meta:
        model = Alert
        fields = '__all__'

