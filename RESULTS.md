---
title: Test observationnel de la prédiction d'atténuation annulaire de Janus-2024 derrière le Dipole Repeller — Résultats v3
date: 2026-05-09
authors: Yacine Arhaliass + assistant Claude (Anthropic)
status: v3.0 — Sprint 4 ajoute le test photométrique direct (2MRS) — celui qui correspond mot-à-mot à la prédiction publiée
---

# Résultats v3 — Test du modèle Janus contre Dipole Repeller : kinématique CF4 + photométrie 2MRS

## TL;DR

Test pré-enregistré de la prédiction discriminante de **Petit-Margnat-Zejli 2024** (EPJ-C 84:1226) sur trois jeux de données publiques en série :

| Sprint | Source | Test | Verdict |
|---|---|---|---|
| 1 | Pantheon+ SN-Ia | impossible (0 SN dans cône DR — zone d'évitement) | abandonné |
| 2 | CosmicFlows-4 (Vpec brut) | χ² = 20.1, p = 0.0002 — signal réel mais forme **monotone positive**, signature dipolaire LCDM | LCDM-compatible |
| 3 | CF4 résidus après 2M++ | χ² = 3.2, p = 0.20 — signal disparaît | non discriminant |
| **4** | **2MRS K-band photométrique (test direct, aligné mot-à-mot avec la prédiction Petit-Zejli HAL-04583560)** | voir ci-dessous | **non discriminant** |

### Sprint 4 — Test photométrique direct 2MRS (le « bon » test)

| Observable | DR χ² | Placebo (100 pos.) | Antipode (Shapley) | Verdict |
|---|---:|---|---|---|
| **A — Médiane $M_K^{app}$ par bin** | 8.05 (df=4, p=0.09) | DR top **53%** | $\chi^2 = 7.96$, **même pattern bin 0** ($\Delta M = +0.30$ mag) | non discriminant |
| **B — Comptage galaxies $K_t < 11.0$** | 50.36 (df=4) | DR top **12%** | $\chi^2 = 11.83$, **même déficit bins 0-1** | non spécifique au DR |

**Lecture** :
- Observable A : aucune structure annulaire. Le seul écart (bin 0 = centre, +0.26 mag, 12 galaxies) est **répliqué à l'antipode Shapley** (+0.30 mag, 14 galaxies) → artefact de petit échantillon, pas signature DR.
- Observable B : χ² élevé mais dominé par un **excès** dans bin 2 (+50 galaxies, présence du superamas Vela), pas par un **déficit annulaire** comme prédit par Janus. Les bins 0-1 (où l'atténuation maximale est attendue) montrent un déficit qui se retrouve aussi à l'antipode.

**Conclusion principale** : aucune des trois observables testées (Vpec brut, Vpec résiduels post-LCDM, photométrie K-band directe) ne révèle de signature angulaire spécifique au Dipole Repeller. Le test photométrique direct — celui qui correspond textuellement à la prédiction publiée par Petit & Zejli — est **non discriminant**.

⚠️ **Caveat permanent** : la formule quantitative reliant la prédiction d'« atténuation annulaire » à une amplitude observable précise (en mag, en N galaxies, ou en Vpec) reste **ma dérivation**, pas une formule explicite des auteurs. Email envoyé à Petit/Zejli demandant leur lecture.

## Contexte et motivation

### La controverse Janus-Damour

Le modèle cosmologique **Janus** (Petit, depuis 1977 ; reformulé en EPJ-C 84:1226 en 2024 avec Margnat et Zejli) propose une cosmologie bimétrique avec masses positives et négatives. Il est contesté techniquement par Thibault Damour (IHES, notes 2019 et 2022) et largement ignoré par la communauté mainstream.

Le **Dipole Repeller** (Hoffman, Pomarède, Tully, Courtois — *Nature Astronomy* 1:0036, 2017) est interprété par Janus-2024 comme une concentration de **matière à masse négative**.

### La prédiction discriminante

L'article HAL-04583560 (Petit-Zejli, mai 2024) précise textuellement :

> *"the invisible mass [du Dipole Repeller] will manifest its presence by a brightness attenuation, not over the entire disk, but in a ring."*

C'est une prédiction **photométrique directe** : la lumière des galaxies derrière le DR doit être atténuée dans un anneau angulaire intermédiaire (ni au centre, ni en périphérie). Sprint 4 teste cette prédiction sur **2MRS** — survey K-band tout-ciel, directement adapté à la mesure d'atténuation annulaire.

## Méthodologie

### Pré-enregistrement (3 versions)

| Tag | Commit | Date | Statut |
|---|---|---|---|
| `v1.0-protocol-frozen` | `ac45458` | 2026-05-09 19:52 | Pantheon+ figé avant data |
| `v2.0-protocol-frozen` | `b06dfd3` | 2026-05-09 20:48 | CF4 figé avant data |
| `v3.0-protocol-frozen` | `bcdc0e1` | 2026-05-09 22:08 | 2MRS figé avant data |

### Données

| Source | Tables | Échantillon | Hash SHA-256 |
|---|---|---|---|
| Pantheon+ | `Pantheon+SH0ES.dat` | 1701 SN-Ia | `1cb0fc379ef0...` |
| CosmicFlows-4 | `table2.dat` (galaxies indiv.) | 55 877 | `8e908928e683...` |
| CosmicFlows-4 | `table4.dat` (groupes) | 38 053 | `b6edfec68bdf...` |
| 2M++ via pvhub | Carrick et al. 2015 | grille 129³ | (LFS GitHub) |
| **2MRS** | `table3.dat` | **44 599 galaxies K-band** | `ea2eebeacdef...` |

### Protocole figé v3 (extrait — voir `01c-protocole-v3-2MRS.md`)

- Position DR : $(l, b) = (305°, +5°)$
- Cône angulaire : $\theta_{DR} < 40°$
- Plage redshift : $0.04 < z < 0.10$
- Ktmag $\leq 11.5$, $e_{Kt} < 0.20$, $|b| > 5°$
- Bins angulaires : $[0,8] [8,18] [18,28] [28,40]$ degrés
- Cosmologie LCDM figée : $H_0 = 70$, $\Omega_m = 0.3$
- 8 régions de contrôle (seed=42) ; 100 placebo (seed=12345)
- Antipode = $(125°, -5°)$ (direction Shapley)

## Résultats détaillés

### Sprint 1 — Pantheon+ (v1, abandonné)

**0 SN-Ia** dans l'échantillon. Le DR (b=+5°) est dans la **zone d'évitement galactique** de Pantheon+. → Pivot vers CF4 (couvre tout le ciel via méthodes IR proche).

### Sprint 2 — CF4 groupes table4 (v1 résultat)

**Échantillon principal** : 89 groupes de galaxies dans le cône DR.

| Bin θ° | N | <Vpec(DR)> km/s | <Vpec(ctrl)> | ΔVpec |
|---|---:|---:|---:|---:|
| [0, 8) | 0 | — | — | — |
| [8, 18) | 4 | +588 ± 453 | +105 | **+483** |
| [18, 28) | 29 | +268 ± 55 | +75 | **+193** |
| [28, 40) | 56 | +233 ± 44 | +107 | **+126** |

**χ² = 20.10 (df=3), p = 0.0002.** Top 3% du placebo. Mais **forme monotone positive**, opposée en signe à la prédiction Janus dérivée.

**Antipode (Shapley)** : ΔVpec = -433, -39, -165 km/s. **χ² = 44.75 (df=3).** Mirror image en signe → signature dipolaire LCDM standard.

### Sprint 3 — Soustraction LCDM via 2M++ (v2 résultat)

Pour chaque galaxie, calcul de Vpec_LCDM via 2M++ Carrick 2015. Test χ² sur les résidus :

| Bin θ° | N | <résidu(DR)> km/s | <résidu(ctrl)> | Δrésidu |
|---|---:|---:|---:|---:|
| [18, 28) | 6 | +444 | +566 | **-122** |
| [28, 40) | 27 | +798 | +582 | **+215** |

**χ² = 3.21 (df=2), p = 0.20.** Non discriminant — LCDM explique tout.

### Sprint 4 — Test photométrique direct 2MRS (v3, nouveau)

**Échantillon DR** : 993 galaxies (vs 89 en CF4 groupes, vs 0 en Pantheon+). Sample antipode : 812 galaxies.

#### Observable A — Médiane $M_K^{app}$ par bin

| Bin θ° | N (DR) | $\tilde M_K^{app}$ DR | $\langle\tilde M_K^{app}\rangle$ ctrl | $\Delta M_K^{app}$ |
|---|---:|---:|---:|---:|
| [0, 8) | 12 | -25.42 ± 0.18 | -25.68 ± 0.05 | **+0.26** |
| [8, 18) | 109 | -25.70 ± 0.06 | -25.58 ± 0.03 | **-0.13** |
| [18, 28) | 411 | -25.65 ± 0.03 | -25.60 ± 0.02 | **-0.05** |
| [28, 40) | 461 | -25.56 ± 0.05 | -25.62 ± 0.01 | **+0.06** |

$\chi^2_A = 8.05$ (df=4), $p = 0.09$. **Antipode** : $\chi^2_A = 7.96$, ΔM bin 0 = **+0.30** (très similaire au DR). Placebo : DR top **53%** des positions aléatoires → totalement non discriminant.

**Lecture** : aucune structure annulaire. L'écart bin 0 (+0.26 mag, 12 galaxies seulement) est **répliqué à l'antipode** (+0.30 mag, 14 galaxies) → artefact de petits échantillons.

#### Observable B — Comptage galaxies $K_t < 11.0$

| Bin θ° | N (DR) | $\langle N \rangle$ ctrl | Δcount |
|---|---:|---:|---:|
| [0, 8) | 2 | 12.6 | **-10.6** |
| [8, 18) | 32 | 45.8 | **-13.8** |
| [18, 28) | 118 | 67.8 | **+50.2** |
| [28, 40) | 110 | 111.1 | **-1.1** |

$\chi^2_B = 50.36$ (df=4). **Mais** placebo : DR top **12%** des positions aléatoires (médiane placebo = 22.96, max = 149.6) — donc la distribution placebo est **très étalée**, et 12% n'est pas significatif.

**Antipode** : déficits similaires bins 0-1 (-7, -12), pas d'excès bin 2 mais $\chi^2 = 11.83$ aussi non négligeable.

**Lecture** : le χ² est dominé par un **excès** dans bin 2 (+50, sur-densité du superamas Vela qui se trouve dans cette tranche angulaire), pas par un déficit annulaire. La prédiction Janus est un **déficit dans les bins 1-2** (anneau d'atténuation), or on observe au contraire un **excès** dans bin 2 et un déficit dans bin 0 — incompatible avec la signature annulaire.

#### Robustesse bins ±20%

| Variation | $\chi^2_A$ | $\chi^2_B$ |
|---|---:|---:|
| Bins +20% | 4.45 | 50.51 |
| Bins -20% | 12.64 | 49.42 |

Observable B très stable. Observable A fragile (entre 4 et 13) — son significativité dépend du choix exact des bins, ce qui confirme qu'il n'y a pas de signal robuste.

## Interprétation

### Synthèse

Les trois observables testées (Vpec brut, Vpec résiduel post-LCDM, photométrie K-band) **convergent vers le même verdict** : aucune signature annulaire spécifique au Dipole Repeller dans les données publiques actuelles.

Le test photométrique direct — qui correspond mot-à-mot à la prédiction publiée — est **non discriminant** :
- Observable A (le plus propre, magnitude résiduelle) : DR au 53e percentile du placebo, et l'écart marginal en bin 0 est répliqué à l'antipode.
- Observable B (comptage) : signal global ($\chi^2 = 50$) mais profil **incompatible** avec la signature annulaire prédite (excès au lieu de déficit dans le bin annulaire), et placebo top 12% non significatif.

### Ce qu'on peut affirmer

1. **Le test photométrique direct ne montre pas la signature annulaire prédite.** C'est le test que les auteurs eux-mêmes ont annoncé pour le JWST.
2. **2MRS, qui couvre 91% du ciel y compris la zone d'évitement, ne montre rien de spécifique au DR.** L'argument « il faut JWST » a moins de force quand on observe que 2MRS échantillonne déjà la cible avec ~1000 galaxies dans le cône.
3. **Trois observables indépendantes (kinématique brute, kinématique résiduelle, photométrie) convergent sur la même conclusion.**

### Ce qu'on NE peut PAS affirmer

1. ❌ « Janus est réfuté ». Le test porte sur **une** prédiction, pas sur le modèle.
2. ❌ « Aucune signature de masses négatives n'existe ». Notre test n'explore qu'une cible (DR) avec deux familles d'observables.
3. ❌ « La prédiction quantitative Janus a été testée ». La forme de la prédiction (amplitude exacte, profil radial précis) reste à clarifier avec les auteurs.

### Caveats explicites

| # | Caveat | Statut v3 |
|---|---|---|
| 1 | Prédiction Janus = dérivation Yacine | ⚠️ **Toujours ouvert** — email v3 envoyé |
| 2 | Bin 0 limité (12 gal) | 🟡 Documenté, sample DR=993 mais sélection bins |
| 3 | Pas de soustraction LCDM | ✅ Comblé Sprint 3 (CF4) |
| 4 | Pas de test photométrique direct | ✅ **Comblé Sprint 4 (2MRS)** |
| 5 | Le DR est-il la bonne cible ? | ⚠️ Question à transmettre aux auteurs |

### Discussion honnête

Le résultat v3 est **encore plus défavorable** à la prédiction Janus :
- v1 : impossible (zone d'évitement Pantheon+)
- v2 : signal LCDM-compatible, opposé à Janus (forme monotone, pas annulaire)
- v3 (**Sprint 3**) : aucun résidu après soustraction LCDM
- v3 (**Sprint 4**) : le test photométrique direct, **textuellement aligné avec la prédiction publiée**, est non discriminant

Il devient difficile d'invoquer « mauvais test » : on a couvert la kinématique (CF4) et la photométrie (2MRS), brut et résidus, sur 4 bins angulaires couvrant tout le profil annulaire prédit, avec validation par 100 placebo et antipode Shapley.

**Caveat critique permanent** : les auteurs Petit-Margnat-Zejli pourraient légitimement arguer que la quantification numérique précise n'est pas dans leur article. Ils n'ont pas publié d'amplitude attendue en mag pour 2MRS. C'est précisément l'objet de l'email v3.

## Reproductibilité

```bash
git clone https://github.com/pando-yacine/janus-cf4-test
cd janus-cf4-test

uv venv .venv && source .venv/bin/activate
uv pip install numpy pandas scipy astropy matplotlib

# Pour la soustraction LCDM (~470 Mo de cubes 2M++)
git lfs install
git lfs clone https://github.com/KSaid-1/pvhub.git /tmp/pvhub-repo

# Données publiques
mkdir -p data/pantheon-plus data/cosmicflows-4 data/2mrs
curl -sL -o data/pantheon-plus/Pantheon+SH0ES.dat \
  "https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/Pantheon+_Data/4_DISTANCES_AND_COVAR/Pantheon%2BSH0ES.dat"
curl -sL -o data/cosmicflows-4/table2.dat.gz \
  "https://cdsarc.cds.unistra.fr/ftp/J/ApJ/944/94/table2.dat.gz"
curl -sL -o data/cosmicflows-4/table4.dat.gz \
  "https://cdsarc.cds.unistra.fr/ftp/J/ApJ/944/94/table4.dat.gz"
curl -sL -o data/2mrs/table3.dat.gz \
  "https://cdsarc.cds.unistra.fr/ftp/J/ApJS/199/26/table3.dat.gz"
gunzip data/cosmicflows-4/*.gz data/2mrs/*.gz

# Pipeline complète
python code/cf4_01_load.py        # Sprint 2
python code/cf4_03_analysis.py
python code/cf4_07_lcdm_subtract.py # Sprint 3
python code/twomrs_01_load.py     # Sprint 4
python code/twomrs_02_analysis.py
python code/twomrs_03_validation.py
python code/twomrs_04_figures.py
```

Tous les résultats numériques dans `results_*.json`. Figures dans `figures/`.

## Livrables

- 9 documents Markdown (3 protocoles + résultats + email + analyses)
- 12 scripts Python (~1500 lignes)
- 9 figures (PDF + PNG)
- 5 fichiers JSON de résultats structurés
- 6 commits Git, 5 tags de version (v1, v2, v3 protocoles + résultats)
- Repo public : https://github.com/pando-yacine/janus-cf4-test

## Suite

- **Court terme** : envoyer email v3 à Petit/Zejli (brouillon dans `EMAIL_PETIT_ZEJLI.md`)
- **Selon réponse** :
  - Si formule quantitative explicite proposée : v4 du protocole, recalcul avec amplitude prédite
  - Si reconnaissance du test : v3 finale, présenter à un journaliste scientifique
  - Si silence : laisser le repo comme état de l'art reproductible

## Disclosure

- Auteur principal Yacine Arhaliass : ingénieur informatique & IA, Pando Studio. **Pas physicien académique.**
- Analyse menée avec assistance Claude (Anthropic), exécution autonome partielle
- Pré-enregistrement public dès la v1 GitHub (timestamps Git)
- Aucun financement, aucun conflit d'intérêt
- Tous résultats publiés (négatifs et non discriminants au même titre que positifs)
- Aucune modification post-data du protocole pré-enregistré
