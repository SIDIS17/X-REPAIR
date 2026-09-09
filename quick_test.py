from xrepair.synthetic import FAULTS,generate_vibration
from xrepair.signal_processing import extract_features
from xrepair.diagnosis import rule_based_diagnosis
from xrepair.ml import load_model,predict

FS=2048.0; RPM=1500.0
model=load_model()
print("="*90)
print("X-REPAIR 17A - TEST RAPIDE")
print("="*90)
for expected,fault in FAULTS.items():
    _,x=generate_vibration(fault,FS,3.0,RPM,17)
    ft,*_=extract_features(x,FS,RPM)
    d=rule_based_diagnosis(ft)
    ml="ML absent"
    if model:
        l,c=predict(ft.to_dict(),model)
        ml=f"ML={l} ({c*100:.1f}%)"
    print(f"Attendu={expected:20s} | Règles={d.label:20s} | {ml}")
print("="*90)
