#! /usr/bin/python3
import datetime
import time
import json
import mysql.connector
import mysql.connector.pooling
import paho.mqtt.client as paho
from sqlqueries import masterSelectQuery, masterUpdateQuery, slaveUpdateQuery, employeeSelectQuery, empUpdateQuery, \
    empAlertInsertQuery, tempSensorUpdateQuery, tempSensorSelectQuery, tempSensorInsertQuery, signalRepeatorUpdateQuery, \
    zoneInsertQuery, zoneSelectQuery, MasterSelectAll, zoneSelectAll
import threading

DB_USERNAME = "vacus"
DB_PASSWORD = "vacus@123"
DB_NAME = "vacusdb"

dbconfig = {
    "database": "vacusdb",
    "user": "vacus",
    "password": "vacus@123"
}

pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=32,
    pool_reset_session=True,
    **dbconfig)

db = pool.get_connection()

#print("---------")
#print(pool)
# print(cnx.pool_size)


BROKER_ENDPOINT = "astrazeneca.vacustech.in"
# BROKER_ENDPOINT = "192.168.0.78"
PORT = 1883
topic = "esp/test1"

select = "select"
update = "update"
many = "many"


def on_message(client, userdata, message):
    # logger.info("Data received")
    print("data recieved")
    serializedJson = message.payload.decode('utf-8')
    jsonData = json.loads(serializedJson)
    #print("json data recieved")
    # print(jsonData)
    storeData(jsonData, message.topic)


def queryData(*args):
    #print("length of args ---------", len(args))
    if len(args) == 4:
        query, payload, cursor, db = (args)
        if len(payload):
            result = cursor.executemany(query, payload)
            #print("result is -------------------------", cursor.rowcount)
            db.commit()
            return None
        else:
            return None
    elif len(args) == 5:
        query, value, type, cursor, db = (args)
        if type == "select":
            cursor.execute(query, value)
            result = cursor.fetchone()
            return result
        elif type == "update":
            cursor.execute(query, value)
            #print("result is -------------------------", cursor.rowcount)
            return None
        else:
            return None
    else:
        return None

def storeData(jsonList, topic):
    try:
        #print("---------storeData function is called")
        cursor = db.cursor()
        timeStamp = datetime.datetime.now()
        masterMacid = jsonList["master"]
        val = (masterMacid,)
        result = queryData(masterSelectQuery, val, select, cursor, db)
        if result is not None:
            masterid, masterMac, floor_id, timestamp = (result)
            #print(masterid, masterMac, floor_id)
            if masterid:
                slaveUpdatePayload = []
                signalRepeaterUpdatePayload = []
                empUpdatePayload = []
                alertPayload = []
                tempSensorUpdatePayload = []
                tempSensorInsertPayload = []
                zoneInsertPayload = []

                # updating master data
                masterTuple = (timeStamp, masterMacid)
                queryData(masterUpdateQuery, masterTuple, update, cursor, db)
                print("master is updated")
                print("length of the assets ", len(jsonList['assets']))

                # iterating the jsonList
                for elem in jsonList['assets']:
                    # checking the emp tagid
                    slaveUpdatePayload.append((timeStamp, elem["slaveaddress"]))

                    if elem["macaddress"][0:11] == "5a-c2-15-01":
                        val = (elem["macaddress"],)
                        result = queryData(employeeSelectQuery, val, select, cursor, db)
                        if result is not None:
                            empDataFrame(elem, floor_id, result, empUpdatePayload, alertPayload, timeStamp)
                            temp = (elem["X"], elem["X"], elem["Y"], elem["Y"], floor_id)
                            zone_result = queryData(zoneSelectQuery, temp, select, cursor, db)
                            if zone_result is not None:
                                zoneInsertPayload.append((timeStamp, result[0], zone_result[0]))
                            else:
                                pass
                        else:
                            pass

                    # checking tag type for sensor
                    elif elem["macaddress"][0:11] == "5a-c2-15-03":
                        temp_val = (elem["macaddress"],)
                        temp_result = queryData(tempSensorSelectQuery, temp_val, select, cursor, select)
                        if temp_result is not None:
                            tempDataFrame(elem, tempSensorInsertPayload, tempSensorUpdatePayload, timeStamp,
                                          temp_result[0])

                    # checking tag type signal repeaters
                    elif elem["macaddress"][0:11] == "5a-c2-15-06":
                        signalRepeaterUpdatePayload.append((timeStamp, elem["macaddress"]))
                    else:
                        pass

                # updatating the slave data at once for every message
                queryData(slaveUpdateQuery, slaveUpdatePayload, cursor, db)
                print("slave data is updated")
                # # updating the mployee tracking data at once for evry message
                queryData(empUpdateQuery, empUpdatePayload, cursor, db)
                print("employee is updated")
                # inserting zone wise tracking Data at once for every message
                queryData(zoneInsertQuery, zoneInsertPayload, cursor, db)
                print("zones is inserted")
                # # inserting the employee alerts into alerts tables for every message at once
                queryData(empAlertInsertQuery, alertPayload, cursor, db)
                print("alert is inserted ")
                # updating the sensor temp humi data at once for evry message
                queryData(tempSensorUpdateQuery, tempSensorUpdatePayload, cursor, db)
                print("sensor is updated")
                # inserting the sensor temp humi data at once for evry message
                queryData(tempSensorInsertQuery, tempSensorInsertPayload, cursor, db)
                print("sensor is inserted")

                # updatating the signal repeaters data at once for every message
                queryData(signalRepeatorUpdateQuery, signalRepeaterUpdatePayload, cursor, db)
                print("signal repeater is updated")

                cursor.close()
                # db.close()
        else:
            print("master is not registered")
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
