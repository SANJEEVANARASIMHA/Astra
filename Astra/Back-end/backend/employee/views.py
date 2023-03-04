import sys
import django.db.utils
from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import datetime
from django.db import transaction
from alert.models import Alert
from alert.serializers import AlertSerializer
# from apilogger import logger
from common.models import FloorMap
from .models import EmployeeRegistration, DistanceCalculation, EmployeeHistory
from .serializers import EmployeeRegistrationSerializer, DistanceCalculationSerializer, FileUploadSerializer, \
    EmpHistorySerializer, EmployeeHistorySerializer

""" API for EmployeeRegistration """


class EmployeeRegistrationAPI(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    """ POST method to add employee"""

    @staticmethod
    def post(request):
        try:

            data = request.data
            keys = ['name', 'tagid', 'role', 'email', 'empid', 'phone']

            if sorted(list(data.keys())) != sorted(keys):
                return Response({"Please Provide All Fields"}, status=status.HTTP_406_NOT_ACCEPTABLE)

            for key, value in data.items():
                if not value:
                    return Response({"message": "Please Provide value for " + str(key)},
                                    status=status.HTTP_406_NOT_ACCEPTABLE)

            if EmployeeRegistration.objects.filter(tagid=data['tagid']).first():
                return Response({"message": "Mac Already Existed"}, status=status.HTTP_208_ALREADY_REPORTED)

            if EmployeeRegistration.objects.filter(email=data['email']).first():
                return Response({"message": "Email Already Existed"}, status=status.HTTP_208_ALREADY_REPORTED)

            if EmployeeRegistration.objects.filter(phoneno=data['phone']).first():
                return Response({"message": "Phone Number Already Existed"}, status=status.HTTP_208_ALREADY_REPORTED)

            emp = EmployeeRegistration()
            emp.tagid = data['tagid']
            emp.name = data["name"]
            emp.role = data["role"]
            emp.empid = data['empid']
            emp.email = data['email']
            emp.phoneno = data['phone']
            emp.save()
            # logger.info(str(request) + str(data['tagid'])+"  is Registred Successfully..!")
            return Response(status=status.HTTP_201_CREATED)

        except Exception as err:
            print(err)
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

    """ GET method to retrieve all details of employee"""

    @staticmethod
    def get(request):
        try:
            if request.GET.get("key") == "all":
                data = EmployeeRegistration.objects.all().order_by('-lastseen')
                ser = EmployeeRegistrationSerializer(data, many=True)
                # logger.info(str(request) + " Employee Health is Fetched Successfully..!")
                return Response(ser.data, status=status.HTTP_200_OK)
            else:
                emp = EmployeeRegistration.objects.filter(
                    tagid=request.GET.get("key")).first()
                if emp:
                    ser = EmployeeRegistrationSerializer(emp)
                    # logger.info(str(request) + " Employee Health is Fetched Successfully..!")
                    return Response(ser.data, status=status.HTTP_200_OK)
                else:
                    return Response({}, status=status.HTTP_404_NOT_FOUND)

        except Exception as err:
            # logger.info(str(request) + str(err))
            return Response(status=status.HTTP_400_BAD_REQUEST)

    """ DELETE method to delete particular employee details """

    @staticmethod
    def delete(request):
        try:
            tagid = request.data.get("tagid")
            if tagid:
                print("----------tagid", tagid)
                employee = EmployeeRegistration.objects.filter(
                    tagid=tagid).first()

                print("employee---", employee)
                if employee:
                    employee.delete()
                    # logger.info(str(request) + str(tagid)+" is Removed SuccessFully ..!")
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"message": "Please Provide TagId"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        except Exception as err:

            print("error-----", err)
            # logger.info("Error:-  "+str(request) + str(err) + " is Removed SuccessFully ..!")

            return Response(err, status=status.HTTP_400_BAD_REQUEST)

    # def update(self, object, data):
    #     if object:
    #         object.name = data['name']
    #         object.role = data['role']
    #         object.tagid = data['tagid']
    #         object.save()

    """ UPDATE method to allocate tag to employee """

    # def patch(self, request):
    #     try:
    #         data = request.data
    #         if data['tagid']:
    #             employee = EmployeeRegistration.objects.filter(tagid=data['tagid']).first()
    #             if employee:
    #                 if employee.id == id:
    #                     self.update(employee, data)
    #                     return Response(status=status.HTTP_200_OK)
    #                 else:
    #                     return Response({"message": "Mac Already Existed"}, status=status.HTTP_208_ALREADY_REPORTED)
    #             else:
    #                 tag = EmployeeRegistration.objects.filter(id=id).first()
    #                 if tag:
    #                     self.update(tag, data)
    #                     return Response(status=status.HTTP_200_OK)
    #                 else:
    #                     return Response(status=status.HTTP_404_NOT_FOUND)
    #         else:
    #             return Response({"message": "Please provide TagId"}, status=status.HTTP_406_NOT_ACCEPTABLE)
    #     except Exception as err:
    #         print(err)
    #         return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)


""" API for EmployeeRegistration """


class EmployeeTrackingAPI(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    """ GET method to add employee"""

    # @staticmethod
    # def post(request):
    #     try:
    #         start = request.data.get("start")
    #         end = request.data.get('end')
    #         print(start, end)
    #         tagid = request.data.get('tagid')
    #         print(tagid)
    #
    #         floor = FloorMap.objects.filter(id=request.data.get('floor')).first()
    #         # print("floor", floor)
    #         emp = EmployeeRegistration.objects.filter(tagid=tagid).first()
    #         # print("employee", emp)
    #         start_date = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
    #         end_date = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")+datetime.timedelta(days=1)
    #         # print("start date", start_date)
    #         # print("end date", end_date)
    #         history = EmployeeHistory.objects.filter(emp=emp, floor=floor, lastseen__gte=start_date, lastseen__lte=end_date)
    #         # print("history")
    #         print(history)
    #         if history:
    #             serializer = EmpHistorySerializer(history, many=True)
    #             return Response(serializer.data, status=status.HTTP_200_OK)
    #         else:
    #             return Response([], status=status.HTTP_200_OK)
    #     except Exception as err:
    #         print(err)
    #         return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get(request):
        try:
            # emp = EmployeeRegistration.objects.raw("select * from employee_employeeregistration where tagid_id in (
            # select id from employee_employeetag where floor_id="+request.GET.get("floorid")+")")
            floor = FloorMap.objects.filter(id=request.GET.get('floor')).first()

            # print("floor id is -=--------", floor)
            emp = EmployeeRegistration.objects.filter(floor=floor).order_by('-lastseen')

            # print("length of employees ", len(emp))
            startTime = datetime.datetime.today() - datetime.timedelta(seconds=30)
            endTime = datetime.datetime.today()
            assetPayload = []
            if emp:
                for asset in emp:
                    # print(asset.tagid)
                    panics = Alert.objects.filter(asset=asset, floor=floor, value=1,
                                                  lastseen__gte=startTime, lastseen__lte=endTime).order_by(
                        '-timestamp').first()

                    # print("panic--------", panics)
                    if panics:
                        serializer2 = AlertSerializer(panics)
                        data = serializer2.data
                        data['tagid'] = asset.tagid
                        data['x'] = asset.x
                        data['y'] = asset.y
                        data['name'] = asset.name
                        data['emptime'] = asset.lastseen
                        assetPayload.append(data)
                    else:
                        freeFall = Alert.objects.filter(asset=asset, floor=floor, value=3,
                                                        lastseen__gte=startTime, lastseen__lte=endTime).order_by(
                            '-timestamp').first()

                        # print("freefall", freeFall)
                        if freeFall:
                            serializer2 = AlertSerializer(freeFall)
                            data = serializer2.data
                            data['tagid'] = asset.tagid
                            data['x'] = asset.x
                            data['y'] = asset.y
                            data['name'] = asset.name
                            data['emptime'] = asset.lastseen

                            assetPayload.append(data)
                        else:
                            # pass
                            # ser = EmployeeRegistrationSerializer(emp)
                            assetPayload.append({
                                "id": asset.id,
                                "value": 0,
                                "timestamp": asset.lastseen,
                                "lastseen": asset.lastseen,
                                "asset": asset.id,
                                "floor": asset.floor.id,
                                "tagid": asset.tagid,
                                "x": asset.x,
                                "y": asset.y,
                                "name": asset.name,
                                'emptime': asset.lastseen
                            })
                return Response(assetPayload, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        except Exception as err:
            print(err)
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)


class EmployeeHistoryAPI(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    """ GET method to add employee"""

    @staticmethod
    def post(request):
        try:
            start = request.data.get("start")
            end = request.data.get('end')
            print(start, end)
            tagid = request.data.get('tagid')
            print(tagid)

            floor = FloorMap.objects.filter(id=request.data.get('floor')).first()
            print("floor", floor)
            emp = EmployeeRegistration.objects.filter(tagid=tagid).first()
            # print("employee", emp)
            start_date = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
            end_date = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
            # print("start date", start_date)
            # print("end date", end_date)
            # print(emp.id)
            if emp:
                if floor:
                    objects = EmployeeHistory.objects.raw(
                        "select id,x, y, battery, lastseen from employee_employeehistory  where emp_id=" + str(
                            emp.id) + " and floor_id=" + str(floor.id) + " and lastseen >='" + str(
                            start_date) + "' and lastseen <='" + str(
                            end_date) + "' group by emp_id,x, y,DATE(lastseen),HOUR(lastseen),MINUTE(lastseen);")
                    print(len(objects))
                    if objects:
                        serializer1 = EmployeeHistorySerializer(objects, many=True)
                        return Response(serializer1.data, status=status.HTTP_200_OK)
                    else:
                        return Response([], status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Please Choose floor "}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Please Enter a Valid Asset Address "}, status=status.HTTP_400_BAD_REQUEST)

            # history = EmployeeHistory.objects.filter(emp=emp, floor=floor, lastseen__gte=start_date, lastseen__lte=end_date)
            # # print("history")
            # print(history)
            # if history:
            #     serializer = EmpHistorySerializer(history, many=True)
            #     return Response(serializer.data, status=status.HTTP_200_OK)
            # else:
            #     return Response([], status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic()
    def patch(self, request):
        try:
            data = request.data
            payload = []
            for row in data:
                emp = EmployeeRegistration.objects.filter(tagid=row['tagid']).first()
                floor = FloorMap.objects.filter(id=row['floor']).first()
                # print(emp, floor)
                if emp and floor:
                    lastseen = datetime.datetime.strptime(row['lastseen'], "%Y-%m-%d %H:%M:%S")
                    history = EmployeeHistory(emp=emp, floor=floor, x=row['X'], y=row['Y'], battery=0.0,
                                              lastseen=lastseen)
                    history.save()
                    # payload.append(history)
            # print(payload)
            # EmployeeHistory.objects.bulk_create(payload)
            return Response(status=status.HTTP_200_OK)

        except Exception as err:
            print(err)
            transaction.set_rollback(True)
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

    """ GET method to add employee"""

    @staticmethod
    def get(request):
        try:
            emp = EmployeeRegistration.objects.filter(tagid="5a-c2-15-01-01-152").first()
            if emp:
                objects = EmployeeHistory.objects.filter(emp=emp)[:29]
                print(len(objects))
                if objects:
                    serializer1 = EmployeeHistorySerializer(objects, many=True)
                    return Response(serializer1.data, status=status.HTTP_200_OK)
                else:
                    return Response([], status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            print(err)
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)


class EmployeeHistoryInsertAPI(APIView):
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    @transaction.atomic()
    def post(self, request):
        try:
            data = request.data
            payload = []
            for row in data:
                emp = EmployeeRegistration.objects.filter(tagid=row['tagid']).first()
                floor = FloorMap.objects.filter(id=row['floor']).first()
                # print(emp, floor)
                if emp and floor:
                    lastseen = datetime.datetime.strptime(row['lastseen'], "%Y-%m-%d %H:%M:%S")
                    history = EmployeeHistory(emp=emp, floor=floor, x=row['X'], y=row['Y'], battery=0.0,
                                              lastseen=lastseen)
                    # history.save()
                    payload.append(history)
            # print(payload)
            EmployeeHistory.objects.bulk_create(payload)
            return Response(status=status.HTTP_200_OK)

        except Exception as err:
            print(err)
            transaction.set_rollback(True)
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)


""" API for Employee Distance Tracking """


class DistanceCalculationAPI(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    """ GET method to add employee"""

    @staticmethod
    def get(request):
        try:
            print(request.GET.get("tagid"))
            emp = EmployeeRegistration.objects.get(
                tagid=request.GET.get("tagid"))
            data = DistanceCalculation.objects.filter(empid=emp.id)
            # print(data)
            if data:
                ser = DistanceCalculationSerializer(data, many=True)
                return Response(ser.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            print(err)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class BulkEmpRegistartion(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @transaction.atomic()
    def post(self, request):
        try:
            payload = []
            data = request.data
            # print(data)
            # mac_ids = EmployeeRegistration.objects.values_list('tagid')
            # tagids = [elem[0] for elem in mac_ids]
            # print("----------", tagids)
            # print(list(mac_ids))
            # result = [elem for elem in data if not elem['tagid'] in tagids]
            print("---- inside bulk registration")
            print(data)
            if data:
                for row in data:

                    data = row
                    keys = ['name', 'tagid', 'role', 'email', 'empid', 'phone']

                    if sorted(list(data.keys())) != sorted(keys):
                        return Response({"message": "please provide all Fields"}, status=status.HTTP_406_NOT_ACCEPTABLE)

                    for key, value in data.items():
                        if not value:
                            return Response({"message": "please Enter value for " + str(key)},
                                            status=status.HTTP_406_NOT_ACCEPTABLE)
                    # print(row['tagid'])
                    if row['tagid'] and row["name"] and row['role'] and row['empid'] and row['email'] and row['phone']:
                        payload.append(EmployeeRegistration(
                            tagid=row['tagid'],
                            name=row["name"],
                            role=row['role'],
                            empid=row['empid'],
                            email=row['email'],
                            phoneno=row['phone']
                        ))
                    else:
                        # transaction.set_rollback(True)
                        return Response({"message": "Please Provide All Fields"}, status=status.HTTP_406_NOT_ACCEPTABLE)

                EmployeeRegistration.objects.bulk_create(payload)
                # logger.info(str(request) + "Bulk Registration SuccessFully Done...!")
                return Response({"status": "success"},
                                status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as err:
            print("error==================", type(err), err)
            # logger.info("Error:- "+str(request) + str(err))
            ex_type, ex_value, ex_traceback = sys.exc_info()
            print(ex_type)
            if ex_type == django.db.utils.IntegrityError:
                return Response({"error": str(err)[8:43]}, status=status.HTTP_208_ALREADY_REPORTED)
            else:
                return Response({"error": str(err)[8:43]}, status=status.HTTP_400_BAD_REQUEST)
            # if err.
            # transaction.set_rollback(True)

    @transaction.atomic()
    def patch(self, request):
        try:
            data = request.data
            payload = []
            if data:
                print(data)
                for row in data:
                    # print(row)
                    if row['tagid'] and row['name'] and row['role'] and row['email'] and row['phone'] and row['empid']:
                        emp = EmployeeRegistration.objects.filter(tagid=row['tagid']).first()

                        # print("empp", emp)
                        if emp:
                            emp.name = row['name']
                            emp.role = row['role']
                            emp.email = row['email']
                            emp.phoneno = row['phone']
                            emp.empid = row['empid']
                            payload.append(emp)
                    else:
                        transaction.set_rollback(True)
                        return Response({"message": "Please Provide All Fields"}, status=status.HTTP_406_NOT_ACCEPTABLE)

                EmployeeRegistration.objects.bulk_update(payload, ['name', 'role', 'email', 'empid', 'phoneno'])
                # logger.info(str(request) + "Bulk updation SuccessFully Done...!")
                return Response({"status": "success"},
                                status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as err:
            print("error==================", err)
            # transaction.set_rollback(True)
            # logger.info("Error:- "+str(request) +str(err))
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)


# from django.shortcuts import render
# from rest_framework import generics
# import io, csv, pandas as pd
# from rest_framework.response import Response
# # remember to import the File model
# # remember to import the FileUploadSerializer and SaveFileSerializer
# class BulkEmpRegistartion(generics.CreateAPIView):
#     serializer_class = FileUploadSerializer
#
#     @transaction.atomic()
#     def post(self, request, *args, **kwargs):
#         try:
#
#                 for row in reader.iteritems():
#                     print(row['role'])
#
#                     # print(row['role'], row['name'], row['tagid'])
#                 # read_file.to_csv("Test.csv",
#                 #                  index=None,
#                 #                  header=True)
#                 #
#
#                 # new_file = []
#                 # for _, row in reader.iterrows():
#                 #     print(row['tagid'], row["name"], row['role'])
#                 #     if row['tagid'] and row["name"] and row['role']:
#                 #         new_file.append(EmployeeRegistration(
#                 #             tagid=row['tagid'],
#                 #             name=row["name"],
#                 #             role=row['role'],
#                 #         ))
#                 # print(new_file)
#                 # EmployeeRegistration.objects.bulk_create(new_file)
#
#             # serializer = self.get_serializer(data=request.data)
#             # serializer.is_valid(raise_exception=True)
#             # file = serializer.validated_data['file']
#             # reader = pd.read_csv(file)
#             # new_file = []
#             # for _, row in reader.iterrows():
#             #     # print(row)
#             #     new_file.append(EmployeeRegistration(
#             #         tagid=row['tagid'],
#             #         name=row["name"],
#             #         role=row['role'],
#             #     ))
#             # EmployeeRegistration.objects.bulk_create(new_file)
#             return Response({"status": "success"},
#                             status.HTTP_201_CREATED)
#         except Exception as err:
#
#             print("error==================", type(err), err)
#             # transaction.set_rollback(True)
#             return Response({"error": str(err)[8:43]}, status=status.HTTP_400_BAD_REQUEST)

#
# class BulkEmpUpdate(generics.CreateAPIView):
#     serializer_class = FileUploadSerializer
#
#     @transaction.atomic()
#     def patch(self, request, *args, **kwargs):
#         try:
#             serializer = self.get_serializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             file = serializer.validated_data['file']
#             reader = pd.read_csv(file)
#             new_file = []
#             tagids = []
#
#             for _, row in reader.iterrows():
#                 print(row)
#                 emp = EmployeeRegistration.objects.filter(tagid=row['tagid']).first()
#                 if emp:
#                     emp.name = row['name']
#                     emp.role = row['role']
#                     new_file.append(emp)
#             EmployeeRegistration.objects.bulk_update(new_file, ['name', 'role'])
#             return Response({"status": "success"},
#                             status.HTTP_201_CREATED)
#         except Exception as err:
#             print("error==================", err)
#             # transaction.set_rollback(True)
#             return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)


#
#
# class BulkEmpRegistartion(APIView):
#     authentication_classes = [SessionAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     @transaction.atomic()
#     def post(self, request):
#         try:
#             payload = []
#             data = request.data
#             # print(data)
#             mac_ids = EmployeeRegistration.objects.values_list('tagid')
#             tagids = [elem[0] for elem in mac_ids]
#             print("----------", tagids)
#             print(list(mac_ids))
#             result = [elem for elem in data if not elem['tagid'] in tagids]
#             print("----")
#             print(result)
#             if data:
#                 for row in data:
#                     print(row['tagid'])
#                     if row['tagid'] and row["name"] and row['role']:
#                         payload.append(EmployeeRegistration(
#                             tagid=row['tagid'],
#                             name=row["name"],
#                             role=row['role'],
#                         ))
#                     else:
#                         # transaction.set_rollback(True)
#                         return Response({"message": "Please Provide All Fields"}, status=status.HTTP_406_NOT_ACCEPTABLE)
#
#                 EmployeeRegistration.objects.bulk_create(payload)
#                 return Response({"status": "success"},
#                                     status.HTTP_201_CREATED)
#             else:
#                 return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
#         except Exception as err:
#             print("error==================", type(err), err)
#             ex_type, ex_value, ex_traceback = sys.exc_info()
#             print(ex_type)
#             if ex_type == django.db.utils.IntegrityError:
#                 return Response({"error": str(err)[8:43]}, status=status.HTTP_208_ALREADY_REPORTED)
#             else:
#                 return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
#             # if err.
# transaction.set_rollback(True)
