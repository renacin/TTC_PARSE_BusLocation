# Name:                                             Renacin Matadeen
# Student Number:                                         N/A
# Date:                                               02/20/2018
# Course:                                                 N/A
# Title                                           Combine Multiple CSVs
#
#
#
#
#
# ----------------------------------------------------------------------------------------------------------------------

import numpy as np
import pandas as pd

from geopy.distance import vincenty
from os import listdir

# ----------------------------------------------------------------------------------------------------------------------


def combine_files_(lc, final_lc, route):

    # Create Main File That Will Contain All The Data, Should Have Identical Headings
    # Add "Epoch_Time"

    headers = ["Date", "Time", "Epoch_Time", "Dir_Tag", "Add_Info", "Route", "Bus_IDs", "Latitude", "Longitude",
               "Heading", "Sec_Since"]

    final_dataframe = pd.DataFrame(columns=headers)

    # Get List of CSV Files In Folder.
    files_in = listdir(lc)
    total_rows = 0
    clean_rows = 0

    for file in files_in:

        if ".csv" in file:

            # Read CSV Into Memory
            df1 = pd.read_csv(lc + "/" + file)

            rows = len(df1.index)
            total_rows += rows

            # Combine All Files, In The Case Of A New Attempt, Default To Concat Two Files
            try:
                frames = [df1, final_dataframe, final_df]
                final_df = pd.concat(frames)

            except:
                frames = [df1, final_dataframe]
                final_df = pd.concat(frames)

            # Things To Attend To
            final_df = final_df.replace(r'\s+', np.nan, regex=True)
            final_df = final_df.dropna()
            final_df = final_df.drop_duplicates()

            final_df = final_df[final_df.Route == route]
            final_df = final_df[final_df.Heading >= 0]

            # Just For Now, Focus, Sort
            # final_df = final_df[final_df.Bus_IDs == Bus_ID]

            final_df = final_df.sort_values('Epoch_Time', ascending=True)

            clean_rows_ = len(final_df.index)
            clean_rows += clean_rows_

        else:
            pass

    file_name = final_lc + "Data_Clean" + str(route) + ".csv"
    final_df.to_csv(file_name, index=False)


def calculate_heading_change(final_lc, route):
    file_name = final_lc + "Data_Clean" + str(route) + ".csv"
    df1 = pd.read_csv(file_name)

    # Create A List To Be Appended To The Main File, At The End
    counter_x = 0
    heading_list = []

    for index, row in df1.iterrows():

        try:
            h1 = (df1["Dir_Tag"][counter_x - 1])
            h2 = (df1["Dir_Tag"][counter_x])

            heading_change = abs(h2-h1)
            counter_x += 1

        except:
            heading_change = 0
            counter_x += 1

        heading_list.append(heading_change)

    df1["Direction_Change"] = pd.DataFrame({'H_C': heading_list})
    df1.to_csv(file_name, index=False)

    del counter_x


def calculate_time_change(final_lc, route):
    file_name = final_lc + "Data_Clean" + str(route) + ".csv"
    df1 = pd.read_csv(file_name)

    # Create A List To Be Appended To The Main File, At The End
    counter_y = 0
    heading_list = []

    # Calculate Time Change
    for index, row in df1.iterrows():
        try:
            h1 = (df1["Epoch_Time"][counter_y - 1])
            h2 = (df1["Epoch_Time"][counter_y])
            heading_change = abs(h2 - h1)
            counter_y += 1
        except:
            heading_change = 0
            counter_y += 1
        heading_list.append(heading_change)
    df1["Time_Change"] = pd.DataFrame({'T_C': heading_list})

    del counter_y
    df1.to_csv(file_name, index=False)

    id_frame = df1
    ending = (int(len(id_frame.index)) - 1)
    counter_x = 0
    begining_list = [0]
    ending_list = []

    # Identify Large Changes In Time, Identify Shift Change From GPS LAG
    for index, row in id_frame.iterrows():
        # If Time Greater Than 10MIN, or 600 SECS
        if id_frame["Time_Change"][counter_x] > 600:
            begining_list.append(int(counter_x))
            ending_list.append(int(counter_x - 1))
            counter_x += 1
        else:
            counter_x += 1

    ending_list.append(ending)
    time_pairs = []

    # Find The Time Pairs
    for x in range(len(begining_list)):
        temp_list = []
        temp_list.append(begining_list[x])
        temp_list.append(ending_list[x])
        time_pairs.append(temp_list)
        del temp_list

    return time_pairs


def calculate_unique_trip(final_lc, route):
    file_name = final_lc + "Data_Clean" + str(route) + ".csv"
    df1 = pd.read_csv(file_name)

    bus_id_frame = df1
    ending = (int(len(bus_id_frame.index)) - 1)

    counter_x = 0
    begining_list = [0]
    ending_list = []

    for index, row in bus_id_frame.iterrows():

        if bus_id_frame["Direction_Change"][counter_x] == 1:
            begining_list.append(int(counter_x))
            ending_list.append(int(counter_x - 1))
            counter_x += 1

        else:
            counter_x += 1

    ending_list.append(ending)
    trip_pairs = []

    for x in range(len(begining_list)):
        temp_list = []
        temp_list.append(begining_list[x])
        temp_list.append(ending_list[x])
        trip_pairs.append(temp_list)
        del temp_list

    return trip_pairs


def find_trip_duration(final_lc, route, t_ps):

    full_list = []

    file_name = final_lc + "Data_Clean" + str(route) + ".csv"
    data_frame_ = pd.read_csv(file_name)

    for pair in t_ps:
        temporary_list = []
        # Time Stamps
        t1 = int(data_frame_["Epoch_Time"][pair[0]])
        t2 = int(data_frame_["Epoch_Time"][pair[1]])

        # Time Elapsed
        ETA = t2 - t1

        date_var = data_frame_["Date"][pair[0]]
        time_var = data_frame_["Time"][pair[0]]
        epoch_var = data_frame_["Epoch_Time"][pair[0]]
        route_var = data_frame_["Route"][pair[0]]
        add_var = data_frame_["Add_Info"][pair[0]]
        bus_id_var = data_frame_["Bus_IDs"][pair[0]]
        dir_var = data_frame_["Dir_Tag"][pair[0]]
        lapsedtime_var = ETA/60
        time_hour = lapsedtime_var/60

        # Find Trip Distance, By Euclidean Measure
        coord_1_lat = data_frame_["Latitude"][pair[0]]
        coord_1_long = data_frame_["Longitude"][pair[0]]
        coord_1 = (coord_1_lat, coord_1_long)

        coord_2_lat = data_frame_["Latitude"][pair[1]]
        coord_2_long = data_frame_["Longitude"][pair[1]]
        coord_2 = (coord_2_lat, coord_2_long)

        distance_m = vincenty(coord_1, coord_2).meters
        distance = float(distance_m)/float(1000)
        distance = round(distance, 4)

        # Calculate Average_Speed
        try:
            speed = distance/float(time_hour)
            speed = round(speed, 2)

        except:
            speed = 0

        # Append Everything
        temporary_list.append(date_var)
        temporary_list.append(time_var)
        temporary_list.append(epoch_var)
        temporary_list.append(route_var)
        temporary_list.append(add_var)
        temporary_list.append(bus_id_var)
        temporary_list.append(dir_var)
        temporary_list.append(lapsedtime_var)
        temporary_list.append(distance)
        temporary_list.append(speed)

        full_list.append(temporary_list)

    return full_list




