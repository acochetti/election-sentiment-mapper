from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np

plt.style.use("ggplot")

fig = plt.figure()
ax = fig.add_subplot(111)

west, south, east, north = -74.26, 40.50, -73.70, 40.92

m = Basemap(projection='merc', llcrnrlat=south, urcrnrlat=north,
            llcrnrlon=west, urcrnrlon=east, resolution='h')

m.drawcoastlines()
m.drawstates()
m.drawmapboundary(fill_color="aqua")
m.fillcontinents(color='#D0F5A9', lake_color='aqua', zorder=0)

# test data to demonstrate animation concept
test_long1 = [-73.943209] * 100
test_lat1 = [40.815872] * 100

test_long2 = [-73.946942] * 100
test_lat2 = [40.612926] * 100

test_long3 = [-74.178921] * 100
test_lat3 = [40.682370] * 100

test_long = [test_long1 + test_long2 + test_long3] * 3
test_lat = [test_lat1 + test_lat2 + test_lat3] * 3

c_t1 = [1] * 70 + [-1] * 30
c_t2 = [1] * 30 + [-1] * 70
c_t3 = [1] * 50 + [-1] * 50

c_t = [c_t1 + c_t2 + c_t3] + [c_t2 + c_t3 + c_t1] + [c_t3 + c_t1 + c_t2]


def animate(i):  # i equals current frame number: 0, 1, 2
    x1_t, y1_t = m(test_long[i], test_lat[i])  # take one set of coordinates off list and transform
    c = list(c_t[i])  # take one set of c values off list

    h_t = m.hexbin(np.array(x1_t), np.array(y1_t), C=np.array(c), reduce_C_function=np.sum, gridsize=4,
                   cmap=plt.cm.coolwarm, vmin=-20, vmax=20)  # vmin/vmax normalize range
    return h_t

# 3 frames, 2000ms interval, repeating, no blitting means each frame is redrawn completely
anim = animation.FuncAnimation(fig, animate, frames=3, interval=2000, repeat=True, blit=False)

# requires ffmpeg to be installed and added to path, fps determined by frames and interval
anim.save("map_animation.mp4")

color_bar = m.colorbar()
color_bar.set_ticks([-20, 20])
color_bar.set_ticklabels(ticklabels=["Candidate 1", "Candidate 2"])  # Placeholder values

plt.title("Candidate Support on Twitter")
plt.show()
