---
title: Brouillon email à Petit / Zejli — version v3
date: 2026-05-09
status: draft pour validation Yacine avant envoi
destinataires: jean-pierre.petit@manaty.net, hicham.zejli@manaty.net
---

# Email à Jean-Pierre Petit et Hicham Zejli — version v3

**Sujet** : Test pré-enregistré de votre prédiction d'atténuation annulaire — kinématique CF4 + photométrie 2MRS

---

Bonjour Monsieur Petit, Bonjour Monsieur Zejli,

Je suis ingénieur en informatique et IA (Pando Studio), pas du tout cosmologiste. Je suis le débat Janus depuis l'EPJ-C 2024 et les notes IHES de Damour. J'ai voulu tester si un non-physicien équipé d'outils IA modernes pouvait monter un test rigoureux et reproductible de votre prédiction discriminante en quelques heures.

J'ai retenu cette prédiction de la HAL-04583560 :

> *"the invisible mass [du Dipole Repeller] will manifest its presence by a brightness attenuation, not over the entire disk, but in a ring."*

J'ai pré-enregistré trois protocoles formels (commits Git tagués avant accès aux données) et exécuté l'analyse en série sur Pantheon+, CosmicFlows-4 (kinématique brute + résidus post-LCDM via 2M++), puis 2MRS (test photométrique direct, K-band, 44599 galaxies).

**Repo public** : https://github.com/pando-yacine/janus-cf4-test

## Résultats

| Sprint | Test | χ² | Verdict |
|---|---|---:|---|
| 1 (Pantheon+) | impossible — 0 SN dans cône DR | — | abandon (zone d'évitement) |
| 2 (CF4 Vpec brut) | groupes DR vs contrôles | 20.1 (p=0.0002) | signal réel mais forme **monotone positive** (signature dipolaire LCDM, pas annulaire) |
| 3 (CF4 résidus 2M++) | Vpec - Vpec_LCDM | 3.2 (p=0.20) | non discriminant |
| **4 (2MRS médiane $M_K^{app}$)** | DR vs ctrl par bin angulaire | 8.0 (p=0.09) | **DR top 53% du placebo** — non discriminant |
| **4 (2MRS comptage $K_t<11$)** | déficit annulaire | 50.4 brut | DR top 12% placebo, mais **excès dans bin 2** au lieu de déficit annulaire ; antipode reproduit le même pattern bins 0-1 |

**En résumé** : le test photométrique direct sur 2MRS, qui correspond textuellement à votre prédiction, ne montre **pas** la signature annulaire dans les données actuelles. L'antipode (direction Shapley) reproduit les mêmes écarts marginaux que le DR → ce sont des fluctuations spatiales naturelles, pas une signature spécifique au Repeller.

## Mes questions

Ma quantification de votre prédiction (amplitude attendue en magnitude, profil radial précis, observable optimal) est **ma dérivation**, pas une formule explicite de votre article. D'où :

1. Avez-vous une **amplitude quantitative** attendue pour l'atténuation annulaire derrière le DR, exprimable directement sur 2MRS K-band (en magnitudes, en N galaxies sous une magnitude limite, ou autre observable) ? L'article HAL-04583560 mentionne JWST mais 2MRS sample déjà ~1000 galaxies dans le cône DR aux bons redshifts.

2. Le profil radial précis : votre « anneau » correspond à quel intervalle angulaire (en degrés autour du centre du DR) ? Mes bins [0,8], [8,18], [18,28], [28,40] degrés couvrent-ils correctement la zone que vous attendez la plus contrastée ?

3. **Le DR est-il la cible optimale** ? Une autre structure (Shapley, Local Void, autres « repellers » identifiés) serait-elle plus discriminante avec les données publiques actuelles, avant attente du JWST ?

4. La soustraction du flow LCDM via 2M++ peut-elle **masquer** un signal Janus parce que le modèle 2M++ contiendrait implicitement de la dynamique que vous attribueriez à des masses négatives ?

## Engagement

- Si vous identifiez une erreur méthodologique : je corrige publiquement le repo, commit traçable.
- Je ne publierai rien de votre réponse sans votre accord explicite.
- Si vous indiquez un autre test plus discriminant exécutable sur données publiques, je l'ajoute en v4.

Merci pour le temps que vous accorderez à cette demande, même très bref.

Cordialement,

**Yacine Arhaliass**
Ingénieur informatique & IA — Pando Studio
yacine@pando-studio.com
