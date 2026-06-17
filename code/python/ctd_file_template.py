import numpy as np


FILL_VALUE_FLOAT64 = np.nan


ctd_netcdf_template = {
    # ---------------------------------------------------------------------
    # Global NetCDF / CF metadata
    # ---------------------------------------------------------------------
    "attrs": {
        "title": "YOUR CTD DATASET TITLE",#XXXXX
        "summary": (#XXXXX
            "Short description of the dataset."
        ),
        "comments": (#XXXXX
            ""
        ),
        "convention": "CF-1.8",#XXXXX
        "featureType": "profile",
        "references": "",
        "processing_level": "",               # Quality Controlled
        "processing_notes": "",

        # Cast / cruise / instrument metadata
        "cast_id": None,                       # e.g., 109
        "platform": "YOUR_PLATFORM",           # e.g., "R/V Sanna"
        "instrument": "YOUR_CTD_MODEL",        # e.g., "SBE19plus"
        "serial_number": "YOUR_SERIAL_NUMBER",
        "seafloor_depth": "UNKNOWN",           # e.g., "475 m"
        "source": (
            "Conductivity, Temperature, and Depth (CTD) data collected "
            "from a ship-deployed CTD instrument."
        ),
        "history": "Describe processing steps used to create this file.",

        # People / organizations
        "creator_name": "YOUR NAME",#XXXXX
        "creator_email": "YOUR_EMAIL",#XXXXX
        "creator_type": "person",#XXXXX
        "creator_institution": "YOUR_INSTITUTION",
        "contact_name": "YOUR NAME",
        "contact_email": "YOUR_EMAIL",
        "institution": "YOUR_INSTITUTION",
        "project": "YOUR_PROJECT",#XXXXX
        "program": "YOUR_PROGRAM",
        "contributor_name": "NAME 1, NAME 2",
        "contributor_role": "author, principal investigator",
        "contributor_email": "email1@example.edu; email2@example.edu",

        # Keywords
        "keywords": "Conductivity, Salinity, Water Depth, Water Temperature",
        "keywords_vocabulary": (
            ""
        ),
        "standard_name_vocabulary": (
            "NetCDF Climate and Forecast (CF) Metadata Convention"
        ),

        # Rights / acknowledgement
        "acknowledgement": "YOUR_ACKNOWLEDGEMENT_TEXT",
        "license": "YOUR_LICENSE",

        # Geospatial/time coverage.
        # These can be filled manually or computed from coordinate data.
        "geospatial_lat_min": None,#XXXXX
        "geospatial_lat_max": None,#XXXXX
        "geospatial_lat_units": "degrees_north",#XXXXX
        "geospatial_lon_min": None,#XXXXX
        "geospatial_lon_max": None,#XXXXX
        "geospatial_lon_units": "degrees_east",#XXXXX
        "geospatial_vertical_min": None,#XXXXX
        "geospatial_vertical_max": None,#XXXXX
        "geospatial_vertical_units": "meters",#XXXXX
        "geospatial_vertical_positive": "down",#XXXXX
        "geospatial_vertical_resolution": 1,#XXXXX
        "geographic_coordinate_system": "WGS84",

        "time_coverage_start": None,           # e.g., "2018-08-25T18:00:08Z" #XXXXX
        "time_coverage_end": None,#XXXXX
        "time_coverage_duration": None,        # e.g., "P0DT0H19M26S"
        "time_coverage_resolution": None,      # e.g., "P0.25S"

        "date_created": None,                  # e.g., datetime.utcnow().isoformat()
        "coordinates": "time latitude longitude",
    },

    # ---------------------------------------------------------------------
    # Dimensions
    # ---------------------------------------------------------------------
    "dims": {
        # Main vertical profile dimension.
        # Set to len(data["coordinates"]["depth"]["data"]).
        "depth": None,

        # Usually one profile/cast per file.
        "profile": 1,
    },

    # ---------------------------------------------------------------------
    # Coordinate variables
    # ---------------------------------------------------------------------
    "coordinates": {
        "depth": {
            "dims": ("depth",),
            "dtype": "float64",
            "data": None,  # 1D array, meters
            "attrs": {
                "long_name": "depth",
                "standard_name": "depth",
                "units": "meters",
                "positive": "down",
                "axis": "Z",
                "coverage_content_type": "coordinate",
                "valid_min": 0.0,
                "valid_max": 0.0,
            },
        },

        "latitude": {
            "dims": ("profile",),
            "dtype": "float64",
            "data": None,  # 1-element array, e.g. np.array([76.165067])
            "attrs": {
                "long_name": "latitude",
                "standard_name": "latitude",
                "units": "degrees_north",
                "coverage_content_type": "coordinate",
                "axis": "Y",
                "valid_min": -90.0,
                "valid_max": 90.0,
                "comments": "Latitude of CTD location (dd.dddd).",
            },
        },

        "longitude": {
            "dims": ("profile",),
            "dtype": "float64",
            "data": None,  # 1-element array, e.g. np.array([-61.268183])
            "attrs": {
                "long_name": "longitude",
                "standard_name": "longitude",
                "units": "degrees_east",
                "coverage_content_type": "coordinate",
                "axis": "X",
                "valid_min": -180.0,
                "valid_max": 180.0,
                "comments": "Longitude of CTD location (dd.dddd).",
            },
        },

        "time": {
            "dims": ("profile",),
            "dtype": "int32",
            "data": None,  # usually np.array([0], dtype=np.int32)
            "attrs": {
                "long_name": "time",
                "standard_name": "time",
                "axis": "T",
                "coverage_content_type": "coordinate",
                "comment": "Time at which the CTD was deployed.",
                "units": "days since YYYY-MM-DD HH:MM:SS",
                "calendar": "proleptic_gregorian",
            },
        },
    },

    # ---------------------------------------------------------------------
    # CTD science variables
    # ---------------------------------------------------------------------
    "variables": {
        "pressure": {
            "dims": ("depth",),
            "dtype": "float64",
            "data": None,
            "attrs": {
                "_FillValue": FILL_VALUE_FLOAT64,
                "long_name": "sea water pressure",
                "standard_name": "sea_water_pressure",
                "units": "dbar",
                "valid_min": 0.0,
                "valid_max": 0.0,
                "comments": "",
            },
        },

        "temperature": {
            "dims": ("depth",),
            "dtype": "float64",
            "data": None,
            "attrs": {
                "_FillValue": FILL_VALUE_FLOAT64,
                "long_name": "in-situ sea water temperature (ITS-90)",
                "standard_name": "sea_water_temperature",
                "units": "degrees_C",
                "coverage_content_type": "physicalMeasurement",
                "seabird_var_name": "tv290C",
                "valid_min": 0.0,
                "valid_max": 0.0,
                "comments": "ITS-90",
                "coordinates": "",
            },
        },

        "conductivity": {
            "dims": ("depth",),
            "dtype": "float64",
            "data": None,
            "attrs": {
                "_FillValue": FILL_VALUE_FLOAT64,
                "long_name": "sea water electrical conductivity",
                "standard_name": "sea_water_electrical_conductivity",
                "units": "S/m",
                "coverage_content_type": "physicalMeasurement",
                "valid_min": 0.0,
                "valid_max": 0.0,
                "coordinates": "",
            },
        },

        "practical_salinity": {
            "dims": ("depth",),
            "dtype": "float64",
            "data": None,
            "attrs": {
                "_FillValue": FILL_VALUE_FLOAT64,
                "long_name": "sea water practical salinity",
                "standard_name": "sea_water_practical_salinity",
                "units": "1",
                "coverage_content_type": "physicalMeasurement",
                "valid_min": 0.0,
                "valid_max": 0.0,
                "coordinates": "",
            },
        },

        "potential_temperature": {
            "dims": ("depth",),
            "dtype": "float64",
            "data": None,
            "attrs": {
                "_FillValue": FILL_VALUE_FLOAT64,
                "long_name": "sea water potential temperature",
                "standard_name": "sea_water_potential_temperature",
                "units": "degrees_C",
                "coverage_content_type": "physicalMeasurement",
                "seabird_var_name": "potemp090C",
                "comments": "",
                "valid_min": 0.0,
                "valid_max": 0.0,
                "coordinates": "",
            },
        },
    },

    # ---------------------------------------------------------------------
    # Optional writer hints
    # ---------------------------------------------------------------------
    "encoding": {
        "default_fill_value": FILL_VALUE_FLOAT64,
        "unlimited_dims": [],
        "format": "NETCDF4",
        "compression": {
            "enabled": True,
            "zlib": True,
            "complevel": 4,
            "shuffle": True,
        },
    },
}
