# Utility Script to Convert MJD to Date Time for PyTide Processing
# Matthew J. Swarr May 30, 2024

from utility import jd_to_date
from utility import days_to_hmsm
import math
import datetime

def main(jd):
    """
    Convert a Julian Day to an `jdutil.datetime` object.
    
    Parameters
    ----------
    jd : float
        Julian day.
        
    Returns
    -------
    dt : `jdutil.datetime` object
        `jdutil.datetime` equivalent of Julian day.
    
    Examples
    --------
    >>> jd_to_datetime(2446113.75)
    datetime(1985, 2, 17, 6, 0)
    
    """
    year, month, day = jd_to_date.main(jd)
    
    frac_days,day = math.modf(day)
    day = int(day)
    
    hour,min,sec,micro = days_to_hmsm.main(frac_days)
    
    return datetime.datetime(year,month,day,hour,min,sec,micro)
