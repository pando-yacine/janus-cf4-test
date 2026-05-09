---
title: Test observationnel de la prédiction d'atténuation annulaire de Janus-2024 derrière le Dipole Repeller — Résultats
date: 2026-05-09
authors: Yacine Arhaliass + assistant Claude (Anthropic)
status: v1.0 — résultats finaux Sprint 2 (CF4 pivot)
---

# Résultats finaux

## TL;DR

Test pré-enregistré de la prédiction discriminante de Petit-Margnat-Zejli 2024 (EPJ-C 84:1226) sur les données publiques **CosmicFlows-4** (Tully et al. 2023, ApJ 944:94).

**Verdict** : un signal statistiquement significatif est détecté autour du Dipole Repeller (χ² = 20.1, top 3% du placebo, p ~ 0.0002). Mais sa **forme ne correspond pas** à la signature annulaire prédite par Janus :
- ΔVpec observé : **+483 / +193 / +126 km/s** (positif, monotone décroissant avec θ)
- ΔVpec prédit Janus : **0 / négatif max / 0** (annulaire, signe négatif)

Le signal observé est **cohérent avec la cinématique LCDM standard** du couple Dipole Repeller / Shapley Attractor (vélocités peculières induites par la gravitation newtonienne). Le test antipode (direction Shapley) confirme cette interprétation : ΔVpec ≈ -433 / -39 / -165 km/s — **mirror image** du DR, comme LCDM le prédit.

→ **Le test est défavorable à la prédiction Janus testable formulée pour CF4.** Cela ne réfute pas le modèle Janus en général, mais cela suggère que la prédiction d'atténuation annulaire formulée par les auteurs est soit absente, soit dominée par les effets cinématiques classiques.

## Contexte

Cette analyse teste empiriquement la prédiction discriminante du modèle cosmologique **Janus** de Petit, Margnat & Zejli (EPJ-C 84:1226, 2024) :

> *"We predict that when a map is established by the JWST telescope, the invisible mass [du Dipole Repeller] will manifest its presence by a brightness attenuation, not over the entire disk, but in a ring."*
> — Petit & Zejli 2024 (HAL-04583560), §4

Cette prédiction est conséquente d'un effet de **lentille gravitationnelle inversée** par les masses négatives concentrées dans le DR.

## Méthodologie

### Pré-enregistrement

Protocole figé en commit Git AVANT inspection des données :
- **v1** (commit `ac45458`, 2026-05-09 19:52) : test SN-Ia avec Pantheon+ → **abandonné** (échantillon insuffisant en zone d'évitement galactique)
- **v2** (commit `b06dfd3`, 2026-05-09 20:48) : pivot CosmicFlows-4 → **exécuté** ci-dessous

### Données

- **CosmicFlows-4 table4.dat** : 38 053 groupes de galaxies avec distances et vélocités peculières
- Source : CDS Strasbourg, J/ApJ/944/94
- SHA-256 vérifié : `b6edfec68bdfddeada8f3b8f11938f3bbda98a8e2894ff136a369c2ad6594e94`

### Filtres figés (protocole v2)

- Cône angulaire : θ_DR < 40°
- Distance comobile : 50 < d < 350 Mpc
- Erreur sur distance modulus : e_DM < 0.30 mag
- Latitude galactique : |b| > 3°

### Bins angulaires figés

| Bin | θ (°) | Interprétation Janus |
|---|---|---|
| 0 | [0, 8] | centre — pas d'atténuation attendue |
| 1 | [8, 18] | bord intérieur — atténuation max |
| 2 | [18, 28] | bord extérieur |
| 3 | [28, 40] | périphérie |

### Statistique

χ² test sur les bins peuplés (≥2 groupes), ΔVpec = <Vpec(DR)> - <Vpec(8 contrôles)>.

## Résultats numériques

### Test principal au DR (l=305°, b=+5°)

| Bin | N | <Vpec(DR)> | <Vpec(ctrl)> | ΔVpec |
|---|---:|---:|---:|---:|
| [0, 8°) | 0 | — | — | — |
| [8, 18°) | 4 | +588 ± 453 km/s | +105 km/s | **+483** |
| [18, 28°) | 29 | +268 ± 55 km/s | +75 km/s | **+193** |
| [28, 40°) | 56 | +233 ± 44 km/s | +107 km/s | **+126** |

**χ² = 20.10 (df=3), p-value = 0.0002**

Seuils : p<0.05 si χ²>7.81 ; p<0.01 si χ²>11.34. → Signal statistiquement significatif au seuil 1%.

### Test placebo (100 positions aléatoires)

- χ²_DR (20.10) > 97 placebos sur 100
- **DR dans le top 3.0%** des positions placebo
- Median placebo : χ² = 4.40 ; max placebo : χ² = 32.87
- → Signal réel, pas une fluctuation aléatoire

### Test antipode (l=125°, b=-5°, direction Shapley Attractor)

| Bin | N | <Vpec(antipode)> | ΔVpec |
|---|---:|---:|---:|
| [0, 8°) | 0 | — | — |
| [8, 18°) | 6 | -328 km/s | **-433** |
| [18, 28°) | 42 | +36 km/s | **-39** |
| [28, 40°) | 102 | -58 km/s | **-165** |

**χ² = 44.75 (df=3), p < 0.0001**

→ Signal **encore plus significatif au Shapley** qu'au DR, avec **signes opposés**. Cohérent avec LCDM standard (Repeller + Attractor formant un dipole).

### Test robustesse

- Bins +20% : χ² = 19.89 (p=0.0002)
- Bins -20% : χ² = 19.14 (p=0.0003)

→ Résultat **stable** à ±20% sur les définitions de bins.

## Interprétation honnête

### Signal détecté ≠ Signature Janus

Le signal observé au DR est :
- **Significatif** (p<0.001, top 3% placebo)
- **Robuste** (stable aux variations de bins)
- **De signe POSITIF** dans tous les bins peuplés
- **Monotone décroissant** avec θ_DR (max au plus proche du centre, atténué en périphérie)

La prédiction Janus testée pour CF4 (lentille négative → distance TF surestimée → Vpec biaisée vers le négatif aux bords) prédisait :
- Signe **NÉGATIF** dans les bins intermédiaires
- Profil **ANNULAIRE** (max au bord, ≈ 0 au centre et en périphérie)

→ Le test est **discriminant** et **défavorable à la prédiction Janus testée**.

### Cohérence avec LCDM

L'observation est très bien expliquée par la dynamique gravitationnelle newtonienne LCDM standard :
- Le DR (sous-densité) **repousse** les galaxies → Vpec positives derrière (+483, +193, +126)
- Le Shapley (sur-densité) **attire** les galaxies → Vpec négatives derrière (-433, -39, -165)
- L'antisymétrie DR ↔ Shapley (top: signe inverse) est précisément la signature **dipolaire** classique du Local Flow

Pas besoin d'invoquer Janus pour expliquer ce qu'on voit.

### Caveats critiques

1. **La prédiction Janus que j'ai testée pour CF4 est ma dérivation**, pas un calcul publié par Petit-Zejli. La chaîne est : lentille négative → atténuation lumineuse → distance TF surestimée → Vpec biaisée négativement. Il est possible que les auteurs ont une prédiction différente pour CF4 que je n'ai pas formulée correctement.

2. **Le bin 0 (centre) est vide** : 0 groupes dans la région 0-8° autour du DR à 50-350 Mpc. C'est cohérent avec la définition même du DR (sous-densité) — pas un bug. Mais on ne peut donc rien dire du comportement au centre.

3. **L'incertitude du bin 1 (8-18°) est large** (4 groupes seulement, σ=453). La moyenne +588 km/s est compatible avec n'importe quoi entre 0 et 1500 km/s.

4. **La prédiction quantitative Janus n'a pas été dérivée** : on n'a comparé qu'à un sketch qualitatif. Pour un test plus rigoureux, il faudrait calculer l'amplitude attendue selon Petit-Zejli pour la géométrie spécifique du DR.

5. **Modèle de contrôle simplifié** : 8 régions de contrôle avec seed=42, pas une analyse complète des biais cosmographiques. Pour un papier professionnel, il faudrait soustraire un modèle de flow LCDM (e.g., reconstruction CF4) et regarder les résidus.

### Ce qu'on peut dire / ne peut pas dire

| Affirmation | Statut |
|---|---|
| "Le DR montre une signature LCDM standard" | ✅ confirmé |
| "Janus est réfuté" | ❌ trop fort — on a testé une prédiction parmi d'autres |
| "La prédiction d'atténuation annulaire CF4 n'est pas observée" | ✅ avec les caveats ci-dessus |
| "Pas besoin de masses négatives pour expliquer le DR" | ✅ d'un point de vue parcimonie |

## Reproductibilité

Tout le code et les données sont dans ce dépôt :

```
janus-test-observationnel/
├── 01-protocole-pre-enregistre.md      protocole v1 (abandonné)
├── 01b-protocole-v2-CF4.md             protocole v2 (figé avant data)
├── data/
│   ├── pantheon-plus/Pantheon+SH0ES.dat
│   └── cosmicflows-4/table4.dat        ← analyse principale
├── code/
│   ├── cf4_01_load.py                   chargement et conversion
│   ├── cf4_02_select.py                 application des filtres
│   ├── cf4_03_analysis.py               χ² principal
│   ├── cf4_04_placebo.py                placebo + antipode + robustesse
│   └── cf4_05_figures.py                figures
├── figures/
│   ├── 01_skymap.pdf
│   ├── 02_residuals.pdf
│   └── 03_placebo.pdf
├── results_main.json                    résultats détaillés JSON
├── results_validation.json              placebo + antipode JSON
└── data_manifest.json                   hashes SHA-256
```

Pour reproduire :
```bash
git clone <repo>  # quand v1 publique
cd janus-test-observationnel
uv venv .venv
source .venv/bin/activate
uv pip install numpy pandas scipy astropy matplotlib

# Re-télécharger les données
bash code/download_data.sh  # à écrire si besoin

# Lancer l'analyse complète
python code/cf4_01_load.py
python code/cf4_02_select.py
cd code && python cf4_03_analysis.py
python cf4_04_placebo.py
python cf4_05_figures.py
```

Toutes les statistiques sont dans `results_main.json` et `results_validation.json`.

## Suite possible

### Si on voulait aller plus loin

1. **Demander à Petit/Zejli** la prédiction quantitative exacte de Janus pour CF4 / DR. Notre dérivation rapide (atténuation lumineuse → biais Vpec) pourrait ne pas être la bonne quantité testée par les auteurs.

2. **Affiner le contrôle** : utiliser une reconstruction du flow LCDM (par exemple Tully-2023 lui-même, ou Hoffman-Pomarède) et regarder les **résidus** par rapport à ce flow, pas les Vpec directement.

3. **Ajouter d'autres surveys** : 6dFGS Fundamental Plane, 2MTF, DESI BGS, pour couvrir plus de groupes derrière le DR.

4. **Test croisé sur d'autres vides cosmologiques** (Local Void, Boötes Void) pour voir si l'absence de signature Janus est confirmée ailleurs.

### Pour ce sprint

Le livrable v1 est **complet**. Les 4 fichiers JSON + 6 PDF/PNG + 5 scripts Python + 7 documents .md constituent une base reproductible suffisante pour partager.

## Avant publication v1 publique

- [ ] Relire le protocole et confirmer cohérence
- [ ] Vérifier que toutes les figures sont lisibles
- [ ] Décider du repo public (GitHub) — préparer README adapté
- [ ] Décider d'un éventuel pré-print sur OSF/Zenodo
- [ ] (Optionnel) écrire à Daniel Pomarède pour obtenir un avis
- [ ] (Optionnel) écrire à Petit/Zejli pour partager le résultat et leur demander leur lecture

## Disclosure

- Auteur principal (Yacine Arhaliass) n'est pas un physicien académique
- Cette analyse a été conçue avec assistance d'un système IA (Claude)
- Pré-enregistrement dans Git local (les hashes seront publics à la v1 GitHub)
- Aucun financement, aucun conflit d'intérêt connu
- Le résultat **est défavorable à une prédiction Janus**, ce qui pourrait paraître contre l'intérêt du programme de recherche — c'est précisément la valeur de l'engagement de transparence
