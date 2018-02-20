# Name:                                             Renacin Matadeen
# Student Number:                                         N/A
# Date:                                               02/20/2018
# Course:                                                 N/A
# Title                                           Parse XML Information
#
#
#
#
#
# ----------------------------------------------------------------------------------------------------------------------

import time
import datetime
import urllib.request
import re
import pandas as pd
import os

# ----------------------------------------------------------------------------------------------------------------------


def get_transit_info(var1, var2, var3, var4, var5, name, lock):

    print_lock = lock

    with print_lock:

        # How much can a bus move in the time provided?
        time.sleep(0.5)

        # How Long Did This Take?
        start = time.time()

        # Initialize Variables
        agency = var1
        route = var2
        epoch_time = var3
        location = var4
        file_name = var5

        dt = str(datetime.datetime.now())
        dt_split = dt.split(" ")
        date = dt_split[0]
        time_var = dt_split[1]

        # Headers
        headers = ["Date", "Time", "Route", "Bus_IDs", "Latitude", "Longitude", "Heading", "Sec_Since"]

        try:
            df1 = pd.read_csv(location + file_name)

        except:
            df1 = pd.DataFrame(columns=headers)

        e_start = time.time()
        # Get Request, Data Only
        x = urllib.request.urlopen("http://webservices.nextbus.com/service/"
                                   "publicXMLFeed?command=vehicleLocations"
                                   "&a=" + agency +
                                   "&r=" + route +
                                   "&t=" + epoch_time)

        # Turn Data Into Text Blob
        text = str(x.read())
        e_end = time.time()

        # Find All Occurrences Of Vehicle IDs
        xml_parse = re.findall(r'<vehicle(.{110,170})>', text)

        # Final List To Append To
        final_list = []

        for x in xml_parse:

            # Temp List To Hold Variables
            temp_list = []

            # PARSE INFORMATION
            try:
                xml_bus_ids = re.search(r'id="([0-9]{1,5})" ', x).group(1)
            except:
                xml_bus_ids = ""

            try:
                xml_bus_lat = re.search(r'lat="([0-9]{1,2}\.[0-9]{4,7})" ', x).group(1)
            except:
                xml_bus_lat = ""

            try:
                xml_bus_long = re.search(r'lon="-([0-9]{1,2}\.[0-9]{4,7})" ', x).group(1)
                xml_bus_long = ("-" + xml_bus_long)
            except:
                xml_bus_long = ""

            try:
                xml_bus_heading = re.search(r'heading="(-?[0-9]{1,3})"', x).group(1)
            except:
                xml_bus_heading = ""

            try:
                xml_bus_sec_since = re.search(r'secsSinceReport="([0-9]{1,4})" ', x).group(1)
            except:
                xml_bus_sec_since = ""

            # APPEND INFORMATION
            temp_list.append(date)
            temp_list.append(time_var)
            temp_list.append(var2)
            temp_list.append(xml_bus_ids)
            temp_list.append(xml_bus_lat)

            # Note Must Add Back The Negative Value
            temp_list.append(xml_bus_long)
            temp_list.append(xml_bus_heading)
            temp_list.append(int(xml_bus_sec_since))

            final_list.append(temp_list)
            del temp_list, xml_bus_ids, xml_bus_lat, xml_bus_long, xml_bus_heading, xml_bus_sec_since

        df = pd.DataFrame(final_list, columns=headers)
        frames = [df1, df]
        final_df = pd.concat(frames)

        # Clean The DF Of Duplicates
        final_df = final_df.drop_duplicates()

        # Clean The DF Of Observations Based On Seconds Since GPS Recorder Call
        final_df_clean = final_df[final_df.Sec_Since == 1]

        print("Rows: " + str(len(final_df_clean.index)) + " , Thread: " + name)

        final_df_clean.to_csv(location + file_name, index=False)

        f_s = int(os.path.getsize(location + file_name))
        file_size = str(f_s / 1000)

        print("File Size: " + file_size + "Kb")

        # Elapsed Time
        end = time.time()
        time_elapsed = round((end - start), 4)
        e_elapsed = round((e_end - e_start), 4)

        process_time = round((time_elapsed - e_elapsed), 4)

        print("Site Access Time: " + str(e_elapsed))
        print("Process Time: " + str(process_time))
        print("")

        del final_list, final_df, final_df_clean

# ----------------------------------------------------------------------------------------------------------------------

