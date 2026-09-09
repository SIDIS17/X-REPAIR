from __future__ import annotations
import json
from pathlib import Path
import numpy as np

DEFAULT_PATH = Path(__file__).resolve().parents[1]/"data"/"baseline.json"

def create_baseline(feature_dicts: list[dict], path: Path = DEFAULT_PATH):
    if not feature_dicts:
        raise ValueError("Aucune mesure fournie.")
    keys = list(feature_dicts[0].keys())
    stats = {}
    for k in keys:
        vals = np.array([float(d[k]) for d in feature_dicts], dtype=float)
        stats[k] = {"mean": float(np.mean(vals)), "std": float(np.std(vals, ddof=1) if len(vals)>1 else 0.0)}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8")
    return stats

def load_baseline(path: Path = DEFAULT_PATH):
    if not path.exists(): return None
    return json.loads(path.read_text(encoding="utf-8"))

def anomaly_score(features: dict, baseline: dict|None):
    if not baseline: return None
    zs = []
    for k,v in features.items():
        if k not in baseline: continue
        mu = baseline[k]["mean"]
        sd = baseline[k]["std"]
        if sd > 1e-9:
            zs.append(abs((float(v)-mu)/sd))
    if not zs: return 0.0
    return float(np.mean(sorted(zs, reverse=True)[:5]))
