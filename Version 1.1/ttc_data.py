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
import pandas as pd
import os
import threading

from parse_function import get_transit_info

# ----------------------------------------------------------------------------------------------------------------------


# Agency Tag
ag = "ttc"
lc = "/Users/Matadeen/Documents/Programming/Python/Threading/Data/"
fn = "TTC_XML_Parse_"

start_number = 0

print_lock = threading.Lock()

while True:

    nfn = fn + str(start_number) + ".csv"

    try:

        nfn_size = int(os.path.getsize(lc + nfn))
        nfn_size = int(nfn_size/1000)

        # If Greater Than 50KB
        if nfn_size > 50:
            start_number = start_number + 1

        else:

            try:
                ep = str(round((time.time())))

                t1 = threading.Thread(target=get_transit_info, name="Thread 1", args=(ag, "505", ep, lc,
                                                                                      nfn, "1", print_lock))

                t2 = threading.Thread(target=get_transit_info, name="Thread 1", args=(ag, "501", ep, lc,
                                                                                      nfn, "2", print_lock))

                t1.start()
                t1.join()

                t2.start()
                t2.join()

            except:
                pass


    except:
        headers = ["Date", "Time", "Route", "Bus_IDs", "Latitude", "Longitude", "Heading", "Sec_Since"]
        temp = pd.DataFrame(columns=headers)
        temp.to_csv(lc + nfn, index=False)

