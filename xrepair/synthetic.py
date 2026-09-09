from __future__ import annotations
import numpy as np

FAULTS = {
    "Normal": "normal",
    "Déséquilibre": "imbalance",
    "Désalignement": "misalignment",
    "Jeu mécanique": "looseness",
    "Défaut de roulement": "bearing_fault",
}

def generate_vibration(
    fault: str = "normal",
    fs: float = 2048.0,
    duration: float = 4.0,
    rpm: float = 1500.0,
    seed: int | None = 17,
) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    n = max(512, int(fs * duration))
    t = np.arange(n) / fs
    f1 = rpm / 60.0

    x = 0.03 * rng.standard_normal(n)
    x += 0.07 * np.sin(2*np.pi*f1*t + rng.uniform(0, 2*np.pi))

    if fault == "normal":
        x += 0.015*np.sin(2*np.pi*2*f1*t)
    elif fault == "imbalance":
        x += 0.75*np.sin(2*np.pi*f1*t)
        x += 0.05*np.sin(2*np.pi*2*f1*t)
    elif fault == "misalignment":
        x += 0.35*np.sin(2*np.pi*f1*t)
        x += 0.62*np.sin(2*np.pi*2*f1*t)
        x += 0.14*np.sin(2*np.pi*3*f1*t)
    elif fault == "looseness":
        for h, a in [(1,0.32),(2,0.29),(3,0.25),(4,0.21)]:
            x += a*np.sin(2*np.pi*h*f1*t + rng.uniform(0,1))
        x += 0.07*np.sign(np.sin(2*np.pi*f1*t))
    elif fault == "bearing_fault":
        x += 0.08*np.sin(2*np.pi*f1*t)
        bp = 4.8*f1
        period = max(1, int(fs/bp))
        resonance = min(650.0, fs*0.35)
        m = max(16, int(fs*0.025))
        tt = np.arange(m)/fs
        pulse = np.exp(-120*tt)*np.sin(2*np.pi*resonance*tt)
        for i in range(0, n, period):
            j = max(0, i + int(rng.integers(-2,3)))
            e = min(n, j+m)
            x[j:e] += 0.85*pulse[:e-j]
        x += 0.05*rng.standard_normal(n)
    else:
        raise ValueError(f"Défaut inconnu: {fault}")
    return t.astype(float), x.astype(float)

def generate_xyz(
    fault: str = "normal",
    fs: float = 2048.0,
    duration: float = 4.0,
    rpm: float = 1500.0,
    seed: int = 17,
):
    t, x = generate_vibration(fault, fs, duration, rpm, seed)
    _, y = generate_vibration(fault, fs, duration, rpm, seed+1)
    _, z = generate_vibration(fault, fs, duration, rpm, seed+2)
    y *= 0.8
    z *= 0.6
    return t, np.column_stack([x, y, z])
