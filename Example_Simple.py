from numpy import *
from matplotlib.pyplot import *
import slime

# 2D
nPix = 256
arrM0 = slime.genPhan(nPix=nPix)["M0"].squeeze()

arrM0Abs = abs(arrM0)
figure(figsize=(3,3), dpi=120)
imshow(arrM0Abs, cmap="gray"); colorbar()
draw(); pause(0.5)

# 3D
nPix = 128
arrM0 = slime.genPhan(nDim=3, nPix=nPix)["M0"].squeeze()

arrM0Abs = abs(arrM0)
figure(figsize=(9,3), dpi=120)
subplot(131)
imshow(arrM0Abs[nPix//2,:,:], cmap="gray"); colorbar()
subplot(132)
imshow(arrM0Abs[:,nPix//2,:], cmap="gray"); colorbar()
subplot(133)
imshow(arrM0Abs[:,:,nPix//2], cmap="gray"); colorbar()
draw(); pause(0.5)

show()