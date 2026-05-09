"""
01_load_and_convert.py

Charge le catalogue Pantheon+SH0ES.dat, convertit RA/DEC en coordonnées
galactiques (l, b), calcule la distance angulaire au Dipole Repeller.

Usage:
    python 01_load_and_convert.py

Sortie:
    data/pantheon_with_galactic.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd
from astropy.coordinates import SkyCoord
import astropy.units as u

# Constantes figées par le protocole pré-enregistré (commit ac45458)
L_DR_DEG = 305.0
B_DR_DEG = 5.0

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "pantheon-plus" / "Pantheon+SH0ES.dat"
OUTPUT = ROOT / "data" / "pantheon_with_galactic.csv"


def angular_distance_deg(l1, b1, l2, b2):
    """Distance angulaire (degrés) entre points (l1,b1) et (l2,b2) sur la sphère, par loi des cosinus sphériques.

    Accepte arrays ou scalaires en chaque argument (broadcast numpy)."""
    l1r = np.deg2rad(l1)
    b1r = np.deg2rad(b1)
    l2r = np.deg2rad(l2)
    b2r = np.deg2rad(b2)
    cos_d = np.sin(b1r) * np.sin(b2r) + np.cos(b1r) * np.cos(b2r) * np.cos(l1r - l2r)
    return np.rad2deg(np.arccos(np.clip(cos_d, -1.0, 1.0)))


def main() -> None:
    print(f"Loading {INPUT.name}...")
    df = pd.read_csv(INPUT, sep=r"\s+", comment="#")
    print(f"  loaded {len(df)} rows, {len(df.columns)} columns")

    # Vérifications
    required = {"CID", "zCMB", "m_b_corr", "m_b_corr_err_DIAG", "RA", "DEC"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Colonnes manquantes: {missing}")

    print("Converting RA/DEC (J2000) → galactic (l, b)...")
    coords = SkyCoord(ra=df["RA"].to_numpy() * u.deg, dec=df["DEC"].to_numpy() * u.deg, frame="icrs")
    df["l_gal"] = coords.galactic.l.deg
    df["b_gal"] = coords.galactic.b.deg

    print(f"Computing angular distance to Dipole Repeller at (l={L_DR_DEG}, b={B_DR_DEG})...")
    df["theta_DR"] = angular_distance_deg(df["l_gal"].to_numpy(), df["b_gal"].to_numpy(), L_DR_DEG, B_DR_DEG)

    # Diagnostics
    print(f"\n--- Diagnostics ---")
    print(f"Redshift range: {df['zCMB'].min():.4f} to {df['zCMB'].max():.4f}")
    print(f"theta_DR range: {df['theta_DR'].min():.2f}° to {df['theta_DR'].max():.2f}°")
    print(f"SN within 30° of DR: {(df['theta_DR'] < 30).sum()}")
    print(f"SN within 30° of DR AND 0.05<z<0.15: {((df['theta_DR'] < 30) & (df['zCMB'] > 0.05) & (df['zCMB'] < 0.15)).sum()}")

    # Sauvegarde
    out_cols = ["CID", "IDSURVEY", "zCMB", "zCMBERR", "m_b_corr", "m_b_corr_err_DIAG",
                "MU_SH0ES", "MU_SH0ES_ERR_DIAG", "IS_CALIBRATOR",
                "RA", "DEC", "l_gal", "b_gal", "theta_DR"]
    df_out = df[out_cols].copy()
    df_out.to_csv(OUTPUT, index=False)
    print(f"\nSaved {len(df_out)} rows → {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
