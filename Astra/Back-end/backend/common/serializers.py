from rest_framework import serializers

from .models import FloorMap

""" Serializer to serialize data of FloorMap model """
class FloorMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloorMap
        fields = '__all__'
