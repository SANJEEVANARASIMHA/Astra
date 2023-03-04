MasterSelectAll = """ select id, gatewayid, floor_id FROM gateway_mastergateway"""
masterSelectQuery = """SELECT * FROM gateway_mastergateway WHERE  gatewayid = %s """
masterUpdateQuery = """update gateway_mastergateway set lastseen=%s where gatewayid=%s"""

slaveUpdateQuery = """update gateway_slavegateway set lastseen=%s where gatewayid=%s """

employeeSelectQuery = """SELECT * FROM employee_employeeregistration WHERE tagid = %s"""
empUpdateQuery = """update employee_employeeregistration set lastseen=%s, battery=%s, floor_id=%s, x=%s,y=%s where tagid=%s """

empAlertInsertQuery = """INSERT INTO alert_alert (value,timestamp,asset_id,floor_id) VALUES (%s, %s, %s, %s)"""

zoneSelectAll = """select * from zones_zones"""
zoneSelectQuery = """SELECT * FROM zones_zones where x1 < %s  and %s <= x2 and y1 < %s and %s <= y2  and floor_id = %s"""
zoneInsertQuery = """INSERT into zones_zonetracking (timestamp, tagid_id, zoneid_id) VALUES (%s, %s, %s) """

tempSensorSelectQuery = """SELECT * FROM sensor_temperaturehumidity where macid=%s"""
tempSensorUpdateQuery = """update sensor_temperaturehumidity set temperature=%s, humidity=%s, lastseen=%s, battery=%s where macid=%s """
tempSensorInsertQuery = """INSERT INTO sensor_dailytemperaturehumidity (temperature, humidity, timestamp, asset_id) VALUES (%s, %s, %s, %s)"""

signalRepeatorUpdateQuery = """update signalrepeator_signalrepeator set lastseen=%s where macid=%s """
