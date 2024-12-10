from numpy import *
from matplotlib.pyplot import *
import slime

# 2D
nPix = 256
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

show()