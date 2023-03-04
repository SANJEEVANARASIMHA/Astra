from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, LargeBinary, ForeignKey, DateTime
from sqlalchemy.sql import func

Base = declarative_base()

""" creating a common_map class for accessing the common_map objects and  attributes """


class FloorMap(Base):
    __tablename__ = 'commom_floormap'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(60), unique=True)
    width = Column(Float)
    height = Column(Float)
    image = Column(LargeBinary)


""" creating a gateway_mastergateway class for accessing the gateway_mastergateway objects and  attributes """


class MasterGateway(Base):
    __tablename__ = 'gateway_mastergateway'

    id = Column(Integer, primary_key=True, autoincrement=True)
    gatewayid = Column(String(20), unique=True)
    floor_id = Column(ForeignKey(FloorMap.id, ondelete='CASCADE'))
    lastseen = Column(DateTime(timezone=True), server_default=func.now())


""" creating a gateway_slavegateway class for accessing the gateway_slavegateway objects and  attributes """


class SlaveGateway(Base):
    __tablename__ = 'gateway_slavegateway'

    id = Column(Integer, primary_key=True, autoincrement=True)
    gatewayid = Column(String(20), unique=True)
    master_id = Column(ForeignKey(
        MasterGateway.id, ondelete='CASCADE'))
    lastseen = Column(DateTime(timezone=True), server_default=func.now())


""" creating a asset_asset class for accessing the asset_asset objects and  attributes """


#
# class employee_tag(Base):
#     __tablename__ = 'employee_employeetag'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     tagid = Column(String(20), unique=True)
#     battery = Column(Float)
#     lastseen = Column(DateTime(timezone=True), server_default=func.now())
#     x = Column(Float)
#     y = Column(Float)
#     floor_id = Column(ForeignKey(common_map.id, ondelete='CASCADE'))
#

class EmpRegistration(Base):
    __tablename__ = 'employee_employeeregistration'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    role = Column(String(100))
    empid = Column(String(100))
    email = Column(String(254))
    phoneno = Column(String(12))
    lastseen = Column(DateTime(timezone=True), server_default=func.now())
    intime = Column(DateTime(timezone=True), server_default=func.now())
    battery = Column(Float)
    x = Column(Float)
    y = Column(Float)
    tagid = Column(String(200))
    floor_id = Column(ForeignKey(FloorMap.id, ondelete='CASCADE'))

    intime = Column(DateTime(timezone=True), server_default=func.now())


class EmpDistanceTracking(Base):
    __tablename__ = 'employee_distancetracking'

    id = Column(Integer, primary_key=True, autoincrement=True)
    distance = Column(Integer)
    tag1_id = Column(ForeignKey(EmpRegistration.id, ondelete='CASCADE'))
    tag2_id = Column(ForeignKey(EmpRegistration.id, ondelete='CASCADE'))
    timestamp = Column(DateTime(timezone=True))


""" creating a sensor_temperaturehumidity class for accessing the sensor_temperaturehumidity tables attributes """


class TemperatureHumidity(Base):
    __tablename__ = 'sensor_temperaturehumidity'

    id = Column(Integer, primary_key=True, autoincrement=True)
    macid = Column(String(20))
    temperature = Column(Float)
    humidity = Column(Float)
    lastseen = Column(DateTime(timezone=True))
    x1 = Column(Float)
    y1 = Column(Float)
    x2 = Column(Float)
    y2 = Column(Float)
    floor_id = Column(ForeignKey(FloorMap.id, ondelete='CASCADE'))
    battery = Column(Float)


class DailyTemperature(Base):
    __tablename__ = 'sensor_dailytemperaturehumidity'

    id = Column(Integer, primary_key=True, autoincrement=True)
    temperature = Column(Float)
    humidity = Column(Float)
    timestamp = Column(DateTime(timezone=True))
    asset_id = Column(ForeignKey(
        TemperatureHumidity.id, ondelete='CASCADE'))


class WeeklyTemperature(Base):
    __tablename__ = 'sensor_weeklytemperaturehumidity'

    id = Column(Integer, primary_key=True, autoincrement=True)
    temperature = Column(Float)
    humidity = Column(Float)
    timestamp = Column(DateTime(timezone=True))
    asset_id = Column(ForeignKey(
        TemperatureHumidity.id, ondelete='CASCADE'))


class MonthlyTemperature(Base):
    __tablename__ = 'sensor_monthlytemperaturehumidity'

    id = Column(Integer, primary_key=True, autoincrement=True)
    temperature = Column(Float)
    humidity = Column(Float)
    timestamp = Column(DateTime(timezone=True))
    asset_id = Column(ForeignKey(
        TemperatureHumidity.id, ondelete='CASCADE'))


class IaqSensor(Base):
    __tablename__ = 'sensor_iaq'

    id = Column(Integer, primary_key=True, autoincrement=True)
    macid = Column(String(20))
    lastseen = Column(DateTime(timezone=True))
    battery = Column(Float)
    co2 = Column(Float)
    floor_id = Column(ForeignKey(FloorMap.id, ondelete='CASCADE'))
    tvoc = Column(Float)
    x = Column(Float)
    y = Column(Float)


class IaqDaily(Base):
    __tablename__ = "sensor_dailyiaq"

    id = Column(Integer, primary_key=True, autoincrement=True)
    co2 = Column(Float)
    tvoc = Column(Float)
    battery = Column(Float)
    timestamp = Column(DateTime(timezone=True))
    asset_id = Column(ForeignKey(IaqSensor.id, ondelete='CASCADE'))


class IaqWeekly(Base):
    __tablename__ = "sensor_weeklyiaq"

    id = Column(Integer, primary_key=True, autoincrement=True)
    co2 = Column(Float)
    tvoc = Column(Float)
    timestamp = Column(DateTime(timezone=True))
    asset_id = Column(ForeignKey(IaqSensor.id, ondelete='CASCADE'))


class IaqMonthly(Base):
    __tablename__ = "sensor_monthyiaq"

    id = Column(Integer, primary_key=True, autoincrement=True)
    co2 = Column(Float)
    tvoc = Column(Float)
    timestamp = Column(DateTime(timezone=True))
    asset_id = Column(ForeignKey(IaqSensor.id, ondelete='CASCADE'))


class SignalRepeater(Base):
    __tablename__ = 'signalrepeator_signalrepeator'

    id = Column(Integer, primary_key=True, autoincrement=True)
    macid = Column(String(20))
    lastseen = Column(DateTime(timezone=True))


""" creating a alert_alert class for accessing the alert_alert tables attributes """


class Alert(Base):
    __tablename__ = 'alert_alert'

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    asset_id = Column(ForeignKey(EmpRegistration.id, ondelete='CASCADE'))
    floor_id = Column(ForeignKey(FloorMap.id, ondelete='CASCADE'))


class Zones(Base):
    __tablename__ = 'zones_zones'

    id = Column(Integer, primary_key=True, autoincrement=True)
    x1 = Column(Float)
    y1 = Column(Float)
    x2 = Column(Float)
    y2 = Column(Float)
    floor_id = Column(ForeignKey(FloorMap.id, ondelete='CASCADE'))


""" ZoneTracking model: """


class ZoneTracking(Base):
    __tablename__ = 'zones_zonetracking'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    zoneid_id = Column(ForeignKey(Zones.id, ondelete='CASCADE'))
    tagid_id = Column(ForeignKey(EmpRegistration.id, ondelete='CASCADE'))


class MultiSensor(Base):
    __tablename__ = 'sensor_multisensor'

    id = Column(Integer, primary_key=True, autoincrement=True)
    MACID = Column(String(20))
    Temp = Column(Float)
    Humi = Column(Float)
    Co2 = Column(Float)
    PM1 = Column(Float)
    PM2 = Column(Float)
    PM4 = Column(Float)
    PM10 = Column(Float)
    NC0 = Column(Float)
    NC1 = Column(Float)
    NC2 = Column(Float)
    NC4 = Column(Float)
    NC10 = Column(Float)
    PtSize = Column(Float)
    O2 = Column(Float)
    VOC = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class VehicleTracking(Base):
    __tablename__ = 'vehicle_vehicletracking'

    id = Column(Integer, primary_key=True, autoincrement=True)
    mac = Column(String(20))
    x = Column(Float)
    y = Column(Float)
    battery = Column(Float)
    temperature = Column(Float)
    humidity = Column(Float)
    gateway = Column(String(50))
    vehicleid = Column(String(40))
    lastseen = Column(DateTime(timezone=True))
    timestamp = Column(Integer)


class TemperatureTracking(Base):
    __tablename__ = 'vehicle_TemperatureTracking'

    id = Column(Integer, primary_key=True, autoincrement=True)
    temperature = Column(Float)
    gateway = Column(String(50))
    lastseen = Column(DateTime(timezone=True))
