import paho.mqtt.client as paho
import json
import datetime
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import yaml
import logging.config
from tables import *
engine = create_engine(
    "mysql+pymysql://vacus:vacus@127.0.0.1/astra", echo=False)

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
BROKER_ENDPOINT = "astrazeneca.vacustech.in"
# BROKER_ENDPOINT = "192.168.0.100"

PORT = 1883
topic = "esp/test1"


def on_message(client, userdata, message):
    logger.info("Data received")
    # print("data recieved")
    serializedJson = message.payload.decode('utf-8')
    jsonData = json.loads(serializedJson)
    storeData(jsonData, message.topic)


def storeData(jsonData, topic):
    print(topic)
    timeStamp = datetime.datetime.now()

    try:
        print("----", jsonData, type(jsonData))
        dailydata = MultiSensor(id=MultiSensor.id,
                                MACID=jsonData["MACID"],
                                Temp=jsonData['Temp'], Humi=jsonData['Hum'], Co2=jsonData['CO2'],
                                PM1=jsonData['PM1.0'], PM2=jsonData['PM2.5'], PM4=jsonData['PM4.0'],
                                PM10=jsonData['PM10.0'], NC0=jsonData['NC0.5'], NC1=jsonData['NC1.0'],
                                NC2=jsonData['NC2.5'], NC4=jsonData['NC4.0'], NC10=jsonData['NC10.0'],
                                PtSize=jsonData['PtSize']
                                , O2=jsonData['O2'], VOC=int(jsonData['VOC']), timestamp=timeStamp)
        session.add(dailydata)
        session.commit()
        print("data inserted")
        logger.info(topic + " data is inserted")

    except Exception as err:
        print("----", str(err))
        logger.info(" esp/test error ", str(err))


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
            logger.info("Connection failed, Reconnecting...")
            print("connection failed")
            time.sleep(5)
            systemcon()


if __name__ == "__main__":
    with open('../logs/tracking.yaml', 'r') as stream:
        logger_config = yaml.load(stream, yaml.FullLoader)
    logging.config.dictConfig(logger_config)
    logger = logging.getLogger('Tracking')

    client = paho.Client()  # create client object
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    systemcon()
    client.subscribe(topic)  # subscribe topic test
    client.loop_forever()

    # while True:
    # pass
