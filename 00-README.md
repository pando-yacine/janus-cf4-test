---
title: Test observationnel — Janus-2024 vs Dipole Repeller
date_creation: 2026-05-09
status: planning (avant collecte des données)
auteur: Yacine Arhaliass + Claude
---

# Test observationnel des anneaux d'atténuation prédits par Janus-2024

## Objectif en une phrase

Tester si les supernovae de type Ia situées **derrière le Dipole Repeller** présentent une **structure annulaire d'atténuation** dans leur magnitude apparente résiduelle, comme prédit par le modèle Janus de Petit-Margnat-Zejli (EPJ-C 84:1226, 2024) — par opposition au modèle ΛCDM standard qui ne prédit aucune structure.

## Pourquoi ce test ?

C'est la **prédiction la plus discriminante** identifiée dans l'article EPJ-C 2024 :

> *"We predict that when a map is established by the JWST telescope, the invisible mass will manifest its presence by a brightness attenuation, not over the entire disk, but in a ring."*
>
> — Petit & Zejli 2024, HAL-04583560 §4

Le Dipole Repeller (Hoffman et al., *Nature Astronomy* 2017) est la **plus grande sous-densité connue** dans notre voisinage cosmique, à ~180 Mpc dans la direction (l, b) ≈ (305°, +5°). Si l'interprétation Janus est correcte (vide = concentration de masse négative), alors les photons traversant ses bords doivent subir une lentille gravitationnelle inversée → atténuation annulaire.

## Pourquoi avec les données existantes ?

**Pas besoin de nouveau temps télescope**. Pantheon+ (1701 SN-Ia, 2022) et CosmicFlows-4 (~56 000 galaxies avec distances et vélocités peculières, 2023) sont publics et couvrent largement la région.

## Engagement méthodologique

⚠️ **Pré-enregistrement obligatoire avant collecte des données.**

Pour éviter le cherry-picking, le protocole d'analyse (cône angulaire, bins, seuils, tests) sera **figé dans `01-protocole-pre-enregistre.md`** AVANT tout téléchargement et **commité avec timestamp dans Git** pour preuve de pré-enregistrement.

Aucune modification du protocole après accès aux données, sauf à documenter la modification et à refaire l'analyse de novo.

## Structure du dossier

```
janus-test-observationnel/
├── 00-README.md                       ← ce fichier
├── 01-protocole-pre-enregistre.md     ← À FIGER avant data
├── 02-sources-donnees.md              ← Pantheon+, CF4, position DR
├── 03-architecture-technique.md       ← Stack Python, modules, deps
├── 04-pipeline-analyse.md             ← Étapes 1→6 + diagrammes Mermaid
├── 05-livrables-et-roadmap.md         ← Output cible + planning d'exécution
├── 06-pieges-et-biais.md              ← Cherry-picking, fishing, déclaration biais
│
├── data/                              ← (gitignoré) données téléchargées
│   ├── pantheon-plus/
│   └── cosmicflows-4/
│
├── code/                              ← scripts et notebooks
│   ├── 01_download_data.py            ← (à écrire) téléchargement
│   ├── 02_select_sample.py            ← sélection des SN candidates
│   ├── 03_angular_binning.py          ← binning autour du DR
│   ├── 04_residuals.py                ← calcul magnitudes résiduelles
│   ├── 05_statistics.py               ← bootstrap + tests
│   ├── 06_placebo.py                  ← test placebo positions aléatoires
│   └── analysis.ipynb                 ← notebook intégrateur
│
└── figures/                           ← figures publiables
```

## Lecture suggérée

1. **D'abord** : `01-protocole-pre-enregistre.md` — c'est l'engagement scientifique
2. **Ensuite** : `04-pipeline-analyse.md` — le déroulé technique
3. **Puis** : `02-sources-donnees.md` et `03-architecture-technique.md` pour les détails
4. **Avant publication éventuelle** : `06-pieges-et-biais.md` — auto-évaluation honnête

## Verdict attendu (avant les données)

Probabilité estimée de chaque issue (à priori, **avant** l'analyse) :

| Issue | Probabilité a priori |
|---|---:|
| Signal annulaire détecté à >3σ avec amplitude compatible Janus | ~5% |
| Signal annulaire à 1-3σ, indicatif mais non discriminant | ~25% |
| Signal compatible avec zéro, non discriminant | ~55% |
| Signal incompatible avec Janus (favorable à ΛCDM) | ~15% |

**Le résultat le plus probable est non-discriminant.** Cela reste un livrable utile : protocole reproductible publié pour la communauté.

## Statut

- [x] Plan rédigé (2026-05-09)
- [ ] Protocole pré-enregistré et figé en Git
- [ ] Données téléchargées
- [ ] Code écrit
- [ ] Analyse exécutée
- [ ] Figures produites
- [ ] Notebook public partageable

## Contact / référents externes possibles (si on va plus loin)

- **Daniel Pomarède** (CEA Saclay, francophone, co-découvreur DR) — pour validation technique
- **Helene Courtois** (Univ. Lyon 1, IUF, co-découvreuse DR) — francophone, accessible
- **Adam Riess team** (JHU) — pour Pantheon+
- **Jean-Pierre Petit** lui-même — pour vérifier les prédictions quantitatives Janus
