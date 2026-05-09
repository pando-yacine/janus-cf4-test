---
title: Brouillon email à Petit / Zejli
date: 2026-05-09
status: draft pour validation Yacine avant envoi
destinataires: jean-pierre.petit@manaty.net, hicham.zejli@manaty.net
---

# Email à Jean-Pierre Petit et Hicham Zejli

**Sujet** : Test observationnel public d'une prédiction du modèle Janus (EPJ-C 84:1226) — demande de vos retours

---

Bonjour Monsieur Petit, Bonjour Monsieur Zejli,

Je vous écris pour vous présenter un travail réalisé en lecteur indépendant et auquel je serais reconnaissant que vous accordiez un regard critique. Je ne suis pas physicien académique, mais j'ai cherché à mener cette démarche avec la plus grande rigueur méthodologique possible.

## Contexte

J'ai lu attentivement votre article *A bimetric cosmological model based on Andreï Sakharov's twin universe approach* (EPJ-C 84:1226, 2024), ainsi que la version HAL-04583560 (mai 2024). J'ai par ailleurs lu intégralement les notes IHES de Thibault Damour de janvier 2019 et décembre 2022, votre version abrégée de la réfutation de juillet 2025, et l'historique des publications du programme Janus.

À la lecture de la HAL-04583560, j'ai retenu cette prédiction comme étant la plus discriminante actuellement testable avec des données publiques :

> *« We predict that when a map is established by the JWST telescope, the invisible mass [du Dipole Repeller] will manifest its presence by a brightness attenuation, not over the entire disk, but in a ring. »*

Constatant qu'aucun test indépendant de cette prédiction n'a, à ma connaissance, été publié en 2024-2026, j'ai monté un protocole d'analyse pré-enregistré et exécuté une première version sur les données publiques.

## Ce que j'ai fait

1. **Pré-enregistrement formel** d'un protocole d'analyse, gelé par commit Git et tag avant tout accès aux données. Deux versions :
   - v1 (Pantheon+ SN-Ia) — abandonnée car le DR tombe dans la zone d'évitement galactique de ce survey
   - v2 (CosmicFlows-4 — Tully et al. 2023) — exécutée

2. **Test discriminant** : ai-je un signal annulaire dans les vélocités peculières des galaxies/groupes derrière le DR, comparé à des régions de contrôle ?

3. **Soustraction LCDM** : j'ai aussi refait le test sur les **résidus** Vpec - V_LCDM, en utilisant la reconstruction publique 2M++ Carrick et al. 2015 (via le package *pvhub* de Said et al.).

## Ce que j'ai trouvé

- **Avant soustraction LCDM** : signal présent au DR (χ² = 20.1, top 3% du placebo, p ≈ 0.0002), **mais signe positif et profil monotone décroissant**, pas annulaire négatif comme la prédiction Janus naïvement formulée pour CF4 le suggérerait. L'antipode (direction Shapley) montre une signature inverse en signe — cohérent LCDM Repeller-Attractor classique.

- **Après soustraction LCDM** (résidus Vpec - V_LCDM) : χ² = 3.2, p = 0.20, **non discriminant**. Les vélocités peculières observées sont entièrement explicables par la dynamique gravitationnelle LCDM standard.

Le détail des résultats, des figures et du code est entièrement public ici :

  **https://github.com/pando-yacine/janus-cf4-test**

## Mes questions

J'ai bien conscience que ma dérivation de la prédiction quantitative testable pour CF4 (« lentille gravitationnelle négative → atténuation luminosité → distance Tully-Fisher surestimée → Vpec biaisée négativement ») est **mon interprétation de votre article**, et qu'elle n'est pas explicitement formulée dans l'EPJ-C 2024 sous cette forme. Les sections 11-12 donnent les lois d'interaction qualitatives mais je n'ai pas trouvé de calcul direct de la signature attendue dans CF4.

D'où mes questions, ouvertement et sans présumer de la conclusion :

1. **Avez-vous une formulation quantitative** de la prédiction d'atténuation annulaire applicable aux vélocités peculières observées dans CosmicFlows-4 ? Ou plutôt à d'autres observables (comptages de galaxies, magnitudes apparentes individuelles, profils de densité de groupes, etc.) ?

2. **Quel est l'observable le plus discriminant** entre Janus et LCDM autour du DR avec les données publiques actuelles, selon vous ?

3. **Considérez-vous qu'un test sur les résidus après soustraction LCDM** (comme je l'ai fait avec 2M++ Carrick) est une démarche valide, ou y a-t-il un risque de masquer le signal Janus en soustrayant un modèle qui contient déjà implicitement une partie de la dynamique attendue par votre théorie ?

4. **Auriez-vous des suggestions** pour améliorer le protocole ou pour identifier une autre structure cosmique (autre vide, autre Repeller) avec une signature plus exploitable que le DR ?

5. **Souhaitez-vous être co-cités** ou vous associer formellement à ce test indépendant, ou préférez-vous garder une distance ?

## Engagement

- Le code, les données et le protocole sont **publics**, libres d'usage et de critique.
- Je m'engage à publier toute réponse de votre part (avec votre accord) ou à ne rien publier (si vous le souhaitez).
- Si vous identifiez une **erreur méthodologique** ou un **biais d'interprétation**, je m'engage à corriger publiquement le repo, en commit traçable.
- Si une analyse plus rigoureuse est possible et que vous souhaitez collaborer, je suis disponible.

Mon objectif n'est pas de réfuter le modèle Janus — j'estime qu'un test indépendant publié, qu'il soit favorable ou défavorable, sert le programme de recherche. La transparence sur les essais incomplets ou non-discriminants est une contribution à la science ouverte.

Je vous remercie sincèrement pour le temps que vous accorderez à cette demande.

Bien cordialement,

Yacine Arhaliass
yacine@pando-studio.com
[éventuellement : votre profil GitHub, votre site, etc.]

---

**P.S.** : J'ai également écrit à Daniel Pomarède (CEA Saclay) en parallèle, comme co-découvreur du Dipole Repeller, pour solliciter un avis méthodologique sur la cinématographie. Vous pouvez me le confirmer si vous préférez que je vous mette en copie d'éventuels échanges.
