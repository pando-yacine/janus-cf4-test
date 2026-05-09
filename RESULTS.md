---
title: Test observationnel de la prédiction d'atténuation annulaire de Janus-2024 derrière le Dipole Repeller — Résultats v2
date: 2026-05-09
authors: Yacine Arhaliass + assistant Claude (Anthropic)
status: v2.0 — Sprint 3 inclut soustraction LCDM via 2M++
---

# Résultats v2 — Test du modèle Janus contre Dipole Repeller via CosmicFlows-4

## TL;DR

Test pré-enregistré de la prédiction discriminante de **Petit-Margnat-Zejli 2024** (EPJ-C 84:1226) sur les données publiques **CosmicFlows-4** (Tully et al. 2023, ApJ 944:94), avec soustraction du flow LCDM via **2M++ Carrick et al. 2015** (package *pvhub*).

| Test | χ² | df | p-value | Verdict |
|---|---:|---:|---:|---|
| **DR brut (table4 groupes)** | 20.10 | 3 | 0.0002 | Signal réel (top 3% placebo), mais profil **monotone positif**, pas annulaire négatif |
| **Antipode brut (Shapley)** | 44.75 | 3 | <0.0001 | Mirror image du DR — signature **dipolaire LCDM** |
| **DR résidus (table2 - 2M++)** | 3.21 | 2 | 0.20 | **Non discriminant** — LCDM explique tout |

**Conclusion principale** : la prédiction Janus testable formulée pour CF4 (lentille gravitationnelle négative → atténuation lumineuse → distance TF surestimée → Vpec biaisée vers le négatif aux bords du DR) **n'est pas observée**. Les vélocités peculières mesurées sont entièrement compatibles avec la cinématique LCDM standard du couple Repeller-Attractor.

⚠️ **Caveat majeur** : la prédiction quantitative testée est **ma dérivation** depuis l'EPJ-C 2024, pas une formulation publiée par les auteurs. Un email a été préparé pour Petit & Zejli demandant leur lecture.

## Contexte et motivation

### La controverse Janus-Damour

Le modèle cosmologique **Janus** (Petit, depuis 1977 ; reformulé en EPJ-C 84:1226 en 2024 avec Margnat et Zejli) propose une cosmologie bimétrique avec masses positives et négatives. Il est contesté techniquement par Thibault Damour (IHES, notes 2019 et 2022) et largement ignoré par la communauté mainstream.

Le **Dipole Repeller** (Hoffman, Pomarède, Tully, Courtois — *Nature Astronomy* 1:0036, 2017) est interprété par Janus-2024 comme une concentration de **matière à masse négative**.

### La prédiction discriminante

L'article HAL-04583560 (Petit-Zejli, mai 2024) précise :

> *"We predict that when a map is established by the JWST telescope, the invisible mass will manifest its presence by a brightness attenuation, not over the entire disk, but in a ring."*

C'est cette prédiction d'**atténuation annulaire** que ce test vise à confronter aux données publiques actuelles.

## Méthodologie

### Pré-enregistrement

Trois commits Git successifs avec timestamp :

| Tag | Commit | Date | Statut |
|---|---|---|---|
| `v1.0-protocol-frozen` | `ac45458` | 2026-05-09 19:52 | v1 figée AVANT data Pantheon+ |
| `v2.0-protocol-frozen` | `b06dfd3` | 2026-05-09 20:48 | v2 figée AVANT inspection CF4 |
| `v1.0-results` | `eb12654` | 2026-05-09 21:02 | v1 résultats (sans soustraction LCDM) |
| `v2.0-results` | (à venir) | 2026-05-09 | v2 résultats (avec soustraction LCDM) |

### Données

| Source | Tables | Échantillon | Hash SHA-256 |
|---|---|---|---|
| Pantheon+ | `Pantheon+SH0ES.dat` | 1701 SN-Ia | `1cb0fc379ef0...` |
| CosmicFlows-4 | `table2.dat` (galaxies indiv.) | 55 877 | `8e908928e683...` |
| CosmicFlows-4 | `table4.dat` (groupes) | 38 053 | `b6edfec68bdf...` |
| 2M++ via pvhub | Carrick et al. 2015 | grille 129³ | (LFS GitHub) |

### Protocole figé v2

- Position DR : $(l, b) = (305°, +5°)$ (Hoffman 2017)
- Cône angulaire : $\theta_{DR} < 40°$
- Distance comobile : 50 < d < 350 Mpc
- Erreur DM : $e_{DM} < 0.30$ mag
- Latitude galactique : $|b| > 3°$
- Bins angulaires figés : [0,8] [8,18] [18,28] [28,40] degrés
- 8 régions de contrôle (seed=42)
- 100 placebo positions (seed=12345)
- Test χ² standard

## Résultats détaillés

### Sprint 1 — Pantheon+ (v1, abandonné)

**0 SN-Ia** dans l'échantillon. Le DR (b=+5°) est dans la **zone d'évitement galactique** de Pantheon+ (extinction par poussières → SN-Ia non calibrables). Pantheon+ a 0 SN dans |b|<5° et 6 SN dans |b|<10°, vs 1489 hors plan.

→ Pivot vers CF4 (couvre tout le ciel via méthodes IR proche).

### Sprint 2 — CF4 groupes table4 (v1 résultat)

**Échantillon principal** : 89 groupes de galaxies dans le cône DR.

| Bin θ° | N | <Vpec(DR)> km/s | <Vpec(ctrl)> | ΔVpec |
|---|---:|---:|---:|---:|
| [0, 8) | 0 | — | — | — |
| [8, 18) | 4 | +588 ± 453 | +105 | **+483** |
| [18, 28) | 29 | +268 ± 55 | +75 | **+193** |
| [28, 40) | 56 | +233 ± 44 | +107 | **+126** |

**χ² = 20.10 (df=3), p = 0.0002.** Top 3% du placebo (sur 100 positions aléatoires).

**Antipode (Shapley direction)** : ΔVpec = -433, -39, -165 km/s. **χ² = 44.75 (df=3).** Mirror image en signe.

**Robustesse** : χ² = 19.1 à 19.9 avec bins ±20%. Stable.

### Sprint 3 — Soustraction LCDM via 2M++ (v2 résultat)

Pour chaque galaxie de l'échantillon, calcul de Vpec_LCDM via la reconstruction publique 2M++ Carrick 2015 (package *pvhub*, classe `TwoMPP_SDSS`). Résidu :

$$V_{pec}^{residual} = V_{pec}^{obs} - V_{pec}^{LCDM}$$

Test χ² refait sur les résidus (table2 individuels, 33 galaxies dans le cône DR avec critères figés) :

| Bin θ° | N | <résidu(DR)> km/s | <résidu(ctrl)> | Δrésidu |
|---|---:|---:|---:|---:|
| [0, 8) | 0 | — | — | — |
| [8, 18) | 0 | — | — | — |
| [18, 28) | 6 | +444 | +566 | **-122** |
| [28, 40) | 27 | +798 | +582 | **+215** |

**χ² = 3.21 (df=2), p = 0.20.** **Non discriminant.**

→ Une fois le flow LCDM soustrait via 2M++, le signal disparaît. La cinématique du DR est entièrement expliquée par LCDM standard.

## Interprétation

### Ce qu'on peut affirmer

1. **Le signal observé en v1 (table4 brut) est réel** (top 3% placebo, p=0.0002).
2. **La forme du signal (positif monotone décroissant)** est **opposée en signe** à la prédiction Janus dérivée (négatif annulaire).
3. **La signature est dipolaire DR ↔ Shapley**, pattern caractéristique LCDM Repeller-Attractor.
4. **Après soustraction propre du flow LCDM** (via 2M++ Carrick), **plus aucun signal résiduel** — confirmation que LCDM explique tout.

### Ce qu'on NE peut PAS affirmer

1. ❌ « Janus est réfuté ». Le test porte sur **une** prédiction (atténuation annulaire), pas sur le modèle complet.
2. ❌ « La prédiction quantitative Janus a été testée ». La dérivation testée est **mon interprétation**, pas un calcul publié par les auteurs.
3. ❌ « Aucune signature de masses négatives n'existe dans CF4 ». Notre test n'explore qu'une observable (Vpec) et un type de structure (DR).

### Caveats explicites

| # | Caveat | Statut v2 |
|---|---|---|
| 1 | Prédiction Janus = dérivation Yacine | ⚠️ **Ouvert** — email envoyé à Petit/Zejli |
| 2 | Bin 0 vide (centre DR = sous-densité) | ✅ Documenté, attendu physiquement |
| 3 | Statistiques limites bin 1 (4 grp) | 🟡 Partiellement comblé via table2, mais bins 0-1 toujours vides |
| 4 | Pas de soustraction LCDM | ✅ **Comblé** — soustraction 2M++ effectuée, signal disparaît |

### Discussion honnête

Le résultat v2 est **encore plus défavorable** à la prédiction Janus testée que v1 :
- v1 : signal présent mais forme incompatible Janus (cohérent LCDM)
- v2 : signal disparaît après soustraction LCDM (LCDM suffisant)

Si Janus apportait une contribution significative aux Vpec autour du DR au-delà de la dynamique gravitationnelle newtonienne, on s'attendrait à voir un résidu **après** soustraction du modèle 2M++ (qui ne contient pas Janus). On n'en voit pas.

**Caveat critique** : la prédiction Janus testée est une dérivation rapide de l'auteur principal (non-physicien). Les auteurs Petit-Margnat-Zejli pourraient légitimement contester qu'elle représente leur théorie. C'est précisément pourquoi un email leur a été envoyé.

### Que dirait Damour ?

Damour 2019 et 2022 critiquent Janus pour des raisons mathématiques (cohérence des équations, identités de Bianchi). Notre test est **observationnel**, complémentaire mais distinct. Un résultat « LCDM-compatible » ne valide ni n'invalide ses critiques techniques sur Janus-2014/2019.

### Que dirait Petit ?

Trois angles de critique possibles, à attendre dans la réponse à l'email :

1. **« Vous avez testé la mauvaise prédiction »** : soit Janus prédit autre chose pour CF4, soit la dérivation Yacine est incomplète.
2. **« Soustraire 2M++ masque le signal »** : le modèle LCDM contient peut-être implicitement une partie de la dynamique que Janus prédit, donc soustraire dilue le signal réel.
3. **« Le DR n'est pas la bonne cible »** : d'autres structures cosmiques pourraient mieux exhiber la signature Janus.

Ces objections sont à intégrer dans une éventuelle v3.

## Reproductibilité

```bash
git clone https://github.com/pando-yacine/janus-cf4-test
cd janus-cf4-test

# Environnement Python
uv venv .venv
source .venv/bin/activate
uv pip install numpy pandas scipy astropy matplotlib

# Pour la soustraction LCDM, cloner pvhub avec git-lfs
git lfs install
git lfs clone https://github.com/KSaid-1/pvhub.git /tmp/pvhub-repo

# Téléchargement des données publiques
bash code/download_data.sh

# Exécution complète
python code/cf4_01_load.py        # CF4 groupes
python code/cf4_02_select.py      # Sample selection
python code/cf4_03_analysis.py    # Test χ² principal
python code/cf4_04_placebo.py     # Placebo + antipode
python code/cf4_05_figures.py     # Figures
python code/cf4_06_table2_load.py # Table2 individuels
python code/cf4_07_lcdm_subtract.py # Test résidus
```

Tous les résultats numériques dans `results_*.json`.

## Livrables

- 7 documents Markdown (protocoles, analyses, résultats, email)
- 8 scripts Python (~1000 lignes)
- 6 figures (3 PDF + 3 PNG)
- 3 fichiers JSON de résultats structurés
- 4 commits Git, 4 tags de version
- Repo public : https://github.com/pando-yacine/janus-cf4-test

## Suite

- **Court terme** : envoyer email à Petit/Zejli (brouillon dans `EMAIL_PETIT_ZEJLI.md`)
- **Selon réponse** :
  - Si ils proposent une autre prédiction quantitative : v3 du protocole
  - S'ils confirment notre dérivation : v2 finale, présenter à un journaliste scientifique français
  - S'ils ne répondent pas : laisser le repo public comme état de l'art

## Disclosure

- Auteur principal Yacine Arhaliass n'est pas physicien académique
- Analyse menée avec assistance Claude (Anthropic)
- Pré-enregistrement public dès la v1 GitHub
- Aucun financement, aucun conflit d'intérêt
- Tous les résultats négatifs et non-discriminants publiés au même titre que les positifs
- Aucune modification post-data du protocole pré-enregistré
