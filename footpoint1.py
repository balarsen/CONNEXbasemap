from mpl_toolkits.basemap import Basemap, shiftgrid, cm
import numpy as np
import matplotlib.pyplot as plt

import h5py



# create the figure and axes instances.
fig = plt.figure()
ax = fig.add_axes([0.1,0.1,0.8,0.8])
# setup of basemap ('lcc' = lambert conformal conic).
# use major and minor sphere radii from WGS84 ellipsoid.
m = Basemap(llcrnrlon=-145.5,llcrnrlat=1.,urcrnrlon=-2.566,urcrnrlat=46.352,\
            rsphere=(6378137.00,6356752.3142),\
            resolution='l',area_thresh=1000.,projection='lcc',\
            lat_1=50.,lon_0=-107.,ax=ax)
# transform to nx x ny regularly spaced 5km native projection grid
nx = int((m.xmax-m.xmin)/5000.)+1; ny = int((m.ymax-m.ymin)/5000.)+1
# topodat = m.transform_scalar(topoin,lons,lats,nx,ny)
# plot image over map with imshow.
# im = m.imshow(topodat,cm.GMT_haxby)
# draw coastlines and political boundaries.
m.drawcoastlines()
m.drawcountries()
m.drawstates()
# draw parallels and meridians.
# label on left and bottom of map.
parallels = np.arange(0.,80,20.)
m.drawparallels(parallels,labels=[1,0,0,1])
meridians = np.arange(10.,360.,30.)
m.drawmeridians(meridians,labels=[1,0,0,1])
# add colorbar
# cb = m.colorbar(im,"right", size="5%", pad='2%')
ax.set_title('ETOPO5 Topography - Lambert Conformal Conic')

from datetime import datetime
# date = datetime.utcnow()
# CS=m.nightshade(date)


import path
# grab the file data
downloads = path.path('C:/Users/balarsen/Downloads')
h5files = downloads.files('*.h5')
print(downloads, h5files)

with h5py.File(h5files[0]) as h5:
    # get the latlon north and south footpoints
    Pfn = h5['Pfn_geod_LatLon'][...]
    Pfs = h5['Pfs_geod_LatLon'][...]
    IsoTime = h5['IsoTime'][...]

# change isotime to datetime
dt = [datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ') for v in IsoTime]

print(Pfn)

x, y = m(Pfn[:,1], Pfn[:,0])
m.scatter(x,y, color='r', marker='o')
# m.plot(Pfn[:,1], Pfn[:,0], color='r')
plt.draw()
plt.show()