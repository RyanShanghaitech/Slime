from numpy import *
import skimage as ski
from enum import Enum

class Part(Enum):
    Air = 0
    Fat = 1
    Body = 2
    Myo = 3
    Blood = 4
    Other = 5

# update masks
def _updateMask_Dynamic(
    z:int|float, nPix:int,
    # mask to be updated
    mskFatOt:ndarray,
    mskFatIn:ndarray,
    mskMyoOt:ndarray,
    mskMyoIn:ndarray,
    # motion parameter
    ampRes:float|int,
    ampCar:float|int,
) -> None:
    # masks
    mskFatOt.fill(0)
    mskFatIn.fill(0)
    mskMyoOt.fill(0)
    mskMyoIn.fill(0)

    # draw body parts
    # Outer border of fat (expanding and contracting with breathing)
    y = 0 # -(1-z/nPix)*nPix*ampRes
    x = 0
    rY = nPix*400e-3 + (1-z/nPix)*nPix*ampRes
    rX = nPix*400e-3 - (1-z/nPix)*nPix*ampRes
    rZ = nPix*480e-3
    rhs = 1 - (z/rZ)**2
    if rhs >= 0:
        tupPtFatOt = ski.draw.ellipse(y+nPix//2, x+nPix//2, rY*sqrt(rhs), rX*sqrt(rhs), (nPix,nPix), pi*0e-2)
        mskFatOt[tupPtFatOt] = 1
    
    # Inner border of fat
    y = 0 # -(1-z/nPix)*nPix*ampRes
    x = 0
    rY = nPix*380e-3 + (1-z/nPix)*nPix*ampRes
    rX = nPix*380e-3 - (1-z/nPix)*nPix*ampRes
    rZ = nPix*450e-3
    rhs = 1 - (z/rZ)**2
    if rhs >= 0:
        tupPtFatIn = ski.draw.ellipse(y+nPix//2, x+nPix//2, rY*sqrt(rhs), rX*sqrt(rhs), (nPix,nPix), pi*2e-2)
        mskFatIn[tupPtFatIn] = 1

    # draw heart
    # Outer ellipse
    y = 0 # -(1-z/nPix)*nPix*ampRes
    x = 0
    rY = nPix*100e-3 + nPix*ampCar
    rX = nPix*120e-3 + nPix*ampCar
    rZ = rY
    rhs = 1 - (z/rZ)**2
    if rhs >= 0:
        tupPtMyoOt = ski.draw.ellipse(y+nPix//2, x+nPix//2, rY*sqrt(rhs), rX*sqrt(rhs), (nPix,nPix))
        mskMyoOt[tupPtMyoOt] = 1

    # Inner ellipse
    y = 0 # -(1-z/nPix)*nPix*ampRes
    x = -nPix*20e-3
    rY = nPix*60e-3  + nPix*2*ampCar
    rX = nPix*60e-3  + nPix*2*ampCar
    rZ = rY
    rhs = 1 - (z/rZ)**2
    if rhs > 0:
        tupPtMyoIn = ski.draw.ellipse(y+nPix//2, x+nPix//2, rY*sqrt(rhs), rX*sqrt(rhs), (nPix,nPix))
        mskMyoIn[tupPtMyoIn] = 1

def _updateMask_Fixed(
    z:int|float, nPix:int,
    lstMskEl:list[ndarray],
) -> None:
    # masks
    for msk in lstMskEl: msk.fill(0)

    # draw eln
    arrY, arrX = meshgrid\
    (
        arange(-nPix//2,nPix//2),
        arange(-nPix//2,nPix//2),
        indexing="ij"
    )
    arrYX = array([arrY,arrX]).transpose(1,2,0)

    nEl = len(lstMskEl)
    r0 = (nPix*2e-1)/(nEl-1)/3
    arrOzy = array([
        [0, -nPix*0.25],
        [0, nPix*0.25],
        [-nPix*0.25, 0],
        [nPix*0.25, 0],
    ])
    for Oz, Oy in arrOzy:
        arrOyx = array([
            Oy*ones([nEl]),
            linspace(-nPix*1e-1, nPix*1e-1, nEl),
        ]).T
        
        for iM in range(nEl):
            Oy, Ox = arrOyx[iM,:]
            r = r0*(1 - abs(Ox-nPix*1e-1)/(nPix*2e-1)/2)
            lstMskEl[iM][sum((arrYX-arrOyx[iM,:])**2,axis=-1) < r**2 - (z-Oz)**2] = 1

def genPhantom\
(
    nDim:int=2, nPix:int=256,
    # motion parameter
    arrAmp:ndarray=array([[0e-3,0e-3]]),
    # number of additional ellipsoid
    nEl:int=5,
):
    assert nDim==2 or nDim==3
    if nDim==2: arrZ = array([0])
    if nDim==3: arrZ = arange(-nPix//2,nPix//2)
    nT = arrAmp.shape[0]
    nZ = arrZ.size
    # image array
    arrPhan = zeros([nT,nZ,nPix,nPix], dtype=uint8)

    # masks
    mskFatOt = zeros([nPix,nPix], dtype=bool)
    mskFatIn = zeros([nPix,nPix], dtype=bool)
    mskMyoOt = zeros([nPix,nPix], dtype=bool)
    mskMyoIn = zeros([nPix,nPix], dtype=bool)
    lstMskEl = [zeros([nPix,nPix], dtype=bool) for _ in range(nEl)]

    # clear image
    arrPhan.fill(0)
    for iZ in range(nZ):
        z = arrZ[iZ]
        _updateMask_Fixed \
        (
            z, nPix,
            lstMskEl
        )
        for iT in range(nT):

            _updateMask_Dynamic \
            (
                z, nPix,
                mskFatOt, mskFatIn, mskMyoOt, mskMyoIn,
                arrAmp[iT,0], arrAmp[iT,1]
            )
        
            # fill fat
            arrPhan[iT][iZ][mskFatOt & ~mskFatIn] = Part.Fat.value
            # fill body
            arrPhan[iT][iZ][mskFatIn & ~mskMyoOt] = Part.Body.value
            # fill myocardium
            arrPhan[iT][iZ][mskMyoOt & ~mskMyoIn] = Part.Myo.value
            # fill blood pool
            arrPhan[iT][iZ][mskMyoIn] = Part.Blood.value
            # fill ellipsoid_n
            for msk in lstMskEl:
                arrPhan[iT][iZ][msk] = Part.Other.value

    return arrPhan