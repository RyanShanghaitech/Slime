from numpy import *
from matplotlib.pyplot import *
import slime

# 2D
nPix = 128
arrPhan = slime.genPhan(nPix=nPix).squeeze()
arrPhan = slime.Enum2M0(arrPhan)

figure(figsize=(9,9), dpi=120)
imshow(arrPhan, cmap="gray"); colorbar()
draw(); pause(0.5)

# 3D
nPix = 128
arrPhan = slime.genPhan(nDim=3,nPix=nPix).squeeze()
arrPhan = slime.Enum2M0(arrPhan)

figure(figsize=(9,3), dpi=120)
subplot(131)
imshow(arrPhan[nPix//2,:,:], cmap="gray"); colorbar()
subplot(132)
imshow(arrPhan[:,nPix//2,:], cmap="gray"); colorbar()
subplot(133)
imshow(arrPhan[:,:,nPix//2], cmap="gray"); colorbar()
draw(); pause(0.5)

# 2D + T
nPix = 256
tScan = 8
tRes = 128
nT = tScan*tRes # int(2*pi*30)
cycRes = pi
cycCar = 1
ampRes = 20e-3*slime.genAmp(tScan, tRes, cycRes, 1)
ampCar = 10e-3*slime.genAmp(tScan, tRes, cycCar, 0)
arrPhan = slime.genPhan(nPix=nPix,arrAmp=vstack([ampRes,ampCar]).T).squeeze()
arrPhan = slime.Enum2M0(arrPhan)

figure(figsize=(9,9), dpi=120)
axim = imshow(arrPhan[0,:,:], cmap="gray"); colorbar()
while 1:
    for iT in range(0,nT,8):
        axim.set_data(arrPhan[iT,:,:])
        draw()
        pause(1e-3)
show()