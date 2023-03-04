from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .models import VehicleTracking
from .serializers import VehicleTrackingSerializer


class VehicleTRackingAPI(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        try:
            data = VehicleTracking.objects.all().order_by('-id').first()
            serializer = VehicleTrackingSerializer(data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def post(request):
        try:
            vehlid = request.data.get("vehicleid")
            data = VehicleTracking.objects.filter(vehicleid=vehlid)
            serializer = VehicleTrackingSerializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(status=status.HTTP_400_BAD_REQUEST)
