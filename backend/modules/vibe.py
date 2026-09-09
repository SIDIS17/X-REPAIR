from __future__ import annotations
from .common import rms, peak, crest_factor, kurtosis_pearson, dft_magnitude, clamp

def analyze(samples: list[float], fs: float, rpm: float) -> dict:
    if len(samples) < 32:
        raise ValueError("Au moins 32 échantillons sont requis.")
    freqs, mags = dft_magnitude(samples, fs)
    f1 = max(rpm/60.0, 1e-9)

    def amp_near(target: float) -> float:
        if not freqs:
            return 0.0
        idx = min(range(len(freqs)), key=lambda i: abs(freqs[i]-target))
        return mags[idx]

    a1, a2, a3, a4 = [amp_near(h*f1) for h in (1,2,3,4)]
    k = kurtosis_pearson(samples)
    r = rms(samples)
    cf = crest_factor(samples)
    hsum = a1+a2+a3+a4+1e-12

    scores = {
        "normal": clamp(0.9 - min(r/1.2, 0.5) - max(k-3.0,0)/10),
        "desequilibre": clamp((a1/hsum)*min(r/0.5, 1.0)),
        "desalignement": clamp((a2/max(a1,1e-9))/1.5),
        "jeu_mecanique": clamp((a2+a3+a4)/max(a1+a2+a3+a4,1e-9)),
        "roulement": clamp(0.55*max(k-3.0,0)/5 + 0.45*max(cf-3.0,0)/5),
    }
    label = max(scores, key=scores.get)
    health = clamp(1.0 - max(v for k2,v in scores.items() if k2 != "normal"))*100
    return {
        "module":"X-Repair Vibe",
        "diagnostic":label,
        "health_score":round(health,1),
        "features":{
            "rms":r, "peak":peak(samples), "crest_factor":cf,
            "kurtosis":k, "f1_hz":f1, "amp_1x":a1, "amp_2x":a2,
            "amp_3x":a3, "amp_4x":a4
        },
        "scores":scores,
        "spectrum":{"frequency_hz":freqs[:160], "amplitude":mags[:160]},
        "recommendation":{
            "normal":"Poursuivre la surveillance périodique.",
            "desequilibre":"Contrôler l'équilibrage, l'encrassement et les fixations.",
            "desalignement":"Vérifier l'alignement des arbres et l'accouplement.",
            "jeu_mecanique":"Inspecter les supports, paliers, boulons et jeux mécaniques.",
            "roulement":"Inspecter le roulement et la lubrification; confirmer par analyse d'enveloppe."
        }[label]
    }
