import slime
from numpy import *
from matplotlib.pyplot import *

nPix = 128

mapPh = slime.genPhMap(3, nPix)
print(mapPh.shape)

stdOm = 1
mapB0 = slime.genB0Map(3, nPix, stdOm)

arrPhan = slime.genPhan(3, nPix).squeeze()
mapM0 = slime.Enum2M0(arrPhan); print(f"mapM0.shape: {mapM0.shape}")
mapT1 = slime.Enum2T1(arrPhan)
mapT2 = slime.Enum2T2(arrPhan)
mapOm = slime.Enum2Om(arrPhan)

# plot
figure(figsize=(9,5), dpi=120)
subplot(121)
imshow(angle(mapPh[nPix//2,:,:]), cmap="hsv", vmin=-pi, vmax=pi)
colorbar()
title("phase map")
subplot(122)
imshow(mapB0[nPix//2,:,:], vmin=-3*stdOm, vmax=3*stdOm)
colorbar().set_label("ppm")
title("B0 map")

figure(figsize=(9,9), dpi=120)
subplot(221)
imshow(mapM0[nPix//2,:,:], vmin=0, vmax=1); colorbar(); title("M0 map")
subplot(222)
imshow(mapT1[nPix//2,:,:], vmin=0, vmax=2000e-3); colorbar(); title("T1 map")
subplot(223)
imshow(mapT2[nPix//2,:,:], vmin=0, vmax=200e-3); colorbar(); title("T2 map")
subplot(224)
imshow(mapOm[nPix//2,:,:], vmin=0, vmax=5e-6*(2*pi*42.58e6*3)); colorbar(); title("Om map")

show()