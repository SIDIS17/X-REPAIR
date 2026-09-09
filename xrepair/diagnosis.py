from __future__ import annotations
from dataclasses import dataclass
from .signal_processing import Features

@dataclass
class Diagnosis:
    label: str
    severity: str
    confidence: float
    explanation: str
    recommendation: str
    scores: dict[str, float]

def clip01(v): return float(min(1.0, max(0.0, v)))

def rule_based_diagnosis(f: Features) -> Diagnosis:
    eps = 1e-9
    hsum = f.amp_1x + f.amp_2x + f.amp_3x + f.amp_4x + eps
    share1 = f.amp_1x/hsum
    r2 = f.amp_2x/max(f.amp_1x,eps)
    r3 = f.amp_3x/max(f.amp_1x,eps)
    r4 = f.amp_4x/max(f.amp_1x,eps)

    vibration = clip01((f.rms-0.12)/0.45)
    impulse = clip01((f.kurtosis-3.0)/5.0)
    hf = clip01((f.hf_ratio-0.12)/0.55)
    crest = clip01((f.crest_factor-2.5)/4.0)

    bearing = clip01(0.55*hf + 0.30*impulse + 0.15*crest)
    hf_penalty = clip01(1 - 0.85*hf)
    imbalance = clip01((0.08 + 0.92*share1*vibration) * hf_penalty)
    misalignment = clip01((0.08 + 0.92*clip01((r2-0.35)/1.0)*max(vibration,.35))*hf_penalty)
    multi = clip01((min(r2,1.2)+min(r3,1.2)+min(r4,1.2)-0.45)/2.5)
    looseness = clip01((0.08 + 0.92*multi*max(vibration,.4))*hf_penalty)

    maxfault = max(imbalance, misalignment, looseness, bearing)
    normal = clip01(0.93 - 0.55*vibration - 0.55*hf - 0.35*maxfault)

    if f.rms < 0.15 and f.hf_ratio < 0.18 and f.kurtosis < 4.0:
        normal = max(normal, .80)
    if f.hf_ratio > .45:
        bearing = max(bearing, .82)

    scores = {
        "Normal": normal,
        "Déséquilibre": imbalance,
        "Désalignement": misalignment,
        "Jeu mécanique": looseness,
        "Défaut de roulement": bearing
    }
    label = max(scores, key=scores.get)
    confidence = float(scores[label])

    severity_index = max(
        clip01((f.rms-.10)/.70),
        clip01((f.kurtosis-3.0)/7.0),
        clip01((f.hf_ratio-.10)/.60)
    )
    if label == "Normal": severity = "Faible"
    elif severity_index < .35: severity = "Faible"
    elif severity_index < .70: severity = "Modérée"
    else: severity = "Élevée"

    exp = {
        "Normal": "Aucune signature générique de défaut ne domine nettement.",
        "Déséquilibre": "La composante 1X domine et le niveau vibratoire est significatif.",
        "Désalignement": "La composante 2X est élevée par rapport à la composante 1X.",
        "Jeu mécanique": "Plusieurs harmoniques 2X, 3X et 4X sont simultanément présents.",
        "Défaut de roulement": "Le signal présente une impulsivité et/ou une énergie haute fréquence élevées."
    }
    rec = {
        "Normal": "Conserver cette mesure comme référence et poursuivre la surveillance.",
        "Déséquilibre": "Contrôler l'équilibrage, l'encrassement, les masses tournantes et les fixations.",
        "Désalignement": "Contrôler l'alignement des arbres, l'accouplement et les contraintes de montage.",
        "Jeu mécanique": "Inspecter les fixations, paliers, supports et jeux mécaniques.",
        "Défaut de roulement": "Inspecter roulement et lubrification; confirmer par analyse d'enveloppe."
    }
    return Diagnosis(label, severity, confidence, exp[label], rec[label], scores)

def fuse(rule_diag: Diagnosis, ml_label: str|None, ml_conf: float|None) -> Diagnosis:
    if ml_label is None or ml_conf is None:
        return rule_diag
    if ml_label == rule_diag.label:
        rule_diag.confidence = float(min(.99, .55*rule_diag.confidence + .45*ml_conf))
        rule_diag.explanation += " Le modèle ML confirme le diagnostic."
        return rule_diag
    if ml_conf >= .90:
        rule_diag.explanation += f" Le modèle ML propose {ml_label} avec forte confiance; vérifier le désaccord."
    return rule_diag
