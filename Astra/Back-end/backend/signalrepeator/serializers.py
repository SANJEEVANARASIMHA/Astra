from rest_framework import serializers

from .models import SignalRepeator


""" Serializer for SignalRepeator Model """
class SignalRepeatorSerializer(serializers.ModelSerializer):    
    class Meta:
        model = SignalRepeator
        fields = "__all__"
