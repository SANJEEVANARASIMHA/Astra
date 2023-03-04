#! /usr/bin/python3

# This script subscribes to the broker(cloud) and stores the receiver data in the web server's database
import mysql.connector
import time
import paho.mqtt.client as paho  # mqtt library
import logging
import logging.handlers
import json
import datetime
import time

DB_USERNAME = "vacus"
DB_PASSWORD = "vacus@123"
DB_NAME = "vacusdb"

BROKER_ENDPOINT = "astrazeneca.vacustech.in"
PORT = 1883
subTopic = "tracking1"


def on_message(client, userdata, message):
    logger.info("Data received, storing it in the database")
    serializedJson = message.payload.decode('utf-8')

    jsonData = json.loads(serializedJson)

    db = mysql.connector.connect(
        host="localhost",
        user=DB_USERNAME,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    storeData(jsonData, db)


def storeData(jsonData, db):
    try:
        timeStamp = datetime.datetime.now()
        print("before --- ", timeStamp)
        master = jsonData["master"]
        sql = """SELECT * FROM gateway_mastergateway WHERE  gatewayid = %s"""
        val = (master,)
        cursor = db.cursor()
        cursor.execute(sql, val)
        result = cursor.fetchone()

        if result is not None:
            floor_id = result[2]

            for elem in jsonData["assets"]:

                temp_humi = """SELECT * FROM sensor_temperaturehumidity where macid=%s"""
                temp_val = (elem["macaddress"],)
                cursor.execute(temp_humi, temp_val)
                temp_result = cursor.fetchone()

                if temp_result is not None:
                    # Updating Temp-Humidity Sensor
                    temp_sql = """update sensor_temperaturehumidity set temperature=%s, humidity=%s, lastseen=%s, 
                    battery=%s where macid=%s """
                    temp_val = (elem["temp"], elem["humidity"], timeStamp, elem["battery"], elem["macaddress"])
                    cursor.execute(temp_sql, temp_val)
                    db.commit()
                    # print("Temp-Humidity Sensor updated!!")

                    sql = """INSERT INTO sensor_dailytemperaturehumidity (temperature, humidity, timestamp, asset_id) 
                    VALUES (%s, %s, %s, %s) """
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
                # slave_sql = """update gateway_slavegateway set lastseen=%s where gatewayid=%s """
                # slave_val = (timeStamp, elem["slaveaddress"])
                # cursor.execute(slave_sql, slave_val)
                # db.commit()
                # print("slave-gateway updated!!")

                # timeStamp1 = datetime.datetime.now()
                # print("after----", timeStamp1)

    except Exception as err:
        print("----------------------", err)
        logger.info("Failed to store data in database - " + str(err))


def on_connect(client, userdata, flags, rc):
    logger.info("Connected to broker")
    client.subscribe(subTopic)  # subscribe topic test


def on_disconnect(client, userdata, rc):
    if rc != 0:
        logger.info("Unexpected disconnection from the broker,reconnecting...")
        systemcon()
        client.subscribe(subTopic)  # subscribe topic test


def systemcon():
    st = 0
    try:
        st = client.connect(BROKER_ENDPOINT, PORT)  # establishing connection
    except:
        st = 1
    finally:
        if st != 0:
            logger.info("Failed to connect to the broker, trying to reconnect...")
            time.sleep(5)
            systemcon()


if __name__ == "__main__":
    # Create the logger for the application and bind the output to /sys/log/ #
    logger = logging.getLogger('tracking-data-subscriber')
    logger.setLevel(logging.INFO)
    logHandler = logging.handlers.SysLogHandler(address='/dev/log')
    logHandler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)s - %(message)s')
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)

    client = paho.Client()  # create client object
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    systemcon()
    client.subscribe(subTopic)  # subscribe topic test
    client.loop_forever()

    while True:
        pass
