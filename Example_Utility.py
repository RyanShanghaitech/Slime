import slime
from numpy import *
from matplotlib.pyplot import *
from matplotlib.colors import ListedColormap

nPix = 128

mapPh = slime.genPhMap(3, nPix, pi/3)
mapB0 = slime.genB0Map(3, nPix, 1) # unit: ppm

dicPhan = slime.genPhan(3, nPix)
mapM0 = dicPhan["M0"].squeeze()
mapT1 = dicPhan["T1"].squeeze()
mapT2 = dicPhan["T2"].squeeze()
mapOm = dicPhan["Om"].squeeze()

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

show()