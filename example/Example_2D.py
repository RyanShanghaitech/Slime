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

fig = figure(figsize=(6,6), dpi=120)
ax = fig.add_subplot(111)
axim = ax.imshow(zeros([nPix,nPix]), cmap='gray', vmin=0, vmax=1)

while 1:
    for iT in range(nT):
        arrPhant = slime.genPhant(2, nPix, arrAmpRes[iT], arrAmpCar[iT])
        arrM0 = slime.Enum2M0(arrPhant, arrAmpCar[iT])
        
        axim.set_data(arrM0)
        ax.set_title(f"time: {iT*tRes:.2f}s")
        draw()
        pause(tRes/10)
        # pause(1e-2)