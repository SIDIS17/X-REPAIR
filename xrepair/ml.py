from __future__ import annotations
from pathlib import Path
import joblib, numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from .synthetic import generate_vibration
from .signal_processing import extract_features

MODEL_PATH = Path(__file__).resolve().parents[1]/"models"/"xrepair_rf.joblib"
FEATURE_ORDER = [
    "rms","peak","peak_to_peak","crest_factor","kurtosis","skewness",
    "dominant_frequency_hz","spectral_centroid_hz","hf_ratio",
    "amp_1x","amp_2x","amp_3x","amp_4x","envelope_peak_hz","envelope_rms"
]

def vectorize(d):
    return np.array([[float(d[k]) for k in FEATURE_ORDER]], dtype=float)

def train_model(samples_per_class=80, fs=2048.0, rpm=1500.0, model_path=MODEL_PATH):
    labels = ["Normal","Déséquilibre","Désalignement","Jeu mécanique","Défaut de roulement"]
    faults = ["normal","imbalance","misalignment","looseness","bearing_fault"]
    X=[]; y=[]; seed=1700
    for label,fault in zip(labels,faults):
        for i in range(samples_per_class):
            rr = rpm*(0.75+0.5*((i%17)/16))
            _,x=generate_vibration(fault,fs,2.2,rr,seed+i)
            ft,*_=extract_features(x,fs,rr)
            X.append([ft.to_dict()[k] for k in FEATURE_ORDER]); y.append(label)
        seed += 1000
    X=np.asarray(X,float); y=np.asarray(y)
    Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.25,random_state=17,stratify=y)
    model=Pipeline([
        ("scale",StandardScaler()),
        ("rf",RandomForestClassifier(
            n_estimators=300, max_depth=14, class_weight="balanced",
            random_state=17, n_jobs=-1
        ))
    ])
    model.fit(Xtr,ytr)
    acc=float(accuracy_score(yte,model.predict(Xte)))
    model_path.parent.mkdir(parents=True,exist_ok=True)
    joblib.dump(model,model_path)
    return model,acc

def load_model(path=MODEL_PATH):
    return joblib.load(path) if path.exists() else None

def predict(features, model=None):
    model = model or load_model()
    if model is None: return None,None
    x=vectorize(features)
    label=str(model.predict(x)[0])
    conf=float(np.max(model.predict_proba(x)[0])) if hasattr(model,"predict_proba") else None
    return label,conf
