from __future__ import annotations
from dataclasses import dataclass, asdict
import numpy as np
from scipy import signal as sp
from scipy.stats import kurtosis, skew

@dataclass
class Features:
    rms: float
    peak: float
    peak_to_peak: float
    crest_factor: float
    kurtosis: float
    skewness: float
    dominant_frequency_hz: float
    spectral_centroid_hz: float
    hf_ratio: float
    amp_1x: float
    amp_2x: float
    amp_3x: float
    amp_4x: float
    envelope_peak_hz: float
    envelope_rms: float

    def to_dict(self):
        return asdict(self)

def sanitize(x):
    a = np.asarray(x, dtype=float).reshape(-1)
    a = a[np.isfinite(a)]
    if a.size < 64:
        raise ValueError("Signal trop court: minimum 64 échantillons.")
    return a

def preprocess(x, fs, highpass_hz=1.0):
    x = sanitize(x)
    x = sp.detrend(x, type="linear")
    nyq = fs/2
    if 0 < highpass_hz < 0.95*nyq:
        sos = sp.butter(4, highpass_hz/nyq, btype="highpass", output="sos")
        try:
            x = sp.sosfiltfilt(sos, x)
        except ValueError:
            pass
    return x

def spectrum(x, fs):
    x = sanitize(x)
    n = len(x)
    w = np.hanning(n)
    y = np.fft.rfft(x*w)
    f = np.fft.rfftfreq(n, 1/fs)
    scale = max(np.sum(w)/2, 1e-12)
    a = np.abs(y)/scale
    if len(a): a[0] *= .5
    return f, a

def amplitude_near(f, a, target, tol):
    if target <= 0 or len(f)==0: return 0.0
    m = (f >= target-tol) & (f <= target+tol)
    if np.any(m): return float(np.max(a[m]))
    return float(a[np.argmin(np.abs(f-target))])

def envelope_analysis(x, fs):
    x = sanitize(x)
    analytic = sp.hilbert(x)
    env = np.abs(analytic)
    env = sp.detrend(env)
    f, a = spectrum(env, fs)
    if len(a)>1:
        i = 1 + int(np.argmax(a[1:]))
        peak_hz = float(f[i])
    else:
        peak_hz = 0.0
    rms = float(np.sqrt(np.mean(env**2)))
    return env, f, a, peak_hz, rms

def extract_features(x, fs, rpm):
    x = preprocess(x, fs)
    f, a = spectrum(x, fs)

    rms = float(np.sqrt(np.mean(x*x)))
    peak = float(np.max(np.abs(x)))
    p2p = float(np.ptp(x))
    cf = float(peak/rms) if rms > 1e-12 else 0.0
    k = float(kurtosis(x, fisher=False, bias=False))
    s = float(skew(x, bias=False))

    if len(a)>1:
        idx = 1 + int(np.argmax(a[1:]))
        dom = float(f[idx])
    else:
        dom = 0.0

    p = a*a
    pt = float(np.sum(p))
    centroid = float(np.sum(f*p)/pt) if pt>1e-12 else 0.0
    hf_start = min(max(0.25*fs, 5.0), 0.45*fs)
    hf_ratio = float(np.sum(p[f>=hf_start])/pt) if pt>1e-12 else 0.0

    f1 = max(rpm/60.0, 1e-6)
    res = fs/max(len(x), 1)
    tol = max(1.5*res, 0.03*f1, 0.5)
    harmonics = [amplitude_near(f,a,h*f1,tol) for h in (1,2,3,4)]

    env, ef, ea, epeak, erms = envelope_analysis(x, fs)

    feat = Features(
        rms=rms, peak=peak, peak_to_peak=p2p, crest_factor=cf,
        kurtosis=k, skewness=s, dominant_frequency_hz=dom,
        spectral_centroid_hz=centroid, hf_ratio=hf_ratio,
        amp_1x=harmonics[0], amp_2x=harmonics[1],
        amp_3x=harmonics[2], amp_4x=harmonics[3],
        envelope_peak_hz=epeak, envelope_rms=erms
    )
    return feat, f, a, env, ef, ea
