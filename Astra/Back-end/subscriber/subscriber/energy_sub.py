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
# BROKER_ENDPOINT = "astrazeneca.vacustech.in"
BROKER_ENDPOINT = "192.168.0.73"

PORT = 1883
topic = "#"


def on_message(client, userdata, message):
    logger.info("Data received")
    # print("data recieved")
    serializedJson = message.payload.decode('utf-8')
    jsonData = json.loads(serializedJson)
    print(message.topic)
    storeData(jsonData, message.topic)


def storeData(jsonData, topic):
    # print("--------", topic)
    timeStamp = datetime.datetime.now()

    try:
        if topic == "esp/test1":
            # print("----", jsonData, type(jsonData))
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
            # logger.info(topic + " data is inserted")

        elif topic == "parking":
            print(topic)
            print(jsonData)
            for row in jsonData:
                if float(row['lad']) < 1.5:
                    vehicle = session.query(Energy_VehicleTracking).filter(
                        Energy_VehicleTracking.tag == row["macaddress"]).order_by(
                        Energy_VehicleTracking.id.desc()).first()
                    if vehicle:
                        if vehicle.vehicle_status:
                            vehicle.timestamp = timeStamp
                            session.commit()
                            print("vehcile status is updated")
                        else:
                            parking_insert(row, timeStamp, True)
                            print("vehicle status is inserted")
                    else:
                        parking_insert(row, timeStamp, True)
                        print("vehicle status is inserted")
                    # logger.info(topic + " data is inserted")
                else:

                    vehicle = session.query(Energy_VehicleTracking).filter(
                        Energy_VehicleTracking.tag == row["macaddress"]).order_by(
                        Energy_VehicleTracking.id.desc()).first()
                    if vehicle:
                        if not vehicle.vehicle_status:
                            vehicle.timestamp = timeStamp
                            session.commit()
                            print("vehcile status is updated")
                        else:
                            parking_insert(row, timeStamp, False)
                            print("data inserted")

                    else:
                        parking_insert(row, timeStamp, False)
                        print("data inserted")
                    # logger.info(topic + " data is inserted")
        elif topic == "energy":
            print(topic)
            print(jsonData)
            energy = session.query(EnergyTracking).filter(
                EnergyTracking.tag == jsonData["macaddress"]).order_by(
                EnergyTracking.id.desc()).first()
            if energy:
                if energy.current == jsonData['cur'] and energy.energy == jsonData['enrg'] / 1000 and energy.powerFactor == jsonData['pf'] and energy.voltage == jsonData['vtg']:
                    energy.timestamp = timeStamp
                    session.commit()
                else:
                    energy_insert(jsonData, timeStamp)
                    print("data inserted")
                    logger.info(topic + " data is inserted")

            else:
                energy_insert(jsonData, timeStamp)
                print("data inserted")
                logger.info(topic + " data is inserted")

        elif topic == "passive":
            print("inside passive")
            print(topic)
            print(jsonData)
            for row in jsonData:
                passive_insert(row, timeStamp, True)
                print("passive data inserted")
                # logger.info(topic + " data is inserted")

        else:
            print(topic, "is not using in this script")

    except Exception as err:
        print("----", str(err))
        session.rollback()
        # logger.info(" esp/test error ", str(err))


def passive_insert(jsonData, timestamp, status):
    passiveTrack = PassiveAsset(id=PassiveAsset.id, tag=jsonData["macaddress"], status=status,
                                timestamp=timestamp)
    session.add(passiveTrack)
    session.commit()


def energy_insert(jsonData, timestamp):
    energyTrack = EnergyTracking(id=EnergyTracking.id,
                                 tag=jsonData["macaddress"],
                                 current=jsonData['cur'], energy=jsonData['enrg'] / 1000,
                                 powerFactor=jsonData['pf'], voltage=jsonData['vtg'],
                                 timestamp=timestamp)
    session.add(energyTrack)
    session.commit()


def parking_insert(row, timestamp, status):
    parkingTrack = Energy_VehicleTracking(id=Energy_VehicleTracking.id, tag=row["macaddress"],
                                          vehicle_status=status, timestamp=timestamp)
    session.add(parkingTrack)
    session.commit()
    print("vehicle status is inserted")


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
