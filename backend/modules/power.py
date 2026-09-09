from __future__ import annotations
from .common import rms, mean, clamp

def analyze(voltage: list[float], current: list[float], nominal_voltage: float | None = None) -> dict:
    n = min(len(voltage), len(current))
    if n < 8:
        raise ValueError("Au moins 8 couples tension/courant sont requis.")
    v = voltage[:n]
    i = current[:n]
    vrms = rms(v)
    irms = rms(i)
    real_power = mean([v[k]*i[k] for k in range(n)])
    apparent = vrms*irms
    pf = real_power/apparent if apparent > 1e-12 else 0.0
    dev = 0.0
    if nominal_voltage:
        dev = abs(vrms-nominal_voltage)/max(nominal_voltage,1e-9)

    stress = clamp(0.5*dev/0.10 + 0.5*max(0,0.75-abs(pf))/0.75)
    if nominal_voltage and dev > 0.10:
        label = "tension_hors_tolerance"
    elif abs(pf) < 0.70 and irms > 0:
        label = "facteur_de_puissance_faible"
    else:
        label = "electrique_normal"

    return {
        "module":"X-Repair Power",
        "diagnostic":label,
        "health_score":round((1-stress)*100,1),
        "features":{
            "vrms":vrms,"irms":irms,"real_power_w":real_power,
            "apparent_power_va":apparent,"power_factor":pf,
            "voltage_deviation_ratio":dev
        },
        "recommendation":"Contrôler alimentation, charge, connexions, cos φ et qualité de puissance selon l'installation."
    }
