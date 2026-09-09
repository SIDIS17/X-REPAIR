from __future__ import annotations
import math
from typing import Iterable

def mean(xs: Iterable[float]) -> float:
    xs = list(xs)
    return sum(xs) / len(xs) if xs else 0.0

def rms(xs: Iterable[float]) -> float:
    xs = list(xs)
    return math.sqrt(sum(x*x for x in xs) / len(xs)) if xs else 0.0

def variance(xs: Iterable[float]) -> float:
    xs = list(xs)
    if not xs:
        return 0.0
    m = mean(xs)
    return sum((x-m)**2 for x in xs)/len(xs)

def std(xs: Iterable[float]) -> float:
    return math.sqrt(variance(xs))

def peak(xs: Iterable[float]) -> float:
    xs = list(xs)
    return max((abs(x) for x in xs), default=0.0)

def crest_factor(xs: Iterable[float]) -> float:
    r = rms(xs)
    return peak(xs)/r if r > 1e-12 else 0.0

def kurtosis_pearson(xs: Iterable[float]) -> float:
    xs = list(xs)
    n = len(xs)
    if n < 4:
        return 0.0
    m = mean(xs)
    v = sum((x-m)**2 for x in xs)/n
    if v <= 1e-18:
        return 0.0
    m4 = sum((x-m)**4 for x in xs)/n
    return m4/(v*v)

def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))

def dft_magnitude(signal: list[float], fs: float, max_bins: int = 512) -> tuple[list[float], list[float]]:
    """Small dependency-free DFT for API demos and short windows.

    For large production datasets, install NumPy/SciPy and replace this with an FFT.
    """
    n = len(signal)
    if n == 0:
        return [], []
    step = max(1, (n//2 + 1)//max_bins)
    freqs, mags = [], []
    for k in range(0, n//2 + 1, step):
        re = 0.0
        im = 0.0
        for i, x in enumerate(signal):
            angle = -2.0*math.pi*k*i/n
            re += x*math.cos(angle)
            im += x*math.sin(angle)
        mag = (2.0/n)*math.sqrt(re*re + im*im)
        freqs.append(k*fs/n)
        mags.append(mag)
    return freqs, mags

def dominant_frequency(signal: list[float], fs: float) -> float:
    f, a = dft_magnitude(signal, fs, max_bins=256)
    if len(a) <= 1:
        return 0.0
    idx = max(range(1, len(a)), key=lambda i: a[i])
    return float(f[idx])
