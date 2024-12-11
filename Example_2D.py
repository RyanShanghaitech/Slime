from numpy import *
from matplotlib.pyplot import *
import slime
from time import time

tScan = 100
tRes = 10
nT = tScan*tRes # int(2*pi*30)
nPix = 256
nZ = 1

cycRes = pi
cycCar = 1

tElapse = time()

ampRes = 20e-3*slime.genAmp(tScan, tRes, cycRes, 1)
ampCar = 10e-3*slime.genAmp(tScan, tRes, cycCar, 0)
arrM0 = slime.genPhan(2, nPix, array([ampRes, ampCar]).T, rtPhan=False, rtT1=False, rtT2=False, rtOm=False)["M0"]

tElapse = time() - tElapse
print(f"tElapse: {tElapse}")

iT = 3

fig = figure()
ax = fig.add_subplot(211)
ax.plot(ampRes, ".-")
ax.set_title("Respiratory")
ax = fig.add_subplot(212)
ax.plot(ampCar, ".-")
ax.set_title("Cardiac")

fig = figure(figsize=(6,6), dpi=120)
ax = fig.add_subplot(111)
axim = ax.imshow(zeros([nPix,nPix]), cmap='gray', vmin=0, vmax=1)

arrM0Abs = abs(arrM0)
while 1:
    for iT in range(nT):
    # for iZ in range(nZ):
        axim.set_data(arrM0Abs[iT,0,:,:])
        ax.set_title(f"iT: {iT}")
        draw()
        pause(tScan/nT)
        # pause(1e-2)