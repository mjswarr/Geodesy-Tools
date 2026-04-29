#!/usr/bin/python

# Matthew J Swarr April 2026
# Download Rinex Files for Select GPS Stations

# Import sys,os,subprocess so that we can use command line prompts
import sys,os
import subprocess
sys.path.append(os.getcwd())

# Import necessay python modules
import numpy as np
import datetime
from utility import read_station_file

# Define station file, data source, and date range to download rinex files

# Station File
sfile = ("./stations/Puget_Sound_Can.txt")

# Data source (1=NASA-CDDIS,2=GAGE)
dsource = 2

# Specify Date Range
frst_date = [2020,1,1,0,0,0]
last_date = [2020,12,31,0,0,0]

# Check if desired output directory exists
# If not, create it.
if not (os.path.isdir("./output/")):
    os.makedirs("./output/")
if not (os.path.isdir("./output/NASA-CDDIS/")):
    os.makedirs("./output/NASA-CDDIS/")
if not (os.path.isdir("./output/GAGE/")):
    os.makedirs("./output/GAGE/")

# Read in Station File
lat,lon,stations = read_station_file.main(sfile)

# Set up master array 
frstdt = datetime.datetime(frst_date[0],frst_date[1],frst_date[2],frst_date[3],frst_date[4],frst_date[5])
lastdt = datetime.datetime(last_date[0],last_date[1],last_date[2],last_date[3],last_date[4],last_date[5])
# date time object used to index dates of interest
dto = np.arange(frstdt, lastdt+datetime.timedelta(days=1), step=datetime.timedelta(days=1), dtype='datetime64').tolist()

# Current working directory
cwd = os.getcwd()

# Loop through each station in station file
stations = ['XMOC']
for i in range(0,len(stations)):

    # Current Station
    station = stations[i]
    #station = 'MYRA'
    print('Downloading data for station : ', station)
    # Download and Read in Time Series
    if (dsource == 1):
        for j in range(0,len(dto)):
            if not (os.path.isdir("./output/NASA-CDDIS/" + station + "/data/y" + str(dto[j].year) + "/d" + (format(dto[j],'%j')) + "/")):
                os.makedirs("./output/NASA-CDDIS/" + station + "/data/y" + str(dto[j].year) + "/d" + (format(dto[j],'%j')) + "/")
            cwd = os.getcwd()
            #print('Current Working Directory Top',cwd)
            ddir = (cwd + "/output/NASA-CDDIS/" + station + "/data/y" + str(dto[j].year) + "/d" + (format(dto[j],'%j')) + "/")
            os.chdir(ddir)
            filename = (station.lower() + (format(dto[j],'%j')) + "0." + str(dto[j].year)[2:] + "d.Z")
            filename2 = (station.lower() + (format(dto[j],'%j')) + "0." + str(dto[j].year)[2:] + "d.gz")
            if not os.path.isfile(filename):
                rnx_url = ("https://cddis.nasa.gov/archive/gnss/data/daily/" + str(dto[j].year) + "/" + (format(dto[j],'%j')) + "/" + str(dto[j].year)[2:] + "d/" + filename)
            if not os.path.isfile(filename2):
                 rnx_url2 = ("https://cddis.nasa.gov/archive/gnss/data/daily/" + str(dto[j].year) + "/" + (format(dto[j],'%j')) + "/" + str(dto[j].year)[2:] + "d/" + filename2)
            # Download Hatanaka Formatted Rinex File
            try:
                # Checking For File With .Z Extension
                os.system("wget --auth-no-challenge " + rnx_url)
                os.system("CRZ2RNX -d " + filename)
            except:
                continue
            try:
                # Checking For File With .gz Extension
                os.system("wget --auth-no-challenge " + rnx_url2)
                os.system("CRZ2RNX -d " + filename2)
            except:
                continue
            os.chdir(cwd)
    if (dsource == 2):
        for j in range(0,len(dto)):
            if not (os.path.isdir("./output/GAGE/" + station + "/data/y" + str(dto[j].year) + "/d" + (format(dto[j],'%j')) + "/")):
                os.makedirs("./output/GAGE/" + station + "/data/y" + str(dto[j].year) + "/d" + (format(dto[j],'%j')) + "/")
            cwd = os.getcwd()
            #print('Current Working Directory Top',cwd)
            ddir = (cwd + "/output/GAGE/" + station + "/data/y" + str(dto[j].year) + "/d" + (format(dto[j],'%j')) + "/")
            os.chdir(ddir)
            filename = (station.lower() + (format(dto[j],'%j')) + "0." + str(dto[j].year)[2:] + "d.Z")
            if not os.path.isfile(filename):
                rnx_url = ("https://gage-data.earthscope.org/archive/gnss/rinex/obs/" + str(dto[j].year) + "/" + (format(dto[j],'%j')) + "/" + filename)
            # provide access token to EarthScope Servers
            access = ' --header "Authorization: Bearer $(es sso access --token)"'
            # Download Hatanaka Formatted Rinex File
            try:
                # Checking For File With .Z Extension
                os.system("wget " + rnx_url + access)
                os.system("CRZ2RNX -d " + filename)
            except:
                continue
            os.chdir(cwd)
