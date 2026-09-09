from __future__ import annotations
import time
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from xrepair.synthetic import generate_vibration
from xrepair.signal_processing import extract_features
from xrepair.ml import FEATURE_ORDER
from xrepair.frugal_ml import ExtremeLearningMachine, benchmark_model, save_elm

LABELS = ["Normal","Déséquilibre","Désalignement","Jeu mécanique","Défaut de roulement"]
FAULTS = ["normal","imbalance","misalignment","looseness","bearing_fault"]

def dataset(n_per_class=45, fs=2048.0):
    X=[]; y=[]
    seed=1000
    for label,fault in zip(LABELS,FAULTS):
        for i in range(n_per_class):
            rpm=900 + (i % 25)*70
            _,x=generate_vibration(fault,fs,2.0,rpm,seed+i)
            f,*_=extract_features(x,fs,rpm)
            X.append([f.to_dict()[k] for k in FEATURE_ORDER])
            y.append(label)
        seed += 500
    return np.asarray(X,float), np.asarray(y)

X,y=dataset()
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.30,stratify=y,random_state=17)

elm=ExtremeLearningMachine(hidden_units=96,alpha=1e-2,random_state=17)
b_elm=benchmark_model(elm,Xtr,ytr,Xte,yte)
save_elm(elm)

rf=Pipeline([
    ("scale",StandardScaler()),
    ("rf",RandomForestClassifier(n_estimators=250,max_depth=12,random_state=17,n_jobs=-1))
])
t0=time.perf_counter(); rf.fit(Xtr,ytr); train=time.perf_counter()-t0
t0=time.perf_counter(); pred=rf.predict(Xte); infer=time.perf_counter()-t0
from sklearn.metrics import accuracy_score
b_rf={
    "accuracy":float(accuracy_score(yte,pred)),
    "train_seconds":float(train),
    "inference_ms_per_sample":float(1000*infer/len(Xte)),
    "parameter_count":"N/A (tree ensemble)"
}

rows=[
    {"model":"Extreme Learning Machine",**b_elm.__dict__},
    {"model":"Random Forest",**b_rf}
]
df=pd.DataFrame(rows)
print(df.to_string(index=False))
out="data/frugal_benchmark.csv"
df.to_csv(out,index=False)
print(f"\nRésultats enregistrés: {out}")
