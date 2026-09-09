from __future__ import annotations
from .common import mean, clamp

def analyze(temperatures_c: list[float], ambient_c: float = 25.0, limit_c: float = 80.0) -> dict:
    if not temperatures_c:
        raise ValueError("Aucune température fournie.")
    tmax = max(temperatures_c)
    tmin = min(temperatures_c)
    tavg = mean(temperatures_c)
    delta = tmax - ambient_c
    spread = tmax - tmin
    severity = clamp(max((tmax-limit_c)/max(limit_c,1), 0) + max(delta-35,0)/60 + spread/100)

    if tmax >= limit_c:
        label = "surchauffe"
    elif delta > 35:
        label = "echauffement_anormal"
    elif spread > 20:
        label = "gradient_thermique_anormal"
    else:
        label = "thermique_normal"

    return {
        "module":"X-Repair Thermal",
        "diagnostic":label,
        "health_score":round((1-severity)*100,1),
        "features":{
            "temperature_max_c":tmax,
            "temperature_min_c":tmin,
            "temperature_moyenne_c":tavg,
            "delta_ambient_c":delta,
            "spread_c":spread,
            "limit_c":limit_c
        },
        "recommendation":"Vérifier ventilation, charge, connexions, dissipateurs et lubrification selon l'équipement."
    }
