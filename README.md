# X-REPAIR 17A — Final Multimodal Edition

<p align="center">
  <img src="assets/branding/spiderman_xrepair.jpg" width="680" alt="X-Repair visual identity">
</p>

**X-Repair 17A** réunit le visuel minimal/neumorphique de **META POMPE** avec une architecture modulaire de diagnostic pour systèmes mécaniques, électromécaniques et électroniques.

## Modules

- **X-Repair Vibe** — vibration, FFT simplifiée, RMS, kurtosis, 1X–4X, défauts mécaniques.
- **X-Repair Circuit** — analyse de netlist, vérifications statiques, exécution optionnelle de `ngspice`.
- **X-Repair Acoustic** — analyse acoustique, impulsivité et fréquence dominante.
- **X-Repair Thermal** — température, gradient thermique et surchauffe.
- **X-Repair Power** — Vrms, Irms, puissance active/apparente et facteur de puissance.
- **X-Repair Core** — fusion multimodale, score de santé et priorité de maintenance.

## Démarrage Windows

Double-cliquer sur :

```text
START_XREPAIR_17A.bat
```

Le script :
1. crée `.venv`,
2. installe FastAPI/Uvicorn,
3. lance l'API sur `http://127.0.0.1:8000`,
4. ouvre l'interface.

Documentation API :

```text
http://127.0.0.1:8000/docs
```

## Architecture

```text
Capteurs / Netlist / Mesures
            |
            v
+---------------------------+
| Vibe      | Acoustic      |
| Thermal   | Power         |
| Circuit   |               |
+-------------+-------------+
              |
              v
        X-Repair Core
              |
              v
Score de santé + priorité + recommandation
```

## X-Repair Circuit et SPICE

Le module peut effectuer une vérification statique sans dépendance externe.
Si `ngspice` est installé dans le PATH, l'option **Lancer SPICE** exécute la netlist.

## Limites

Cette version est un **prototype d'ingénierie**. Les scores et règles génériques ne doivent pas être utilisés comme décision de sécurité ou de maintenance industrielle sans calibration et validation sur équipements réels.

## Sources de conception

Le langage visuel reprend les éléments fournis dans le prototype META POMPE : fond blanc, accent violet, typographie Plus Jakarta Sans, cartes neumorphiques, indicateurs de santé et approche SPA.
