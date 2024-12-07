from numpy import *
from matplotlib.pyplot import *
import lubdub
from time import time

nPix = 256
nT = 30 # int(2*pi*30)
nZ = nPix

tElapse = time()
arrM0_ = lubdub.genPhantom(linspace(0,2*pi,nT,0), linspace(-nZ//2,nZ//2,nZ,0), nPix)
tElapse = time() - tElapse
print(f"tElapse: {tElapse:.2f}")
print(arrM0_.nbytes)
exit()
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
for iT in range(nT):
    axim.set_data(arrM0[iT,nZ//2,:,:])
    ax.set_title(f"iT: {iT}")
    draw()
    pause(2*pi/nT)