# FUNCTION TO READ IN A STATION LOCATION FILE
# Same function as that used and written by Hilary R. Martens.

import numpy as np

def main(filename):
    lat,lon = np.loadtxt(filename,usecols=(0,1),unpack=True)
    sta = np.loadtxt(filename,usecols=(2,),dtype='U',unpack=True)
    return lat,lon,sta

