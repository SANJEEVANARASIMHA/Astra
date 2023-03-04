#! /usr/bin/python3

#
# This script recieves the data from the zone monitors and forwards it to the web
# server after doing all the computations
#
import datetime
import time
from multiprocessing import Process, Semaphore, Queue
from time import sleep
import logging
import logging.handlers
import socket
import signal,os
import json
import mysql.connector

RECEIVE_BUFFER = 500000
SOCKET_BINDING_ADDR = ('127.0.0.1', 12345)

DB_USERNAME = "vacus"
DB_PASSWORD = "vacus"
DB_NAME = "astra"
topic = "tracking"


def on_message(client, userdata, message):
    logger.info("Data received")
    # print("data recieved")
    serializedJson = message.payload.decode('utf-8')
    jsonData = json.loads(serializedJson)
    storeData(jsonData, message.topic)


def storeData(jsonList, db):

    try:
        timeStamp = datetime.datetime.now()
        print("before --- ", timeStamp)
        master = jsonList["master"]
        sql = """SELECT * FROM gateway_mastergateway WHERE  gatewayid = %s"""
        val = (master,)
        cursor = db.cursor()
        cursor.execute(sql, val)
        result = cursor.fetchone()

        if result is not None:
            floor_id = result[2]

            temp = (timeStamp, master)
            sql = """update gateway_mastergateway set lastseen=%s where gatewayid=%s"""
            cursor = db.cursor()
            cursor.execute(sql, temp)
            db.commit()

            cursor = db.cursor()

            for elem in jsonList["assets"]:
                print("after----", timeStamp)

                # Updating Employee
                emp_sql = """update employee_employeeregistration set lastseen=%s, battery=%s, floor_id=%s, x=%s,y=%s where tagid=%s """
                val = (timeStamp, elem["battery"], floor_id, elem["X"], elem["Y"], elem["macaddress"])
                cursor.execute(emp_sql, val)
                db.commit()
                # print("employee data id updated!!")

                # Updating Slave-Gateway
                slave_sql = """update gateway_slavegateway set lastseen=%s where gatewayid=%s """
                val1 = (timeStamp, elem["slaveaddress"])
                cursor.execute(slave_sql, val1)
                db.commit()
                # print("slave-gateway updated!!")

                # Inserting Employee Alert
                sql = """SELECT * FROM employee_employeeregistration WHERE tagid = %s"""
                val = (elem["macaddress"],)
                cursor.execute(sql, val)
                result = cursor.fetchone()
                # print("result", result)
                if result is not None:
                    if elem["alert"] > 0 and elem["alert"] != 2:
                        temp = (elem["alert"], timeStamp, result[0], floor_id)

                        emp_alert = """INSERT INTO alert_alert (value,timestamp,asset_id,floor_id) VALUES (%s, %s, %s, %s)"""
                        cursor.execute(emp_alert, temp)
                        db.commit()

                        zone = """SELECT * FROM zones_zones where x1 < %s  and %s <= x2 and y1 < %s and %s <= y2 """
                        temp = (elem["X"], elem["X"], elem["Y"], elem["Y"])
                        cursor.execute(zone, temp)
                        result1 = cursor.fetchone()
                        print("result1", result1)
                        if result1 is not None:
                            zone_tracking = """INSERT into zones_zonetracking (timestamp, tagid_id, zoneid_id) VALUES (%s, %s, %s) """
                            zone_temp = (timeStamp, result[0], result1[0])
                            cursor.execute(zone_tracking, zone_temp)
                            db.commit()
                            print("Zone Data inserted")

                        time = datetime.datetime.now()
                        print("after", time)

                temp_humi = """SELECT * FROM sensor_temperaturehumidity where macid=%s"""
                temp_val = (elem["macaddress"],)
                cursor.execute(temp_humi, temp_val)
                temp_result = cursor.fetchone()

                if temp_result is not None:
                    # Updating Temp-Humidity Sensor
                    temp_sql = """update sensor_temperaturehumidity set temperature=%s, humidity=%s, lastseen=%s, battery=%s where macid=%s """
                    temp_val = (elem["temp"], elem["humidity"], timeStamp, elem["battery"], elem["macaddress"])
                    cursor.execute(temp_sql, temp_val)
                    db.commit()
                    # print("Temp-Humidity Sensor updated!!")

                    sql = """INSERT INTO sensor_dailytemperaturehumidity (temperature, humidity, timestamp, asset_id) VALUES (%s, %s, %s, %s)"""
                    val = (elem["temp"], elem["humidity"], timeStamp, temp_result[0])
                    cursor.execute(sql, val)
                    db.commit()
                    # print("Daily Temp-humidity data inserted")

                # Updating Signal-Repeater
                signal_repeator = """update signalrepeator_signalrepeator set lastseen=%s where macid=%s"""
                sig_val = (timeStamp, elem["macaddress"])
                cursor.execute(signal_repeator, sig_val)
                db.commit()

                # Updating Slave-Gateway
                slave_sql = """update gateway_slavegateway set lastseen=%s where gatewayid=%s """
                slave_val = (timeStamp, elem["slaveaddress"])
                cursor.execute(slave_sql, slave_val)
                db.commit()

        else:
            logger.info("No data to be stored in db")
    except Exception as err:
        logger.info("ERROR OCCURED - " + str(err))

    os.kill(os.getpid(), signal.SIGKILL)


def on_connect(client, userdata, flags, rc):
    logger.info("Connected to broker")
    # print("connected to broker ----------------")
    client.subscribe(topic)  # subscribe topic test


def on_disconnect(client, userdata, rc):
    if rc != 0:
        logger.info("Disconnection from broker, Reconnecting...")
        # print("disconnection")
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
    # Create the logger for the application and bind the output to /sys/log/ #
    logger = logging.getLogger('processing-service')
    logger.setLevel(logging.INFO)

    logHandler = logging.handlers.SysLogHandler(address='/dev/log')
    logHandler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(name)s - %(message)s')

    logHandler.setFormatter(formatter)

    logger.addHandler(logHandler)

    skt = bindSocketAddress(logger)

    if (skt != None):
        Manager(skt, logger)