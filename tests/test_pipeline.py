import numpy as np
from xrepair.synthetic import generate_vibration
from xrepair.signal_processing import extract_features
from xrepair.diagnosis import rule_based_diagnosis

def test_pipeline():
    t,x=generate_vibration("normal",2048,2,1500,1)
    ft,*_=extract_features(x,2048,1500)
    d=rule_based_diagnosis(ft)
    assert len(t)==len(x)
    assert np.isfinite(ft.rms)
    assert d.label in ["Normal","Déséquilibre","Désalignement","Jeu mécanique","Défaut de roulement"]

def test_bearing_has_hf_or_kurtosis():
    _,n=generate_vibration("normal",2048,3,1500,2)
    _,b=generate_vibration("bearing_fault",2048,3,1500,2)
    fn,*_=extract_features(n,2048,1500)
    fb,*_=extract_features(b,2048,1500)
    assert fb.hf_ratio>fn.hf_ratio or fb.kurtosis>fn.kurtosis
