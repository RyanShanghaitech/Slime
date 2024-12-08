from numpy import *
from matplotlib.pyplot import *
import lubdub
from time import time
from scipy.ndimage import gaussian_filter

tScan = 100
tRes = 10
nPix = 256
nT = tScan*tRes # int(2*pi*30)
nZ = 1

cycRes = 2*pi
cycCar = 1

tElapse = time()
arrT_Res = sort(random.rand(nT)*tScan)
arrT_Car = linspace(0, tScan, nT)
ampRes = 20e-3*sin(2*pi/cycRes*arrT_Res); ampRes = gaussian_filter(ampRes, tRes)
ampCar = 10e-3*sin(2*pi/cycCar*arrT_Car)
arrP = lubdub.genPhantom(2, nPix, array([ampRes, ampCar]).T)
print(arrP.shape)
tElapse = time() - tElapse
print(f"tElapse: {tElapse}")

arrM0 = lubdub.Enum2M0(arrP)

iT = 3

fig = figure()
ax = fig.add_subplot(211)
ax.plot(ampRes, ".-")
ax = fig.add_subplot(212)
ax.plot(ampCar, ".-")
fig = figure(figsize=(6,6), dpi=120)
ax = fig.add_subplot(111)
axim = ax.imshow(zeros([nPix,nPix]), cmap='gray', vmin=0, vmax=1)

while 1:
    for iT in range(nT):
    # for iZ in range(nZ):
        axim.set_data(arrM0[iT,0,:,:])
        ax.set_title(f"iT: {iT}")
        draw()
        pause(tScan/nT)
        # pause(1e-2)