import datetime
import math
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum
from weightscale.models import SensorReading, Sensors
from weightscale.serializers import SensorsSerializer, SensorDetailSerializer


class SensorsAPIView(APIView):

    def get(self, request):
        try:
            sensors = Sensors.objects.all()
            if sensors:
                serializer = SensorsSerializer(sensors, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response([], status=status.HTTP_200_OK)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            id = request.data.get('tagid')
            sensor = Sensors.objects.filter(id=id).first()
            if sensor:
                display = {'id': sensor.id, 'timestamp': sensor.timestamp, 'currentDiff': sensor.display,
                           'battery': sensor.battery}
                print("----------------------------")
                print(display)
                # serializer = SensorDetailSerializer(sensor)
                return Response(display, status=status.HTTP_200_OK)
            else:
                return Response([], status=status.HTTP_200_OK)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)


class NewSensorGraphAPI(APIView):

    def get(self, request):
        try:
            dataPayload = []
            graph = request.GET.get('key')
            id = request.GET.get('tagid')
            currentDate = datetime.datetime.now().date()
            print("-----------------", currentDate)
            weekList = self.getWeekList(currentDate)
            monthList = self.getMonthList(currentDate)

            if graph == "weekly":
                for date in weekList:
                    print("-weekly-------------")
                    print(weekList)
                    payload = self.creatingPayload(date, id)
                    if payload:
                        dataPayload.append(payload)
                return Response(dataPayload, status=status.HTTP_200_OK)
            elif graph == "monthly":
                print("monthly-------------")
                print(monthList)
                for date in monthList:
                    payload = self.creatingPayload(date, id)
                    if payload:
                        dataPayload.append(payload)
                return Response(dataPayload, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

    def creatingPayload(self, date, id):
        data = {}
        daily_objects = SensorReading.objects.filter(tagid=id, timestamp__startswith=str(date),
                                                     dcstatus=1).aggregate(Sum('reading'))
        if daily_objects:
            if daily_objects['reading__sum']:
                object = SensorReading.objects.filter(timestamp__startswith=str(date)).order_by('-timestamp').first()
                if object:
                    if object.dcstatus == 0:
                        data['date'] = date
                        data['reading'] = object.reading + daily_objects['reading__sum']
                        return data
                    else:
                        data['date'] = date
                        data['reading'] = daily_objects['reading__sum']
                        return data
                else:
                    data['date'] = date
                    data['reading'] = daily_objects['reading__sum']
                    return data
            else:
                dict_obj = self.getReadingWithDcStatusZero(id, date)
                return dict_obj
        else:
            dict_obj = self.getReadingWithDcStatusZero(id, date)
            return dict_obj

    def getMonthList(self, currentDate):
        monthly_list = []
        for row in range(1, 31):
            a = currentDate - datetime.timedelta(days=row)
            if str(currentDate)[0:7] == str(a)[0:7]:
                monthly_list.append(str(a))
        monthly_list.reverse()
        return monthly_list

    def getWeekList(self, currentDate):
        weekly_list = []
        for row in range(1, 8):
            a = currentDate - datetime.timedelta(days=row)
            weekly_list.append(a)
        weekly_list.reverse()
        return weekly_list

    def getReadingWithDcStatusZero(self, id, date):
        data = {}
        daily_objects = SensorReading.objects.filter(tagid=id, timestamp__startswith=str(date)).order_by('-timestamp').first()
        if daily_objects:
            if daily_objects.dcstatus == 0:
                data['date'] = date
                data['reading'] = daily_objects.reading
                return data
            else:
                return None
        else:
            return None