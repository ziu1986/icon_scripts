import os, sys, glob
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import datetime as dt

def plot(ax, data, var='lai'):
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

plt.close('all')
src = os.environ['MODELS'] + "/icon/build_lnd/experiments/jsbalone_R2B4_sfa/jsbalone_R2B4_sfa_lnd_basic_ml_2000*"
data = []
for each in sorted(glob.glob(src)):
    tmp = xr.open_dataset(each)
    time = [dt.datetime.strptime("%s" % each.data, "%Y%m%d.%f") for each in tmp.time]
    tmp['time'] = time
    data.append(tmp['pheno_lai_veg'])

data = xr.concat(data, dim='time')
# Plot it
f, ax = plt.subplots(3,1, sharex=True, sharey=True)

for idata, iax in zip((data.sel(time='2000-02-01'),data.sel(time='2000-06-15'), data.sel(time='2000-12-01')), ax):
    plot(iax, idata)
    
fig2 = plt.figure()
data.sum(dim='ncells').plot()
ax21 = fig2.gca()
ax21.set_ylabel("LAI")
ax21.set_xlabel("Time")




plt.show(block=False)
plt.savefig("jsbach_standalone_test.png")