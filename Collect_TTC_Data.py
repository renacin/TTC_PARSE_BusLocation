# Name:                                             Renacin Matadeen
# Student Number:                                         N/A
# Date:                                               02/03/2018
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

from XML_PARSE_FUNCTION import get_transit_info

# ----------------------------------------------------------------------------------------------------------------------

# Variables Of Focus
ag = "ttc"
rt_1 = "505"
lc = "/Users/Matadeen/Documents/Programming/Python/Threading/Data/"
fn = "TTC_XML_Parse_"

start_number = 0

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
                get_transit_info(ag, rt_1, ep, lc, nfn)

            except:
                pass


    except:
        headers = ["Date", "Time", "Route", "Bus_IDs", "Latitude", "Longitude", "Heading", "Sec_Since"]
        temp = pd.DataFrame(columns=headers)
        temp.to_csv(lc + nfn, index=False)

