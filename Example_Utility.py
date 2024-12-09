import lubdub
from numpy import *
from matplotlib.pyplot import *

nPix = 128

mapPh = lubdub.genPhMap(nPix, 3)
print(mapPh.shape)

stdOm = 1
mapB0 = lubdub.genB0Map(nPix, 3, stdOm)

figure()

subplot(121)
imshow(angle(mapPh[nPix//2,:,:]), cmap="hsv", vmin=-pi, vmax=pi)
colorbar()
title("phase map")

subplot(122)
imshow(mapB0[nPix//2,:,:], vmin=-3*stdOm, vmax=3*stdOm)
colorbar().set_label("ppm")
title("B0 map")

show()