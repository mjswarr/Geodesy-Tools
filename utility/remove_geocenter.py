import numpy as np

## Function to compute geocenter motion to align IGS20 timeseries with CF reference frame ##
## Annual and semi-annual geocenter motion derived from Altamami et al., 2023 ##

def main(decimal_year, station_lat, station_lon):
    # Convert input to numpy array if it's not already
    if not hasattr(decimal_year, '__iter__'):
        decimal_year = np.array([decimal_year])
    else:
        decimal_year = np.array(decimal_year)
    
    # Annual amplitude and phase (in degrees)
    annual_amp_x = 1.23
    annual_phase_x = -123.2
    annual_amp_y = 3.48
    annual_phase_y = 152.9
    annual_amp_z = 2.76
    annual_phase_z = -139.5
    
    # Semi-annual amplitude and phase (in degrees)
    semiannual_amp_x = 0.49
    semiannual_phase_x = 107.2
    semiannual_amp_y = 0.22
    semiannual_phase_y = 1.6
    semiannual_amp_z = 1.19
    semiannual_phase_z = 30.5
    
    # Calculate motion for each component in XYZ
    # Annual component
    x_motion = annual_amp_x * np.cos(2*np.pi*decimal_year - np.pi/180*annual_phase_x)
    y_motion = annual_amp_y * np.cos(2*np.pi*decimal_year - np.pi/180*annual_phase_y)
    z_motion = annual_amp_z * np.cos(2*np.pi*decimal_year - np.pi/180*annual_phase_z)
    
    # Semi-annual component
    x_motion += semiannual_amp_x * np.cos(4*np.pi*decimal_year - np.pi/180*semiannual_phase_x)
    y_motion += semiannual_amp_y * np.cos(4*np.pi*decimal_year - np.pi/180*semiannual_phase_y)
    z_motion += semiannual_amp_z * np.cos(4*np.pi*decimal_year - np.pi/180*semiannual_phase_z)
    
    # Convert degrees to radians for lat/lon
    lat = np.radians(station_lat)
    lon = np.radians(station_lon)
    
    # Rotation matrix for XYZ to ENU conversion
    R = np.array([
        [-np.sin(lon), np.cos(lon), 0],
        [-np.sin(lat)*np.cos(lon), -np.sin(lat)*np.sin(lon), np.cos(lat)],
        [np.cos(lat)*np.cos(lon), np.cos(lat)*np.sin(lon), np.sin(lat)]
    ])
    
    # Convert XYZ to ENU
    xyz = np.array([x_motion, y_motion, z_motion])
    enu = R @ xyz
    
    return enu[0]/1000,enu[1]/1000,enu[2]/1000
