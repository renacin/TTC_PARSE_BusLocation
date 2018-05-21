# Name:                                             Renacin Matadeen
# Student Number:                                        N/A
# Date:                                               05/15/2018
# Course:                                                N/A
# Title                                          PostgresSQL & Python
#
#
#
# ----------------------------------------------------------------------------------------------------------------------

import psycopg2
import multiprocessing
from pprint import pprint
import time

from Data_Collection import collect_data

# ----------------------------------------------------------------------------------------------------------------------

'''

Purpose: In this attempt, PostgresSQL will be used, in conjunction with Python, as a storage method for
real-time data. PostgresSQL will be used opposed to SQLite or other similar Databases, as it will allow for 
multiple concurrent connections, while allowing for continuous data collection

'''

# ----------------------------------------------------------------------------------------------------------------------


class DatabaseConnection:
    # Initialize the connection with the database

    # All functions, and methods will be stored within a class, this will make things easier down the line
    # Within the initial __init__ method, we will connect to the database, and create a cursor
    # Note when we call the DatabaseConnection() the init method is implicitly run

    # Connect To Database
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                "dbname='TTC_Data_Test' user='postgres' host='host' password='password' port='port' ")
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()

        except:
            pprint("Cannot connect to database")

    # Create a table within the database, must include pertinent columns
    def create_table(self):
        create_table_command = "CREATE TABLE TTC_Data(Date DATE," \
                               "Time varchar(25), " \
                               "Epoch_Time INTEGER, " \
                               "Dir_Tag INTEGER, " \
                               "Add_Info varchar(10), " \
                               "Route INTEGER, " \
                               "Bus_IDs INTEGER, " \
                               "Latitude REAL, " \
                               "Longitude REAL," \
                               "Heading INTEGER, " \
                               "Sec_Since INTEGER)"

        self.cursor.execute(create_table_command)

        # Write data to database. This function will take a cleaned list, and write the contents to
        # an awaiting database. This function should be object oriented as it will be used amongst
        # many processes.

    def write_to_db(self, var1):
        cleaned_list = var1

        # iterate through each object, and each subsequent item
        for item in cleaned_list:
            try:
                insert_command = "INSERT INTO TTC_Data(Date, " \
                                 "Time, Epoch_Time, Dir_Tag, " \
                                 "Add_Info, Route, Bus_IDs, " \
                                 "Latitude, Longitude, Heading, " \
                                 "Sec_Since) Values('" \
                                 + item[0] + "','" \
                                 + item[1] + "','" \
                                 + item[2] + "','" \
                                 + item[3] + "','" \
                                 + item[4] + "','" \
                                 + item[5] + "','" \
                                 + item[6] + "','" \
                                 + item[7] + "','" \
                                 + item[8] + "','" \
                                 + item[9] + "','" \
                                 + str(item[10]) + "')"

                self.cursor.execute(insert_command)

            except:
                pass

    def clean_db(self):
        # Delete Observations Older Than 2 Weeks, For Now 1 Day
        ep = round((time.time())) - 86400  # 1209600
        create_del_command = "DELETE FROM TTC_Data WHERE Epoch_Time <" + str(ep)
        self.cursor.execute(create_del_command)


def main_function(var_route):

    # Main Function With Integration With MultiProcessing
    # Since Multiprocessing Is Used, Little Concern Is Placed In Shared Memory Space

    rt = var_route
    ag = "ttc"

    # Using Dynamic Programming Create A Unique Connection To The Database
    exec("db_con_" + str(rt) + " = DatabaseConnection()")

    # Once Connected Start Parsing & Uploading Data
    # Added Try & Except To Stop When A Keyboard Interrupt Is Detected
    while True:

        try:
            time.sleep(0.5)
            ep = str(round((time.time())))
            cleaned_data = collect_data(ag, rt, ep)

            # Append Data To Database
            exec("db_con_" + str(rt) + ".write_to_db(cleaned_data)")

            # Clean Database, Remove Obs Older Than The Past 2 Weeks
            exec("db_con_" + str(rt) + ".clean_db()")

        except KeyboardInterrupt:
            print("Break Detected")
            break

        except:
            print(str(var_route) + " :Error")

    # Close The Connection
    exec("db_con_" + str(rt) + ".close()")


# ----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':

    # Connect To The Database
    database_connection = DatabaseConnection()

    # Add Tables If Not Present
    try:
        database_connection.create_table()

    except:
        pass

    # Search Parameters, Including List Of Routes To Focus On
    routes = ["501", "504", "505", "506", "509", "510", "511", "512", "514"]

    # Continuously collect data, and append to the database
    # Iterate Through Each Route And Set Up A Processing Node For It
    for route in routes:
        exec("p" + route + " = multiprocessing.Process(target=main_function, args=(route,)) ")

    # Once Multi Processing Has Been Set Up, Start All
    for route in routes:
        time.sleep(0.1)
        exec("p" + route + ".start()")







