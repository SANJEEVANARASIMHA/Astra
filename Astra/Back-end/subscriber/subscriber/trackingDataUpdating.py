#! /usr/bin/python3
import datetime
import time
import json
import mysql.connector
import paho.mqtt.client as paho
from sqlqueries import masterSelectQuery, masterUpdateQuery, slaveUpdateQuery, employeeSelectQuery, empUpdateQuery, \
    empAlertInsertQuery, tempSensorUpdateQuery, tempSensorSelectQuery, tempSensorInsertQuery, signalRepeatorUpdateQuery, \
    zoneInsertQuery, zoneSelectQuery, MasterSelectAll, zoneSelectAll
import threading

DB_USERNAME = "vacus"
DB_PASSWORD = "vacus"
DB_NAME = "astra"

db = mysql.connector.connect(
    host="localhost",
    user=DB_USERNAME,
    password=DB_PASSWORD,
    database=DB_NAME
)
cursor = db.cursor()

BROKER_ENDPOINT = "astrazeneca.vacustech.in"
# BROKER_ENDPOINT = "192.168.0.78"
PORT = 1883
topic = "tracking"
from sortedcontainers import SortedList

allMasters = None
allZones = None

#
# def getMasters(cursor):
#     global allMasters
#     print(" calling getMasters Functions")
#     cursor.execute(MasterSelectAll)
#     allMasters = cursor.fetchall()
#     print(allMasters)
#     threading.Timer(15, getMasters, args=[cursor]).start()
#
#
# def getZones(cursor):
#     global allZones
#     print(" calling getZones Functions")
#     cursor.execute(zoneSelectAll)
#     allZones = cursor.fetchall()
#
#     print(allZones)
#     print("---------zones ")
#     threading.Timer(15, getZones, args=[cursor]).start()

#
# def findMaster(allMasters, masterMacid):
#     if allMasters is not None:
#         for (id, macid, floor_id) in allMasters:
#             if macid == masterMacid:
#                 return id, macid, floor_id


def on_message(client, userdata, message):
    # logger.info("Data received")
    print("data recieved")
    serializedJson = message.payload.decode('utf-8')
    jsonData = json.loads(serializedJson)
    print("json data recieved")
    # print(jsonData)
    storeData(jsonData, message.topic, db)


def storeData(jsonList, topic, db):
    try:
        cursor = db.cursor()
        print("---------storeData function is called")
        print(allMasters)
        timeStamp = datetime.datetime.now()
        masterMacid = jsonList["master"]

        val = (masterMacid,)
        cursor.execute(masterSelectQuery, val)
        result = cursor.fetchone()
        # print("master result ", result)
        if result is not None:
            masterid, masterMac, floor_id, timestamp = (result)
            print(masterid, masterMac, floor_id)
            if masterid:
                    slaveUpdatePayload = []
                    signalRepeaterUpdatePayload = []
                    empUpdatePayload = []
                    alertPayload = []
                    tempSensorUpdatePayload = []
                    tempSensorInsertPayload = []
                    zoneInsertPayload = []
                    masterTuple = (timeStamp, masterMacid)
                    cursor.execute(masterUpdateQuery, masterTuple)
                    db.commit()
                    print("length of the assets ", len(jsonList['assets']))

                    for elem in jsonList['assets']:
                        if elem["macaddress"][0:11] == "5a-c2-15-01":
                            val = (elem["macaddress"],)
                            cursor.execute(employeeSelectQuery, val)
                            result = cursor.fetchone()
                            # print("result", result)
                            if result is not None:
                                empUpdatePayload.append(
                                    (timeStamp, elem["battery"], floor_id, elem["X"], elem["Y"], elem["macaddress"]))
                                if elem["alert"] > 0 and elem["alert"] != 2:
                                    alertPayload.append((elem["alert"], timeStamp, result[0], floor_id))
                                else:
                                    pass
                                temp = (elem["X"], elem["X"], elem["Y"], elem["Y"], floor_id)
                                cursor.execute(zoneSelectQuery, temp)
                                zone_result = cursor.fetchone()
                                # print("result1", result1)
                                if zone_result is not None:
                                    zoneInsertPayload.append((timeStamp, result[0], zone_result[0]))
                                else:
                                    pass
                            else:
                                pass
                        elif elem["macaddress"][0:11] == "5a-c2-15-03":
                            # temp_humi = """SELECT * FROM sensor_temperaturehumidity where macid=%s"""
                            temp_val = (elem["macaddress"],)
                            cursor.execute(tempSensorSelectQuery, temp_val)
                            temp_result = cursor.fetchone()
                            if temp_result is not None:
                                tempSensorInsertPayload.append((elem["temp"], elem["humidity"], timeStamp, temp_result[0]))
                                tempSensorUpdatePayload.append((elem["temp"], elem["humidity"], timeStamp, elem["battery"], elem["macaddress"]))
                                # tempSensorInsertPayload.append((elem["temp"], elem["humidity"], timeStamp, temp_result[0]))
                        elif elem["macaddress"][0:11] == "5a-c2-15-06":
                            signalRepeaterUpdatePayload.append((timeStamp, elem["macaddress"]))
                        else:
                            pass

                    # updatating the slave data at once for every message
                    if len(slaveUpdatePayload):
                        cursor.executemany(slaveUpdateQuery, slaveUpdatePayload)
                        db.commit()
                        print("slave is updated")
                    # updatating the signal repeaters data at once for every message
                    if len(signalRepeaterUpdatePayload):
                        cursor.executemany(signalRepeatorUpdateQuery, signalRepeaterUpdatePayload)
                        db.commit()
                        print("signal repeater is updated")
                    # # updating the mployee tracking data at once for evry message
                    if len(empUpdatePayload):
                        cursor.executemany(empUpdateQuery, empUpdatePayload)
                        db.commit()
                        print("employee is updated")
                    # # inserting the employee alerts into alerts tables for every message at once
                    if len(alertPayload):
                        cursor.executemany(empAlertInsertQuery, alertPayload)
                        db.commit()
                        print("alert is inserted ")
                    # updating the sensor temp humi data at once for evry message
                    if len(tempSensorUpdatePayload):
                        cursor.executemany(tempSensorUpdateQuery, tempSensorUpdatePayload)
                        db.commit()
                        print("sensor is updated")

                    # inserting the sensor temp humi data at once for evry message
                    if len(tempSensorInsertPayload):
                        cursor.executemany(tempSensorInsertQuery, tempSensorInsertPayload)
                        db.commit()
                        print("sensor is inserted")

                    # inserting zone wise tracking Data at once for every message
                    if len(zoneInsertPayload):
                        cursor.executemany(zoneInsertQuery, zoneInsertPayload)
                        db.commit()
                        print("zones is inserted")
                    cursor.close()
        else:
            print("No data to be stored in db")
            # logger.info("No data to be stored in db")
    except Exception as err:
        # logger.info("ERROR OCCURED - " + str(err))
        print(err)


def on_connect(client, userdata, flags, rc):
    # logger.info("Connected to broker")
    print("connected to broker ----------------")
    client.subscribe(topic)  # subscribe topic test


def on_disconnect(client, userdata, rc):
    if rc != 0:
        # logger.info("Disconnection from broker, Reconnecting...")
        print("disconnection")
        systemcon()
        client.subscribe(topic)  # subscribe topic test


def systemcon():
    st = 0
    try:
        st = client.connect(BROKER_ENDPOINT, PORT)  # establishing connection
    except:
        st = 1
    finally:
        if (st != 0):
            # logger.info("Connection failed, Reconnecting...")
            print("connection failed")
            time.sleep(5)
            systemcon()


if __name__ == "__main__":
    # with open('../logs/tracking.yaml', 'r') as stream:
    #     logger_config = yaml.load(stream, yaml.FullLoader)
    # logging.config.dictConfig(logger_config)
    # logger = logging.getLogger('Tracking')
    # start_time = threading.Timer("5000", getMasters(cursor))
    # start_time.start()
    # getMasters(cursor)
    client = paho.Client()  # create client object
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    systemcon()
    client.subscribe(topic)  # subscribe topic test
    client.loop_forever()

# while True:
#       getMasters(cursor)
#       time.sleep(5)
