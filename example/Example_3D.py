from numpy import *
from matplotlib.pyplot import *
import slime
from time import time

tScan = 10
tRes = 10e-3
nT = int(tScan/tRes)
nPix = 256

cycRes = pi/2
cycCar = 1
arrAmpRes = 20e-3*slime.genAmp(tScan, tRes, cycRes, 1)
arrAmpCar = 10e-3*slime.genAmp(tScan, tRes, cycCar, 0)

fig = figure()
ax = fig.add_subplot(211)
ax.plot(arrAmpRes, ".-")
ax.set_title("Respiratory")
ax = fig.add_subplot(212)
ax.plot(arrAmpCar, ".-")
ax.set_title("Cardiac")

fig = figure(figsize=(9,3), dpi=120)
ax1 = fig.add_subplot(131)
axim1 = ax1.imshow(zeros([nPix,nPix]), cmap='gray', vmin=0, vmax=1)
ax2 = fig.add_subplot(132)
axim2 = ax2.imshow(zeros([nPix,nPix]), cmap='gray', vmin=0, vmax=1)
ax3 = fig.add_subplot(133)
axim3 = ax3.imshow(zeros([nPix,nPix]), cmap='gray', vmin=0, vmax=1)

while 1:
    for iT in range(0,nT,10):
        arrPhant = slime.genPhant(3, nPix, arrAmpRes[iT], arrAmpCar[iT])
        arrM0 = slime.Enum2M0(arrPhant, arrAmpCar[iT])
        
        axim1.set_data(arrM0[nPix//2,:,:])
        axim2.set_data(arrM0[:,nPix//2,:])
        axim3.set_data(arrM0[:,:,nPix//2])
        ax2.set_title(f"time: {iT*tRes:.2f}s")
        draw()
        pause(tRes/10)