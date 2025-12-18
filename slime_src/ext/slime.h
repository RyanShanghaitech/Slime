#pragma once

#include <vector>
#include <cstdint>

extern bool genPhant
(
    int64_t lNDim, int64_t lNPix,
    double dResAmp, double dCarAmp,
    std::vector<uint8_t>* voSlime
);