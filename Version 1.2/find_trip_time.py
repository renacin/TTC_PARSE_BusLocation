# Name:                                             Renacin Matadeen
# Student Number:                                         N/A
# Date:                                               02/20/2018
# Course:                                                 N/A
# Title                                   Calculate Trip Time For All Observations
#
#
#
#
#
# ----------------------------------------------------------------------------------------------------------------------

import pandas as pd

from combine_functions import combine_files_
from combine_functions import calculate_time_change
from combine_functions import calculate_heading_change
from combine_functions import calculate_unique_trip
from combine_functions import find_trip_duration

# ----------------------------------------------------------------------------------------------------------------------

# File Names & Variables That Will Be Worked With
lc = "/Users/Matadeen/Documents/Programming/Python/Threading/Data"
final_lc = "/Users/Matadeen/Documents/Programming/Python/Threading/Data/Final/"
route = 501

# ----------------------------------------------------------------------------------------------------------------------

# Create File That Will Contain Final Trip Durations
trip_dur_list = []


# Combine All files, And Find Unique IDs
combine_files_(lc, final_lc, route)
df = pd.read_csv(final_lc + "Data_Clean" + str(route) + ".csv")

# Focus On One Specific Route
df = df.loc[df['Route'] == route]
vehicles_IDs = list(df['Bus_IDs'].unique())

# Cycle Through Each ID
for vehicle in vehicles_IDs:

    # Select, And Organize Focus ID, And Save CSV
    focus_id_ = df.loc[df['Bus_IDs'] == int(vehicle)]
    focus_id_1 = focus_id_.sort_values('Epoch_Time', ascending=True)
    dataframe = focus_id_1.copy()

    # Create A CSV
    file_name = final_lc + "Data_Clean" + str(route) + ".csv"
    dataframe.to_csv(file_name, index=False)
    time_pairs = calculate_time_change(final_lc, route)

    # Read CSV
    ff = pd.read_csv(final_lc + "Data_Clean" + str(route) + ".csv")

    # Cycle Through Each Time Pairs
    for pair in time_pairs:
        pair = list(pair)

        # Also Must Accommodate For Fence Post Issue & Save
        focused_dataframe = ff[pair[0]:pair[1] + 1]
        focused_dataframe.to_csv(file_name, index=False)

        # Find Individual Trips Within Shift
        calculate_heading_change(final_lc, route)

        # Returns Trip Pairs
        trip_pairs = calculate_unique_trip(final_lc, route)

        # Calculate Time
        full_list = find_trip_duration(final_lc, route, trip_pairs)

        for observation in full_list:
            trip_dur_list.append(observation)

        del full_list

headers = ["Date", "Time", "Epoch", "Route", "Addi_Info", "ID", "Direction", "Time_To_Complete", "Distance", "Avg_Speed"]
final_dataframe = pd.DataFrame(trip_dur_list, columns=headers)
final_dataframe.to_csv(final_lc + "Data_Clean" + str(route) + ".csv", index=False)





















