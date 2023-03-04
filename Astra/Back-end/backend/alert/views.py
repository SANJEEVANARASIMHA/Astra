import datetime
import json

from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# from apilogger import logger
from common.models import FloorMap
from employee.models import EmployeeRegistration
from .models import Alert
from .serializers import AlertSerializer


class Alerts(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        try:
            currentDate = datetime.date.today().strftime("%Y-%m-%d")
            floor_id = request.data.get('floor')

            if floor_id:
                floor = FloorMap.objects.filter(id=floor_id).first()
                # alerts = Alert.objects.filter(value__gt=0)
                alerts = Alert.objects.filter(timestamp__startswith=currentDate, floor=floor, value__gt=0)
                alertSerializer = AlertSerializer(alerts, many=True)
                return Response(alertSerializer.data, status=status.HTTP_200_OK)
            else:
                return Response([], status=status.HTTP_200_OK)
        except Exception as err:
            # logger.info("Error:-  "+str(request) + str(err))
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def post(request):
        try:
            value = request.data.get('value')
            currentDate = datetime.date.today().strftime("%Y-%m-%d")
            if value:
                alerts = Alert.objects.filter(value=value).order_by('-lastseen')
                # alerts = Alert.objects.filter(timestamp__startswith=currentDate,value=value).order_by('-lastseen')
                if alerts[:100]:
                    alertSerializer = AlertSerializer(alerts, many=True)
                    return Response(alertSerializer.data, status=status.HTTP_200_OK)
                else:
                    return Response([], status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"message": "please provide alert value"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as err:
            # logger.info("Error:-  "+str(request) + str(err))
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)


class AlertPanicApi(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        try:
            assetPayload = []
            startTime = datetime.datetime.today() - datetime.timedelta(minutes=2)
            endTime = datetime.datetime.today()
            floor_id = request.GET.get('floor')
            # print("---------", startTime, endTime)
            if floor_id:
                floor = FloorMap.objects.filter(id=floor_id).first()
                if floor:
                    for asset in EmployeeRegistration.objects.all():
                        panics = Alert.objects.filter(asset=asset, floor=floor, value=1,
                                                      timestamp__gte=startTime, timestamp__lte=endTime).order_by('-timestamp')

                        # print("panic--------", panics)
                        if panics:
                            serializer2 = AlertSerializer(panics)
                            assetPayload.append(serializer2.data)
                        else:
                            freeFall = Alert.objects.filter(asset=asset, floor=floor, value=3,
                                                            timestamp__gte=startTime, timestamp__lte=endTime).order_by('-timestamp').first()

                            # print("freefall", freeFall)
                            if freeFall:
                                serializer2 = AlertSerializer(freeFall)
                                assetPayload.append(serializer2.data)
                            else:
                                pass
                        # if panics:
                        #     for row in panics:
                        #         serializer2 = AlertSerializer(row)
                        #         assetPayload.append(serializer2.data)
                        #         break
                        # else:
                        #     freeFall = Alert.objects.filter(asset=asset, floor=floor, value=3,
                        #                                   timestamp__gte=startTime, timestamp__lte=endTime).order_by('-timestamp')
                        #     if freeFall:
                        #         for row in freeFall:
                        #             serializer2 = AlertSerializer(row)
                        #             assetPayload.append(serializer2.data)
                        #             break

                        # if panics:
                        #     serializer2 = AlertSerializer(panics, many=True)
                        #     assetPayload.append(serializer2.data)
                    return Response(assetPayload, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Floor is not Existed"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"message": "Please provide Floor id "}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as err:
            print("error------", err)
            # logger.info("Error:-  "+str(request) + str(err))
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

#
#
# class AlertPanicApi(APIView):
#     authentication_classes = [SessionAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     @staticmethod
#     def get(request):
#         try:
#             assetPayload = []
#             objectPayload = []
#             startTime = datetime.datetime.today()
#
#             endTime = datetime.datetime.today() + datetime.timedelta(minutes=2)
#
#             floor_id = request.GET.get('floor')
#
#             print("---------")
#             if floor_id:
#                 floor = FloorMap.objects.filter(id=floor_id).first()
#                 if floor:
#                     for asset in EmployeeRegistration.objects.all():
#                         panics = Alert.objects.filter(asset=asset, floor=floor, value__in=(1, 3),
#                                                       timestamp__gt=startTime, timestamp__lt=endTime).order_by('-timestamp')[:2]
#
#                         print(startTime)
#                         if panics:
#                             print(len(panics))
#                             for row in panics:
#                                 print(row.value, panics[1].value)
#                                 if row.value == panics[1].value:
#                                     print("true")
#                                     serializer = AlertSerializer(row)
#                                     assetPayload.append(serializer.data)
#                                     break
#                                 else:
#                                     print("else")
#                                     if row.value == 1:
#                                         serializer1 = AlertSerializer(row)
#                                         assetPayload.append(serializer1.data)
#                                         break
#                                     elif row.value == 3:
#                                         if panics[1].timestamp <= row.timestamp <= \
#                                                 panics[1].timestamp + datetime.timedelta(minutes=1):
#
#                                             # print("t")
#                                             serializer1 = AlertSerializer(panics[1])
#                                             assetPayload.append(serializer1.data)
#                                             break
#                                         else:
#                                             serializer1 = AlertSerializer(row)
#                                             assetPayload.append(serializer1.data)
#
#                         # if panics:
#                         #     serializer2 = AlertSerializer(panics, many=True)
#                         #     assetPayload.append(serializer2.data)
#                     return Response(assetPayload, status=status.HTTP_200_OK)
#                 else:
#                     return Response({"message": "Floor is not Existed"}, status=status.HTTP_404_NOT_FOUND)
#             else:
#                 return Response({"message": "Please provide Floor id "}, status=status.HTTP_406_NOT_ACCEPTABLE)
#         except Exception as err:
#             print("error------", err)
#             return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
