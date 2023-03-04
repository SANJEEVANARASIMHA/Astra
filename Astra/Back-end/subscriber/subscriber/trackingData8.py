# IMPORTING PACKAGES NEEDED
# removed cheking date condition
import paho.mqtt.client as paho
import json
import datetime
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import yaml
import logging.config
from tables2 import *

# creating the database engine object
engine = create_engine("mysql+pymysql://vacus:vacus@127.0.0.1/astra", echo=False)

# creating the session maker object
Session = sessionmaker(bind=engine)
# creating the session object
session = Session()
# Base = declarative_base()

# mqtt broker end point
# BROKER_ENDPOINT = "psa.vacustech.in"
BROKER_ENDPOINT = "192.168.0.8"
# mqtt connecting port
PORT = 1883
# mqtt topic
topic = "LoadCell"

time_oil = datetime.datetime.now()
oil_value = 100

currdate = datetime.datetime.today().date()


def on_message(client, userdata, message):
    """ this is a call back function it will invoke on message event """
    # logger.info("Data received")
    print("data recieved topic is ", message.topic)
    # decoding the message
    serializedJson = message.payload.decode('utf-8')

    # print(serializedJson)
    # if message lenth is greater than the 20 then it is considered as actual message
    if len(serializedJson) > 20:
        print("----------")
        # converting the decoded message into json format
        jsonData = json.loads(serializedJson)
        print(jsonData)
        # calling storeData function by passing the aruguments called jsonData, message topic
        storeData(jsonData, message.topic)


#


def storeData(jsonData, topic):
    # creating the timestamp object for inserting the timestamp of message recieved
    timeStamp = datetime.datetime.now()
    try:
        # fixing the sensor mac address for perticular device and checking the condition
        if jsonData['id'] == "5a-c2-15-0b-00-01":
            # creating the current date object
            # quering from the sensor reading table  based on mac address either its presented or not
            sensor = session.query(SensorReading).filter(
                SensorReading.tagid == jsonData['id']).order_by(SensorReading.id.desc()).first()
            print("sensor is presented", sensor)
            # checking object is presented or not
            if sensor:
                # if math.floor(float(jsonData['reading'])) == 13:
                # checking the presented object is todays object or not
                # checking the distancelidar is lesser than 400
                if jsonData['distancelidar'] < 400:
                    distancelidarLesser(jsonData, sensor, timeStamp)
                else:
                    distancelidarGreater(jsonData, timeStamp)
            else:
                distancelidarChecking(jsonData, timeStamp)
        else:
            pass
    except Exception as err:
        # if any error comes in the sense close the session object
        session.close()
        # logger.info("error " + str(err))
        print("error---------------------------------", str(err))


def distancelidarLesser(jsonData, sensor, timeStamp):
    print("distancelidar is less than 400 ")
    # if distancelidar is less than 400 in the sence it has to insert one new record into database
    jsonData['dcstatus'] = 0
    if float(jsonData['Reading']) >= sensor.reading:
        sensor_insert(jsonData, timeStamp)
        print("sensor is inserted")
        # print("object is presented greater than equal to 15 inserted sensor reading")
        # checking the difference between previouse reading and current reading
        add_wastage = float(jsonData['Reading']) - sensor.reading
        # if reding difference greater than 0.200 gramns consider it as wastages
        print("add wastage object difference  ", add_wastage)
        if add_wastage > 0.200:
            sensor_daily = session.query(SensorDaily).filter(
                SensorDaily.tagid == jsonData['id']).order_by(
                SensorDaily.id.desc()).first()

            # checking the object is presented in sensor Daily table
            if sensor_daily:
                print("sessor daily object is presented")
                # jsonData['Reading'] = add_wastage
                print("---------------", str(sensor_daily.timestamp).split(" ")[0], str(currdate))
                # checking the presented object is todays object or not
                # if dc status is equal to 1 in the sense add wastge
                if sensor_daily.dcstatus == 1:
                    jsonData['Reading'] = 0.0 + add_wastage
                else:
                    # add the previouse wastage and current wastage into sensorDaily table
                    jsonData['Reading'] = sensor_daily.reading + add_wastage
                sensorDailyInsert(jsonData, timeStamp)
                # if presented object is not todays object in the sense then it will insert new
                # record into SensorDaily table
            else:
                # no object is presented in the sense it  will insert one new record into
                # sensorDaily table
                jsonData['Reading'] = add_wastage
                sensorDailyInsert(jsonData, timeStamp)
        else:
            pass
    else:
        pass


def distancelidarGreater(jsonData, timeStamp):
    jsonData = distancelidarChecking(jsonData, timeStamp)
    # quering object is presented or not from sensorDaily table
    sensor_daily = session.query(SensorDaily).filter(
        SensorDaily.tagid == jsonData['id']).order_by(
        SensorDaily.id.desc()).first()


    # dtStr = sensor_daily.timestamp checking presented object is todays object or not  condition
    # got true in the sense one record to sensorDaily
    if sensor_daily:
        jsonData['Reading'] = sensor_daily.reading
        # creating the sensorDailyInsert object
        sensorDailyInsert(jsonData, timeStamp)
        # logger.info("sensor Daily object is inserted")
        print("sensor Daily object is inserted")


def distancelidarChecking(jsonData, timeStamp):
    """ it will check the distancelidar and reading according to that  it will update the dustbin status and insert
    one new record into sensor Reading table """

    if jsonData['distancelidar'] >= 400 and jsonData['Reading'] < 15.0:
        jsonData['dcstatus'] = 1
    else:
        jsonData['dcstatus'] = 0
    # creating the wastage object
    sensor_insert(jsonData, timeStamp)
    print("sensor distancelidar wastage object is inserted")
    # logger.info("sensor distancelidar  wastage object is inserted")
    return jsonData


def sensor_insert(jsonData, timeStamp):
    """ it will create the sensorReading object and inserts a new record in SensorReading table """
    # print("inside of sensor insert ")
    # print(jsonData)

    object_insert = SensorReading(id=SensorReading.id, tagid=jsonData['id'], reading=jsonData['Reading'],
                                  distancelader=jsonData['distancelidar'], dcstatus=jsonData['dcstatus'],
                                  battery=jsonData['bt'], timestamp=timeStamp)

    session.add(object_insert)
    session.commit()
    print("sensorReading wastage object is inserted")
    # logger.info("sensorReading wastage object is inserted")
    # return object_insert


def sensorDailyInsert(jsonData, timeStamp):
    """ it wil take the jsonData object and create SensorDaily object and inserts a new records to the SensorDaily
    Table """
    # print("inside of sensor insert ")
    print(jsonData)

    object_insert = SensorDaily(id=SensorDaily.id, tagid=jsonData['id'], reading=jsonData['Reading'],
                                distancelader=jsonData['distancelidar'], dcstatus=jsonData['dcstatus'],
                                battery=jsonData['bt'], timestamp=timeStamp)

    session.add(object_insert)
    session.commit()
    print("sensorReading wastage object is inserted")
    # logger.info("sensorReading wastage object is inserted")
    # return object_insert


def on_connect(client, userdata, flags, rc):
    """ on connection of broker it subscribes the topic """
    # logger.info("Connected to broker")
    print("connected to broker")
    client.subscribe(topic)  # subscribe topic test


def on_disconnect(client, userdata, rc):
    """ on dis-connection of broker event this call back function will invoke and get the connection and subscribe
    the topic """

    if rc != 0:
        # logger.info("Disconnection from broker, Reconnecting...")
        print("disconnection  Reconnecting...")
        systemcon()
        client.subscribe(topic)  # subscribe topic test


def systemcon():
    """ on disconnection of broker it will try to re-connect to the broker"""
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
    # with open('/home/pi/Desktop/logs/tracking.yaml', 'r') as stream:
    #     logger_config = yaml.load(stream, yaml.FullLoader)
    # logging.config.dictConfig(logger_config)
    # logger = logging.getLogger('Tracking')

    client = paho.Client()  # create client object
    client.on_connect = on_connect  # on connection event on connect call back function will invoke
    client.on_message = on_message  # on message event on_message call back function will invoke
    client.on_disconnect = on_disconnect  # on disconnection of broken event on_disconnection call back function invoke

    systemcon()
    client.subscribe(topic)  # subscribe topic test
    client.loop_forever()

    # while True:
    # pass

