from __future__ import annotations
from .common import rms, peak, crest_factor, kurtosis_pearson, dominant_frequency, clamp

def analyze(samples: list[float], fs: float) -> dict:
    if len(samples) < 32:
        raise ValueError("Au moins 32 échantillons sont requis.")
    r = rms(samples)
    p = peak(samples)
    cf = crest_factor(samples)
    k = kurtosis_pearson(samples)
    dom = dominant_frequency(samples, fs)

    impulsive = clamp(max(k-3.0,0)/7)
    high_tone = clamp(dom/(0.45*fs)) if fs > 0 else 0
    anomaly = clamp(0.45*min(r/0.5,1)+0.30*impulsive+0.25*high_tone)
    health = (1-anomaly)*100

    if anomaly < 0.25:
        label = "acoustique_normale"
    elif impulsive > 0.55:
        label = "impacts_ou_roulement_suspects"
    elif high_tone > 0.60:
        label = "composante_aigue_anormale"
    else:
        label = "bruit_anormal_a_controler"

    return {
        "module":"X-Repair Acoustic",
        "diagnostic":label,
        "health_score":round(health,1),
        "features":{
            "rms":r,"peak":p,"crest_factor":cf,"kurtosis":k,
            "dominant_frequency_hz":dom
        },
        "recommendation":"Comparer avec une référence saine, vérifier bruit de roulement, cavitation, frottement et ventilation."
    }
