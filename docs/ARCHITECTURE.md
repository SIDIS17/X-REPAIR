# Architecture X-Repair 17A

## Couche interface
SPA HTML/Tailwind inspirée du prototype META POMPE.

## Couche API
FastAPI expose un endpoint pour chacun des modules.

## Couche modules
- vibe.py
- acoustic.py
- thermal.py
- power.py
- circuit.py
- core.py

## Rôle de Core
Core ne remplace pas les diagnostics spécialisés. Il agrège leurs scores de santé avec des poids configurables et fournit une priorité de maintenance.

## Extension future
- ingestion fichiers WAV/CSV,
- base de données historique,
- modèle ML entraîné sur données réelles,
- analyse d'enveloppe haute performance NumPy/SciPy,
- LLM pour explication de diagnostic,
- acquisition temps réel via WebSocket,
- images thermiques,
- intégration SPICE plus complète.
