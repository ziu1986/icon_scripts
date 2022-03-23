import os, sys, glob
import numpy as np
import xarray as xr
import yaml

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

def init(config_file):
    # Read configuration
    with open(r'%s' % config_file) as file:
        config_list = yaml.load(file, Loader=yaml.FullLoader)
    file.close()
    return(config_list)

def main():
    # Configuration
    config = init('config.yml')
    src = config['input']
    target = config['output']
    fracts = config['fractions'] #np.array((0.7, 0.3*0.75, 0.3*0.25))
    old_name = config['old_variable']
    new_names = config['new_variables']#('fract_pft11', 'fract_pft12', 'fract_pft13')

    names = new_names
    names.insert(0,old_name)

    data = read_data(src)

    for ifract, iname in zip(fracts, names):
        pft_tmp = extend_landfrac(data[0], old_name, iname, ifract)
        data[0][iname] = pft_tmp

    data[0].to_netcdf(target)

if __name__ == "__main__":
    main()