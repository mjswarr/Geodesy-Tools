#!/usr/bin/python

## Need to alter this script so that it takes in the station to be processed, start time, and end time ##
## This way we can submit multiple job requests at once ##
## Hopefully the reference position sit.xyz file does not causes issues ##

# Matthew J Swarr 22 May, 2024
# Structure of script based upon analyze_gps.py written by HRM
# Kinematic Processing of GNSS Data Using PRIDE-PPPAR

## NOTE TO SELF: This script will currently process one station at a time. Need to alter so that this script can be passed a station  of interest and the time range to process the data ##
## This allows us to process multiple stations at once ##

# Import sys,os,subprocess so we can use command line prompts
import sys,os
import glob
import subprocess
sys.path.append(os.getcwd())

# Import python modules needed to run code
import numpy as np
import pandas as pd
from scipy import signal
import datetime
#from utility import read_station_file
from utility import jd_to_datetime
from utility import backwards_smoothing

# Define station file, date range of interest

# Station file (Lat,Lon,StaId)
# We only need the station ID to run this script
#sfile = ("./stations/Puget_Sound_Can.txt")

# Date range to process data (YYYY,MM,DD,HH,MM,SS)
frst_date = [2016,1,1,0,0,0]
last_date = [2016,12,31,0,0,0]

# Read in Station File
#lat,lon,stations = read_station_file.main(sfile)

# Set up master array
frstdt = datetime.datetime(frst_date[0],frst_date[1],frst_date[2],frst_date[3],frst_date[4],frst_date[5])
lastdt = datetime.datetime(last_date[0],last_date[1],last_date[2],last_date[3],last_date[4],last_date[5])
# date time object used to index dates
dto = np.arange(frstdt, lastdt+datetime.timedelta(days=1), step=datetime.timedelta(days=1), dtype='datetime64').tolist()

# Current working directory
cwd = os.getcwd()

# Loop through Stations
stations = ['CPXX']
for i in range(0,len(stations)):

    # Current Station
    station = stations[i]
    print('Currently working on station : ', station)
    # Kinematic positioning using PRIDE-PPPAR for each day
    # Need to alter so if there is a date with no data then the loop will continue and not break.
    for j in range(0,len(dto)):
        print(station.lower() + (format(dto[j],'%j')) + "0." + str(dto[j].year)[2:] + "o")
        #filename = f"test/{station.lower() + format(dto[j], '%j') + '0.' + str(dto[j].year)[2:] + 'o'}"
        filename = f"../../gnss-data/{station}/data/y{format(dto[j], '%Y')}/d{format(dto[j], '%j')}/{station.lower() + format(dto[j], '%j') + '0.' + str(dto[j].year)[2:] + 'o'}"
        print(filename)
        command = f"pdp3 -sys G -frq G12 -m P300 -i 30 -c 7 -hion -p V3 -toff O -z S 0.00005 -h S 0.000005 {filename}"
        # Run the command (be cautious of shell injection vulnerabilities)
        try:
            os.system(command)
        # If data is not present for a given day continue rather than break loop
        except:
            continue
        # Convert XYZ output file to ENU
        filename = f"{format(dto[j],'%Y')}/{format(dto[j], '%j')}/{'kin_' + format(dto[j], '%Y') + format(dto[j], '%j') + '_' + station.lower()}"
        filename_enu = f"{format(dto[j],'%Y')}/{format(dto[j], '%j')}/{'kin_' + format(dto[j], '%Y') + format(dto[j], '%j') + '_' + station.lower() + '_enu'}"
        command = f"xyz2enu {filename} {filename_enu}"
        try:
            print(": Converting XYZ to ENU :")
            os.system(command)
        except:
            continue
    
    # Compile ENU Observations into master file
    all_files = sorted(glob.glob(os.path.join(format(dto[j],'%Y')+"/???/*_" + station.lower() + "_enu")))

    df_full = []

    for filename in all_files:
        df = pd.read_csv(filename,delim_whitespace=True,usecols=[0,1,2,3,4,8],header=None)
        df_full.append(df)

    df_full = pd.concat(df_full, axis=0, ignore_index=True)
    df_full['Date'] = 0

    for i in range(0,len(df_full)):
        df_full['Date'].loc[i] = jd_to_datetime.main(((df_full[0] + df_full[1]/(24*60*60)) + 2400000.5)[i])
    df_full['Date'] = pd.to_datetime(df_full['Date'])

    # Create columns needed for PyTide with 'standard' file structure
    # YYYY MM DD hh mm ss E N U err
    df_full[13] = df_full['Date'].dt.year
    df_full[14] = df_full['Date'].dt.month
    df_full[15] = df_full['Date'].dt.day
    df_full[16] = df_full['Date'].dt.hour
    df_full[17] = df_full['Date'].dt.minute
    df_full[18] = df_full['Date'].dt.second
    df_full.drop(columns=['Date'],inplace=True)
    df_full.drop(columns=[0,1],inplace=True)

    # Reorganizing dataframe
    df_full = df_full.iloc[:,[4,5,6,7,8,9,0,1,2,3]]
    
    # Rounding some times so each datapoint is spaced by 300 seconds
    df_full[17][df_full[18] == 59] += 1
    df_full[16][df_full[17] ==60] += 1
    df_full[17][df_full[17] == 60] = 0
    df_full[18][df_full[18] == 59] = 0
    

    # Window size for backwards smoothing
    # Converting units from m to mm to be consistent with desired structure for PyTide
    #window_size = 12 # 30 minutes
    #df_full[2] = signal.savgol_filter(df_full[2]*1000,window_size,2,mode='interp')
    #df_full[3] = signal.savgol_filter(df_full[3]*1000,window_size,2,mode='interp')
    #df_full[4] = signal.savgol_filter(df_full[4]*1000,window_size,2,mode='interp')
    
    # Check if desired output directory exists
    # If not, create it. Similar to LoadDef scripts
    if not (os.path.isdir("./output/")):
        os.makedirs("./output/")
    if not (os.path.isdir("./output/" + station + "/")):
        os.makedirs("./output/" + station + "/")
    if not (os.path.isdir("./output/" + station + "/" + format(dto[j],'%Y') + "/")):
        os.makedirs("./output/" + station + "/" + format(dto[j],'%Y') + "/")
   
    # Output file for specific year data is being procssed
    df_full.to_csv("./output/" + station + "/"  + format(dto[j],'%Y') + "/" + station + "_" + format(dto[j],'%Y'),header=None,sep=' ',index=False,mode='w')

    # Output file for full time period of interest (writing file in append mode)
    df_full.to_csv("./output/" + station + "/" + station, header=None,sep=' ',index=False,mode='a') 
