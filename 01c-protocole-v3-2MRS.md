---
title: Protocole pré-enregistré v3 — test photométrique 2MRS K-band
date_freeze: TBD (à figer avant inspection des magnitudes autour du DR)
git_commit_hash: TBD
status: DRAFT — à freeze
predecessors:
  - 01-protocole-pre-enregistre.md (v1, abandonné — Pantheon+ insuffisant)
  - 01b-protocole-v2-CF4.md (v2, exécuté — non-discriminant après LCDM)
---

# Protocole v3 — Test photométrique direct dans 2MRS

## Pourquoi v3 ?

Les v1 et v2 testaient des **proxys** de la prédiction Janus (Vpec → biais distance TF). Le test "vrai" demande de tester **directement la photométrie** des galaxies derrière le DR, comme l'énoncent les auteurs :

> *"the invisible mass [du Dipole Repeller] will manifest its presence by a brightness attenuation, not over the entire disk, but in a ring."*
> — Petit & Zejli 2024 (HAL-04583560), §4

**2MRS** (Huchra et al. 2012, J/ApJS/199/26) est le survey le plus adapté :
- 44 599 galaxies avec magnitudes K-band **corrigées d'extinction**
- Redshifts spectroscopiques indépendants de la magnitude
- **Couverture sky 91%** y compris la zone d'évitement (K-band traverse la poussière)
- Limite Ks ≤ 11.75 mag, |b| ≥ 5° (8° près du bulbe)
- Public via Vizier

## H0 et H1

- **H0 (null, LCDM)** : la distribution des magnitudes apparentes des galaxies à $z$ fixé est **invariante en angle** au DR. Les galaxies derrière le DR ont les mêmes propriétés statistiques que celles dans des directions de contrôle.

- **H1 (Janus)** : il existe un **décalage des magnitudes apparentes vers le faible** (atténuation) dans une **gamme angulaire intermédiaire** correspondant aux bords du DR, et **pas au centre ni en périphérie**. Forme **annulaire**.

## Définitions opérationnelles figées

### Position du Dipole Repeller (gélée v1, v2, v3)

- $(l_{DR}, b_{DR}) = (305.0°, +5.0°)$ — Hoffman et al. 2017
- distance comobile ~180 Mpc, $z_{DR} \approx 0.042$

### Sélection de l'échantillon principal

| Critère | Valeur |
|---|---|
| Source | 2MRS table3.dat (Huchra+ 2012, J/ApJS/199/26, 44599 galaxies) |
| Cône angulaire | $\theta_{DR} < 40°$ |
| Plage de redshift | $0.04 < z < 0.10$ ($z = cz/c$ avec $c = 299792.458$ km/s) |
| Magnitude Ktmag | $K_t \leq 11.5$ mag (sous limite de complétude) |
| Erreur Ktmag | $e_{Kt} < 0.20$ mag |
| Latitude galactique | $|b| > 5°$ (suit la limite naturelle 2MRS) |

### Bins angulaires figés (identiques à v2)

| Bin | $\theta$ (°) | Interprétation Janus |
|---|---|---|
| 0 | $[0, 8]$ | centre — pas d'atténuation attendue |
| 1 | $[8, 18]$ | bord intérieur — atténuation max |
| 2 | $[18, 28]$ | bord extérieur |
| 3 | $[28, 40]$ | périphérie |

### Observables et tests

#### Observable A : magnitude absolue apparente $M_K^{app}$

Pour chaque galaxie $i$ :
$$M_K^{app, i} = K_t^i - DM(z_i)$$

où $DM(z) = 5\log_{10}(d_L(z)/\text{10 pc})$ est le distance modulus calculé en cosmologie LCDM standard ($H_0 = 70$, $\Omega_m = 0.3$).

Si toutes les galaxies derrière le DR appartiennent à la même fonction de luminosité K-band, la distribution de $M_K^{app}$ doit être identique en distribution dans tous les bins angulaires. **Sous Janus**, l'atténuation décalerait $M_K^{app}$ vers les valeurs plus élevées (= magnitudes apparentes plus faibles) dans les bins 1-2.

**Test 1 — Médiane de $M_K^{app}$ par bin** :
$$\Delta M^{(b)} = \tilde M_K^{app}(\text{DR, bin } b) - \tilde M_K^{app}(\text{contrôles, bin } b)$$

avec erreur via bootstrap (1000 itérations).

#### Observable B : comptage à magnitude limite fixée

Pour chaque bin, compter les galaxies vérifiant $K_t \leq K_{lim}$ (avec $K_{lim} = 11.0$ mag — sous la limite de complétude pour permettre détection d'un déficit). Si Janus atténue, certaines galaxies tombent sous le seuil → déficit annulaire :
$$N_{DR}^{(b)} \text{ vs } N_{ctrl}^{(b)}$$

**Test 2 — Test de Poisson** sur le ratio $N_{DR}/\langle N_{ctrl}\rangle$ par bin.

#### Choix de cosmologie LCDM (figé)

- $H_0 = 70$ km/s/Mpc
- $\Omega_m = 0.3$
- $\Omega_\Lambda = 0.7$
- Univers plat
- Distance modulus calculé avec `astropy.cosmology.FlatLambdaCDM`

### Régions de contrôle

Identiques à v2 : 8 positions générées par `numpy.random.default_rng(seed=42)` selon les contraintes :
- $|b| > 20°$
- distance angulaire au DR $> 60°$
- distance angulaire à l'antipode $> 60°$

### Statistique de test (figée)

**Test principal A** : χ² sur les bins peuplés
$$\chi^2_A = \sum_b \frac{(\Delta M^{(b)})^2}{\sigma^2_{\Delta M^{(b)}}}$$

**Test principal B** : χ² sur ratios de comptage
$$\chi^2_B = \sum_b \frac{(N_{DR}^{(b)} - \langle N_{ctrl}\rangle^{(b)})^2}{\langle N_{ctrl}\rangle^{(b)}}$$
(test de Poisson, variance ≈ moyenne pour grand N)

**Seuils décisionnels (df=3 attendu si bins 1-3 peuplés, df=2 si bin 1 vide)** :
- p > 0.05 : non rejet H0
- 0.01 < p < 0.05 : suggestif
- p < 0.01 : significatif

### Tests de validation (figés)

1. **Placebo** : 100 positions aléatoires (seed=12345), $|b| > 10°$, $\theta_{DR} > 50°$, $\theta_{antipode} > 50°$. χ² du DR doit être dans le top 5%.
2. **Antipode** : refaire à $(l, b) = (125°, -5°)$ (Shapley dir.). En Janus, signal opposé en signe (excès de lumière) ou nul (pas de concentration de masse négative au Shapley).
3. **Robustesse** : varier les bins de ±20%.
4. **Test de cohérence** : observable A et observable B doivent donner des conclusions cohérentes.

### Critères de publication

- Si $\chi^2_A$ ET $\chi^2_B$ dans top 5% du placebo → signal candidat.
- Sinon : non discriminant, mais publier comme livrable méthodologique.
- Tous résultats publiés, négatifs inclus.

## Engagement de transparence

Identique aux v1, v2 (cf. `06-pieges-et-biais.md`).

⚠️ **Avant freeze** : aucune inspection des magnitudes 2MRS dans la direction du DR n'a été effectuée. Le ReadMe de Vizier a été lu (format des colonnes), c'est tout.

## Pour figer ce document

```bash
git add 01c-protocole-v3-2MRS.md
git commit -m "freeze: pre-registered protocol v3 — 2MRS K-band photometric test"
git tag v3.0-protocol-frozen
```
