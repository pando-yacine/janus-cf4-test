"""
cf4_01_load.py

Charge CosmicFlows-4 table4.dat (38053 groupes), parse le format fixed-width
selon le ReadMe, calcule θ_DR pour chaque groupe.

Sortie: data/cf4_groups.csv avec colonnes: PGC, DM, e_DM, Dist, V3k, Vpec, l_gal, b_gal, theta_DR
"""

from pathlib import Path
import numpy as np
import pandas as pd

# Constantes figées par protocole v2 (commit b06dfd3)
L_DR_DEG = 305.0
B_DR_DEG = 5.0

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "cosmicflows-4" / "table4.dat"
OUTPUT = ROOT / "data" / "cf4_groups.csv"


def angular_distance_deg(l1, b1, l2, b2):
    l1r = np.deg2rad(l1)
    b1r = np.deg2rad(b1)
    l2r = np.deg2rad(l2)
    b2r = np.deg2rad(b2)
    cos_d = np.sin(b1r) * np.sin(b2r) + np.cos(b1r) * np.cos(b2r) * np.cos(l1r - l2r)
    return np.rad2deg(np.arccos(np.clip(cos_d, -1.0, 1.0)))


def parse_table4(path):
    """Parse fixed-width format de CF4 table4.dat selon ReadMe.

    Bytes (1-indexed) → Python slice (0-indexed):
      1-7   PGC          → [0:7]
      9-14  DMzp         → [8:14]
      16-20 e_DMzp       → [15:20]
      22-26 Dist (Mpc)   → [21:26]
      28-32 Vh           → [27:32]
      34-38 Vls          → [33:38]
      40-44 V3k          → [39:44]
      46-50 fV3k         → [45:50]
      52-57 Vpds         → [51:57]
      59-63 Vpwf         → [58:63]
      65-69 Vpec         → [64:69]
      71-75 Hi           → [70:75]
      77-82 logHi        → [76:82]
      84-91 RAdeg        → [83:91]
      93-100 DEdeg       → [92:100]
      102-109 GLON       → [101:109]
      111-118 GLAT       → [110:118]
      120-127 SGL        → [119:127]
      129-136 SGB        → [128:136]
    """
    rows = []
    with open(path, "r") as f:
        for line in f:
            try:
                row = {
                    "PGC": int(line[0:7].strip()),
                    "DMzp": float(line[8:14].strip()),
                    "e_DMzp": float(line[15:20].strip()),
                    "Dist_Mpc": float(line[21:26].strip()),
                    "V3k": int(line[39:44].strip()) if line[39:44].strip() else np.nan,
                    "Vpec": int(line[64:69].strip()) if line[64:69].strip() else np.nan,
                    "RAdeg": float(line[83:91].strip()),
                    "DEdeg": float(line[92:100].strip()),
                    "GLON": float(line[101:109].strip()),
                    "GLAT": float(line[110:118].strip()),
                    "SGL": float(line[119:127].strip()),
                    "SGB": float(line[128:136].strip()),
                }
                rows.append(row)
            except (ValueError, IndexError) as e:
                # skip malformed lines (rare)
                continue
    return pd.DataFrame(rows)


def main():
    print(f"Loading {INPUT.name}...")
    df = parse_table4(INPUT)
    print(f"  parsed {len(df)} groups")

    # Sanity checks de structure
    assert df["GLAT"].between(-90, 90).all(), "GLAT out of range"
    assert df["GLON"].between(-1, 361).all(), "GLON out of range"
    assert df["Dist_Mpc"].min() > 0, "Negative distance"

    # Calcul de θ_DR pour chaque groupe
    df["theta_DR"] = angular_distance_deg(df["GLON"].to_numpy(), df["GLAT"].to_numpy(),
                                          L_DR_DEG, B_DR_DEG)

    # Diagnostics globaux (PAS spécifiques au DR — pour ne pas biaiser)
    print(f"\n--- Diagnostics globaux (sans regarder le DR) ---")
    print(f"GLON range: {df['GLON'].min():.1f}° to {df['GLON'].max():.1f}°")
    print(f"GLAT range: {df['GLAT'].min():.1f}° to {df['GLAT'].max():.1f}°")
    print(f"Distance range: {df['Dist_Mpc'].min():.1f} to {df['Dist_Mpc'].max():.1f} Mpc")
    print(f"Vpec range: {df['Vpec'].min():.0f} to {df['Vpec'].max():.0f} km/s")
    print(f"e_DMzp median: {df['e_DMzp'].median():.3f} mag")
    print(f"\nCouverture sky:")
    print(f"  |b| < 5°  (zone d'évitement strict): {(df['GLAT'].abs() < 5).sum():>6d} groupes")
    print(f"  |b| < 10° (zone d'évitement large) : {(df['GLAT'].abs() < 10).sum():>6d} groupes")
    print(f"  hors plan galactique (|b|>10°)     : {(df['GLAT'].abs() >= 10).sum():>6d} groupes")

    # Sauvegarde
    df.to_csv(OUTPUT, index=False)
    print(f"\nSaved {len(df)} groups → {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
