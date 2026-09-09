1. Présentation générale

X-Repair 17A est une plateforme intelligente et multimodale destinée au diagnostic, à la surveillance de l’état de santé et à l’assistance à la maintenance des systèmes mécaniques, électromécaniques et électroniques.

Le projet part d’un principe simple : une panne laisse généralement plusieurs signatures mesurables. Une machine peut vibrer anormalement, chauffer, produire un bruit inhabituel, consommer un courant différent ou présenter des tensions incompatibles avec son fonctionnement nominal. X-Repair cherche donc à exploiter simultanément plusieurs sources d’information au lieu de dépendre d’un seul capteur.

Le système est organisé autour de six modules spécialisés :

X-Repair Vibe — diagnostic vibratoire ;
X-Repair Circuit — diagnostic des circuits et appareils électroniques ;
X-Repair Acoustic — diagnostic acoustique ;
X-Repair Thermal — surveillance thermique ;
X-Repair Power — analyse électrique et énergétique ;
X-Repair Core — fusion des diagnostics et décision globale.

Le projet reprend également l’approche visuelle du prototype META POMPE, notamment l’interface SPA, le style blanc/violet, les cartes neumorphiques et la logique de tableau de bord destinée au diagnostic terrain. L’architecture initiale META POMPE associait déjà une interface interactive à un backend FastAPI pour le diagnostic et la maintenance prédictive.

2. Objectif principal

L’objectif de X-Repair est de transformer des mesures physiques brutes en informations directement exploitables pour la maintenance.

La chaîne générale est :

$$ \boxed{ \text{Acquisition} \rightarrow \text{Traitement} \rightarrow \text{Extraction de caractéristiques} \rightarrow \text{Diagnostic} \rightarrow \text{Fusion} \rightarrow \text{Décision de maintenance} } $$

À terme, la philosophie du projet est :

$$ \boxed{ \text{Détecter} \rightarrow \text{Localiser} \rightarrow \text{Diagnostiquer} \rightarrow \text{Expliquer} \rightarrow \text{Proposer une correction} \rightarrow \text{Vérifier} } $$

La version actuelle doit toutefois être considérée comme un prototype de diagnostic et de réparation assistée. Elle ne réalise pas encore physiquement le remplacement automatique d’un composant ou la réparation robotisée d’une machine.

3. X-Repair Vibe

X-Repair Vibe est consacré aux machines tournantes : moteurs électriques, pompes, ventilateurs, motoréducteurs et autres équipements produisant des vibrations.

Le système reçoit une série d’échantillons vibratoires et extrait plusieurs indicateurs :

$$ RMS= \sqrt{\frac{1}{N}\sum_{n=1}^{N}x_n^2} $$

ainsi que la valeur de crête, le facteur de crête, la kurtosis et les composantes fréquentielles associées au régime de rotation.

Si le moteur fonctionne à \(N\) tr/min :

$$ f_{1X}=\frac{N}{60} $$

X-Repair recherche notamment :

$$ 1X,\quad2X,\quad3X,\quad4X $$

Ces composantes permettent de construire des signatures compatibles avec certains défauts.

Dans la version actuelle, le module peut rechercher principalement :

déséquilibre, désalignement, jeu mécanique, défaut de roulement ou fonctionnement considéré comme normal.

Par exemple, une forte composante \(1X\) peut orienter vers un déséquilibre, alors qu’une composante \(2X\) importante peut être compatible avec certains désalignements.

Le module produit ensuite un diagnostic, un score de santé et une recommandation de maintenance.

4. X-Repair Acoustic

X-Repair Acoustic analyse les signatures sonores d’une machine.

Le principe est proche de l’analyse vibratoire, mais la source est acoustique.

Le système calcule notamment :

$$ RMS,\quad Peak,\quad Crest\ Factor,\quad Kurtosis $$

ainsi qu’une fréquence dominante.

Une augmentation de l’impulsivité peut indiquer des impacts, des frottements ou certaines anomalies de roulement. Une forte composante aiguë peut également signaler un comportement acoustique inhabituel.

Cette orientation est cohérente avec le prototype META POMPE, qui était conçu autour de l’analyse audio de pompes et du diagnostic de phénomènes tels que cavitation, usure de roulements ou désalignement.

Dans X-Repair, l’objectif est cependant plus général : le module Acoustic doit pouvoir être utilisé sur différents types de machines.

5. X-Repair Thermal

X-Repair Thermal surveille l’évolution de la température d’un équipement.

Il exploite actuellement des mesures numériques de température plutôt qu’une analyse complète d’image thermographique.

Les principales grandeurs sont :

$$ T_{\max} $$ $$ T_{\min} $$ $$ T_{\text{moy}} $$

et :

$$ \Delta T=T_{\max}-T_{\text{ambiante}} $$

Le système peut ainsi distinguer des situations comme :

fonctionnement thermique normal, échauffement anormal, gradient thermique important ou surchauffe.

Pour un moteur, cela peut orienter vers une surcharge, un problème de ventilation, de lubrification ou un défaut électrique.

Pour une carte électronique, une élévation de température peut aider à localiser un composant soumis à une dissipation excessive.

Une future version pourra intégrer une caméra thermique et traiter directement une matrice de températures ou une image infrarouge.

6. X-Repair Power

X-Repair Power analyse les grandeurs électriques d’une machine ou d’un équipement.

À partir de signaux de tension et de courant, il calcule notamment :

$$ V_{RMS} = \sqrt{ \frac{1}{N} \sum_{n=1}^{N}v_n^2 } $$ $$ I_{RMS} = \sqrt{ \frac{1}{N} \sum_{n=1}^{N}i_n^2 } $$

la puissance active :

$$ P= \frac{1}{N} \sum_{n=1}^{N}v_n i_n $$

la puissance apparente :

$$ S=V_{RMS}I_{RMS} $$

et un facteur de puissance estimé :

$$ PF=\frac{P}{S} $$

Le système peut ainsi détecter certaines situations élémentaires :

tension hors tolérance, facteur de puissance faible ou fonctionnement électrique considéré comme normal.

À terme, ce module pourra également intégrer :

déséquilibre triphasé ;
harmoniques ;
THD ;
puissance réactive ;
courant de démarrage ;
signature de courant moteur ;
détection de surcharge ;
défauts d’isolement indirects.
7. X-Repair Circuit

X-Repair Circuit constitue la branche électronique de la plateforme.

Son objectif est d’assister le diagnostic des :

cartes électroniques, alimentations, amplificateurs, filtres, systèmes analogiques et autres appareils contenant des circuits électriques ou électroniques.

Le principe général est :

$$ \boxed{ \text{Circuit réel} \leftrightarrow \text{Modèle électronique} } $$

Le module actuel peut recevoir une netlist SPICE et analyser sa structure.

Il identifie notamment différents composants :

$$ R,\ C,\ L,\ D,\ Q,\ V,\ I $$

et effectue plusieurs vérifications statiques, par exemple :

absence de .end, absence apparente d’alimentation, problème potentiel de référence de masse ou présence d’une résistance de \(0\,\Omega\).

Lorsque ngspice est installé sur la machine, X-Repair Circuit peut également lancer la simulation.

L’objectif avancé est beaucoup plus ambitieux :

$$ \text{Mesures réelles} + \text{SPICE} + \text{IA} \rightarrow \text{Diagnostic électronique} $$

Le système devra pouvoir comparer les valeurs réelles et simulées sur différents nœuds :

$$ e_i = V_{mesuré,i} - V_{simulé,i} $$

puis rechercher les composants dont une défaillance expliquerait ces écarts.

Par exemple :

Composant suspect : R4
Valeur ou connexion potentiellement incorrecte.
Vérification recommandée : mesurer R4 hors tension puis vérifier la polarisation de Q1.

Une future version intégrera plus complètement le concept initial LLM–SPICE, où le LLM sera chargé de sélectionner les tests, interpréter les résultats et expliquer le diagnostic, tandis que SPICE restera responsable du calcul électrique.

8. X-Repair Core

X-Repair Core est le niveau supérieur du système.

Il ne remplace pas les modules spécialisés. Il reçoit leurs résultats et les fusionne.

Architecture :

X-Repair Vibe ──────┐
X-Repair Acoustic ──┤
X-Repair Thermal ───┤
X-Repair Power ─────┼──► X-Repair Core
X-Repair Circuit ───┘
                         │
                         ▼
                    Score global
                         │
                         ▼
               Priorité maintenance

Chaque module fournit notamment un :

$$ HealthScore_i $$

X-Repair Core effectue ensuite une combinaison pondérée :

$$ H= \frac{ \sum_i w_i H_i }{ \sum_i w_i } $$

où \(w_i\) représente l’importance du module.

Le système peut ensuite classer l’état global de l’équipement en catégories telles que :

bon, surveillance nécessaire, dégradé ou critique.

La priorité de maintenance devient alors par exemple :

$$ H\geq85 \Rightarrow \text{surveillance normale} $$ $$ 65\leq H<85 \Rightarrow \text{contrôle planifié} $$ $$ 40\leq H<65 \Rightarrow \text{inspection prioritaire} $$ $$ H<40 \Rightarrow \text{inspection immédiate} $$

Ces seuils sont actuellement génériques et doivent être calibrés expérimentalement avant tout usage industriel.

9. Interface utilisateur

L’interface X-Repair reprend le langage visuel développé pour META POMPE.

Le script de fusion fourni pour META POMPE montre une interface basée sur TailwindCSS, Plus Jakarta Sans, une palette blanche et violette, des cartes neumorphiques, plusieurs écrans de navigation et des animations de diagnostic.

Dans X-Repair, cette logique a été adaptée pour présenter les six modules dans un tableau de bord unique.

L’utilisateur peut passer de :

Vibe → Circuit → Acoustic → Thermal → Power → Core

et visualiser :

le diagnostic ;
le score de santé ;
les caractéristiques calculées ;
les recommandations ;
les résultats bruts retournés par l’API.

L’image Spider-Man fournie est intégrée comme élément visuel de l’identité actuelle du prototype.

10. Architecture logicielle

La plateforme suit actuellement une architecture client–serveur.

             INTERFACE WEB
                  │
                  ▼
              FastAPI
                  │
      ┌───────────┼───────────┐
      │           │           │
      ▼           ▼           ▼
    Vibe       Acoustic     Thermal
      │           │           │
      └─────┐     │     ┌─────┘
            ▼     ▼     ▼
           X-Repair Core
            ▲           ▲
            │           │
          Power      Circuit

Le backend repose sur Python + FastAPI, ce qui correspond également au choix architectural initial du projet META POMPE.

La documentation interactive de l’API est accessible à :

http://127.0.0.1:8000/docs
11. Acquisition embarquée

Le projet contient également un firmware de démonstration pour :

ESP32 + ADXL345.

L’accéléromètre mesure les vibrations sur trois axes :

$$ a_x,\quad a_y,\quad a_z $$

et transmet les valeurs via le port série.

Cette architecture prépare l’évolution de X-Repair vers un système de surveillance physique :

Moteur
  ↓
ADXL345
  ↓
ESP32
  ↓
USB / série
  ↓
X-Repair
  ↓
Diagnostic

Pour une version industrielle, un capteur vibratoire plus performant pourra remplacer l’ADXL345 selon les fréquences et amplitudes recherchées.

12. Applications pratiques

X-Repair peut être développé pour plusieurs secteurs :

maintenance industrielle, moteurs électriques, pompes, ventilateurs, convoyeurs, groupes électrogènes, motoréducteurs, systèmes HVAC, appareils électroménagers, cartes électroniques, alimentations, ateliers de réparation et laboratoires pédagogiques.

Pour un technicien, l’objectif est de passer de :

« La machine fait un bruit bizarre. »

à :

« Une augmentation de la vibration 2X a été détectée, accompagnée d’une élévation thermique. Le système recommande de vérifier l’alignement et l’accouplement. »

Ou, pour une carte électronique :

« Le comportement du nœud de sortie n’est pas compatible avec le modèle nominal. Vérifier R4, Q1 et la polarisation du transistor. »

13. Maintenance prédictive

Le projet vise également la maintenance conditionnelle et prédictive.

Au lieu de remplacer un composant selon une durée fixe, X-Repair cherche à suivre son état réel :

$$ Health(t) $$

On peut alors étudier son évolution :

$$ \frac{dHealth}{dt} $$

et détecter une dégradation avant une panne.

META POMPE prévoyait déjà une logique de score de santé et de RUL — Remaining Useful Life.

X-Repair peut reprendre cette direction lorsque suffisamment de données historiques réelles auront été collectées.

14. Intelligence artificielle et frugalité

Le projet ne doit pas être basé uniquement sur une IA opaque.

L’architecture cible est hybride :

$$ \boxed{ Physique + Traitement\ du\ signal + Règles + Machine\ Learning } $$

Une direction de recherche importante est l’IA frugale, capable de fonctionner sur des machines avec peu de ressources.

Des modèles comme :

Random Forest ;
SVM ;
Extreme Learning Machine ;
modèles quantique-inspirés ;

pourront être comparés selon :

$$ Accuracy $$ $$ F1 $$ $$ T_{training} $$ $$ T_{inference} $$ $$ RAM $$ $$ Energy $$

L’objectif n’est donc pas seulement la précision, mais aussi la possibilité de déployer X-Repair sur du matériel embarqué.

15. Ce qui fonctionne actuellement

La version finale du prototype possède déjà une base fonctionnelle comprenant :

frontend, API FastAPI, modules Vibe, Circuit, Acoustic, Thermal, Power, Core, lanceur Windows .bat, tests Python, firmware ESP32/ADXL345, documentation technique et interface unifiée.

Les fichiers Python de la version générée ont également passé une vérification de compilation syntaxique.

16. Ce qui reste à développer

La partie la plus importante pour transformer X-Repair en véritable système industriel est maintenant la validation expérimentale.

Il faudra notamment obtenir des données réelles de machines saines et défectueuses, établir des baselines, calibrer les seuils, entraîner les modèles sur des datasets réels et tester la généralisation sur des équipements jamais vus durant l’apprentissage.

Pour X-Repair Circuit, il faudra également intégrer plus profondément :

$$ \boxed{ Mesure + SPICE + LLM } $$

avec injection automatique de défauts et génération d’hypothèses.

Pour X-Repair Acoustic, il faudra ajouter une vraie acquisition microphone/audio.

Pour Thermal, une caméra thermique.

Pour Power, un module d’acquisition électrique sécurisé.

17. Vision finale

À long terme, l’architecture complète peut devenir :

                     X-REPAIR 17A
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
       Vibration       Acoustic        Thermal
          │               │               │
          ├───────────────┼───────────────┤
          │               │               │
          ▼               ▼               ▼
        Power          Circuit          History
          │               │               │
          └───────────────┼───────────────┘
                          ▼
                     X-Repair Core
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
         Diagnostic   Health Score   Prognostic
             │            │            │
             └────────────┼────────────┘
                          ▼
                 Maintenance Decision
                          │
                          ▼
                Repair Recommendation
                          │
                          ▼
                  Human / Robot Repair
                          │
                          ▼
                     Re-validation

La véritable ambition de X-Repair est donc de créer une plateforme générale de maintenance intelligente, applicable aussi bien à une machine tournante qu’à une carte électronique.

Formulation académique recommandée

X-Repair 17A : conception et développement d’une plateforme multimodale, intelligente, explicable et frugale pour le diagnostic, la maintenance conditionnelle et la réparation assistée des systèmes électromécaniques et électroniques.

Description courte GitHub

X-Repair 17A is a multimodal intelligent maintenance platform combining vibration, acoustic, thermal, electrical power and electronic circuit diagnostics into a unified health assessment and repair-assistance system.

Slogan

X-Repair 17A — Detect. Diagnose. Understand. Repair.