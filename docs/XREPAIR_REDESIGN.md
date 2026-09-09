# X-Repair 17A — Refonte v0.3

## Positionnement
X-Repair devient une plateforme de maintenance conditionnelle et de diagnostic assisté,
plutôt qu'un simple classifieur de vibrations.

## Architecture
1. Acquisition : CSV, série, ESP32/ADXL345.
2. Signal : detrend, filtrage, FFT, enveloppe.
3. Signatures : RMS, crête, kurtosis, énergie HF, 1X–4X.
4. Référence machine : baseline et score d'anomalie.
5. Intelligence hybride :
   - règles physiques explicables ;
   - Random Forest ;
   - Extreme Learning Machine frugale.
6. Fusion : diagnostic + confiance + indice de santé.
7. Maintenance : priorité d'inspection et recommandations.
8. Validation : benchmarks précision, temps d'entraînement et latence.

## Principe scientifique
Le système ne doit pas "écouter un moteur et deviner". Il compare des signatures mesurées,
des fréquences liées au régime et une référence propre à la machine. Le modèle ML complète
l'analyse physique mais ne la remplace pas.

## Prochaine étape
Pour une validation académique sérieuse :
- dataset réel multi-moteurs ;
- séparation train/validation/test par moteur ;
- comparaison RF / SVM / ELM / modèle quantique-inspiré ;
- tests à différents régimes et charges ;
- matrice de confusion, F1 macro, latence, RAM et énergie ;
- étude de généralisation à une machine non vue.
