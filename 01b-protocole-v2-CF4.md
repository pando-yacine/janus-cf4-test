---
title: Protocole pré-enregistré v2 — pivot CosmicFlows-4
date_freeze: TBD (à figer par commit Git AVANT de regarder les valeurs CF4 autour du DR)
git_commit_hash: TBD
status: DRAFT — validation puis freeze
predecessor: 01-protocole-pre-enregistre.md (commit ac45458, abandonné car Pantheon+ insuffisant en zone d'évitement)
---

# Protocole v2 — Test de la signature de masse négative du Dipole Repeller via CosmicFlows-4

## Contexte du pivot

Le protocole v1 (test SN-Ia annulaire avec Pantheon+) a été **abandonné honnêtement** après Sprint 1 :
- 0 SN-Ia satisfait les critères figés
- Cause : DR à $b = +5°$ dans la zone d'évitement galactique, où Pantheon+ a quasi-aucune SN
- Diagnostic : `RESULTS_SPRINT1.md`

Pivot : utiliser **CosmicFlows-4 (Tully et al. 2023)**, qui couvre tout le ciel (y compris la zone d'évitement) et fournit **distances + vélocités peculières** pour 38 053 groupes de galaxies.

## H0 et H1 reformulés pour CF4

### Prédiction Janus selon Petit-Margnat-Zejli 2024 (EPJ-C 84:1226)

Le Dipole Repeller est interprété en Janus comme une **concentration de matière à masse négative**. Cette concentration produit deux effets observables :

1. **Effet gravitationnel newtonien** : repousse les galaxies positives (= notre univers observable). Cet effet est **déjà observé** et est précisément ce qui définit le DR comme "Repeller".

2. **Effet de lentille gravitationnelle inversée** sur les sources positives d'arrière-plan : les photons rasant les bords de la concentration sont défléchis (atténués), pas ceux passant par le centre.

L'effet (1) est compatible avec l'interprétation LCDM standard (le DR est juste un vide). L'effet (2) est **spécifique à Janus** et constitue notre prédiction discriminante.

### Signature observable dans CF4

Avec CF4, on ne mesure pas la luminosité directement. Mais les distances Tully-Fisher (TF) et Fundamental Plane (FP) sont **dérivées de la magnitude apparente** des galaxies, calibrée sur leur kinématique (largeur de raie HI pour TF, dispersion de vitesses pour FP).

→ Si une galaxie d'arrière-plan est atténuée par lentille négative (Janus), sa magnitude apparente est plus faible que prédite par sa kinématique. La distance TF/FP estimée est alors **surestimée**.

→ La vélocité peculière apparente $V_{pec} = c z_{CMB} - H_0 \cdot d_{TF}$ est **biaisée vers les valeurs négatives** (la galaxie semble se rapprocher plus vite que sa distance Hubble vraie).

### Hypothèses figées

- **H0 (null, LCDM)** : la distribution des $V_{pec}$ des groupes CF4 derrière le DR est **expliquée intégralement** par la dynamique gravitationnelle newtonienne (le DR repousse, les flows convergent comme prédit par les simulations N-body LCDM). Pas de structure annulaire résiduelle dans les $V_{pec}$ après soustraction de ce flow.

- **H1 (Janus)** : il existe un **résidu annulaire** dans les $V_{pec}$ des groupes CF4 derrière le DR, **après** soustraction du modèle de flow LCDM, attribuable à la lentille gravitationnelle inversée. Le résidu doit être **plus négatif aux bords du DR** (rayon angulaire intermédiaire) qu'au centre ou en périphérie.

### Test simplifié exécutable

⚠️ Modéliser le flow LCDM précis demande une expertise cosmographique au-delà de ce sprint. **Test simplifié** : on compare la distribution des $V_{pec}$ derrière le DR à celle dans des **régions de contrôle** sur le ciel, pour des bins angulaires concentriques équivalents. Si Janus est correct, on attend un **profil asymétrique annulaire** dans la région DR mais pas dans les régions de contrôle.

## Définitions opérationnelles figées

### Position du Dipole Repeller (gélée)

Identique à v1 :
- $(l_{DR}, b_{DR}) = (305.0°, +5.0°)$ — Hoffman et al. 2017
- Distance comobile $d_{DR} \approx 180$ Mpc
- Rayon angulaire caractéristique ~25° vue depuis nous

### Sélection de l'échantillon principal

| Critère | Valeur figée |
|---|---|
| Source | CF4 table4.dat (38 053 groupes) |
| Cône angulaire | $\theta_{DR} < 40°$ (élargi vs v1 car prédiction CF4 plus diffuse) |
| Plage de distance | $50 \text{ Mpc} < d < 350 \text{ Mpc}$ (groupes derrière le DR mais dans le volume bien échantillonné) |
| Erreur sur DM | $e_{DMzp} < 0.30$ mag (qualité raisonnable) |
| Exclusion zone galactique stricte | $\|b\| > 3°$ (pas $\|b\| > 10°$ pour ne pas exclure le DR lui-même) |

### Bins angulaires figés

| Bin | $\theta$ (°) | Interprétation Janus |
|---:|---|---|
| 0 | $[0, 8]$ | "centre" — pas de signature attendue |
| 1 | $[8, 18]$ | "bord intérieur" — résidu max attendu |
| 2 | $[18, 28]$ | "bord extérieur" — résidu moyen |
| 3 | $[28, 40]$ | "périphérie" — résidu faible |

### Statistique de test (figée)

**Observable** : $\bar V_{pec}^{(b)}$ = moyenne des $V_{pec}$ par bin angulaire, après normalisation par le contrôle.

**Construction du contrôle** :
- Pour chaque bin, calculer $\bar V_{pec}^{(b)}$ dans la **région DR** (cône de 40° centré sur $l_{DR}, b_{DR}$).
- Calculer $\bar V_{pec}^{(b)}$ dans **N=8 régions de contrôle** également réparties sur le ciel (à des $(l, b)$ tirés sur l'octahedron : (0°, 0°), (90°, 0°), (180°, 0°), (270°, 0°), avec leurs symétriques en latitude). **Exclure** la région DR et son antipode (Shapley) ainsi que le plan galactique.
- Pour chaque bin, calculer $\Delta V_{pec}^{(b)} = \bar V_{pec, DR}^{(b)} - \langle \bar V_{pec, ctrl}^{(b)} \rangle$ avec son erreur empirique (std des contrôles).

**Test principal** : χ² sur les 4 bins :
$$\chi^2 = \sum_b \frac{(\Delta V_{pec}^{(b)})^2}{\sigma_{\Delta V}^2}$$

**Seuils décisionnels** :
- $\chi^2 < 9.49$ (df=4, p>0.05) : non rejet H0
- $\chi^2 \in [9.49, 13.28]$ : suggestif
- $\chi^2 > 13.28$ : signal statistiquement significatif

**Test discriminant Janus vs LCDM** : signature qualitative attendue Janus = bin 0 ≈ 0, bins 1-2 négatifs, bin 3 ≈ 0. LCDM peut produire une variation monotone (non annulaire). On notera la **forme** du profil.

### Tests de validation (figés)

1. **Placebo angulaire** : refaire l'analyse à 100 positions aléatoires sur le ciel (excluant le cône DR principal et $|b| < 10°$). $\chi^2_{DR}$ doit être dans le top 5%.

2. **Test antipode** : refaire à $(l, b) = (125°, -5°)$ (antipode du DR ≈ direction Shapley). En LCDM standard, le Shapley Attractor produit une signature opposée. En Janus, on s'attend aussi à un signal opposé, mais peut-être pas exactement annulaire (pas de "concentration de masse négative" au Shapley).

3. **Test robustesse** : varier les bornes des bins de ±20% et vérifier que le résultat (significatif ou non) ne change pas qualitativement.

### Critères de publication / non-publication

- **Si $\chi^2_{DR}$ > 13.28 ET dans le top 5% du placebo** : signal candidat
- **Sinon** : résultat non discriminant, à publier comme protocole reproductible

Dans tous les cas, code et données sur GitHub + commit hash de pré-enregistrement noté.

## Engagements de transparence

Identiques au protocole v1 (cf. `06-pieges-et-biais.md`).

## Pour figer ce document

```bash
cd /Users/yacinearhalaiss/Workspace/1.KMS/private/projet-revelation/janus-test-observationnel
# Vérifier qu'on n'a pas regardé les valeurs CF4 autour du DR avant de freezer
git add 01b-protocole-v2-CF4.md
git commit -m "freeze: pre-registered protocol v2 — CF4 pivot for Janus DR test"
git tag v2.0-protocol-frozen
git log -1 --format="%H %ci" 01b-protocole-v2-CF4.md
```

⚠️ **À ce stade** : on a téléchargé table4.dat et regardé seulement les 2 premières lignes pour vérifier le format. **Pas regardé** la distribution des Vpec autour du DR. Le protocole peut être figé sans biais.
