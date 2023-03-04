import datetime
from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from energy.models import EnergyTracking, PassiveAsset, VehicleTracking
from energy.serializers import EnergySerializer, PassiveAssetSerializer, VehicleTrackingSerializer, ParkingSerializer


# Create your views here.
class EnergyAPIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """ This GET Request is used to get the Energy tag details only single tag with updated data"""
        try:
            object = EnergyTracking.objects.all().last()
            serializer = EnergySerializer(object, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({"energy": str(err)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """ This POST Request is used to get the Perticular key data and its needed two parameters
            1.column(for which parameter you need a data that parameters has to send as a column)
            2. mac(it is a macaddress of the energyTag)
        """
        try:
            currentDate = datetime.datetime.now().date()
            column = request.data.get('column')
            mac = request.data.get('mac')
            print(mac, column)
            if column and mac:
                print("if confition is true")
                sensors = EnergyTracking.objects.filter(tag=mac, timestamp__startswith=currentDate).values(column,
                                                                                                          'timestamp')
                print("length ", len(sensors))
                if sensors:
                    print("indie senodrdss")
                    data = list(sensors)
                    if data:
                        return Response(data, status=status.HTTP_200_OK)
                    else:
                        return Response([], status=status.HTTP_200_OK)
                else:
                    return Response([], status=status.HTTP_200_OK)
            else:
                return Response({"message": "please provide the mac and column"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)


class VehicleTrackingAPIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """ This GET request is used to get the VehicleTracking Either it is in a status of parked or unparked"""
        try:
            # objects = VehicleTracking.objects.raw('select id, tag, max(timestamp) as timestamp from energy_vehicletracking where timestamp>=CURDATE() group by tag')
            tags = VehicleTracking.objects.raw('select distinct(tag), id from energy_vehicletracking group by tag order by tag')
            parkTags = ParkingSerializer(tags, many=True)
            payload = []
            for row in parkTags.data:
                # print(row['tag'])
                object = VehicleTracking.objects.filter(tag=row['tag']).last()
                serializer = VehicleTrackingSerializer(object)
                payload.append(serializer.data)
            # payload1 = [
            #     {
            #         "id": 7,
            #         "tag": "5a-c2-15-11-00-16",
            #         "vehicle_status": True,
            #         "timestamp": "2022-11-08T16:58:26.930090"
            #     },
            #     {
            #         "id": 8,
            #         "tag": "5a-c2-15-11-00-15",
            #         "vehicle_status": False,
            #         "timestamp": "2022-11-08T16:58:26.930090"
            #     },
            # ]
            return Response(payload, status=status.HTTP_200_OK)

        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)


class PassiveAssetAPIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """ It is used to get the data of an passive Asset """
        try:
            currentDate = datetime.datetime.now().date()
            objects = PassiveAsset.objects.filter(timestamp__startswith=currentDate).order_by('-timestamp')
            serializer = PassiveAssetSerializer(objects, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            return Response(status.HTTP_200_OK)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

