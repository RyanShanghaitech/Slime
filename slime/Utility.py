from numpy import *
from scipy.ndimage import gaussian_filter
from .Type import Part

def genPhMap(nDim:int=2, nPix:int=256, mean:int|float|None=None, std:int|float=pi/16) -> ndarray:
    """
    # return
    smooth complex rotation factor
    """
    if mean == None: mean = random.uniform(-pi,pi)
    mapPh = random.uniform(-pi, pi, [nPix for _ in range(nDim)])
    sigma = nPix/4
    mapPh = gaussian_filter(mapPh, sigma)
    # normalize
    mapPh -= mapPh.mean(); mapPh = asarray(mapPh)
    mapPh /= mapPh.std()
    mapPh *= std
    mapPh += mean
    # convert to rotation factor
    mapPh = exp(1j*mapPh)
    mapPh = mapPh/abs(mapPh)
    return mapPh

def genB0Map(nDim:int=2, nPix:int=256, mean:int|float=0, std:int|float=1e-6*(2*pi*42.58e6*3)) -> ndarray:
    """
    # return
    smooth random number
    """
    mapB0 = random.uniform(-1, 1, [nPix for _ in range(nDim)])
    sigma = nPix/4
    mapB0 = gaussian_filter(mapB0, sigma)
    # normalize
    mapB0 -= mapB0.mean(); mapB0 = asarray(mapB0)
    mapB0 /= mapB0.std()
    mapB0 *= std
    mapB0 += mean
    return mapB0

def genCsm(nDim:int=2, nPix:int=256, nCh:int=12, mean:int|float|None=None, std:int|float=pi/16) -> ndarray:
    if mean == None: mean = random.uniform(-pi,pi)
    mapC = zeros([nCh,*(nPix for _ in range(nDim))], dtype=complex128)
    arrCoor = meshgrid\
    (
        *(linspace(-0.5,0.5,nPix,0) for _ in range(nDim)),
        indexing="ij"
    ); arrCoor = array(arrCoor).transpose(*arange(1,nDim+1), 0)
    arrTht = linspace(0,2*pi,nCh,0)
    arrCoorCoil = zeros([nCh,nDim], dtype=float64)
    arrCoorCoil[:,-2:] = 1*array([sin(arrTht), cos(arrTht)]).T
    if nDim == 3:
        arrCoorCoil[0::2,0] = 0.2
        arrCoorCoil[1::2,0] = -0.2
    for iCh in range(nCh):
        mapC[iCh] = genPhMap(nDim=nDim, nPix=nPix, mean=mean, std=std)
        dist = sqrt(sum((arrCoor - arrCoorCoil[iCh])**2, axis=-1))
        mapC[iCh] *= exp(-dist)
    return mapC

def genAmp(tScan:int|float, tRes:int|float, cyc:int|float, isRand:bool=True):
    """
    # parameter
    `tScan`: how many seconds this waveform contains
    `tRes`: how many ticks per second
    `cyc`: cycle of desired signal in second
    `isRand`: whether to randomize the waveform
    """
    nT = tScan*tRes

    if isRand:
        arrT = sort(random.rand(nT)*tScan)
        arrAmp = sin(2*pi/cyc*arrT)

        sigma = cyc*tRes/8
        arrAmp = gaussian_filter(arrAmp, sigma)
    else:
        arrT = linspace(0, tScan, nT)
        arrAmp = sin(2*pi/cyc*arrT)

    return arrAmp

def Enum2M0(arrPhan:ndarray) -> ndarray:
    mapM0 = zeros_like(arrPhan, dtype=float64)
    mapM0[arrPhan==Part.Air.value] = 0 # random.randn(sum(arrPhan==Part.Air.value))*1e-3
    mapM0[arrPhan==Part.Fat.value] = 1.0
    mapM0[arrPhan==Part.Body.value] = 0.5
    mapM0[arrPhan==Part.Myo.value] = 0.2
    mapM0[arrPhan==Part.Blood.value] = 0.8
    mapM0[arrPhan==Part.Other.value] = 1.0
    return mapM0

def Enum2T1(arrPhan:ndarray) -> ndarray:
    mapT1 = zeros_like(arrPhan, dtype=float64)
    mapT1[arrPhan==Part.Air.value] = inf # 10000e-3 #random.uniform(1e-3, 10000e-3, sum(arrPhan==Part.Air.value))
    mapT1[arrPhan==Part.Fat.value] = 350e-3
    mapT1[arrPhan==Part.Body.value] = 1600e-3
    mapT1[arrPhan==Part.Myo.value] = 1300e-3
    mapT1[arrPhan==Part.Blood.value] = 1500e-3
    mapT1[arrPhan==Part.Other.value] = 1000e-3 # arbitary value
    return mapT1

def Enum2T2(arrPhan:ndarray) -> ndarray:
    mapT2 = zeros_like(arrPhan, dtype=float64)
    mapT2[arrPhan==Part.Air.value] = 1e-6 # random.uniform(1e-3, 1000e-3, sum(arrPhan==Part.Air.value))
    mapT2[arrPhan==Part.Fat.value] = 75e-3
    mapT2[arrPhan==Part.Body.value] = 40e-3
    mapT2[arrPhan==Part.Myo.value] = 50e-3
    mapT2[arrPhan==Part.Blood.value] = 225e-3
    mapT2[arrPhan==Part.Other.value] = 10e-3 # arbitary value
    return mapT2

def Enum2Om(arrPhan:ndarray, B0:int|float=3) -> ndarray:
    mapOm = zeros_like(arrPhan, dtype=float64)
    ppm2om = 1e-6*(2*pi*42.58e6*B0)
    mapOm[arrPhan==Part.Air.value] = 0 # random.uniform(1e-3, 10e-3, sum(arrPhan==Part.Air.value))*ppm2om
    mapOm[arrPhan==Part.Fat.value] = 3.5*ppm2om
    mapOm[arrPhan==Part.Body.value] = 0
    mapOm[arrPhan==Part.Myo.value] = 0
    mapOm[arrPhan==Part.Blood.value] = 0
    mapOm[arrPhan==Part.Other.value] = 3.5*ppm2om
    return mapOm