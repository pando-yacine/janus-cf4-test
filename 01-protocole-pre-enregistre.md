---
title: Protocole d'analyse pré-enregistré
date_freeze: 2026-05-09 19:52:08 +0200
git_commit_hash: ac45458a6d086e167830cee05b32abd7fde97d28
git_tag: v1.0-protocol-frozen
status: FROZEN (commit confirmé avant tout téléchargement de données)
---

# Protocole pré-enregistré — Test annulaire derrière Dipole Repeller

⚠️ **Ce document doit être figé par un commit Git AVANT le premier accès aux données Pantheon+/CF4.** Aucune modification ultérieure du protocole sans nouvel enregistrement et refonte de l'analyse.

## H0 et H1

- **H0 (null)** : la distribution des magnitudes résiduelles SN-Ia derrière le Dipole Repeller est **plate** en fonction de la distance angulaire au centre du DR. Compatible avec ΛCDM.
- **H1 (Janus)** : la distribution présente un **excès d'atténuation** (résiduels positifs, $\Delta m > 0$) dans une **gamme angulaire intermédiaire** correspondant aux bords de la sous-densité, et **pas d'excès** au centre.

## Définitions opérationnelles figées

### Position du Dipole Repeller (gélée)

| Coordonnée | Valeur figée | Source |
|---|---|---|
| Longitude galactique $l_{DR}$ | **305.0°** | Hoffman et al. 2017, Nature Astronomy 1:0036 |
| Latitude galactique $b_{DR}$ | **+5.0°** | id. |
| Distance comobile $d_{DR}$ | **180 Mpc** ($z_{DR} \approx 0.042$) | id. |
| Échelle caractéristique $R_{DR}$ | **rayon angulaire ~25°** (taille apparente vue depuis nous) | estimation à partir de la cosmographie CF4 |

### Sélection de l'échantillon principal

| Critère | Valeur |
|---|---|
| Source | Pantheon+ DR1 (Scolnic et al. 2022) |
| Cône angulaire | $\theta < 30°$ autour de $(l_{DR}, b_{DR})$ |
| Plage de redshift | $0.05 < z_{CMB} < 0.15$ (= sources nettement derrière le DR mais pas trop loin pour minimiser autres effets) |
| Erreur photométrique max | $\sigma_{m_B} < 0.20$ mag |
| Quality flag Pantheon+ | utiliser ceux marqués pour analyse cosmologique |

**Estimation préliminaire** : ~50–100 SN-Ia attendues dans cet échantillon.

### Bins angulaires (figés)

| Bin | $\theta$ (°) | Interprétation Janus |
|---:|---|---|
| 0 | $[0, 5]$ | "centre" — pas d'atténuation attendue |
| 1 | $[5, 12]$ | "bord intérieur" — atténuation max attendue |
| 2 | $[12, 20]$ | "bord extérieur" — atténuation moyenne |
| 3 | $[20, 30]$ | "périphérie" — atténuation faible |

### Calcul des résiduels

Pour chaque SN $i$ :
$$\Delta m_i = m_{B,i}^{\text{obs}} - m_B^{\Lambda CDM}(z_i; H_0=70, \Omega_m=0.3)$$

**Choix de cosmologie ΛCDM de référence** (figé) :
- $H_0 = 70$ km/s/Mpc
- $\Omega_m = 0.3$
- $\Omega_\Lambda = 0.7$
- Univers plat

Les vélocités peculières seront corrigées en utilisant les vitesses du référentiel CMB (déjà fournies dans Pantheon+ comme `zCMB`).

### Statistique de test (figée)

**Test principal** : $\chi^2$ entre la distribution observée des résiduels par bin et la prédiction H0 (résiduels = 0 dans tous les bins).

$$\chi^2 = \sum_{b=0}^{3} \frac{\langle \Delta m \rangle_b^2}{\sigma_{\langle\Delta m\rangle_b}^2}$$

avec $\sigma_{\langle\Delta m\rangle_b} = \sigma_{\text{intrinsèque}}/\sqrt{N_b}$ et $\sigma_{\text{intrinsèque}} \approx 0.15$ mag.

**Seuils décisionnels** :
- $\chi^2 < 9.49$ (df=4, p>0.05) : **non rejet de H0**, signal compatible avec ΛCDM
- $\chi^2 \in [9.49, 13.28]$ (0.01 < p < 0.05) : **suggestif** mais non concluant
- $\chi^2 > 13.28$ (p < 0.01) : **signal statistiquement significatif**

**Test discriminant Janus vs ΛCDM** : signature qualitative attendue Janus = bin 0 résiduel ≈ 0, bins 1-2 résiduels positifs, bin 3 résiduel ≈ 0. ΛCDM = tous les bins ≈ 0.

### Tests de validation (figés)

1. **Placebo angulaire** : refaire l'analyse complète à 100 positions aléatoires sur le ciel (excluant le cône DR principal et le plan galactique $|b| < 10°$). Construire la distribution des $\chi^2$ obtenus. Notre $\chi^2_{DR}$ doit être **dans le top 5%** pour être considéré comme signal réel.

2. **Test de rotation** : refaire l'analyse avec le même cône mais centré aux antipodes du DR (vers le Shapley Attractor, attendu opposé). On attend en Janus le **signe contraire** (excès de luminosité = $\Delta m < 0$) — c'est un test bonus.

3. **Test de robustesse** : varier les bornes des bins de ±20% et vérifier que le résultat (significatif ou non) ne change pas qualitativement.

### Critères de publication / non-publication

- **Si $\chi^2_{DR}$ > 13.28 ET dans le top 5% du placebo** : signal candidat, à présenter comme telle (avec toutes les caveats)
- **Sinon** : résultat non discriminant, à publier quand même comme protocole reproductible (résultat négatif)
- **Dans tous les cas** : code et données mises à disposition publiquement (GitHub + Zenodo) avec hash de pré-enregistrement

## Engagements de transparence

1. Le code complet sera publié, pas seulement les figures.
2. Les paramètres d'analyse seront ceux du présent document, sans ajustement post-hoc.
3. Si une modification est nécessaire après inspection des données (ce qui est mauvais signe), elle sera **explicitement documentée** comme "analyse exploratoire post-hoc" — pas comme test pré-enregistré.
4. Les résultats du test placebo seront publiés intégralement (pas seulement le summary statistic du DR).

## Pour figer ce document

```bash
cd /Users/yacinearhalaiss/Workspace/1.KMS/private/projet-revelation/janus-test-observationnel
git add 01-protocole-pre-enregistre.md
git commit -m "freeze: pre-registered analysis protocol for Janus DR test"
git log -1 --format="%H %ci" 01-protocole-pre-enregistre.md
# noter le hash de commit ici dans le frontmatter
```

⚠️ **Note** : `/private` est gitignored au niveau KMS racine. Pour le pré-enregistrement public, on devra :
- Soit créer un repo Git **séparé** dédié à ce protocole (option propre)
- Soit publier sur OSF (Open Science Framework, gratuit) — `https://osf.io/`
- Soit timestamp-er sur Zenodo (DOI permanent)

**Recommandé** : OSF avec timestamp + DOI Zenodo le jour du freeze.
