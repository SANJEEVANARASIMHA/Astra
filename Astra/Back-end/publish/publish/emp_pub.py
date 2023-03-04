#!/usr/bin/python3
import datetime
import logging
# import json package
import logging.handlers
import time
import json
import datetime

import paho.mqtt.client as mqtt
from random import randint

PORT = 1883  # MQTT data listening port
# SubTopic = "tracking"


BROKER_ENDPOINT = "astrazeneca.vacustech.in"
SLAVE_ADDR = "5a-c2-15-0a-00-0a"
print(SLAVE_ADDR)

count = 0


def processDataFrame(value):
    global count
    count = value
    print("valueless=====>", count)
    """
    function to process data array
    :param data_array:
    :return: none
    """

    # {"master": "5a-c2-15-08-00-01", "assets": [
    #     {"macaddress": "5a-c2-15-01-05-01", "X": 115.89, "Y": 7.88, "temp": 0.0, "humidity": 0.0, "airflow": 0.0,
    #      "iaq": 0.0, "alert": 4.0, "battery": 88.0, "slaveaddress": "5a-c2-15-0a-00-03"}]}

    # {"macaddress": "5a-c2-15-03-01-c2", "X": 10.1, "Y": 10.1, "temp": 26.0, "humidity": 85.0, "airflow": 0.0,
    #  "iaq": 91.0, "alert": 0.0, "battery": 0.0, "slaveaddress": "5a-c2-15-0a-00-2d"}

    assetpayload = []
    sensorpayload = []
    iaqpayload = []
    iaqpayload2 = []
    statpayload = []

    x = 1 + count
    y = 1 + count

    packet = 5 + count

    empl_list = ["5a-c2-15-01-01-5a", "5a-c2-15-01-01-6b", "5a-c2-15-01-01-74", "5a-c2-15-01-01-69", "5a-c2-15-01-01-5c", "5a-c2-15-01-01-4d", "5a-c2-15-01-01-6f", "5a-c2-15-01-01-72", "5a-c2-15-01-01-57", "5a-c2-15-01-01-62", "5a-c2-15-01-01-58","5a-c2-15-01-01-68", "5a-c2-15-01-01-4f", "5a-c2-15-01-01-75", "5a-c2-15-01-01-5f", "5a-c2-15-01-01-64", "5a-c2-15-01-01-78", "5a-c2-15-01-01-63", "5a-c2-15-01-01-50", "5a-c2-15-01-01-4e", "5a-c2-15-01-01-55", "5a-c2-15-01-01-5e", "5a-c2-15-01-01-4b", "5a-c2-15-01-01-76", "5a-c2-15-01-01-6e", "5a-c2-15-01-01-71", "5a-c2-15-01-01-48", "5a-c2-15-01-01-67", "5a-c2-15-01-01-60", "5a-c2-15-01-01-59", "5a-c2-15-01-01-7a", "5a-c2-15-01-01-4c", "5a-c2-15-01-01-6d", "5a-c2-15-01-01-7b", "5a-c2-15-01-01-56", "5a-c2-15-01-01-6a", "5a-c2-15-01-01-37", "5a-c2-15-01-01-34", "5a-c2-15-01-01-47", "5a-c2-15-01-01-19", "5a-c2-15-01-01-40", "5a-c2-15-01-01-44"]

    empl_list1 = ["5a-c2-15-01-01-19", "5a-c2-15-01-01-34", "5a-c2-15-01-01-37", "5a-c2-15-01-01-40", "5a-c2-15-01-01-44", "5a-c2-15-01-01-47", "5a-c2-15-01-01-48", "5a-c2-15-01-01-4b", "5a-c2-15-01-01-4c", "5a-c2-15-01-01-4d", "5a-c2-15-01-01-4e","5a-c2-15-01-01-4f", "5a-c2-15-01-01-50", "5a-c2-15-01-01-54", "5a-c2-15-01-01-55", "5a-c2-15-01-01-56", "5a-c2-15-01-01-57", "5a-c2-15-01-01-58", "5a-c2-15-01-01-59", "5a-c2-15-01-01-5a", "5a-c2-15-01-01-5c", "5a-c2-15-01-01-5e", "5a-c2-15-01-01-5f", "5a-c2-15-01-01-6e", "5a-c2-15-01-01-71", "5a-c2-15-01-01-48", "5a-c2-15-01-01-67", "5a-c2-15-01-01-60", "5a-c2-15-01-01-59", "5a-c2-15-01-01-7a", "5a-c2-15-01-01-4c", "5a-c2-15-01-01-6d", "5a-c2-15-01-01-7b", "5a-c2-15-01-01-56", "5a-c2-15-01-01-6a", "5a-c2-15-01-01-37", "5a-c2-15-01-01-34", "5a-c2-15-01-01-47", "5a-c2-15-01-01-19", "5a-c2-15-01-01-40", "5a-c2-15-01-01-44"]

    # for i in range(201, 240):
    for i in  range(25, 99):
        dummy = {}
        # dummy["macaddress"] = str(i)
        dummy["macaddress"] = "5a-c2-15-" + "{0:02x}-{1:02x}-{2:02x}".format(1, 1, i)

        # dummy["macaddress"] = "5a-c2-15-" + "{0:02x}-{1:02x}-{2:02x}".format(1, 1, i)
        dummy["slaveaddress"] = SLAVE_ADDR
        if dummy["macaddress"] == "5a-c2-15-01-01-19":
            dummy["X"] = 48.0
            dummy["Y"] = 6.0
        elif dummy["macaddress"] == "5a-c2-15-01-01-34":
            dummy["X"] = 2.0
            dummy["Y"] = 3.9
        elif dummy["macaddress"] == "5a-c2-15-01-01-37":
            dummy["X"] = 3.4
            dummy["Y"] = 15.0
        elif dummy["macaddress"] == "5a-c2-15-01-01-40":
            dummy["X"] = 15.0
            dummy["Y"] = 15.0
        elif dummy["macaddress"] == "5a-c2-15-01-01-5c":
            dummy["X"] = 21.0
            dummy["Y"] = 9.0
        elif dummy["macaddress"] == "5a-c2-15-01-01-5e":
            dummy["X"] = 27.0
            dummy["Y"] = 18.0
        elif dummy["macaddress"] == "5a-c2-15-01-01-5f":
            dummy["X"] = 29.0
            dummy["Y"] = 5.0
        elif dummy["macaddress"] == "5a-c2-15-01-01-44":
            dummy["X"] = 40.0
            dummy["Y"] = 12.0
        elif dummy["macaddress"] == "5a-c2-15-01-01-4b":
            dummy["X"] = 12.0
            dummy["Y"] = 12.0
        elif dummy["macaddress"] == "5a-c2-15-01-01-4f":
            dummy["X"] = 12.0
            dummy["Y"] = 17.0

        elif dummy["macaddress"] == "5a-c2-15-01-01-58":
            dummy["X"] = 2.0
            dummy["Y"] = 30.0
        elif dummy["macaddress"] == "5a-c2-15-01-01-56":
            dummy["X"] = 4.0
            dummy["Y"] = 33.0
        elif dummy["macaddress"] == "5a-c2-15-01-01-57":
            dummy["X"] = 3.4
            dummy["Y"] = 43.0
        elif dummy["macaddress"] == "5a-c2-15-01-01-4e":
            dummy["X"] = 15.0
            dummy["Y"] = 35.0
        elif dummy["macaddress"] == "5a-c2-15-01-01-5f":
            dummy["X"] = 21.0
            dummy["Y"] = 39.0
        elif dummy["macaddress"] == "5a-c2-15-01-01-64":
            dummy["X"] = 41.0
            dummy["Y"] = 32.0
        elif dummy["macaddress"] == "5a-c2-15-01-01-78":
            dummy["X"] = 29.0
            dummy["Y"] = 29.0
        elif dummy["macaddress"] == "5a-c2-15-01-01-63":
            dummy["X"] = 31.0
            dummy["Y"] = 38.0
        elif dummy["macaddress"] == "5a-c2-15-01-01-50":
            dummy["X"] = 12.0
            dummy["Y"] = 23.0
        elif dummy["macaddress"] == "5a-c2-15-01-01-4e":
            dummy["X"] = 25.0
            dummy["Y"] = 29.0

        elif dummy["macaddress"] == "5a-c2-15-01-01-55":
            dummy["X"] = 89.0
            dummy["Y"] = 23.0
        elif dummy["macaddress"] == "5a-c2-15-01-01-5e":
            dummy["X"] = 71.0
            dummy["Y"] = 33.0
        elif dummy["macaddress"] == "5a-c2-15-01-01-4b":
            dummy["X"] = 74.3
# valueless=====> 4
            dummy["Y"] = 43.0
        elif dummy["macaddress"] == "5a-c2-15-01-01-76":
            dummy["X"] = 85.0
            dummy["Y"] = 35.0
        elif dummy["macaddress"] == "5a-c2-15-01-01-6e":
            dummy["X"] = 96.0
            dummy["Y"] = 39.0
        elif dummy["macaddress"] == "5a-c2-15-01-01-71":
            dummy["X"] = 101.0
            dummy["Y"] = 32.0
        #elif dummy["macaddress"] == "5a-c2-15-01-01-48":
        #    dummy["X"] = 76.0
        #    dummy["Y"] = 33.0
        elif dummy["macaddress"] == "5a-c2-15-01-01-67":
            dummy["X"] = 116.0
            dummy["Y"] = 38.0
        elif dummy["macaddress"] == "5a-c2-15-01-01-60":
            dummy["X"] = 72.0
            dummy["Y"] = 33.0
        elif dummy["macaddress"] == "5a-c2-15-01-01-59":
            dummy["X"] = 86.0
            dummy["Y"] = 29.0

        elif dummy["macaddress"] == "5a-c2-15-01-01-7a":
            dummy["X"] = 69.0
            dummy["Y"] = 8.0
        elif dummy["macaddress"] == "5a-c2-15-01-01-4c":
            dummy["X"] = 71.0
            dummy["Y"] = 6.0
        elif dummy["macaddress"] == "5a-c2-15-01-01-6d":
            dummy["X"] = 74.0
            dummy["Y"] = 13.0
        elif dummy["macaddress"] == "5a-c2-15-01-01-7b":
            dummy["X"] = 85.0
            dummy["Y"] = 15.0
        elif dummy["macaddress"] == "5a-c2-15-01-01-56":
            dummy["X"] = 96.0
            dummy["Y"] = 9.0
        elif dummy["macaddress"] == "5a-c2-15-01-01-6a":
            dummy["X"] = 101.0
            dummy["Y"] = 3.0
        elif dummy["macaddress"] == "5a-c2-15-01-01-37":
            dummy["X"] = 76.0
            dummy["Y"] = 9.0
        elif dummy["macaddress"] == "5a-c2-15-01-01-34":
            dummy["X"] = 116.0
            dummy["Y"] = 8.0
        elif dummy["macaddress"] == "5a-c2-15-01-01-47":
            dummy["X"] = 101.0
            dummy["Y"] = 18.0
        elif dummy["macaddress"] == "5a-c2-15-01-01-19":
            dummy["X"] = 82.0
            dummy["Y"] = 3.0
        else:
            dummy["macaddress"] = "5a-c2-15-01-01-19"
            dummy["X"] = 82.0
            dummy["Y"] = 3.0

        dummy["temp"] = "{0:d}.{1:d}".format(randint(0, 0), randint(0, 0))
        dummy["humidity"] = "{0:d}.{1:d}".format(randint(0, 0), randint(0, 0))
        dummy["airflow"] = int(0)
        dummy["iaq"] = int(0)
        # dummy["packet"] = packet
        dummy["alert"] = int(randint(0, 0))
        dummy["battery"] = int(randint(88, 96))

        x = x + 2
        y = y + 2
        packet = packet + 1
        # print(dummy["macaddress"], dummy["X"], dummy["Y"], dummy["packet"])
        assetpayload.append(dummy)


        for i in range(256, 288):
           jsonny = {}
           jsonny["macaddress"] = "5a-c2-15-" + "{0:02x}-{1:02x}-{2:02x}".format(1, 1, i)
           jsonny["X"] = "{0:d}.{1:d}".format(randint(3, 43), randint(1, 1))
           jsonny["Y"] = "{0:d}.{1:d}".format(randint(3, 18), randint(1, 1))
           jsonny["temp"] = 0
           jsonny["humidity"] = 0
           jsonny["airflow"] = 0
           jsonny["iaq"] = 0
           jsonny["alert"] = int(randint(0, 0))
           jsonny["battery"] = int(93)
           jsonny["slaveaddress"] = "5a-c2-15-0a-00-01"
           #assetpayload.append(jsonny)

        for i in range(286, 317):
           jsonny = {}
           jsonny["macaddress"] = "5a-c2-15-" + "{0:02x}-{1:02x}-{2:02x}".format(1, 1, i)
           jsonny["X"] = "{0:d}.{1:d}".format(randint(69, 117), randint(1, 1))
           jsonny["Y"] = "{0:d}.{1:d}".format(randint(3, 18), randint(1, 1))
           jsonny["temp"] = 0
           jsonny["humidity"] = 0
           jsonny["airflow"] = 0
           jsonny["iaq"] = 0
           jsonny["alert"] = int(randint(0, 0))
           jsonny["battery"] = int(93)
           jsonny["slaveaddress"] = "5a-c2-15-0a-00-01"
           #assetpayload.append(jsonny)


        for i in range(317, 338):
           jsonny = {}
           jsonny["macaddress"] = "5a-c2-15-" + "{0:02x}-{1:02x}-{2:02x}".format(1, 1, i)
           jsonny["X"] = "{0:d}.{1:d}".format(randint(69, 117), randint(1, 1))
           jsonny["Y"] = "{0:d}.{1:d}".format(randint(27, 44), randint(1, 1))
           jsonny["temp"] = 0
           jsonny["humidity"] = 0
           jsonny["airflow"] = 0
           jsonny["iaq"] = 0
           jsonny["alert"] = int(randint(0, 0))
           jsonny["battery"] = int(93)
           jsonny["slaveaddress"] = "5a-c2-15-0a-00-01"
           assetpayload.append(jsonny)


        for i in range(80, 112):
           jsonny = {}
           jsonny["macaddress"] = "5a-c2-15-" + "{0:02x}-{1:02x}-{2:02x}".format(1, 1, i)
           jsonny["X"] = "{0:d}.{1:d}".format(randint(2, 42), randint(1, 1))
           jsonny["Y"] = "{0:d}.{1:d}".format(randint(27, 44), randint(1, 1))
           jsonny["temp"] = 0
           jsonny["humidity"] = 0
           jsonny["airflow"] = 0
           jsonny["iaq"] = 0
           jsonny["alert"] = int(randint(0, 0))
           jsonny["battery"] = int(93)
           jsonny["slaveaddress"] = "5a-c2-15-0a-00-01"
           assetpayload.append(jsonny)


        print()
    count = count + 1

    print(len(assetpayload))
    ret = client.publish("tracking", payload=json.dumps({"master": "5a-c2-15-08-00-03", "assets": assetpayload}))

    print("published")
    print(ret)

    # , qos=0)
    #ret = client.publish("slave_tracking", payload=json.dumps(assetpayload), qos=0)
    # print("published")

    # for i in range(155, 255):
    #     jsonny = {}
    #     # jsonny["master"] = "5a-c2-15-" + "{0:02x}-{1:02x}-{2:02x}".format(8, 0, i)
    #     jsonny["macaddress"] = "5a-c2-15-" + "{0:02x}-{1:02x}-{2:02x}".format(3, 0, i)
    #     jsonny["slaveaddress"] = "5a-c2-15-0a-00-01"
    #     jsonny["X"] = "{0:d}.{1:d}".format(randint(0, 0), randint(0, 0))
    #     jsonny["Y"] = "{0:d}.{1:d}".format(randint(0, 0), randint(0, 0))
    #     jsonny["temp"] = int(20)
    #     jsonny["humidity"] = int(10)
    #     jsonny["airflow"] = int(0)
    #     # jsonny["co2"] = int(30)
    #     # jsonny["tvoc"] = int(40)
    #     jsonny["iaq"] = int(0)
    #     # jsonny["packet"] = int(20)
    #     jsonny["alert"] = int(randint(0, 0))
    #     jsonny["battery"] = int(33)
        # assetpayload.append(jsonny)
    #
    # ret = client.publish("tracking", payload=json.dumps(sensorpayload), qos=0)

    # ret = client.publish("tracking", payload=json.dumps({"master": "5a-c2-15-08-00-0a", "assets": assetpayload}), qos=0)

# ----------------------*******************************--------------------------------#

    # master = ['5a-c2-15-08-00-01', '5a-c2-15-08-00-02', '5a-c2-15-08-00-03', '5a-c2-15-08-00-04', '5a-c2-15-08-00-05',
    #           '5a-c2-15-08-00-0a', '5a-c2-15-08-00-0b', '5a-c2-15-08-00-0c']
    # macarange = [1, 32, 33, 64, 65, 96, 97, 128, 129, 160, 161, 192, 193, 224, 225, 256]
    #
    # emprange = [1, 450, 451, 900, 901, 1350, 1351, 1800, 1801, 2250, 2251, 2700, 2701, 3150, 3151, 3600]
    #
    # j = 0
    # k = 1
    # e = 0
    # g = 1
    #
    # for address in master:
    #
    #     for i in range(macarange[j], macarange[k]):
    #         dummy = {}
    #         dummy["macaddress"] = "5a-c2-15-" + "{0:02x}-{1:02x}-{2:02x}".format(3, 0, i)
    #         dummy["slaveaddress"] = "5a-c2-15-0a-00-01"
    #         dummy["X"] = "{0:d}.{1:d}".format(randint(0, 0), randint(0, 0))
    #         dummy["Y"] = "{0:d}.{1:d}".format(randint(0, 0), randint(0, 5))
    #         dummy["temp"] = int(20)
    #         dummy["humidity"] = int(10)
    #         dummy["airflow"] = int(0)
    #         dummy["iaq"] = int(0)
    #         dummy["alert"] = int(randint(0, 0))
    #         dummy["battery"] = int(randint(88, 96))
    #
    #         #sensorpayload.append(dummy)
    #     print(e, g)
    #     for i in range(emprange[e], emprange[g]):
    #         dummy1 = {}
    #         dummy1["macaddress"] = "5a-c2-15-" + "{0:02x}-{1:02x}-{2:02x}".format(1, 1, i)
    #         dummy1["slaveaddress"] = SLAVE_ADDR
    #         dummy1["X"] = x
    #         dummy1["Y"] = y
    #         dummy1["temp"] = "{0:d}.{1:d}".format(randint(50, 50), randint(0, 5))
    #         dummy1["humidity"] = "{0:d}.{1:d}".format(randint(1, 2), randint(0, 0))
    #         dummy1["airflow"] = int(0)
    #         dummy1["iaq"] = int(0)
    #         dummy1["alert"] = int(randint(3, 5))
    #         dummy1["battery"] = int(randint(88, 96))
    #
    #         #sensorpayload.append(dummy1)
    #     # print(address)
    #     j = k + 1
    #     k = j + 1
    #
    #     e = g + 1
    #     g = g + 2
        # ret = client.publish("tracking", payload=json.dumps({"master": address, "assets": sensorpayload}), qos=0)

    # print("published")


# ----------------------------------*********************************--------------------------------------#


# The callback for when the client receives a CANNOCK response from the server.
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


# def on_connect(client, userdata, flags, rc):
#     print("Connected to broker")


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
        processDataFrame(count)
        time.sleep(30)
    except KeyboardInterrupt:
        # Data_port.close()
        client.loop_stop()
        break
