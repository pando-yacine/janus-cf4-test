"""
cf4_02_select.py

Applique les filtres figés du protocole v2 (commit b06dfd3):
  - cône θ_DR < 40°
  - distance 50-350 Mpc
  - e_DMzp < 0.30 mag
  - |b| > 3° (exclure plan galactique strict)

Affiche les comptes mais ne montre PAS les Vpec du DR avant test principal.
"""

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data" / "cf4_groups.csv")

print(f"=== CF4 : {len(df)} groupes ===\n")

# Filtres figés (protocole v2)
mask = (
    (df["theta_DR"] < 40.0) &
    (df["Dist_Mpc"] > 50.0) & (df["Dist_Mpc"] < 350.0) &
    (df["e_DMzp"] < 0.30) &
    (df["GLAT"].abs() > 3.0)
)
sample = df[mask].copy()
print(f"Échantillon après filtres v2 : {len(sample)} groupes")

# Distribution par bin angulaire (compte uniquement, pas les Vpec)
BINS_DEG = [(0, 8), (8, 18), (18, 28), (28, 40)]
print(f"\nDistribution par bin angulaire :")
for i, (lo, hi) in enumerate(BINS_DEG):
    n = ((sample["theta_DR"] >= lo) & (sample["theta_DR"] < hi)).sum()
    print(f"  Bin {i} [{lo:>2d}°, {hi:>2d}°) : {n:>5d} groupes")

# Sanity checks
n_total = len(sample)
n_per_bin = [((sample["theta_DR"] >= lo) & (sample["theta_DR"] < hi)).sum() for lo, hi in BINS_DEG]
min_per_bin = min(n_per_bin)
print(f"\n--- Sanity checks ---")
print(f"N total: {n_total} {'✓' if n_total >= 30 else '✗ INSUFFISANT'}")
print(f"N min par bin: {min_per_bin} {'✓' if min_per_bin >= 5 else '✗ BIN TROP PEU PEUPLÉ'}")
print(f"e_DMzp moyen: {sample['e_DMzp'].mean():.3f} mag")
print(f"Distance moyenne: {sample['Dist_Mpc'].mean():.1f} Mpc")

# Sauvegarde
out = ROOT / "data" / "cf4_sample_main.csv"
sample.to_csv(out, index=False)
print(f"\nSaved sample → {out.relative_to(ROOT)}")

# Filtre de groupes valides aussi pour Vpec (certains ont Vpec = NaN)
n_with_vpec = sample["Vpec"].notna().sum()
print(f"\nN avec Vpec valide: {n_with_vpec}")
