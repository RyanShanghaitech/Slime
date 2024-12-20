from numpy import *
from matplotlib.pyplot import *
import slime
from time import time

tScan = 10
tRes = 10
nT = tScan*tRes # int(2*pi*30)
nPix = 128
nZ = nPix

cycRes = pi
cycCar = 1

t = time()

ampRes = 10e-3*slime.genAmp(tScan, tRes, cycRes, 1)
ampCar = 10e-3*slime.genAmp(tScan, tRes, cycCar, 0)
arrM0 = slime.genPhan(3, nPix, array([ampRes, ampCar]).T)["M0"]

t = time() - t
print(f"elapsed time: {t}")

fig = figure()
ax = fig.add_subplot(211)
ax.plot(ampRes, ".-")
ax.set_title("Respiratory")
ax = fig.add_subplot(212)
ax.plot(ampCar, ".-")
ax.set_title("Cardiac")

fig = figure(figsize=(9,3), dpi=120)
ax1 = fig.add_subplot(131)
axim1 = ax1.imshow(zeros([nPix,nPix]), cmap='gray', vmin=0, vmax=1)
ax2 = fig.add_subplot(132)
axim2 = ax2.imshow(zeros([nPix,nPix]), cmap='gray', vmin=0, vmax=1)
ax3 = fig.add_subplot(133)
axim3 = ax3.imshow(zeros([nPix,nPix]), cmap='gray', vmin=0, vmax=1)

arrM0Abs = abs(arrM0)
while 1:
    for iT in range(nT):
    # for iZ in range(nZ):
        axim1.set_data(arrM0Abs[iT,nPix//2,:,:])
        axim2.set_data(arrM0Abs[iT,:,nPix//2,:])
        axim3.set_data(arrM0Abs[iT,:,:,nPix//2])
        ax1.set_title(f"iT: {iT}")
        ax2.set_title(f"iT: {iT}")
        ax3.set_title(f"iT: {iT}")
        draw()
        pause(tScan/nT)
        # pause(1e-2)