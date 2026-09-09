# Architecture

```text
Capteur / CSV / Générateur
          |
          v
     Acquisition
          |
          v
  Prétraitement signal
          |
   +------+------+
   |             |
   v             v
 Domaine temps   FFT + enveloppe
   |             |
   +------+------+
          |
          v
Extraction caractéristiques
          |
   +------+------+
   |             |
   v             v
Règles          ML
   |             |
   +------+------+
          |
          v
Diagnostic + baseline
          |
          v
Recommandation + export
```
