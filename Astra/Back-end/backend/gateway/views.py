from django.shortcuts import render

from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# from apilogger import logger
from common.models import FloorMap
from gateway.models import MasterGateway, SlaveGateway
from gateway.serializers import MasterSerializer, SlaveSerializer

""" API for MasterGateway """


class MasterGatewayAPI(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    """ POST method to store details of master gateway with floor it is attached """

    @staticmethod
    def post(request):
        try:
            var = MasterGateway()
            var.gatewayid = request.data.get("macaddress")
            var.floor = FloorMap.objects.get(id=request.data.get("id"))
            var.save()
            # logger.info("Error:- " + str(request) + " MasterGateway " + str(
            #     request.data.get("macaddress")) + " Registred Succeefully..!")
            return Response(status=status.HTTP_200_OK)

        except Exception as err:
            print(err)
            # logger.info("Error:- " + str(request) + str(err))
            return Response(status=status.HTTP_400_BAD_REQUEST)

    """ GET method to retrieve all details """

    @staticmethod
    def get(request):
        try:
            data = MasterGateway.objects.all().order_by('gatewayid')
            ser = MasterSerializer(data, many=True)
            # logger.info(str(request) + " MasterGateway Health is Fetched Successfully..!")

            return Response(ser.data, status=status.HTTP_200_OK)
        except Exception as err:
            # logger.info("Error:- " + str(request) + str(err))
            return Response(status=status.HTTP_400_BAD_REQUEST)

    """ DELETE method to delete particular master along with all slaves registered under master """

    @staticmethod
    def delete(request):
        try:
            data = MasterGateway.objects.filter(gatewayid=request.data.get("macaddress"))
            data.delete()
            # logger.info(str(request) + " MasterGateway " + str(request.data.get("macaddress")) + " UnRegistred Succeefully..!")
            return Response(status=status.HTTP_200_OK)
        except Exception as err:
            # logger.info("Error:- " + str(request) + str(err))
            return Response(status=status.HTTP_400_BAD_REQUEST)


""" API for SlaveGateway """


class SlaveGatewayAPI(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    """ POST method to store details of slave gateway with master it is attached """

    @staticmethod
    def post(request):
        try:
            master = MasterGateway.objects.get(gatewayid=request.data.get('master'))
            slave = SlaveGateway()
            slave.gatewayid = request.data.get("macaddress")
            slave.master = master
            slave.save()
            # logger.info(str(request) + " SlaveGateway " + str(request.data.get("macaddress")) + " Registred Succeefully..!")
            return Response(status=status.HTTP_200_OK)

        except Exception as err:
            print(err)
            # logger.info("Error:- " + str(request) + str(err))
            return Response(status=status.HTTP_400_BAD_REQUEST)

    """ GET method to retrieve all details """

    @staticmethod
    def get(request):
        try:
            data = SlaveGateway.objects.all().order_by('gatewayid')
            ser = SlaveSerializer(data, many=True)
            # logger.info(str(request) + " SlaveGateway Health is Fetched Successfully..!")
            return Response(ser.data, status=status.HTTP_200_OK)

        except Exception as err:
            # logger.info("Error:- " + str(request) + str(err))
            return Response(status=status.HTTP_400_BAD_REQUEST)

    """ DELETE method to delete particular slave details"""

    @staticmethod
    def delete(request):
        try:
            data = SlaveGateway.objects.filter(gatewayid=request.data.get("macaddress"))
            data.delete()
            # logger.info(str(request) + " SlaveGateway " + str(request.data.get("macaddress")) + " unRegistred Succeefully..!")
            return Response(status=status.HTTP_200_OK)

        except Exception as err:
            # logger.info("Error:- " + str(request) + str(err))
            return Response(status=status.HTTP_400_BAD_REQUEST)
