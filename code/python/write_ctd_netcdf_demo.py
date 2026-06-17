

import numpy as np
from ctd_file_template import ctd_netcdf_template as ctd
from write_ctd_netcdf import write_ctd_netcdf

# -------------------------------------------------------------------------
# Example fake CTD profile
# -------------------------------------------------------------------------
n_depth = 101

depth = np.arange(n_depth, dtype="float64")        # 0 to 100 m
pressure = depth * 1.01                            # fake dbar
temperature = 10.0 - 0.025 * depth                 # fake degrees C
conductivity = 3.0 + 0.002 * depth                 # fake S/m
salinity = 32.0 + 0.01 * depth                     # fake practical salinity
potential_temperature = temperature - 0.01         # fake potential temp

latitude = 76.165067
longitude = -61.268183
start_time = "2018-08-25 18:00:08"

file_name = "../../data/processed/test_from_python.nc"

# -------------------------------------------------------------------------
# Fill dimensions
# -------------------------------------------------------------------------
ctd["dims"]["depth"] = n_depth
ctd["dims"]["profile"] = 1

# -------------------------------------------------------------------------
# Fill coordinate data
# -------------------------------------------------------------------------
ctd["coordinates"]["depth"]["data"] = depth
ctd["coordinates"]["latitude"]["data"] = np.array([latitude], dtype="float64")
ctd["coordinates"]["longitude"]["data"] = np.array([longitude], dtype="float64")
ctd["coordinates"]["time"]["data"] = np.array([0], dtype="int32")
ctd["coordinates"]["time"]["attrs"]["units"] = f"days since {start_time}"

# -------------------------------------------------------------------------
# Fill science variable data
# -------------------------------------------------------------------------
ctd["variables"]["pressure"]["data"] = pressure
ctd["variables"]["temperature"]["data"] = temperature
ctd["variables"]["conductivity"]["data"] = conductivity
ctd["variables"]["practical_salinity"]["data"] = salinity
ctd["variables"]["potential_temperature"]["data"] = potential_temperature

# -------------------------------------------------------------------------
# Fill or compute useful global attributes
# -------------------------------------------------------------------------
ctd["attrs"]["title"] = "Example CTD profile written from Python"
ctd["attrs"]["summary"] = "Synthetic CTD profile used to test NetCDF writing."
ctd["attrs"]["processing_level"] = "Quality Controlled"
ctd["attrs"]["platform"] = "Example Vessel"
ctd["attrs"]["instrument"] = "Example CTD"

ctd["attrs"]["creator_name"] = "YOUR NAME"
ctd["attrs"]["creator_email"] = "YOUR_EMAIL"
ctd["attrs"]["creator_institution"] = "YOUR_INSTITUTION"
ctd["attrs"]["contact_name"] = "YOUR NAME"
ctd["attrs"]["contact_email"] = "YOUR_EMAIL"

ctd["attrs"]["geospatial_lat_min"] = latitude
ctd["attrs"]["geospatial_lat_max"] = latitude
ctd["attrs"]["geospatial_lon_min"] = longitude
ctd["attrs"]["geospatial_lon_max"] = longitude
ctd["attrs"]["geospatial_vertical_min"] = float(np.nanmin(depth))
ctd["attrs"]["geospatial_vertical_max"] = float(np.nanmax(depth))

ctd["attrs"]["time_coverage_start"] = "2018-08-25T18:00:08Z"
ctd["attrs"]["time_coverage_end"] = "2018-08-25T18:00:08Z"

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
out_file = write_ctd_netcdf(ctd, file_name)
print(f"Wrote {out_file}")
