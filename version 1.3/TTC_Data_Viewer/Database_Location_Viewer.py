# Name:                                             Renacin Matadeen
# Student Number:                                         N/A
# Date:                                               03/15/2018
# Course:                                                 N/A
# Title                             From A Connected Database, View Points Spatially
#
#
#
#
#
# ----------------------------------------------------------------------------------------------------------------------

import time
import datetime
import psycopg2
import matplotlib

# Agg Will Be Used To Prevent A GUI from Being Rendered
matplotlib.use('Agg')

import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------------------------------------------------


def gather():
    # Gather Data From The Data Base & Create List
    # In this case Select Unique Obs Of Vehicles,
    gather_command = "SELECT DISTINCT ON (bus_ids) bus_ids, epoch_time, latitude, longitude, heading, add_info " \
                     "FROM TTC_data " \
                     "ORDER BY bus_ids, epoch_time DESC;"

    cursor.execute(gather_command)
    rows = cursor.fetchall()
    sel_data = rows
    del rows

    return sel_data


# ----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':

    # Connect To The Database
    try:
        connection = psycopg2.connect("dbname='TTC_Data_Test' user='postgres' "
                                      "host='host' password='password' port='port' ")
        connection.autocommit = True
        cursor = connection.cursor()

    except:
        print("Cannot connect to database")

    counter_x = 0
    while True:
        # Instantiate A Figure
        fig = plt.figure()
        plt.figure(figsize=(19, 10))
        plt.axis([-79.30, -79.55, 43.58, 43.72])
        plt.grid = True
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")

        time.sleep(5)
        # Gather Recent Points From The Database
        recent_locations = gather()
        ep_time = round((time.time()))

        # Change Title For User Feedback
        now = datetime.datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M")
        plt.title(str(date_time) + ":" + str(now.second))

        x_coord = []
        y_coord = []
        heading_coord = []

        # Things To Include
        obs_list = ["A", "bus", "buscon", "con", "default", "Lbus"]

        for obs in recent_locations:
            # Final Filter, Look For Fresh Data
            # Obs Older Than 30 Minutes Considered Stale, And No longer Viewed

            # Look For Streetcars Only
            if obs[5] in obs_list:
                if obs[1] < (ep_time - 1800):
                    pass
                else:
                    x_coord.append(obs[3])
                    y_coord.append(obs[2])
                    heading_coord.append(obs[4])
            else:
                pass

        counter_y = 0
        for x in x_coord:
            plt.plot(x_coord[counter_y], y_coord[counter_y], marker=(3, 0, int(heading_coord[counter_y])),
                     markersize=6, markeredgewidth=0.5, markeredgecolor="k", c="r", )

            # Currently Can Change The Size Of Annotations
            # plt.annotate(str(int(heading_coord[counter_y])), (x_coord[counter_y], y_coord[counter_y]))

            counter_y += 1

        counter_x += 1

        # Export Data
        plt.savefig('D:/MRP_Images/plot_' + str(counter_x) + '.png')
        plt.close("all")
        del fig





