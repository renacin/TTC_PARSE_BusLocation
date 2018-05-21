# Name:                                             Renacin Matadeen
# Student Number:                                         N/A
# Date:                                               03/15/2018
# Course:                                                 N/A
# Title                           Parse XML Information W/ MultiProcessing - Primary Function
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

# ----------------------------------------------------------------------------------------------------------------------


def collect_data(var1, var2, var3):
    # Parse data & insert into database
    agency = var1
    route = var2
    epoch_time = var3

    dt = str(datetime.datetime.now())
    dt_split = dt.split(" ")
    date = dt_split[0]
    time_var = dt_split[1]

    # Get Request, Data Only
    x = urllib.request.urlopen("http://webservices.nextbus.com/service/"
                               "publicXMLFeed?command=vehicleLocations"
                               "&a=" + agency +
                               "&r=" + route +
                               "&t=" + epoch_time)

    # Turn Data Into Text Blob
    text = str(x.read())

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
            # 8 - 15 characters
            xml_dir_tag = re.search(r'dirTag="(.{8,20})" ', x).group(1)
            xml_dir_tag = xml_dir_tag.split("_")

            dir_tag = xml_dir_tag[1]
            add_in = xml_dir_tag[2]
            add_info = add_in.replace(str(route), "")

            if add_info == "":
                add_info = "default"

            else:
                pass

        except:
            dir_tag = ""
            add_info = ""

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
        temp_list.append(epoch_time)
        temp_list.append(dir_tag)
        temp_list.append(add_info)
        temp_list.append(var2)
        temp_list.append(xml_bus_ids)
        temp_list.append(xml_bus_lat)

        # Note Must Add Back The Negative Value
        temp_list.append(xml_bus_long)
        temp_list.append(xml_bus_heading)
        temp_list.append(int(xml_bus_sec_since))

        final_list.append(temp_list)
        del temp_list, xml_bus_ids, xml_bus_lat, xml_bus_long, xml_bus_heading, xml_bus_sec_since, dir_tag

    # Ensuring clean data is collected; isolating for points that have been observed within the past 3 seconds,
    # and removing values where the heading is -4 (an error)

    clean_list = []
    for num_val in range(len(final_list)):

        temp_focus = final_list[num_val]
        t_heading = temp_focus[9]
        t_sec_since = temp_focus[10]

        if t_heading == "-4" or t_sec_since > 1:
            pass

        else:
            clean_list.append(temp_focus)

    return clean_list


# ----------------------------------------------------------------------------------------------------------------------
