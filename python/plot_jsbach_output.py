import os, sys, glob
import numpy as np
import xarray as xr
import yaml
import matplotlib.pyplot as plt
import datetime as dt


def plot_global(ax, data):
    x = data['clon'].data
    y = data['clat'].data
    lai = data.data

    img2 = ax.tricontourf(x,y,lai, 20, cmap=plt.cm.gist_earth_r) # choose 20 contour levels, just to show how good its interpolation is
    cbar = plt.colorbar(img2, ax=ax)
    cbar.set_label("LAI")
   
    ax.set_yticks(np.arange(-np.pi/2, np.pi/2+0.1, np.pi/4))
    ax.set_yticklabels(np.arange(-90,91,180/4.))
    ax.set_xlabel("Longitude (deg)")
    ax.set_ylabel("Latitude (deg)")
    ax.set_xticks(np.arange(-np.pi, np.pi+0.1,np.pi/3))
    ax.set_xticklabels(np.arange(-180, 181, 180/3.))

    ax.set_title(str(data.time.data)[:10])

def plot_season(ax, data):
    data.sum(dim='ncells').plot()
    ax.set_ylabel("LAI")
    ax.set_xlabel("Time")

def read_data(src):
    data = []
    for each in sorted(glob.glob(src)):
        tmp = xr.open_dataset(each)
        time = [dt.datetime.strptime("%s" % each.data, "%Y%m%d.%f") for each in tmp.time]
        tmp['time'] = time
        data.append(tmp['pheno_lai_veg'])

    data = xr.concat(data, dim='time')
    return(data)

def init(config_file):
    plt.close('all')
    # Read configuration
    with open(r'%s' % config_file) as file:
        config_list = yaml.load(file, Loader=yaml.FullLoader)
    file.close()
    return(config_list)

def main():
    plt.close('all')
    # Load config
    config = init("config_plot_jsb_output.yml")

    src = os.environ['MODELS'] + '/icon/' + config["src"]
    print(src)
    b_print = config["print"]
  
    data = read_data(src)
    
    # Plot it
    f, ax = plt.subplots(3,1, sharex=True, sharey=True)

    for idata, iax in zip((data.sel(time='2000-02-01'),data.sel(time='2000-06-15'), data.sel(time='2000-12-01')), ax):
        plot_global(iax, idata)
        
    f2, ax2 = plt.subplots(1)

    plot_season(ax2, data)

    plt.show(block=False)

    if b_print:
        f.savefig("jsbach_standalone_test.png")


if __name__ == "__main__":
    main()