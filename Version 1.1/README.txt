Author:Renacin Matadeen
Email: renacin.matadeen@ryerson.ca
Date: 02/20/18
Title: TTC NextBus XML Parser
Version: 1.1

Purpose:
This program was created in order to parse, and save bus locations, to a CSV file. It should be noted that this program, will only pull information in regards to one particular bus route. To elaborate, if the 505, bus route is entered within the final function, all busses currently operating on that route will be focused on. Additionally, since the function utilizes, a while loop, as well as current EPOCH timestamps, the most current locations will be focused on. Pandas was also used within this program, to help filter out old, and unneeded information.

Version Note:
In this version, multithreading was used to parse bus locations for two routes. However, due to a limitation in the Python Global Interpreter Lock, or better yet, the general method of operation, the speed of reading, cleaning, and writing was limited to that of  a linear program. True parallel programing was not achieved due to the fact that common variables, found within the parse function, as well as a common dump-file, the CSV, were used. Another big limitation, in terms of speed, was the time it took to access the XML site; this resulted in roughly 70% of the time to complete.

General Note:
In the next version, an attempt to use processors - and processing, the alternative to threading, will be used in order to create separate memory environments, this will be an attempt to speed up the entire process. 

