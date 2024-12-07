from numpy import *
import skimage as ski
from enum import Enum

class Part(Enum):
    ArmL = 1
    ArmR = 2
    Fat = 3
    Body = 4
    Myo = 5
    Blood = 6

# update masks
def _updateMask(
    t:float, z:float, nPix:int,
    # mask to be updated
    mskFatOt:ndarray,
    mskFatIn:ndarray,
    mskArmL:ndarray,
    mskArmR:ndarray,
    mskMyoOt:ndarray,
    mskMyoIn:ndarray,
    # motion parameter
    cycRes:float|int, # s
    cycHea:float|int, # s
    ampRes:float|int,
    ampMyoOt:float|int,
    ampMyoIn:float|int
) -> None:
    # masks
    mskFatOt.fill(0)
    mskFatIn.fill(0)
    mskArmL.fill(0)
    mskArmR.fill(0)
    mskMyoOt.fill(0)
    mskMyoIn.fill(0)

    # Breathing phase and Heabeat phase (using sine waves)
    phRes = (t/cycRes)*2*pi
    phHea = (t/cycHea)*2*pi

    # draw body parts
    # Outer border of fat (expanding and contracting with breathing)
    y = nPix*500e-3 - (1-abs(z/nPix))*nPix*ampRes*sin(phRes)
    x = nPix*500e-3
    rY = nPix*250e-3 + (1-abs(z/nPix))*nPix*ampRes*sin(phRes)
    rX = nPix*300e-3
    tupPtFatOt = ski.draw.ellipse(y, x, rY, rX, (nPix,nPix), pi*0e-2)
    mskFatOt[tupPtFatOt] = 1
    
    # Inner border of fat
    y = nPix*500e-3 - (1-abs(z/nPix))*nPix*ampRes*sin(phRes)
    x = nPix*500e-3
    rY = nPix*250e-3 - nPix*30e-3 + (1-abs(z/nPix))*nPix*ampRes*sin(phRes)
    rX = nPix*300e-3 - nPix*30e-3
    tupPtFatIn = ski.draw.ellipse(y, x, rY, rX, (nPix,nPix), pi*5e-2)
    mskFatIn[tupPtFatIn] = 1

    # draw arms
    # Left arm
    y = nPix*550e-3
    x = nPix*500e-3-nPix*400e-3
    rY = nPix*80e-3 + 20e-3*(nPix/2 - abs(z))
    rX = nPix*80e-3
    tupPtArmL = ski.draw.ellipse(y, x, rY, rX, (nPix,nPix), -pi*5e-2)
    mskArmL[tupPtArmL] = 1
    
    # Right arm
    y = nPix*550e-3
    x = nPix*500e-3+nPix*400e-3
    rY = nPix*80e-3 + 20e-3*(nPix/2 - abs(z))
    rX = nPix*80e-3
    tupPtArmR = ski.draw.ellipse(y, x, rY, rX, (nPix,nPix), pi*0e-2)
    mskArmR[tupPtArmR] = 1

    # draw heart
    # Outer ellipse
    y = nPix*500e-3 - (1-abs(z/nPix))*nPix*ampRes*sin(phRes) - nPix*60e-3
    x = nPix*500e-3
    rY = nPix*100e-3 + nPix*ampMyoOt*sin(phHea)
    rX = nPix*125e-3 + nPix*ampMyoOt*sin(phHea)
    rZ = rY
    rhs = 1 - (z/rZ)**2
    if rhs > 0:
        tupPtMyoOt = ski.draw.ellipse(y, x, rY*sqrt(rhs), rX*sqrt(rhs), (nPix,nPix))
        mskMyoOt[tupPtMyoOt] = 1

    # Inner ellipse
    y = nPix*500e-3 - (1-abs(z/nPix))*nPix*ampRes*sin(phRes) - nPix*60e-3
    x = nPix*500e-3 - nPix*20e-3
    rY = nPix*60e-3  + nPix*ampMyoIn*sin(phHea)
    rX = nPix*60e-3  + nPix*ampMyoIn*sin(phHea)
    rZ = rY
    rhs = 1 - (z/rZ)**2
    if rhs > 0:
        tupPtMyoIn = ski.draw.ellipse(y, x, rY*sqrt(rhs), rX*sqrt(rhs), (nPix,nPix))
        mskMyoIn[tupPtMyoIn] = 1

def genPhantom\
(
    arrT:ndarray, arrZ:ndarray, nPix:int,
    # motion parameter
    cycRes = 2*pi, # s
    cycHea = 1, # s
    ampRes = 5e-3,
    ampMyoOt = 8e-3,
    ampMyoIn = 16e-3,
):
    # image array
    arrP = zeros([arrT.size,arrZ.size,nPix,nPix], dtype=uint8)

    # masks
    mskFatOt = zeros([nPix,nPix], dtype=bool)
    mskFatIn = zeros([nPix,nPix], dtype=bool)
    mskArmL = zeros([nPix,nPix], dtype=bool)
    mskArmR = zeros([nPix,nPix], dtype=bool)
    mskMyoOt = zeros([nPix,nPix], dtype=bool)
    mskMyoIn = zeros([nPix,nPix], dtype=bool)

    # clear image
    arrP.fill(0)
    for iT in range(arrT.size):
        for iZ in range(arrZ.size):
            t = arrT[iT]
            z = arrZ[iZ]

            _updateMask \
            (
                t, z, nPix,
                mskFatOt, mskFatIn, mskArmL, mskArmR, mskMyoOt, mskMyoIn,
                cycRes, cycHea, ampRes, ampMyoOt, ampMyoIn,
            )
        
            # fill left arm
            arrP[iT][iZ][mskArmL] = Part.ArmL.value
            # fill right arm
            arrP[iT][iZ][mskArmR] = Part.ArmR.value
            # fill fat
            arrP[iT][iZ][mskFatOt & ~mskFatIn] = Part.Fat.value
            # fill body
            arrP[iT][iZ][mskFatIn & ~mskMyoOt] = Part.Body.value
            # fill myocardium
            arrP[iT][iZ][mskMyoOt & ~mskMyoIn] = Part.Myo.value
            # fill blood pool
            arrP[iT][iZ][mskMyoIn] = Part.Blood.value

    return arrP