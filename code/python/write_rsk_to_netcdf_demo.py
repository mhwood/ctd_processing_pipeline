#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""



Created on Thu Jun 18 08:59:01 2026

@author: nataliemcgee
"""

from pyrsktools import RSK
import gsw
import numpy as np
from ctd_file_template import ctd_netcdf_template as ctd
from write_ctd_netcdf import write_ctd_netcdf

# Instantiate an RSK class object, passing the path to an RSK file
rsk_file = "/Users/nataliemcgee/Downloads/206288_20260312_1232 Deep OG March 12, 2026.rsk"

# Output NetCDF4 filename
output_filename = "rbr_to_netcdf_example"

# -------------------------------------------------------------------------
# Metadata to enter by hand: 
# -------------------------------------------------------------------------

# dataset details
ctd["attrs"]["title"] = "Example RBR CTD profile taken from .rsk file"
ctd["attrs"]["summary"] = "A single RBR CTD profile used to test NetCDF writing."
ctd["attrs"]["processing_level"] = "Quality Controlled"
ctd["attrs"]["processing_notes"] = "Describe the processing that occurred"
ctd["attrs"]["history"] = "Log of processing steps"

# project details
ctd["attrs"]["project"] = "2026 Research Cruise"
ctd["attrs"]["program"] = ""
ctd["attrs"]["platform"] = "R/V Black Pearl"

# contact details
ctd["attrs"]["creator_name"] = "Elizabeth Swann"
ctd["attrs"]["creator_email"] = "e.swann@dju.edu"
ctd["attrs"]["creator_institution"] = "Davy Jones University"
ctd["attrs"]["contact_name"] = "Captain Jack Sparrow"
ctd["attrs"]["contact_email"] = "itscaptainjacksparrow@dju.edu"

# location of cast
latitude = 71       # degrees north
longitude = -51     # degrees east

# -----------------------------------------------------------------------------
# Additional metadata and the variable/profile data pulled from RSK file: 
# -----------------------------------------------------------------------------

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
    # Fill dimensions
    # -------------------------------------------------------------------------
    
    ctd["dims"]["depth"] = len(depth)
    ctd["dims"]["profile"] = 1  # This demo is for a .rsk file with 1 profile

    # -------------------------------------------------------------------------
    # Fill coordinate data
    # -------------------------------------------------------------------------
    
    start_time = data["timestamp"][0].astype("datetime64[ms]").item().isoformat()
    end_time = data["timestamp"][-1].astype("datetime64[ms]").item().isoformat()

    ctd["coordinates"]["depth"]["data"] = depth
    ctd["coordinates"]["latitude"]["data"] = np.array([latitude], dtype="float64")
    ctd["coordinates"]["longitude"]["data"] = np.array([longitude], dtype="float64")
    ctd["coordinates"]["time"]["data"] = np.array([0], dtype="int32")
    ctd["coordinates"]["time"]["attrs"]["units"] = f"days since {start_time}"

    # -------------------------------------------------------------------------
    # Fill science variable data
    # -------------------------------------------------------------------------
    
    ctd["variables"]["pressure"]["data"] = sea_pressure
    ctd["variables"]["temperature"]["data"] = insitu_temperature
    ctd["variables"]["conductivity"]["data"] = conductivity
    ctd["variables"]["practical_salinity"]["data"] = practical_salinity
    ctd["variables"]["potential_temperature"]["data"] = potential_temperature

    # -------------------------------------------------------------------------
    # Fill additional global attributes from RSK file
    # -------------------------------------------------------------------------

    # Instrument model
    ctd["attrs"]["instrument"] = (
        getattr(rsk.instrument, "model", None)
        if getattr(rsk, "instrument", None)
        else None
    )

    # Instrument serial number
    ctd["attrs"]["serial_number"] = (
        getattr(rsk.instrument, "serialID", None)
        if getattr(rsk, "instrument", None)
        else None
    )

    # Time coverage
    ctd["attrs"]["time_coverage_start"] = start_time
    ctd["attrs"]["time_coverage_end"] = end_time
    
    # Vertical coverage
    ctd["attrs"]["geospatial_vertical_min"] = float(np.nanmin(depth))
    ctd["attrs"]["geospatial_vertical_max"] = float(np.nanmax(depth))

    
# -------------------------------------------------------------------------
# Optionally update valid_min / valid_max from the actual arrays
# -------------------------------------------------------------------------

ctd["coordinates"]["depth"]["attrs"]["valid_min"] = float(np.nanmin(depth))
ctd["coordinates"]["depth"]["attrs"]["valid_max"] = float(np.nanmax(depth))

for name in [
    "pressure",
    "temperature",
    "conductivity",
    "practical_salinity",
    "potential_temperature",
]:
    values = np.asarray(ctd["variables"][name]["data"])
    ctd["variables"][name]["attrs"]["valid_min"] = float(np.nanmin(values))
    ctd["variables"][name]["attrs"]["valid_max"] = float(np.nanmax(values))

# -------------------------------------------------------------------------
# Write file
# -------------------------------------------------------------------------
out_file = write_ctd_netcdf(ctd, output_filename)
print(f"Wrote {out_file}")








