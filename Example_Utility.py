import slime
from numpy import *
from matplotlib.pyplot import *
from matplotlib.colors import ListedColormap

nDim = 3
nPix = 128

mapPh = slime.Utility.genPhMap(nDim, nPix, pi/3)
mapB0 = slime.Utility.genB0Map(nDim, nPix, 1) # unit: ppm

dicPhan = slime.genPhan(3, nPix, rtM0=1, rtT1=1, rtT2=1, rtOm=1)
mapM0 = dicPhan["M0"].squeeze()
mapT1 = dicPhan["T1"].squeeze()
mapT2 = dicPhan["T2"].squeeze()
mapOm = dicPhan["Om"].squeeze()
mapC = slime.genCsm(nDim, nPix)

# plot
cmT1 = ListedColormap(loadtxt("./Resource/lipari.csv"), name="T1")
cmT2 = ListedColormap(loadtxt("./Resource/navia.csv"), name="T2")

figure(figsize=(9,5), dpi=120)
subplot(121)
imshow(angle(mapPh[:,nPix//2,:]), cmap="hsv", vmin=-pi, vmax=pi)
colorbar()
title("phase map")
subplot(122)
imshow(mapB0[:,nPix//2,:], vmin=-3, vmax=3)
colorbar().set_label("ppm")
title("B0 map")

mapM0Abs = abs(mapM0)
figure(figsize=(9,9), dpi=120)
subplot(221)
imshow(mapM0Abs[:,nPix//2,:], cmap="gray"); colorbar(); title("M0 map")
subplot(222)
imshow(mapT1[:,nPix//2,:]*1000, cmap=cmT1); colorbar().set_label("ms"); title("T1 map")
subplot(223)
imshow(mapT2[:,nPix//2,:]*1000, cmap=cmT2); colorbar().set_label("ms"); title("T2 map")
subplot(224)
imshow(mapOm[:,nPix//2,:]); colorbar(); title("Om map")

mapCsmAbs = abs(mapC)
figure(figsize=(9,9), dpi=120)
for iFig in range(3*4):
    subplot(3,4,iFig+1)
    imshow(mapCsmAbs[iFig,nPix-2,:,:], cmap="gray", vmin=0, vmax=1)

mapCsmAng = angle(mapC)
figure(figsize=(9,9), dpi=120)
for iFig in range(3*4):
    subplot(3,4,iFig+1)
    imshow(mapCsmAbs[iFig,nPix-2,:,:], cmap="hsv", vmin=-pi, vmax=pi)

show()