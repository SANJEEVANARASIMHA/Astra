import mysql.connector
import datetime
from time import strftime, gmtime

# import statement for creating logs
import yaml
import logging.config

import configparser


def distance_calculation():
    try:
        config = configparser.RawConfigParser()
        config.read('../utils/db_details.properties')

        host = config.get('DatabaseSection', 'database.host')
        dbname = config.get('DatabaseSection', 'database.dbname')
        user = config.get('DatabaseSection', 'database.user')
        password = config.get('DatabaseSection', 'database.password')

        # Creating database connection object and connecting to data base
        db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=dbname
        )

        cursor = db.cursor()

        tag1_qry = "select distinct(tag1_id) from employee_distancetracking"
        cursor.execute(tag1_qry)
        tag1_list = cursor.fetchall()

        for tag1 in tag1_list:
            tag2_qry = "select distinct(tag2_id) from employee_distancetracking where tag1_id=%s"
            cursor.execute(tag2_qry, tag1)
            tag2_list = cursor.fetchall()

            for tag2 in tag2_list:
                datalist = "select timestamp from employee_distancetracking where tag1_id={} and tag2_id={}".format(
                    tag1[0], tag2[0])
                cursor.execute(datalist)
                data = cursor.fetchall()

                if len(data) > 1:
                    start = data[0][0]
                    tempstart = data[0][0]
                    end = data[0][0]
                    i = 1
                    temp = 1

                    while i < len(data):
                        end = data[i][0]

                        if (end - tempstart).total_seconds() <= 31:
                            tempstart = data[i][0]
                            temp = temp + 1

                        else:
                            emp = 'select id, name from employee_employeeregistration where id={}'.format(
                                tag1[0])
                            cursor.execute(emp)
                            emp1 = cursor.fetchone()
                            emp = 'select name from employee_employeeregistration where id={}'.format(
                                tag2[0])
                            cursor.execute(emp)
                            emp2 = cursor.fetchone()
                            dur = (end - start).total_seconds()
                            if emp1 and emp2:
                                qry = 'insert into employee_distancecalculation(empid, name1, name2, starttime, endtime, duration) values(%s, %s, %s, %s, %s, %s)'
                                var = (emp1[0], emp1[1], emp2[0], start,
                                       end, strftime("%H:%M:%S", gmtime(dur)))
                                cursor.execute(qry, var)
                                db.commit()
                            start = data[i][0]
                        i = i + 1

                    if temp == len(data):
                        emp = 'select id, name from employee_employeeregistration where id={}'.format(
                            tag1[0])
                        cursor.execute(emp)
                        emp1 = cursor.fetchone()
                        emp = 'select name from employee_employeeregistration where id={}'.format(
                            tag2[0])
                        cursor.execute(emp)
                        emp2 = cursor.fetchone()
                        dur = (end - start).total_seconds()
                        if emp1 and emp2:
                            qry = 'insert into employee_distancecalculation(empid, name1, name2, starttime, endtime, duration) values(%s, %s, %s, %s, %s, %s)'
                            var = (emp1[0], emp1[1], emp2[0], start,
                                   end, strftime("%H:%M:%S", gmtime(dur)))
                            cursor.execute(qry, var)
                            db.commit()

            logger.info("Inserted data into distance table.")

    except Exception as error:
        logger.info("Error: ", str(error))

    finally:
        cursor.close()


if __name__ == '__main__':
    with open('../logs/logging_distancetracking.yaml', 'r') as stream:
        logger_config = yaml.load(stream, yaml.FullLoader)
    logging.config.dictConfig(logger_config)
    logger = logging.getLogger('GroundFloor -')
    distance_calculation()
