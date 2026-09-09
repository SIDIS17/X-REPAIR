# X-Repair 17A v0.3 — Hybrid Frugal Condition Monitoring

X-Repair 17A est un prototype de maintenance conditionnelle pour moteurs et machines tournantes.

## Ce qui change dans la refonte
- diagnostic physique explicable + ML ;
- analyse temporelle, FFT et enveloppe ;
- baseline propre à la machine ;
- score d'anomalie ;
- indice de santé 0–100 ;
- priorité de maintenance ;
- Random Forest ;
- Extreme Learning Machine (ELM) pour l'apprentissage frugal ;
- benchmark précision / entraînement / latence ;
- acquisition CSV et série ;
- firmware ESP32 + ADXL345.

## Lancement Windows
Double-cliquer sur `START_XREPAIR_17A.bat`.

## Benchmark frugal
Après installation, lancer `BENCHMARK_FRUGAL.bat`.

## Limite importante
Les signaux synthétiques servent à valider l'architecture et le code. Ils ne prouvent pas
une performance industrielle. Une validation réelle exige des mesures de moteurs sains et
défectueux, une séparation stricte des machines entre apprentissage et test, et une
confirmation des diagnostics par inspection.
