from numpy import *
import skimage as ski
from .Type import Part
from .Utility import Enum2M0, Enum2T1, Enum2T2, Enum2Om, genPhMap, genB0Map, genCsm


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
    y = 0 # -(1/2-abs(z/nPix))*nPix*ampRes
    x = 0
    rY = nPix*400e-3 + nPix*ampRes
    rX = nPix*400e-3 - 0.5*nPix*ampRes
    rZ = nPix*480e-3
    rhs = 1 - (z/rZ)**2
    # print(f"rY: {rY:.2f}, rX: {rX:.2f}")
    # print(f"rhs: {rhs:.4f}, rY: {sqrt(rY**2*rhs):.2f}, rX: {sqrt(rX**2*rhs):.2f}")
    if rhs >= 0:
        tupPtFatOt = ski.draw.ellipse(y+nPix//2, x+nPix//2, sqrt(rY**2*rhs), sqrt(rX**2*rhs), (nPix,nPix), pi*0e-2)
        mskFatOt[tupPtFatOt] = 1
    
    # Inner border of fat
    y = 0 # -(1/2-abs(z/nPix))*nPix*ampRes
    x = 0
    rY = nPix*380e-3 + nPix*ampRes
    rX = nPix*380e-3 - 0.5*nPix*ampRes
    rZ = nPix*450e-3
    rhs = 1 - (z/rZ)**2
    if rhs >= 0:
        tupPtFatIn = ski.draw.ellipse(y+nPix//2, x+nPix//2, sqrt(rY**2*rhs), sqrt(rX**2*rhs), (nPix,nPix), pi*4e-2)
        mskFatIn[tupPtFatIn] = 1

    # draw heart
    # Outer ellipse
    y = 0 # -(1/2-abs(z/nPix))*nPix*ampRes
    x = 0
    rY = nPix*100e-3 + nPix*ampCar
    rX = nPix*120e-3 + nPix*ampCar
    rZ = rY
    rhs = 1 - (z/rZ)**2
    if rhs >= 0:
        tupPtMyoOt = ski.draw.ellipse(y+nPix//2, x+nPix//2, sqrt(rY**2*rhs), sqrt(rX**2*rhs), (nPix,nPix))
        mskMyoOt[tupPtMyoOt] = 1

    # Inner ellipse
    y = 0 # -(1/2-abs(z/nPix))*nPix*ampRes
    x = -nPix*20e-3
    rY = nPix*60e-3 + nPix*2*ampCar
    rX = nPix*60e-3 + nPix*2*ampCar
    rZ = rY
    rhs = 1 - (z/rZ)**2
    if rhs > 0:
        tupPtMyoIn = ski.draw.ellipse(y+nPix//2, x+nPix//2, sqrt(rY**2*rhs), sqrt(rX**2*rhs), (nPix,nPix))
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
    r0 = (nPix*4e-1)/(nEl+1)/2; r0 *= 3/4
    arrOzy = array([
        [0, -nPix*0.20],
        [0, nPix*0.20],
        [-nPix*0.25, 0],
        [nPix*0.25, 0],
    ]); arrOzy = around(arrOzy)
    for Oz, Oy in arrOzy:
        arrOyx = array([
            Oy*ones([nEl]),
            linspace(-nPix*2e-1, nPix*2e-1, nEl+2, 1)[1:-1],
        ]).T; arrOyx = around(arrOyx)
        
        for iM in range(nEl):
            Oy, Ox = arrOyx[iM,:]
            r = r0*(1 - abs(Ox-nPix*2e-1)/(nPix*4e-1))
            lstMskEl[iM][sum((arrYX-arrOyx[iM,:])**2,axis=-1) < r**2 - (z-Oz)**2] = 1

def genPhan\
(
    nDim:int=2, nPix:int=256,
    # motion parameter
    arrAmp:ndarray|None=None,
    # whether to return M0 map, T1 map, T2 map, etc, or original enum phantom
    rtM0:bool=True, rtT1:bool=False, rtT2:bool=False, rtOm:bool=False, rtPhan:bool=False, 
    # number of additional ellipsoids for resolution test
    nEl:int=5,
) -> dict|ndarray[uint8]:
    assert nDim==2 or nDim==3
    if nDim==2:
        arrZ = array([0])
        if arrAmp is None: arrAmp = array([[60e-3,0e-3]])
    if nDim==3:
        arrZ = arange(-nPix//2,nPix//2)
        if arrAmp is None: arrAmp = array([[0e-3,0e-3]])
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

    # generate image
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

    # dictionary to be returned
    dic = dict()
    if rtPhan: dic["Phan"] = arrPhan
    if rtM0: dic["M0"] = Enum2M0(arrPhan)*genPhMap(nDim=nDim, nPix=nPix)
    if rtT1: dic["T1"] = Enum2T1(arrPhan)
    if rtT2: dic["T2"] = Enum2T2(arrPhan)
    if rtOm: dic["Om"] = Enum2Om(arrPhan) + genB0Map(nDim=nDim, nPix=nPix)

    return dic if len(dic) != 0 else arrPhan