---
title: Veille — travaux open source liés au modèle Janus
date: 2026-05-09
type: veille
---

# Veille — travaux liés au modèle Janus

État au 2026-05-09. Vérifié avant de démarrer notre propre code, pour ne pas réinventer.

## Repos GitHub existants sur le modèle Janus

### 1. [J-Gravity/J-GravityDispatcher](https://github.com/J-Gravity/J-GravityDispatcher)

- **Description** : *"J-Gravity is a cosmological scale particle simulator that was built with the purpose of testing the Janus Cosmological Model. (...) The worker is a program that runs on a computer and participates in the pool of workers doing all the calculations for the simulation on the gpu using OpenCL. (...) Built the Dispatcher and Workers in C and the renderer in C++."*
- **Langages** : C (97%), C++ (1%), Makefile, Ruby
- **Statut** : 8 stars, dernier push **2017-08-24** (avant Janus-2014 corrigé, avant Janus-2019, avant Janus-2024)
- **But** : simulation distribuée N-body de la dynamique JCM
- **Utile pour nous ?** Non directement — c'est de la simulation pure, pas de l'analyse de données observationnelles. Pourrait servir en phase 2 si on voulait calculer la prédiction quantitative Janus exacte pour la géométrie spécifique du Dipole Repeller (mais hors scope).

### 2. [francisseco/Janus-CUDA-Nbody](https://github.com/francisseco/Janus-CUDA-Nbody)

- **Description** : *"Modified CUDA sample code to simulate a basic N-body problem for Janus Cosmological Model (JCM)."*
- **Langages** : C++ (90%), CUDA (10%)
- **Statut** : 25 stars, dernier push **2019-04-28**
- **But** : N-body GPU pour JCM
- **Utile pour nous ?** Non. Idem ci-dessus.

### 3. [januscosmologicalmodel.com](https://januscosmologicalmodel.com/)

- Site officiel de présentation du modèle (Petit-Margnat-Zejli + équipe)
- **Pas de repo de code, pas de notebook, pas de dataset**
- Section "Publications" et "Map" du modèle, mais pas d'open source

### 4. [Zenodo : Zejli 2024](https://zenodo.org/records/13621613)

- *Modèle Cosmologique Janus - Univers bimétrique : Perspectives & Défis*, Hicham Zejli 2024
- **17 Mo PDF uniquement**. Pas de code, pas de notebook.

## Ce qui n'existe pas

À notre connaissance après recherche au 2026-05-09 :

- ❌ **Aucun repo public** des auteurs Petit-Margnat-Zejli avec leur code de calcul de prédictions Janus
- ❌ **Aucun notebook supplémentaire** accompagnant l'article EPJ-C 84:1226 (2024)
- ❌ **Aucune analyse publiée** confrontant les prédictions Janus aux données Pantheon+ ou CosmicFlows-4
- ❌ **Aucun test observationnel** de la prédiction d'atténuation annulaire derrière le Dipole Repeller

## Implication pour notre travail

Notre test :
1. **Ne réinvente pas** une simulation N-body (les deux repos C/CUDA existent déjà)
2. **Comble un trou réel** : analyse observationnelle directe de la prédiction discriminante de Janus-2024
3. Pourrait **se croiser avec** les simulations existantes en phase 2 si besoin de prédiction quantitative

## Données cosmologiques publiques utilisables

| Source | Type | Lien |
|---|---|---|
| **Pantheon+** | 1701 SN-Ia, magnitudes calibrées | [GitHub PantheonPlusSH0ES](https://github.com/PantheonPlusSH0ES/DataRelease) |
| **CosmicFlows-4** | ~56k galaxies, distances, peculiar velocities | [EDD Hawaii](https://edd.ifa.hawaii.edu/) |
| **Dipole Repeller** position | Hoffman et al. 2017 | [Nature Astronomy](https://www.nature.com/articles/s41550-016-0036) |

## Communauté académique active sur les modèles bimétriques

À noter pour contexte (en dehors du programme Janus strict) :
- **Hossenfelder & Farnes 2018** — modèle "negative mass + matter creation" dans A&A 620 A92, sans citer Petit
- **Banik & Kroupa** — critique de Farnes 2018, peuvent être ouverts à d'autres modèles avec dynamique non-standard
- **Cosmological tensions community** (Hubble tension, S8 tension) — communauté ouverte aux modèles alternatifs en 2024-2026 vu les anomalies JWST + DESI

## Conclusion de la veille

Notre démarche est **originale et utile**. On peut continuer.
