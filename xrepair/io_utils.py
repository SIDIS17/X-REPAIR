from __future__ import annotations
import io, time
import numpy as np
import pandas as pd

TIME_COLUMNS = ["time","t","timestamp","temps"]
SIGNAL_COLUMNS = ["acceleration","accel","vibration","signal","value","valeur","x","ax"]

def read_csv_signal(file_obj, fallback_fs: float):
    raw = file_obj.read()
    if isinstance(raw,str): raw = raw.encode()
    df = None
    for sep in [",",";","\t"]:
        try:
            cand = pd.read_csv(io.BytesIO(raw), sep=sep)
            if len(cand.columns)>=1:
                df = cand
                if len(cand.columns)>1: break
        except Exception: pass
    if df is None or df.empty: raise ValueError("CSV vide ou illisible.")

    lm = {str(c).strip().lower():c for c in df.columns}
    tc = next((lm[c] for c in TIME_COLUMNS if c in lm), None)
    sc = next((lm[c] for c in SIGNAL_COLUMNS if c in lm), None)
    if sc is None:
        nums = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
        if tc in nums: nums.remove(tc)
        if not nums: raise ValueError("Aucune colonne numérique détectée.")
        sc = nums[-1]

    x = pd.to_numeric(df[sc], errors="coerce").to_numpy(float)
    if tc is not None:
        t = pd.to_numeric(df[tc], errors="coerce").to_numpy(float)
        m = np.isfinite(t)&np.isfinite(x)
        t,x = t[m],x[m]
        dt = np.diff(t)
        dt = dt[(dt>0)&np.isfinite(dt)]
        fs = 1/np.median(dt) if len(dt) else fallback_fs
    else:
        x = x[np.isfinite(x)]
        fs = float(fallback_fs)
        t = np.arange(len(x))/fs
    if len(x)<64: raise ValueError("Minimum 64 échantillons.")
    return t,x,float(fs)

def read_serial_signal(port, baudrate, n_samples, timeout_s=15.0):
    import serial
    vals=[]
    start=time.monotonic()
    with serial.Serial(port, baudrate=baudrate, timeout=.5) as ser:
        ser.reset_input_buffer()
        while len(vals)<n_samples and time.monotonic()-start<timeout_s:
            line=ser.readline().decode("utf-8","ignore").strip()
            if not line or line.startswith("#"): continue
            tok=line.replace(";",",").split(",")[-1].strip()
            try: vals.append(float(tok))
            except ValueError: pass
    if len(vals)<64: raise RuntimeError(f"Seulement {len(vals)} échantillons reçus.")
    return np.asarray(vals,float)
