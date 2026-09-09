from __future__ import annotations
from pathlib import Path
import numpy as np, pandas as pd, plotly.graph_objects as go, streamlit as st

from xrepair.synthetic import FAULTS, generate_vibration
from xrepair.signal_processing import extract_features
from xrepair.diagnosis import rule_based_diagnosis, fuse
from xrepair.io_utils import read_csv_signal, read_serial_signal
from xrepair.ml import load_model, predict, train_model
from xrepair.baseline import load_baseline, anomaly_score, create_baseline
from xrepair.report import build_payload, to_json_bytes, to_csv_bytes
from xrepair.health import machine_health_index, maintenance_priority

ROOT=Path(__file__).resolve().parent
LOGO=ROOT/"assets"/"logo_17a.jpeg"

st.set_page_config(page_title="X-Repair 17A",page_icon="🛠️",layout="wide")
st.markdown("""
<style>
.block-container{padding-top:1rem}
.x-title{font-size:2.2rem;font-weight:800;letter-spacing:.03em}
.card{padding:1rem;border:1px solid rgba(127,127,127,.25);border-radius:14px}
</style>""",unsafe_allow_html=True)

c1,c2=st.columns([1,5])
with c1:
    if LOGO.exists(): st.image(str(LOGO),width=130)
with c2:
    st.markdown('<div class="x-title">X-Repair 17A</div>',unsafe_allow_html=True)
    st.write("Diagnostic vibratoire intelligent — moteurs et machines tournantes")

with st.sidebar:
    st.header("Configuration")
    mode=st.radio("Source",["Démonstration","Fichier CSV","Port série"])
    fs_input=st.number_input("Fréquence échantillonnage [Hz]",100.0,100000.0,2048.0,100.0)
    rpm=st.number_input("Régime [tr/min]",60.0,30000.0,1500.0,50.0)
    st.caption(f"1X = {rpm/60:.2f} Hz")
    use_ml=st.toggle("Activer ML",True)
    baseline=load_baseline()
    if baseline: st.success("Baseline disponible")
    else: st.info("Baseline absente")

    model=load_model()
    if use_ml and model is None:
        if st.button("Entraîner le modèle"):
            with st.spinner("Entraînement..."):
                model,acc=train_model()
            st.success(f"Accuracy validation synthétique: {acc:.3f}")

t=x=None
fs=float(fs_input)
source=mode

if mode=="Démonstration":
    a,b=st.columns([2,1])
    with a: label=st.selectbox("Scénario",list(FAULTS.keys()))
    with b: duration=st.slider("Durée [s]",1.0,10.0,4.0,.5)
    t,x=generate_vibration(FAULTS[label],fs,duration,rpm,17)
    source=f"Démo — {label}"

elif mode=="Fichier CSV":
    up=st.file_uploader("CSV de vibration",type=["csv","txt"])
    if up:
        try:
            t,x,fs=read_csv_signal(up,fs)
            source=up.name
            st.success(f"{len(x)} échantillons — fs={fs:.2f} Hz")
        except Exception as e: st.error(str(e))

else:
    a,b,c=st.columns(3)
    with a: port=st.text_input("Port","COM3")
    with b: baud=st.selectbox("Baudrate",[9600,57600,115200,230400],index=3)
    with c: ns=int(st.number_input("Échantillons",256,200000,4096,256))
    if st.button("Acquérir"):
        try:
            with st.spinner("Acquisition..."):
                x=read_serial_signal(port,baud,ns,20)
                t=np.arange(len(x))/fs
                source=f"Série {port}"
        except Exception as e: st.error(str(e))

if x is None:
    st.info("Chargez ou générez un signal.")
    st.stop()

feat,f,a,env,ef,ea=extract_features(x,fs,rpm)
diag=rule_based_diagnosis(feat)
ml_label=ml_conf=None
if use_ml:
    model=load_model()
    if model:
        ml_label,ml_conf=predict(feat.to_dict(),model)
diag=fuse(diag,ml_label,ml_conf)

anom=anomaly_score(feat.to_dict(),baseline)
health=machine_health_index(diag, anom)
priority=maintenance_priority(health)

st.subheader("Diagnostic")
m1,m2,m3,m4=st.columns(4)
m1.metric("État probable",diag.label)
m2.metric("Sévérité",diag.severity)
m3.metric("Confiance règles",f"{diag.confidence*100:.1f}%")
m4.metric("RMS",f"{feat.rms:.4f}")

h1,h2=st.columns(2)
h1.metric("Indice de santé machine",f"{health:.1f}/100")
h2.metric("Priorité maintenance",priority)

if anom is not None:
    st.metric("Score d'anomalie vs baseline",f"{anom:.2f}")

st.markdown(f"""<div class="card"><b>Interprétation :</b> {diag.explanation}<br><br>
<b>Recommandation :</b> {diag.recommendation}</div>""",unsafe_allow_html=True)

if ml_label is not None:
    st.caption(f"ML : {ml_label} — confiance {ml_conf*100:.1f}%")

st.warning("Prototype expérimental : calibrer les seuils et valider sur le moteur réel avant décision de maintenance.")

st.subheader("Signal temporel")
fig=go.Figure()
step=max(1,len(t)//12000)
fig.add_trace(go.Scatter(x=t[::step],y=np.asarray(x)[::step],mode="lines",name="Vibration"))
fig.update_layout(height=340,xaxis_title="Temps [s]",yaxis_title="Amplitude")
st.plotly_chart(fig,use_container_width=True)

st.subheader("FFT")
fig2=go.Figure()
fig2.add_trace(go.Scatter(x=f,y=a,mode="lines",name="FFT"))
f1=rpm/60
for h in range(1,5):
    if h*f1 <= fs/2:
        fig2.add_vline(x=h*f1,line_dash="dot",annotation_text=f"{h}X")
fig2.update_layout(height=380,xaxis_title="Fréquence [Hz]",yaxis_title="Amplitude")
st.plotly_chart(fig2,use_container_width=True)

st.subheader("Enveloppe")
fig3=go.Figure()
fig3.add_trace(go.Scatter(x=ef,y=ea,mode="lines",name="FFT enveloppe"))
fig3.update_layout(height=330,xaxis_title="Fréquence [Hz]",yaxis_title="Amplitude")
st.plotly_chart(fig3,use_container_width=True)

st.subheader("Caractéristiques")
df=pd.DataFrame({"Indicateur":list(feat.to_dict().keys()),"Valeur":list(feat.to_dict().values())})
st.dataframe(df,use_container_width=True,hide_index=True)

with st.expander("Scores par hypothèse"):
    s=pd.DataFrame({"Hypothèse":diag.scores.keys(),"Score":diag.scores.values()}).sort_values("Score",ascending=False)
    st.dataframe(s,use_container_width=True,hide_index=True)

with st.expander("Créer une baseline depuis ce signal"):
    st.write("Cette version crée une baseline mono-mesure. Pour une vraie machine, utiliser plusieurs mesures saines.")
    if st.button("Enregistrer ce signal comme baseline"):
        create_baseline([feat.to_dict()])
        st.success("Baseline enregistrée.")

payload=build_payload(source,fs,rpm,feat.to_dict(),diag,ml_label,ml_conf,anom)

st.subheader("Export")
e1,e2=st.columns(2)
with e1:
    st.download_button("Télécharger JSON",to_json_bytes(payload),"xrepair_diagnostic.json","application/json",use_container_width=True)
with e2:
    st.download_button("Télécharger CSV",to_csv_bytes(payload),"xrepair_diagnostic.csv","text/csv",use_container_width=True)
