import os, sys, glob
import numpy as np
import xarray as xr
import yaml

def extend_frac(data, var_name, var_name_new, fract):
    xr.set_options(keep_attrs=True)
    var_orig = data[var_name]
    var_new = var_orig.copy()*fract
    var_new.name = var_name_new
    try:
        var_new.assign_attrs(long_name= var_new.long_name.replace(var_name[:-2], var_name_new[:-2]))
    except AttributeError:
        print("Extending transitions...")

    return var_new

def read_data(src):
    data = []
    for each in sorted(glob.glob(src)):
        print("Reading %s" % (src))
        data.append(xr.open_dataset(each, decode_times=False))
    return data

def init(config_file):
    # Read configuration
    with open(r'%s' % config_file) as file:
        config_list = yaml.load(file, Loader=yaml.FullLoader)
    file.close()
    return(config_list)

def save_data(data, target):
    print("Saving... %s" % (target))
    data.to_netcdf(target)

def main():
    # Configuration
    config = init('config.yml')
    src = config['input']
    target = config['output']
    fracts = config['fractions']
    old_name = config['old_variable']
    new_names = config['new_variables']

    names = new_names
    names.insert(0,old_name)

    data = read_data(src)
    
    print("Converting...")

    for ifract, iname in zip(fracts, names):
        print("%s x %1.3f -> %s" % (old_name, ifract, iname))
        pft_tmp = extend_frac(data[0], old_name, iname, ifract)
        data[0][iname] = pft_tmp

    save_data(data[0], target)

if __name__ == "__main__":
    main()