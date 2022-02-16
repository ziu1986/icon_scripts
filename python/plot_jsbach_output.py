from doctest import ELLIPSIS_MARKER
import os, sys, glob
import numpy as np
import xarray as xr
import yaml
import matplotlib.pyplot as plt
from matplotlib.colors import DivergingNorm
import datetime as dt

def plot_global(ax, data, **kwargs):
    x = data['clon'].data
    y = data['clat'].data
    lai = data.data

    b_diff = kwargs.pop('diff', False)
    if b_diff:
        map = plt.cm.BrBG
        norm = DivergingNorm(0) #TwoSlopeNorm(0)
        level = 40
    else:
        map = plt.cm.gist_earth_r
        norm = None
        level = 20

    img2 = ax.tricontourf(x,y,lai, level, norm=norm, cmap=map) # choose 20 contour levels, just to show how good its interpolation is
    cbar = plt.colorbar(img2, ax=ax)
    cbar.set_label("LAI")
   
    ax.set_yticks(np.arange(-np.pi/2, np.pi/2+0.1, np.pi/4))
    ax.set_yticklabels(np.arange(-90,91,180/4.))
    ax.set_xticks(np.arange(-np.pi, np.pi+0.1,np.pi/3))
    ax.set_xticklabels(np.arange(-180, 181, 180/3.))
    ax.set_xlabel("Longitude (deg)")
    ax.set_ylabel("Latitude (deg)")

    ax.set_title(str(data.time.data)[:10])

def plot_season(ax, data, **kwargs):
    b_diff = kwargs.pop('diff', False)
    data.sum(dim='ncells').plot()
    if b_diff:
        ax.set_ylabel("$\Delta$LAI")
    else:
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

    src_base = os.environ['MODELS'] + '/icon/'
    
    b_print = config["print"]
    b_diff = config["diff"]
  
    data = read_data(src_base + config["src"])
    
    if b_diff:
        data = read_data(src_base + config["src2"]) - data

    # Plot it
    f, ax = plt.subplots(3,1, sharex=True, sharey=True)
    
    f.canvas.set_window_title("lai_global_map")

    for idata, iax in zip((data.sel(time='2000-02-01'),data.sel(time='2000-06-15'), data.sel(time='2000-12-01')), ax):
        plot_global(iax, idata, diff=b_diff)
        
    f2, ax2 = plt.subplots(1)
    f2.canvas.set_window_title("lai_global_time")

    plot_season(ax2, data, diff=b_diff)

    plt.show(block=False)

    if b_print:
        f.savefig("jsbach_standalone_test.png")


if __name__ == "__main__":
    main()