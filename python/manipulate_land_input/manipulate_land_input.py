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
    datalist = []
    infilenamelist = []
    for each in sorted(glob.glob(src)):
        print("Reading %s" % (src))
        datalist.append(xr.open_dataset(each, decode_times=False))
        infilenamelist.append(each)
    return datalist, infilenamelist

def init(config_file):
    # Read configuration
    with open(r'%s' % config_file) as file:
        config_list = yaml.load(file, Loader=yaml.FullLoader)
    file.close()
    return(config_list)

def save_data(data, target):
    print("Saving... %s" % (target))
    data.to_netcdf(target)

def generate_outname(infilename, outfilename, **karg):
    if outfilename == "":
        return("new_" + os.path.basename(infilename))
    elif outfilename.find('.nc') < 0:
        return(outfilename + '_' + os.path.basename(infilename))
    else:
        return(outfilename)

def main():
    # Configuration
    if len(sys.argv) == 1:
        config_file = 'config.yml'
    else:
        config_file = sys.argv[1]

    config = init(config_file)
    src = config['input']
    target = config['output']
    fracts = config['fractions']
    old_name = config['old_variable']
    new_names = config['new_variables']

    names = new_names
    names.insert(0,old_name)

    data, infilenamelist = read_data(src)

    print("Converting...")

    for idata, iifile in zip(data, infilenamelist):
        for ifract, iname in zip(fracts, names):
            print("%s x %1.3f -> %s" % (old_name, ifract, iname))
            pft_tmp = extend_frac(idata, old_name, iname, ifract)
            idata[iname] = pft_tmp

        save_data(idata, generate_outname(iifile, target))

if __name__ == "__main__":
    main()