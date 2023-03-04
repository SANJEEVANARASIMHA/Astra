import paho.mqtt.client as paho
import json
import datetime
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
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
PORT = 1883
topic = "tracking_iaq"


def on_message(client, userdata, message):
    # logger.info("Data received")
    print("Data Recieved")
    serializedJson = message.payload.decode('utf-8')
    jsonData = json.loads(serializedJson)
    storeData(jsonData)


def storeData(jsonData):
    try:
        timeStamp = datetime.datetime.now()
        if jsonData:
            masterid = jsonData["master"]
            """Retrieveing Master Gateway object"""
            master = session.query(MasterGateway).filter(
                MasterGateway.gatewayid == masterid).first()

            if master is not None:
                # print("master", master.id)

                """ Updating master gateway lastseen """
                # floor_id = master.floor_id
                master.lastseen = timeStamp
                session.commit()

                for elem in jsonData['assets']:
                    # print(elem['macaddress'])
                    iaq = session.query(IaqSensor).filter(IaqSensor.macid == elem['macaddress']).first()

                    if iaq:
                        iaq.lastseen = timeStamp
                        iaq.battery = elem['battery']
                        iaq.co2 = elem['co2']
                        iaq.tvoc = elem['tvoc']
                        session.commit()
                        # print("iaq sensor updated")

                        dailyiaq = IaqDaily(
                            co2=elem["co2"],
                            tvoc=elem["tvoc"], asset_id=iaq.id,
                            timestamp=timeStamp, battery=elem['battery'])
                        session.add(dailyiaq)
                        session.commit()

    except Exception as err:
        # logger.info("Error: ", str(err))
        print("error", str(err))


def on_connect(client, userdata, flags, rc):
    # logger.info("Connected to broker")
    print("Connected to broker")
    client.subscribe(topic)  # subscribe topic test


def on_disconnect(client, userdata, rc):
    if rc != 0:
        # logger.info("Disconnection from broker, Reconnecting...")
        print("Disconnection from broker, Reconnecting...")

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
            print("Connection failed, Reconnecting...")
            time.sleep(5)
            systemcon()


if __name__ == "__main__":
    #
    with open('../logs/tracking.yaml', 'r') as stream:
        logger_config = yaml.load(stream, yaml.FullLoader)
    logging.config.dictConfig(logger_config)
    logger = logging.getLogger('IAQ Sensor-Tracking')

    client = paho.Client()  # create client object
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    systemcon()
    client.subscribe(topic)  # subscribe topic test
    client.loop_forever()

    while True:
        pass
