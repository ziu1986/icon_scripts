import os, sys, glob
import numpy as np
import xarray as xr

def extend_landfrac(data, var_name, var_name_new, fract):
    xr.set_options(keep_attrs=True)
    var_orig = data[var_name]
    var_new = var_orig.copy()*fract
    var_new.name = var_name_new
    var_new.assign_attrs(long_name= var_new.long_name.replace(var_name[:-2], var_name_new[:-2]))
    return var_new

def read_data(src):
    data = []
    for each in sorted(glob.glob(src)):
        data.append(xr.open_dataset(each))
    return data


src = os.environ['DATA'] + "/icon/pool/data/ICON/grids/private/jsbach/mpim/0013/land/r0001/*11pfts*"

fracts = np.array((0.7, 0.3*0.75, 0.3*0.25))
new_names = ('fract_pft11', 'fract_pft12', 'fract_pft13')

data = read_data(src)

for ifract, iname in zip(fracts, new_names):
    pft_tmp = extend_landfrac(data[0], "fract_pft11", iname, ifract)
    data[0][iname] = pft_tmp

data[0].to_netcdf("bc_land_frac_13pfts_1979.nc")