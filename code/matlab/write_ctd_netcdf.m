function write_ctd_netcdf(data,filename)
    ga = data.global_attributes;
    var = data.variables;
    dim = data.dimensions;

    % create netcdf file
    nc = netcdf.create(filename,'NETCDF4');

    % define dimensions
    dimid_prof = netcdf.defDim(nc,'profile',length(var.time.Values));
    dimid_depth = netcdf.defDim(nc,'depth',length(var.depth.Values));

    % define global attributes
    varid = netcdf.getConstant('NC_GLOBAL');
    ga_fn=fieldnames(ga);
    for i=1:length(ga_fn)
        netcdf.putAtt(nc,varid,ga_fn{i},ga.(ga_fn{i}))
    end
    if length(var.time.Values)>1
        netcdf.putAtt(nc,varid,'geospatial_lat_min',min(var.lat.Values))
        netcdf.putAtt(nc,varid,'geospatial_lat_max',max(var.lat.Values))
        netcdf.putAtt(nc,varid,'geospatial_lon_min',min(var.lat.Values))
        netcdf.putAtt(nc,varid,'geospatial_lon_max',max(var.lat.Values))
        netcdf.putAtt(nc,varid,'time_coverage_start',min(var.time.Values))
        netcdf.putAtt(nc,varid,'time_coverage_end',max(var.time.Values))
    else
        netcdf.putAtt(nc,varid,'geospatial_lat_min',var.lat.Values)
        netcdf.putAtt(nc,varid,'geospatial_lon_min',var.lat.Values)
        netcdf.putAtt(nc,varid,'geospatial_lat_min',var.lat.Values)
        netcdf.putAtt(nc,varid,'time_coverage_start',var.time.Values)
    end

    %define variables
    var_fn=fieldnames(var);
    for i=1:length(var_fn)
        dn=length(var.(var_fn{i}).Dimensions);
        for d=1:dn
            if strcmp(var.(var_fn{i}).Dimensions(d),'z')
                dim_id(d)=dimid_depth;
            elseif strcmp(var.(var_fn{i}).Dimensions(d),'profile')
                dim_id(d)=dimid_prof;
            end
        end
        if strcmp(var.(var_fn{i}).Datatype,'double')
            dt="NC_DOUBLE";
        elseif strcmp(var.(var_fn{i}).Datatype,'string')
            dt="NC_STRING";
        end
        varid(i)=netcdf.defVar(nc,var_fn{i},dt,dim_id);
        att_fn=fieldnames(var.(var_fn{i}).Attributes);
        for j=1:length(att_fn)
            if strcmp(att_fn{j},'FillValue')
                att='_FillValue';
            else
                att=att_fn{j};
            end
            netcdf.putAtt(nc,varid(i),att,var.(var_fn{i}).Attributes.(att_fn{j}));
        end
    end

    netcdf.endDef(nc)

    %write variables
    for i=1:length(var_fn)
        dn=length(var.(var_fn{i}).Dimensions);
        for d=1:dn
            if strcmp(var.(var_fn{i}).Dimensions(d),'z')
                dim_id(d)=dimid_depth;
            elseif strcmp(var.(var_fn{i}).Dimensions(d),'profile')
                dim_id(d)=dimid_prof;
            end
        end
        si=size(var.(var_fn{i}).Values); si=si(si~=1);
        netcdf.putVar(nc,varid(i),zeros(size(si)),si,var.(var_fn{i}).Values)
    end

    netcdf.close(nc)

end