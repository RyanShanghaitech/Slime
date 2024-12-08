from numpy import *
from matplotlib.pyplot import *
import lubdub
from time import time

T = 2*pi
nPix = 128
nT = 128 # int(2*pi*30)
nZ = nPix

tElapse = time()
arrM0_ = lubdub.genPhantom(linspace(0,T,nT,0), linspace(-nZ//2,nZ//2,nZ,0), nPix)
tElapse = time() - tElapse
print(f"tElapse: {tElapse}")

arrM0 = zeros_like(arrM0_, dtype=float64)
arrM0[arrM0_==lubdub.Part.ArmL.value] = 0.5
arrM0[arrM0_==lubdub.Part.ArmR.value] = 0.5
arrM0[arrM0_==lubdub.Part.Fat.value] = 0.8
arrM0[arrM0_==lubdub.Part.Body.value] = 0.5
arrM0[arrM0_==lubdub.Part.Myo.value] = 0.2
arrM0[arrM0_==lubdub.Part.Blood.value] = 1.0

fig = figure(figsize=(6,6), dpi=120)
ax = fig.add_subplot(111)
axim = ax.imshow(zeros([nPix,nPix]), cmap='gray', vmin=0, vmax=1)
iT = 3; iZ = nPix*1//4

while 1:
    # for iT in range(nT):
    for iZ in range(nZ):
        axim.set_data(arrM0[iT,iZ,:,:])
        ax.set_title(f"iT: {iT} iZ: {iZ}")
        draw()
        pause(T/nT)