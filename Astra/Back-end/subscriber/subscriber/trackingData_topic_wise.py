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
    "mysql+pymysql://vacus@123:vacus@127.0.0.1/vacusdb", echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
BROKER_ENDPOINT = "astrazeneca.vacustech.in"
# BROKER_ENDPOINT = "192.168.0.100"

PORT = 1883
topic = "tracking1"


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
        masterid = jsonData["master"]
        """Retrieveing Master Gateway object"""
        master = session.query(MasterGateway).filter(
            MasterGateway.gatewayid == masterid).first()

        print("master objects ", jsonData['master'], master.gatewayid)
        if master is not None:
            """ Updating master gateway lastseen """
            floor_id = master.floor_id
            master.lastseen = timeStamp
            session.commit()

            # print("master is updated")

            """ Iterating through all array of asset """
            for elem in jsonData["assets"]:

                print(elem['macaddress'])
                """ Retrieveing Slave Gateway object """
                slave = session.query(SlaveGateway).filter(
                    SlaveGateway.gatewayid == elem["slaveaddress"]).first()

                if slave is not None:
                    print("slave gateway", slave.gatewayid, elem["slaveaddress"])
                    """ Updating slave gateway lastseen """
                    slave.lastseen = timeStamp
                    session.commit()
                    # print("slave is updated")

                """ Retrieveing Employee Object"""

                # print("macaadss----------------", elem['macaddress'], elem['X'], elem['Y'])
                if elem["macaddress"][0:11] == "5a-c2-15-01":
                    # print("success", elem["macaddress"][0:11])
                    employee = session.query(EmpRegistration).filter(
                        EmpRegistration.tagid == elem["macaddress"]).first()
                    if employee:
                        print("employee  ---", employee.tagid, elem['macaddress'])
                        """ Updating health, tracking and alert data for employee tag """
                        if employee.intime.date() != datetime.datetime.today().date():
                            employee.intime = datetime.datetime.today()
                        employee.lastseen = timeStamp
                        employee.battery = elem["battery"]
                        employee.floor_id = floor_id
                        employee.x = elem['X']
                        employee.y = elem['Y']
                        session.commit()

                        print("employee tracking is updated")

                        if elem["alert"] > 0 and elem['alert'] != 2:
                            employee_alert = Alert(id=Alert.id, value=elem["alert"], timestamp=timeStamp,
                                                   floor_id=floor_id,
                                                   asset_id=employee.id)
                            session.add(employee_alert)
                            session.commit()

                            # print("alert is inserted")

                        # emptag = session.query(EmpRegistration).filter(
                        #     EmpRegistration.tagid_id == employee.id).first()
                        # if emptag:
                        zone = session.query(Zones).filter(
                            Zones.x1 < elem['X'], Zones.x2 >= elem['X'], Zones.y1 < elem['Y'],
                            Zones.y2 >= elem['Y']).first()
                        if zone:
                            track = ZoneTracking(
                                id=ZoneTracking.id, zoneid_id=zone.id, tagid_id=employee.id, timestamp=timeStamp)
                            session.add(track)
                            session.commit()

                            # print("zone tracking is inserted")
                # else:
                #     pass

                """ Retrieveing Temperature/Humidity object"""

                # print("sensor before")
                # print("success", elem["macaddress"][0:11])

                if elem["macaddress"][0:11] == "5a-c2-15-03":
                    # print("sensor success", elem["macaddress"][0:11] )
                    temp = session.query(TemperatureHumidity).filter(
                        TemperatureHumidity.macid == elem["macaddress"],
                        TemperatureHumidity.floor_id == master.floor_id).first()
                    # print("sensor after")

                    # print("sensor object", temp)
                    if temp:
                        """ Updating temp, humid, health data of particular asset """
                        temp.temperature = elem["temp"]
                        temp.humidity = elem["humidity"]
                        temp.lastseen = timeStamp
                        # temp.floor_id = floor_id
                        temp.battery = elem["battery"]
                        session.commit()

                        # print(elem["macaddress"], "temp humi is updated")

                        dailydata = DailyTemperature(
                            temperature=elem["temp"],
                            humidity=elem["humidity"], asset_id=temp.id,
                            timestamp=timeStamp)
                        session.add(dailydata)
                        session.commit()
                        # print("temp daily inserted")
                # else:
                #     pass

                """ Retrieveing IRQ sensor object """

                if elem["macaddress"][0:11] == "5a-c2-15-04":

                    # print("indie sof iaq senbsor ")
                    print("success", elem["macaddress"][0:11])
                    iaq = session.query(IaqSensor).filter(
                        IaqSensor.macid == elem["macaddress"]).first()

                    # print("iaq  is-------------------", iaq, elem["macaddress"])
                    if iaq:
                        """ Updating lastseen and battery status"""
                        iaq.lastseen = timeStamp
                        iaq.battery = elem["battery"]
                        iaq.co2 = elem["co2"]
                        iaq.tvoc = elem["tvoc"]
                        session.commit()

                        # print("iaq is updated ")

                        dailydata = IaqDaily(id=IaqDaily.id,
                                             co2=elem["co2"], battery=elem['battery'], tvoc=elem["tvoc"],
                                             asset_id=iaq.id, timestamp=timeStamp)
                        session.add(dailydata)
                        session.commit()
                        # print("iaq is inserted")

                if elem["macaddress"][0:11] == "5a-c2-15-06":
                    print("success", elem["macaddress"][0:11])
                    """ Retrieveing Signal repeater object """
                    signal = session.query(SignalRepeater).filter(
                        SignalRepeater.macid == elem["macaddress"]).first()
                    if signal:
                        """ Updating lastseen """
                        signal.lastseen = timeStamp
                        session.commit()
                        # print("signal repeater is updated")
    except Exception as err:

        print("-----------------", err)
        session.close()
        # print(str(err))
        logger.info(str(err))


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
    with open('/home/ubuntu/logs/tracking.yaml', 'r') as stream:
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
