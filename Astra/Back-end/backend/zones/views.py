from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import datetime
from .models import Zones, ZoneTracking, WeeklyZoneTracking, MonthlyZoneTracking
from .serializers import ZoneSerializer, ZoneTrackingSerializer, WeeklyZoneTrackingSerializer
from common.models import FloorMap

""" API for MasterGateway """


class ZoneAPI(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    """ POST method to store new tag """

    @staticmethod
    def post(request):
        try:
            var = Zones()
            var.floor = FloorMap.objects.get(id=request.data.get("id"))
            var.zonename = request.data.get("zonename")
            var.x1 = request.data.get("x1")
            var.y1 = request.data.get("y1")
            var.x2 = request.data.get("x2")
            var.y2 = request.data.get("y2")
            var.save()
            # logger.info("Error:- " + str(request) + " " + str(request.data.get("zonename")) + "Registered Suceessfully")
            return Response(status=status.HTTP_201_CREATED)

        except Exception as err:
            # logger.info("Error:- " + str(request) + " " + str(err))
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

    """ GET method to retrieve all details """

    @staticmethod
    def get(request):
        try:
            data = Zones.objects.filter(floor=request.GET.get("floorid"))
            if data:
                ser = ZoneSerializer(data, many=True)
                return Response(ser.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        except Exception as err:
            # logger.info("Error:- " + str(request) + " " + str(err))
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

    """ DELETE method to delete particular record based on floor and zone """

    @staticmethod
    def delete(request):
        try:
            data = Zones.objects.filter(floor=request.data.get(
                "floorid"), zonename=request.data.get("zonename"))
            if data:
                data.delete()
                # logger.info("Error:- " + str(request) + " " + str(request.data.get("zonename")) + "UnRegistered
                # Suceessfully")
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            # logger.info("Error:- " + str(request) + " " + str(err))
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)


""" API for ZoneTracking """


class ZoneTrackingAPI(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    """ POST method to retrieve all details """

    @staticmethod
    def post(request):
        try:
            zone = Zones.objects.filter(floor=request.data.get(
                "floorid"), zonename=request.data.get("zonename")).first()
            print(zone.id, ".....................")
            # data = ZoneTracking.objects.raw(
            #     "select id, substr(temp.timestamp,12,5) as timestamp, count(*) as count from (select * from zones_zonetracking where zoneid_id = " + str(
            #         zone.id) + " group by DATE(timestamp),HOUR(timestamp),MINUTE(timestamp), tagid_id,zoneid_id) as temp group by DATE(temp.timestamp),HOUR(temp.timestamp),MINUTE(temp.timestamp)")
            # print(data)
            data = ZoneTracking.objects.raw(
                "select id, temp.timestamp as timestamp, count(*) as count from (select * from zones_zonetracking where timestamp >= CURDATE() and zoneid_id = " + str(
                    zone.id) + " group by DATE(timestamp),HOUR(timestamp),MINUTE(timestamp), tagid_id,zoneid_id) as temp group by DATE(temp.timestamp),HOUR(temp.timestamp),MINUTE(temp.timestamp)")
            print(data)

            if data:
                print(data, "++++++++++++++++++++++")
                ser = ZoneTrackingSerializer(data, many=True)
                return Response(ser.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        except Exception as err:
            # logger.info("Error:- " + str(request) + " " + str(err))
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)


""" API for WeeklyZoneTracking """


class WeeklyZoneTrackingAPI(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    """ POST method to retrieve all details """

    @staticmethod
    def post(request):
        try:
            endDate = datetime.datetime.today()
            startDate = endDate - datetime.timedelta(days=7)
            zone = Zones.objects.filter(floor=request.data.get(
                "floorid"), zonename=request.data.get("zonename")).first()
            data = WeeklyZoneTracking.objects.filter(
                zoneid=zone, timestamp__gte=startDate, timestamp__lte=endDate)
            if data:
                ser = WeeklyZoneTrackingSerializer(data, many=True)
                return Response(ser.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        except Exception as err:
            print(err)
            # logger.info("Error:- " + str(request) + " " + str(err))
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)


""" API for MonthlyZoneTracking """


class MonthlyZoneTrackingAPI(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    """ POST method to get all data"""

    @staticmethod
    def post(request):
        try:
            currentDate = datetime.date.today()
            month = currentDate.month
            year = currentDate.year
            if month < 10:
                month = "0" + str(month)
            dt = str(year) + "-" + str(month)
            zone = Zones.objects.filter(floor=request.data.get(
                "floorid"), zonename=request.data.get("zonename")).first()
            data = MonthlyZoneTracking.objects.filter(
                zoneid=zone, timestamp__startswith=dt)
            if data:
                ser = WeeklyZoneTrackingSerializer(data, many=True)
                return Response(ser.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            # logger.info("Error:- " + str(request) + " " + str(err))
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
#
