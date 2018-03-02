Author:Renacin Matadeen
Email: renacin.matadeen@ryerson.ca
Date: 03/02/18
Title: TTC NextBus XML Parser
Version: 1.2

Purpose:
There are two main programs within this version. The first, is a comprehensive tool to parse data pertaining the number of vehicles on a particular TTC route, and save them to CSVs whose file size is less than 50KB. This was done in anticipation of system slow downs regarding growing memory demands, as file sizes got bigger. And, the second, a program that combines each subsequent file, and interprets each unique trip, as well as trip statistics such as time to complete trip, average speed - in KM/H, and distance between ends - in KM, and calculated using Vincenty's formulae. 

Version Note:
In this version multi-threading, or multiprocessing were not used as the focus was on developing a script that would be able to interpret unique trips for the entire dataset. 

General Note:
In the next version, an attempt to use processors - and processing, will be made.  

