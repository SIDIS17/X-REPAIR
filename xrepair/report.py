from __future__ import annotations
from datetime import datetime
import json, pandas as pd

def build_payload(source, fs, rpm, features, diag, ml_label=None, ml_conf=None, anomaly=None):
    return {
        "project":"X-Repair 17A",
        "timestamp":datetime.now().isoformat(timespec="seconds"),
        "source":source,
        "sampling_frequency_hz":float(fs),
        "rpm":float(rpm),
        "features":features,
        "diagnosis":{
            "label":diag.label,
            "severity":diag.severity,
            "confidence":diag.confidence,
            "explanation":diag.explanation,
            "recommendation":diag.recommendation,
            "scores":diag.scores
        },
        "ml":{"label":ml_label,"confidence":ml_conf},
        "baseline_anomaly_score":anomaly
    }

def to_json_bytes(payload):
    return json.dumps(payload,indent=2,ensure_ascii=False).encode("utf-8")

def to_csv_bytes(payload):
    row={
        "timestamp":payload["timestamp"],
        "source":payload["source"],
        "fs_hz":payload["sampling_frequency_hz"],
        "rpm":payload["rpm"],
        "diagnosis":payload["diagnosis"]["label"],
        "severity":payload["diagnosis"]["severity"],
        "confidence":payload["diagnosis"]["confidence"],
        "ml_label":payload["ml"]["label"],
        "ml_confidence":payload["ml"]["confidence"],
        "baseline_anomaly_score":payload["baseline_anomaly_score"]
    }
    for k,v in payload["features"].items():
        row["feature_"+k]=v
    return pd.DataFrame([row]).to_csv(index=False).encode("utf-8-sig")
