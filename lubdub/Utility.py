from numpy import *
from .Function import Part
from scipy.ndimage import gaussian_filter

def genPhMap(nPix:int, ndim:int, norm:bool=True) -> ndarray:
    """
    # return
    smooth complex rotation factor
    """
    mapPh = random.uniform(-pi, pi, [nPix for _ in range(ndim)])
    mapPh = exp(1j*mapPh)
    sigma = nPix/2
    mapPh = gaussian_filter(mapPh, sigma)
    mapPh = mapPh/abs(mapPh)
    if norm:
        mapPh /= exp(1j*angle(mapPh).mean())
    return mapPh

def genB0Map(nPix:int, ndim:int, stdOm:int|float, norm:bool=True) -> ndarray:
    """
    # return
    smooth random number between -maxOm~maxOm
    """
    mapB0 = random.uniform(-stdOm, stdOm, [nPix for _ in range(ndim)])
    sigma = nPix/2
    mapB0 = gaussian_filter(mapB0, sigma)
    if norm:
        mapB0 -= mapB0.mean(); mapB0 = asarray(mapB0)
        mapB0 /= mapB0.std()
        mapB0 *= stdOm
    return mapB0

def genAmp(tScan:int|float, tRes:int|float, cyc:int|float, isRand:bool=True):
    """
    # parameter
    `tScan`: how many seconds this amplitude contains
    `tRes`: how many ticks per second
    `cyc`: cycle of desired signal in second
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

def Enum2M0(arrIn:ndarray) -> ndarray:
    arrOt = zeros_like(arrIn, dtype=float64)
    arrOt[arrIn==Part.Air.value] = random.randn(sum(arrIn==Part.Air.value))*1e-3
    arrOt[arrIn==Part.Fat.value] = 1.0
    arrOt[arrIn==Part.Body.value] = 0.5
    arrOt[arrIn==Part.Myo.value] = 0.2
    arrOt[arrIn==Part.Blood.value] = 0.8
    arrOt[arrIn==Part.Other.value] = 1.0
    return arrOt

def Enum2T1(arrIn:ndarray) -> ndarray:
    arrOt = zeros_like(arrIn, dtype=float64)
    arrOt[arrIn==Part.Air.value] = clip(150 + random.randn(sum(arrIn==Part.Air.value))*50, 1, 300)
    arrOt[arrIn==Part.Fat.value] = 370e-3
    arrOt[arrIn==Part.Body.value] = 1420e-3
    arrOt[arrIn==Part.Myo.value] = 1200e-3
    arrOt[arrIn==Part.Blood.value] = 1650e-3
    arrOt[arrIn==Part.Other.value] = 1000e-3 # arbitary value
    return arrOt

def Enum2T2(arrIn:ndarray) -> ndarray:
    arrOt = zeros_like(arrIn, dtype=float64)
    arrOt[arrIn==Part.Air.value] = clip(1200 + random.randn(sum(arrIn==Part.Air.value))*400, 1, 2400)
    arrOt[arrIn==Part.Fat.value] = 80e-3
    arrOt[arrIn==Part.Body.value] = 50e-3
    arrOt[arrIn==Part.Myo.value] = 50e-3
    arrOt[arrIn==Part.Blood.value] = 200e-3
    arrOt[arrIn==Part.Other.value] = 10e-3 # arbitary value
    return arrOt

def Enum2Om(arrIn:ndarray, B0:int|float=3) -> ndarray:
    arrOt = zeros_like(arrIn, dtype=float64)
    ppm2om = 1e-6*(2*pi*42.58e6*B0)
    arrOt[arrIn==Part.Air.value] = random.randn(sum(arrIn==Part.Air.value))*1*ppm2om
    arrOt[arrIn==Part.Fat.value] = 3.5*ppm2om
    arrOt[arrIn==Part.Body.value] = 0
    arrOt[arrIn==Part.Myo.value] = 0
    arrOt[arrIn==Part.Blood.value] = 0
    arrOt[arrIn==Part.Other.value] = 0
    return arrOt