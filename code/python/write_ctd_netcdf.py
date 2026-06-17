
from datetime import datetime, timezone

import numpy as np
from netCDF4 import Dataset


def _clean_attr_value(value):
    """
    NetCDF attributes cannot be None.
    Convert None to empty string and NumPy scalars to Python scalars.
    """
    if value is None:
        return ""
    if isinstance(value, np.generic):
        return value.item()
    return value


def _write_attrs(nc_obj, attrs):
    """
    Write attributes to either a Dataset or Variable.
    Skip _FillValue because netCDF4 requires it during createVariable().
    """
    for key, value in attrs.items():
        if key == "_FillValue":
            continue
        nc_obj.setncattr(key, _clean_attr_value(value))


def _get_fill_value(var_spec, template):
    """
    Get variable-specific _FillValue, falling back to template default.
    Return None if no fill value should be used.
    """
    attrs = var_spec.get("attrs", {})
    fill_value = attrs.get(
        "_FillValue",
        template.get("encoding", {}).get("default_fill_value", None),
    )

    # netCDF4 can handle np.nan as a floating _FillValue.
    if fill_value is None:
        return None

    return fill_value


def _compression_kwargs(template):
    """
    Convert template compression settings into createVariable kwargs.
    """
    compression = template.get("encoding", {}).get("compression", {})

    if not compression.get("enabled", False):
        return {}

    return {
        "zlib": compression.get("zlib", True),
        "complevel": compression.get("complevel", 4),
        "shuffle": compression.get("shuffle", True),
    }


def _validate_template(template):
    """
    Basic validation before writing.
    """
    dims = template["dims"]

    for dim_name, dim_len in dims.items():
        if dim_len is None:
            raise ValueError(f"Dimension {dim_name!r} is None.")

    for section_name in ("coordinates", "variables"):
        for var_name, var_spec in template[section_name].items():
            data = var_spec.get("data", None)

            if data is None:
                raise ValueError(
                    f"{section_name}.{var_name}.data is None. "
                    f"Fill this before writing."
                )

            arr = np.asarray(data)
            var_dims = var_spec.get("dims", ())

            expected_shape = tuple(dims[dim] for dim in var_dims)

            if arr.shape != expected_shape:
                raise ValueError(
                    f"{section_name}.{var_name} has shape {arr.shape}, "
                    f"expected {expected_shape} from dims {var_dims}."
                )


def write_ctd_netcdf(template, output_path="test_from_python.nc"):
    """
    Write a CTD NetCDF file from the nested dictionary template.

    Parameters
    ----------
    template : dict
        Filled CTD NetCDF dictionary.
    output_path : str
        Output NetCDF filename.

    Returns
    -------
    str
        Path to the written NetCDF file.
    """
    _validate_template(template)

    nc_format = template.get("encoding", {}).get("format", "NETCDF4")
    unlimited_dims = set(template.get("encoding", {}).get("unlimited_dims", []))
    compress_kwargs = _compression_kwargs(template)

    with Dataset(output_path, mode="w", format=nc_format) as ds:
        # ---------------------------------------------------------------
        # Dimensions
        # ---------------------------------------------------------------
        for dim_name, dim_len in template["dims"].items():
            if dim_name in unlimited_dims:
                ds.createDimension(dim_name, None)
            else:
                ds.createDimension(dim_name, dim_len)

        # ---------------------------------------------------------------
        # Global attributes
        # ---------------------------------------------------------------
        global_attrs = dict(template.get("attrs", {}))
        global_attrs["filename"] = output_path

        if not global_attrs.get("date_created"):
            global_attrs["date_created"] = datetime.now(
                timezone.utc
            ).strftime("%Y-%m-%dT%H:%M:%SZ")

        _write_attrs(ds, global_attrs)

        # ---------------------------------------------------------------
        # Coordinate variables
        # ---------------------------------------------------------------
        for var_name, var_spec in template.get("coordinates", {}).items():
            dtype = var_spec.get("dtype", "float64")
            dims = var_spec.get("dims", ())
            data = np.asarray(var_spec["data"], dtype=dtype)

            fill_value = _get_fill_value(var_spec, template)

            # Usually coordinate variables should not be compressed or filled.
            create_kwargs = {}
            if fill_value is not None and "_FillValue" in var_spec.get("attrs", {}):
                create_kwargs["fill_value"] = fill_value

            var = ds.createVariable(
                var_name,
                dtype,
                dims,
                **create_kwargs,
            )

            _write_attrs(var, var_spec.get("attrs", {}))
            var[:] = data

        # ---------------------------------------------------------------
        # Science/data variables
        # ---------------------------------------------------------------
        for var_name, var_spec in template.get("variables", {}).items():
            dtype = var_spec.get("dtype", "float64")
            dims = var_spec.get("dims", ())
            data = np.asarray(var_spec["data"], dtype=dtype)

            fill_value = _get_fill_value(var_spec, template)

            create_kwargs = dict(compress_kwargs)

            if fill_value is not None:
                create_kwargs["fill_value"] = fill_value

            var = ds.createVariable(
                var_name,
                dtype,
                dims,
                **create_kwargs,
            )

            _write_attrs(var, var_spec.get("attrs", {}))
            var[:] = data

    return output_path
