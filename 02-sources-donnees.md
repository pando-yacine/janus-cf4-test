---
title: Sources de données — accès, formats, schémas
date: 2026-05-09
type: spec-data
---

# Sources de données

## 1. Pantheon+ (catalogue principal de SN-Ia)

### Accès

- **Repo officiel** : https://github.com/PantheonPlusSH0ES/DataRelease
- **Branche** : `main`
- **License** : open (data release publique)
- **Article** : Scolnic et al. 2022, ApJ 938:113 — [arXiv:2112.03863](https://arxiv.org/abs/2112.03863)

### Fichiers cibles à télécharger

| Fichier | Contenu | Taille |
|---|---|---|
| `Pantheon+_Data/4_DISTANCES_AND_COVAR/Pantheon+SH0ES.dat` | Catalogue principal — 1701 SN-Ia | ~600 ko |
| `Pantheon+_Data/4_DISTANCES_AND_COVAR/Pantheon+SH0ES_STAT+SYS.cov` | Matrice de covariance complète | ~25 Mo |
| `Pantheon+_Data/2_LIGHTCURVES/...` | Courbes de lumière individuelles | optionnel |

### Schéma des colonnes (Pantheon+SH0ES.dat)

| Colonne | Description | Unité |
|---|---|---|
| `CID` | identifiant SN | string |
| `IDSURVEY` | survey d'origine | int |
| `zHD` | redshift Hubble Diagram (corrigé peculier) | adim |
| `zHDERR` | erreur sur zHD | adim |
| `zCMB` | redshift dans le frame CMB | adim |
| `zCMBERR` | erreur | adim |
| `zHEL` | redshift héliocentrique | adim |
| `m_b_corr` | magnitude apparente B corrigée | mag |
| `m_b_corr_err_DIAG` | erreur magnitude | mag |
| `MU_SH0ES` | distance modulus | mag |
| `MU_SH0ES_ERR_DIAG` | erreur distance modulus | mag |
| `RA` | ascension droite J2000 | deg |
| `DEC` | déclinaison J2000 | deg |
| `HOST_RA`, `HOST_DEC` | position de la galaxie hôte | deg |
| `HOST_ANGSEP` | séparation angulaire SN-host | arcsec |
| `IS_CALIBRATOR` | flag calibrateur (Cepheides) | 0/1 |

### Conversion équatorial → galactique

Les coordonnées RA/DEC sont en J2000 équatorial. Pour le test, on les convertira en galactique $(l, b)$ via `astropy.coordinates`.

```python
from astropy.coordinates import SkyCoord
import astropy.units as u

c = SkyCoord(ra=df['RA'].values*u.deg, dec=df['DEC'].values*u.deg, frame='icrs')
df['l_gal'] = c.galactic.l.deg
df['b_gal'] = c.galactic.b.deg
```

### Estimation de l'échantillon utile

Critères du protocole figé :
- $\theta_{DR} < 30°$ : cône de 30° d'ouverture autour de $(305°, +5°)$ → couvre ~7% du ciel
- $0.05 < z_{CMB} < 0.15$ : ~environ 50–60% des SN Pantheon+

**Estimation** : 1701 × 0.07 × 0.55 ≈ **65 SN-Ia** dans l'échantillon principal.

À confirmer après téléchargement.

---

## 2. CosmicFlows-4 (champ de vélocités peculières)

### Accès

- **Site EDD (Extragalactic Distance Database)** : https://edd.ifa.hawaii.edu/
- **Article** : Tully et al. 2023, ApJ 944:94 — [arXiv:2209.11238](https://arxiv.org/abs/2209.11238)
- **Format** : tables ASCII via interface EDD ou via Vizier (`J/ApJ/944/94`)

### Utilité dans le test

CosmicFlows-4 fournit :
1. **Position 3D du Dipole Repeller** confirmée dans le frame CMB
2. **Champ de densité reconstruit** dans la sphère locale → permet de vérifier que les SN choisies passent bien "derrière" le DR
3. **Vélocités peculières** prédites pour chaque galaxie (croisement utile avec hôtes Pantheon+)

### Tables principales

| Table | Contenu | Lignes |
|---|---|---|
| `CF4_distances.dat` | Distances et vélocités peculières | ~56 000 |
| `CF4_density_field.fits` | Champ de densité 3D reconstruit | grille 256³ |

### Question pratique

Pour le test minimal de phase 1, **CosmicFlows-4 n'est pas strictement nécessaire** — on peut directement utiliser les redshifts Pantheon+ qui sont déjà corrigés du movement peculier. CF4 sera utile pour :
- Vérifier que l'échantillon SN passe géométriquement derrière le DR
- Affiner la localisation du DR (qui pourrait avoir évolué entre Hoffman 2017 et CF4 2023)
- Étendre l'analyse aux galaxies non-SN si le signal SN est marginal

**Décision figée** : phase 1 = Pantheon+ seulement. CF4 = phase 2 si phase 1 est suggestive.

---

## 3. Position du Dipole Repeller

### Source primaire

**Hoffman, Pomarède, Tully, Courtois 2017**, *Nature Astronomy* 1:0036.
DOI : [10.1038/s41550-016-0036](https://doi.org/10.1038/s41550-016-0036)

### Coordonnées extraites de l'article

| Coordonnée | Valeur |
|---|---|
| Direction (galactique) | $(l, b) \approx (305°, +5°)$ |
| Direction (super-galactique) | $(SGL, SGB) \approx (140°, -30°)$ |
| Distance approximate | 180 ± 50 Mpc |
| "Taille" caractéristique | rayon ~50 Mpc |
| Anti-pôle (Shapley Attractor) | $(l, b) \approx (305°, +30°)$ — opposé en force, pas en position |

### Mise à jour CF4 (Tully 2023)

CosmicFlows-4 confirme la structure et raffine la position. Pour le protocole figé, on utilise la valeur originale Hoffman 2017 et on prendra une **incertitude angulaire de ±5°** comme test de robustesse.

---

## 4. Téléchargement — commandes prévues (à exécuter en phase 2)

```bash
cd /Users/yacinearhalaiss/Workspace/1.KMS/private/projet-revelation/janus-test-observationnel/data

# Pantheon+
mkdir -p pantheon-plus && cd pantheon-plus
curl -L -o Pantheon+SH0ES.dat \
  "https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/Pantheon+_Data/4_DISTANCES_AND_COVAR/Pantheon%2BSH0ES.dat"
curl -L -o Pantheon+SH0ES_STAT+SYS.cov \
  "https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/Pantheon+_Data/4_DISTANCES_AND_COVAR/Pantheon%2BSH0ES_STAT%2BSYS.cov"
cd ..

# CosmicFlows-4 (optionnel phase 2)
mkdir -p cosmicflows-4 && cd cosmicflows-4
# URL exacte à confirmer via EDD interface
```

⚠️ **À ne PAS exécuter avant le freeze du protocole** (commit Git de `01-protocole-pre-enregistre.md`).

---

## 5. Licence et attribution

- **Pantheon+** : usage académique libre. Citation requise : Scolnic et al. 2022, ApJ 938:113.
- **CosmicFlows-4** : open data via EDD. Citation : Tully et al. 2023, ApJ 944:94.
- **Hoffman 2017** : citation pour position DR.
- **Petit-Margnat-Zejli 2024** : citation pour la prédiction testée (EPJ-C 84:1226).
- **Damour 2019, 2022** : citations pour le contexte de la controverse.

Toute publication issue de cette analyse devra inclure ces citations.
