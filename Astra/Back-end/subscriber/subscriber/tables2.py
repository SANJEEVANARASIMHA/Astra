import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, LargeBinary, ForeignKey, DateTime
from sqlalchemy.sql import func

Base = declarative_base()

""" creating a common_map class for accessing the common_map objects and  attributes """


class SensorReading(Base):
    __tablename__ = 'weightsensor_sensorreading'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tagid = Column(String(200))
    reading = Column(Float)
    distancelader = Column(Float)
    dcstatus = Column(Integer)
    battery = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class SensorDaily(Base):
    __tablename__ = 'weightsensor_sensordaily'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tagid = Column(String(200))
    reading = Column(Float)
    distancelader = Column(Float)
    dcstatus = Column(Integer)
    battery = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
