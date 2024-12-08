from numpy import *
from matplotlib.pyplot import *
import lubdub

nPix = 1024

# 2D
nPix = 1024
arrPhan = lubdub.genPhantom(nPix=nPix).squeeze()
arrPhan = lubdub.Enum2M0(arrPhan)

figure()
imshow(arrPhan, cmap="gray"); colorbar()
draw(); pause(0.5)

# 3D
nPix = 256
arrPhan = lubdub.genPhantom(nDim=3,nPix=nPix).squeeze()
arrPhan = lubdub.Enum2M0(arrPhan)

figure()
subplot(131)
imshow(arrPhan[nPix//2,:,:], cmap="gray"); colorbar()
subplot(132)
imshow(arrPhan[:,nPix//2,:], cmap="gray"); colorbar()
subplot(133)
imshow(arrPhan[:,:,nPix//2], cmap="gray"); colorbar()
draw(); pause(0.5)

# 2D + T
nPix = 1024
tScan = 8
nT = tScan*128 # int(2*pi*30)
cycRes = 2*pi
cycCar = 1
arrT_Res = sort(random.rand(nT)*tScan)
arrT_Car = linspace(0, tScan, nT)
ampRes = 20e-3*sin(2*pi/cycRes*arrT_Res)
ampCar = 10e-3*sin(2*pi/cycCar*arrT_Car)
arrPhan = lubdub.genPhantom(nPix=nPix,arrAmp=vstack([ampRes,ampCar]).T).squeeze()
arrPhan = lubdub.Enum2M0(arrPhan)

figure()
axim = imshow(arrPhan[0,:,:], cmap="gray"); colorbar()
while 1:
    for iT in range(0,nT,8):
        axim.set_data(arrPhan[iT,:,:])
        draw()
        pause(1e-3)
show()