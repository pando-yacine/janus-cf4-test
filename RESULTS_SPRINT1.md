---
title: Résultats Sprint 1 — protocole pré-enregistré non exécutable avec Pantheon+
date: 2026-05-09
status: SPRINT 1 TERMINÉ — décision à prendre pour la suite
---

# Sprint 1 — Résultat principal

## Verdict en une phrase

**Le protocole pré-enregistré ne peut pas être exécuté avec Pantheon+ seul** : 0 SN-Ia satisfait les critères figés, parce que le Dipole Repeller se trouve dans la zone d'évitement galactique où Pantheon+ n'a quasiment aucune SN.

## Détails de la diagnostic

### Protocole pré-enregistré (commit ac45458)

- Cône angulaire : θ_DR < 30°
- Plage redshift : 0.05 < z_CMB < 0.15
- Qualité photométrique : σ_m < 0.20 mag

### Résultat

| Critère | N de SN |
|---|---:|
| Cône 30°, sans autre filtre | 13 |
| Cône 30° + 0.05 < z < 0.15 | 1 |
| **Cône 30° + 0.05 < z < 0.15 + σ < 0.20** (protocole figé) | **0** |

### Cause identifiée : zone d'évitement galactique

Le Dipole Repeller est à $(l, b) = (305°, +5°)$ — **proche du plan galactique**.

Distribution en latitude galactique de Pantheon+ :

| Région | N de SN |
|---|---:|
| `\|b\| < 5°` (plan galactique strict) | **0** |
| `\|b\| < 10°` (zone d'évitement classique) | **6** |
| `\|b\| > 30°` (hors plan galactique) | 1489 |

**Pantheon+ évite quasi-totalement la zone galactique** à cause de l'extinction par les poussières interstellaires (les SN-Ia sont alors trop atténuées pour être correctement calibrées en magnitude). Cette limitation est connue dans la communauté SN cosmologique mais devient ici **rédhibitoire** pour notre test puisque le DR tombe précisément dans cette zone.

### 10 SN les plus proches du DR

```
    CID      l_gal      b_gal  theta_DR    zCMB  σ_m
 2001cz    302.11      23.29     18.50    0.013  0.345
 2013aa    321.40      14.99     18.97    0.005  0.594
 2013aa    321.40      14.99     18.97    0.005  0.580
2017cbv    321.44      15.07     19.05    0.005  0.578
2017cbv    321.44      15.07     19.05    0.005  0.578
 2000ca    313.20      27.83     24.13    0.025  0.188
  1993O    312.42      28.92     24.93    0.051  0.227
 2008bc    283.60      -8.60     25.30    0.016  0.225
 2007as    294.79     -20.71     27.60    0.018  0.233
 2005al    317.58      30.62     28.23    0.016  0.218
```

→ Toutes les SN proches sont **soit trop précoces (z < 0.04)** soit **mal photométrées (σ > 0.2 mag)**, à cause de l'extinction.

## Pourquoi cela n'invalide PAS le test conceptuel

Cette difficulté est **propre à Pantheon+**, pas à la prédiction Janus :

- Le DR est réel et reconnu (Hoffman et al. 2017, confirmé CF4)
- La prédiction Janus-2024 (atténuation annulaire des sources d'arrière-plan) est testable, en principe
- Mais **les SN-Ia derrière le DR sont mal échantillonnées** par les surveys actuels à cause de l'extinction

## Pivots possibles

### Pivot A — CosmicFlows-4 (recommandé)

Plutôt que de tester l'**atténuation lumineuse** des SN-Ia, tester la **distance peculière** des galaxies via Tully-Fisher dans CF4 :
- ~56 000 galaxies, beaucoup en zone d'évitement
- Couvre largement la direction DR
- Test différent : il s'agirait de vérifier si la **carte de densité reconstruite** à partir des distances galactiques montre des **anomalies dans la luminosité de fond** au-delà du DR

**Avantages** : couverture du ciel, échantillon massif, indépendance de l'extinction (mesures IR proche)

**Inconvénients** : test plus complexe à formaliser ; redéfinition partielle de la prédiction Janus à tester

### Pivot B — 2MASS Redshift Survey (2MRS)

Catalogue de ~45 000 galaxies en infrarouge proche, couvre 91% du ciel y compris la zone d'évitement.
- Magnitudes K-band, peu affectées par l'extinction galactique
- Pas de calibration de magnitude absolue précise comme SN-Ia → test plus indirect

### Pivot C — Combiner Pantheon+ + DESI BGS + galaxies

Approche multi-probe : utiliser Pantheon+ aux hautes latitudes + DESI BGS pour la couverture totale.
**Plus complexe, mais le plus rigoureux.**

### Pivot D — Reformuler la prédiction Janus

Demander à l'équipe Petit-Margnat-Zejli s'ils ont des prédictions pour d'autres structures cosmiques accessibles avec Pantheon+ (vides cosmologiques mieux situés sur le ciel).

## Décision attendue

Vue l'impossibilité d'exécuter le test pré-enregistré, **trois options** :

1. **Stop — publier l'échec comme un livrable**. La découverte que le DR tombe dans la zone d'évitement Pantheon+ est en soi un résultat utile (montre que ce test particulier exige un autre survey).

2. **Pivot A** (CF4) — refaire un protocole pré-enregistré dédié, démarrer Sprint 2.

3. **Pivot D** — contacter Petit/Zejli pour identifier une autre structure cosmique testable avec Pantheon+.

## Ce qui est conservé

Que la décision soit 1, 2 ou 3 :
- Le protocole pré-enregistré reste un livrable scientifique (montre la rigueur)
- Le code de chargement et conversion est réutilisable
- La diagnostic de la zone d'évitement est un résultat vérifié et reproductible

## État du repo (2026-05-09 fin de Sprint 1)

```
janus-test-observationnel/
├── 00-README.md                       ✅
├── 01-protocole-pre-enregistre.md     ✅ commit ac45458
├── 02-sources-donnees.md              ✅
├── 03-architecture-technique.md       ✅
├── 04-pipeline-analyse.md             ✅
├── 05-livrables-et-roadmap.md         ✅
├── 06-pieges-et-biais.md              ✅
├── RELATED_WORK.md                    ✅
├── RESULTS_SPRINT1.md                 ⬅ ce fichier
├── data_manifest.json                 ✅ Pantheon+ téléchargé, hashé
├── code/
│   ├── 01_load_and_convert.py         ✅ exécuté avec succès
│   └── 02_diagnose_sample.py          ✅ exécuté avec succès
├── data/
│   ├── pantheon-plus/Pantheon+SH0ES.dat  ✅ 566 ko, 1701 SN
│   └── pantheon_with_galactic.csv     ✅ avec coords galactiques
└── figures/                           (vide)
```

## Time spent : ~30 min de wall-clock

Pas de cluster, pas de coût, juste du laptop Python.
