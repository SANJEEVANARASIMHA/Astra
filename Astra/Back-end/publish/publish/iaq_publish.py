#!/usr/bin/python3
import datetime
import logging
# import json package
import logging.handlers
import time
import json

import paho.mqtt.client as mqtt
from random import randint

PORT = 1883  # MQTT data listening port
SubTopic = "tracking"

BROKER_ENDPOINT = "astrazeneca.vacustech.in"

SLAVE_ADDR = "5a-c2-15-0a-00-02"
#print(SLAVE_ADDR)


def processDataFrame():
    '''
    function to process data array
    :param data_array:
    :return: none
    '''

    # {"master": "5a-c2-15-08-00-01", "assets": [
    #     {"macaddress": "5a-c2-15-01-05-01", "X": 115.89, "Y": 7.88, "temp": 0.0, "humidity": 0.0, "airflow": 0.0,
    #      "iaq": 0.0, "alert": 4.0, "battery": 88.0, "slaveaddress": "5a-c2-15-0a-00-03"}]}

    payload = []

    master = ['5a-c2-15-08-00-0a']
    macarange = [1, 20]

    j =0
    k =1
    for address in master:

        for i in range(macarange[j], macarange[k]):
            dummy = {}
            dummy["macaddress"] = "5a-c2-15-" + "{0:02x}-{1:02x}-{2:02x}".format(4, 1, i)
            dummy["battery"] = int(randint(88, 96))
            dummy["co2"] = "{0:d}.{1:d}".format(randint(500, 510), randint(0, 5))
            dummy["tvoc"] = "{0:d}.{1:d}".format(randint(25, 30), randint(0, 5))
            # dummy["slaveaddress"] = SLAVE_ADDR
            payload.append(dummy)

        print(payload)
        j=k+1
        k=j+1
        ret = client.publish("tracking_iaq", payload=json.dumps({"master": address, "assets": payload}),
                             qos=1)

        #print("pubvlished success ", ret)

    master = ['5a-c2-15-08-00-0b', '5a-c2-15-08-00-0c']
    macarange = [13, 21, 21, 24]

    j = 0
    k = 1
    for address in master:
        for i in range(macarange[j], macarange[k]):
            dummy = {}
            dummy["macaddress"] = "5a-c2-15-" + "{0:02x}-{1:02x}-{2:02x}".format(4, 0, i)
            dummy["battery"] = int(randint(88, 96))
            dummy["co2"] = "{0:d}.{1:d}".format(randint(500, 510), randint(0, 5))
            dummy["tvoc"] = "{0:d}.{1:d}".format(randint(25, 30), randint(0, 5))
            # dummy["slaveaddress"] = SLAVE_ADDR
            payload.append(dummy)

        print(payload)
        j = k + 1
        k = j + 1
        ret = client.publish("tracking_iaq", payload=json.dumps({"master": address, "assets": payload}),
                             qos=1)

        #print("pubvlished success ", ret)


    master = ['5a-c2-15-08-00-01', '5a-c2-15-08-00-03', '5a-c2-15-08-00-04', '5a-c2-15-08-00-05']
    macarange = [1, 7, 7, 13, 24, 28, 28, 32]

    j = 0
    k = 1
    for address in master:

        for i in range(macarange[j], macarange[k]):
            dummy = {}
            dummy["macaddress"] = "5a-c2-15-" + "{0:02x}-{1:02x}-{2:02x}".format(4, 0, i)
            dummy["battery"] = int(randint(88, 96))
            dummy["co2"] = "{0:d}.{1:d}".format(randint(500, 510), randint(0, 5))
            dummy["tvoc"] = "{0:d}.{1:d}".format(randint(25, 30), randint(0, 5))
            # dummy["slaveaddress"] = SLAVE_ADDR
            payload.append(dummy)

        print(payload)
        j = k + 1
        k = j + 1
        ret = client.publish("tracking_iaq", payload=json.dumps({"master": address, "assets": payload}),qos=1)

        #print("published success ", ret)




# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, user_data, flags, rc):
    print("Connected with result code " + str(rc))


def systemcon():
    st = 0
    try:
        st = client.connect(BROKER_ENDPOINT, PORT)  # establishing connection
    except:
        st = 1
    finally:
        if st != 0:
            time.sleep(5)
            systemcon()


def on_connect(client, userdata, flags, rc):
    print("Connected to broker")


def on_disconnect(client, userdata, rc):
    if rc != 0:
        # logging.info("Unexpected disconnection.")
        systemcon()


client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
systemcon()
# Connecting to both MQTT brokers
client.loop_start()

while True:
    try:
        # process serial data
        processDataFrame()
        time.sleep(60)
    except KeyboardInterrupt:
        # Data_port.close()
        client.loop_stop()
        break
