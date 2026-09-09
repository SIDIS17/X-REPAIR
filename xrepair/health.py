from __future__ import annotations

def machine_health_index(diagnosis, anomaly_score=None) -> float:
    """Return a 0..100 health score. Prototype heuristic, not a safety rating."""
    penalty = 55.0 * float(diagnosis.confidence if diagnosis.label != "Normal" else 0.0)
    severity_penalty = {"Faible": 5.0, "Modérée": 18.0, "Élevée": 35.0}.get(diagnosis.severity, 10.0)
    if diagnosis.label == "Normal":
        severity_penalty = 0.0
    anomaly_penalty = 0.0 if anomaly_score is None else min(25.0, 5.0*float(anomaly_score))
    return max(0.0, min(100.0, 100.0 - penalty - severity_penalty - anomaly_penalty))

def maintenance_priority(health: float) -> str:
    if health >= 85: return "Surveillance normale"
    if health >= 65: return "Contrôle planifié"
    if health >= 40: return "Inspection prioritaire"
    return "Inspection immédiate recommandée"
