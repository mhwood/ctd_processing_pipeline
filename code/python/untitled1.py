#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""



Created on Thu Jun 18 08:59:01 2026

@author: nataliemcgee
"""

from pyrsktools import RSK
import gsw
from ctd_file_template import ctd_netcdf_template as ctd
from write_ctd_netcdf import write_ctd_netcdf


# Create empty dictionaries
global_metadata = {}
variable_data = {}


# -------------------------------------------------------------------------
# Metadata to enter by hand: 
# -------------------------------------------------------------------------

# dataset details
global_metadata["title"] = "Example RBR CTD profile taken from .rsk file"
global_metadata["summary"] = "A single RBR CTD profile used to test NetCDF writing."
global_metadata["processing_level"] = "Quality Controlled"
global_metadata["processing_notes"] = "Describe the processing that occurred"
global_metadata["history"] = "Log of processing steps"

# project details
global_metadata["project"] = "2026 Research Cruise"
global_metadata["program"] = ""
global_metadata["platform"] = "R/V Black Pearl"

# contact details
global_metadata["creator_name"] = "Elizabeth Swann"
global_metadata["creator_email"] = "e.swann@dju.edu"
global_metadata["creator_institution"] = "Davy Jones University"
global_metadata["contact_name"] = "Captain Jack Sparrow"
global_metadata["contact_email"] = "itscaptainjacksparrow@dju.edu"
    
# location of cast 
latitude = 71       # degrees north
longitude = -51     # degrees east

# -----------------------------------------------------------------------------
# Additional metadata and the variable/profile data pulled from RSK file: 
# -----------------------------------------------------------------------------

# Instantiate an RSK class object, passing the path to an RSK file
rsk_file = "/Users/nataliemcgee/Downloads/206288_20260312_1232 Deep OG March 12, 2026.rsk"


with RSK(rsk_file) as rsk:

    # Access the data: 
    rsk.readdata()
    data = rsk.dataArrays[0]

    # Extract the variable data
    pressure = data["pressure"]
    temperature = data["temperature"]
    conductivity = data["conductivity"]
    insitu_temperature = data["temperature"]
    
    # If your RBR dataset includes a specific sea_pressure, you can skip this
    sea_pressure = pressure - 10.1325  # Account for surface atmospheric pres. (dbar)

    # Calculate derived variables
    depth = gsw.z_from_p(sea_pressure, latitude)
    practical_salinity = gsw.SP_from_C(conductivity, temperature, sea_pressure)
    absolute_salinity = gsw.SA_from_SP(practical_salinity, sea_pressure, longitude, latitude)
    potential_temperature = gsw.pt0_from_t(absolute_salinity, temperature, sea_pressure)
    
    # -------------------------------------------------------------------------
    # Calculate the length of the dimensions
    # -------------------------------------------------------------------------
    
    # length of depth dimension
    global_metadata["dimension_depth"] = (len(depth))
    
    # number of profiles
    global_metadata["dimension_profiles"] = 1 # This demo is for a .rsk file with 1 profile
    
    # -------------------------------------------------------------------------
    # Fill variable data
    # -------------------------------------------------------------------------

    variable_data["pressure"] = sea_pressure
    variable_data["temperature"] = insitu_temperature
    variable_data["conductivity"] = conductivity
    variable_data["practical_salinity"] = practical_salinity
    variable_data["potential_temperature"] = potential_temperature

    # -------------------------------------------------------------------------
    # Fill the additional global attribute metadata
    # -------------------------------------------------------------------------
    
    # what instrument was used
    global_metadata["instrument"] = (
        getattr(rsk.instrument, "model", None)
        if getattr(rsk, "instrument", None)
        else None
    )
    
    # instrument serial number
    global_metadata["serial_number"] = (
        getattr(rsk.instrument, "serialID", None)
        if getattr(rsk, "instrument", None)
        else None
    )

    # time coverage start
    global_metadata["time_coverage_start"] = (
        data["timestamp"][0]
        .astype("datetime64[ms]")
        .item()
        .isoformat()
    )

    # time coverage end  
    global_metadata["time_coverage_end"] = (
        data["timestamp"][-1]
        .astype("datetime64[ms]")
        .item()
        .isoformat()
    )

    
print('done')
print(global_metadata)
print(variable_data)







