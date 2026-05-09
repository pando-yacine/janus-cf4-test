"""
twomrs_01_load.py

Sprint 4 — chargement de 2MRS table3 (44599 galaxies, K-band).
Parse fixed-width selon ReadMe, calcule θ_DR et magnitudes utiles.
"""

from pathlib import Path
import numpy as np
import pandas as pd
from astropy.cosmology import FlatLambdaCDM

# Constantes figées par protocole v3 (commit bcdc0e1)
L_DR_DEG = 305.0
B_DR_DEG = 5.0
H0 = 70.0
OM0 = 0.3
C_KMS = 299792.458

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "2mrs" / "table3.dat"
OUTPUT = ROOT / "data" / "2mrs_with_galactic.csv"


def angular_distance_deg(l1, b1, l2, b2):
    l1r = np.deg2rad(l1)
    b1r = np.deg2rad(b1)
    l2r = np.deg2rad(l2)
    b2r = np.deg2rad(b2)
    cos_d = np.sin(b1r) * np.sin(b2r) + np.cos(b1r) * np.cos(b2r) * np.cos(l1r - l2r)
    return np.rad2deg(np.arccos(np.clip(cos_d, -1.0, 1.0)))


def parse_2mrs_table3(path):
    """Parse 2MRS table3.dat fixed-width selon ReadMe.

    Bytes (1-indexed) → Python slice (0-indexed):
       1-16   ID
      18-26   RAdeg
      28-36   DEdeg
      38-46   GLON
      48-56   GLAT
      58-63   Kcmag (extinction-corrected isophotal)
      79-84   Ktmag (extinction-corrected total extrapolated)
      100-104 e_Kcmag
      118-122 e_Ktmag
      136-140 E(B-V)
      174-178 cz (km/s)
      180-182 e_cz
    """
    rows = []
    with open(path, "r") as f:
        for line in f:
            if len(line) < 200:
                continue
            try:
                cz_s = line[173:178].strip()
                if not cz_s:
                    continue
                ktmag_s = line[78:84].strip()
                kcmag_s = line[57:63].strip()
                row = {
                    "ID": line[0:16].strip(),
                    "RAdeg": float(line[17:26].strip()),
                    "DEdeg": float(line[27:36].strip()),
                    "GLON": float(line[37:46].strip()),
                    "GLAT": float(line[47:56].strip()),
                    "Kcmag": float(kcmag_s) if kcmag_s else np.nan,
                    "Ktmag": float(ktmag_s) if ktmag_s else np.nan,
                    "e_Ktmag": float(line[117:122].strip()) if line[117:122].strip() else np.nan,
                    "EBV": float(line[135:140].strip()) if line[135:140].strip() else np.nan,
                    "cz_kms": int(cz_s),
                    "e_cz": int(line[179:182].strip()) if line[179:182].strip() else 0,
                }
                rows.append(row)
            except (ValueError, IndexError):
                continue
    return pd.DataFrame(rows)


def main():
    print(f"Loading {INPUT.name}...")
    df = parse_2mrs_table3(INPUT)
    print(f"  parsed {len(df)} galaxies")

    # Redshift adimensionné
    df["z"] = df["cz_kms"] / C_KMS

    # Distance modulus LCDM (cosmologie figée)
    cosmo = FlatLambdaCDM(H0=H0, Om0=OM0)
    df["DM_LCDM"] = cosmo.distmod(df["z"].clip(lower=1e-5)).value

    # Magnitude absolue apparente (= M_K si galaxie suit luminosité L*, sinon distribution)
    df["M_Kt_app"] = df["Ktmag"] - df["DM_LCDM"]

    # θ au DR
    df["theta_DR"] = angular_distance_deg(df["GLON"].to_numpy(), df["GLAT"].to_numpy(),
                                          L_DR_DEG, B_DR_DEG)

    # Diagnostics globaux
    print(f"\n--- Diagnostics globaux ---")
    print(f"GLON range: {df['GLON'].min():.1f}° to {df['GLON'].max():.1f}°")
    print(f"GLAT range: {df['GLAT'].min():.1f}° to {df['GLAT'].max():.1f}°")
    print(f"|b|<5° (zone d'évitement stricte): {(df['GLAT'].abs() < 5).sum():>6d} galaxies")
    print(f"|b|<10° (zone d'évitement large) : {(df['GLAT'].abs() < 10).sum():>6d} galaxies")
    print(f"hors plan (|b|>10°)              : {(df['GLAT'].abs() >= 10).sum():>6d} galaxies")
    print(f"\nKtmag range: {df['Ktmag'].min():.2f} to {df['Ktmag'].max():.2f}")
    print(f"cz range: {df['cz_kms'].min():>6d} to {df['cz_kms'].max():>6d} km/s")
    print(f"  → z range: {df['z'].min():.4f} to {df['z'].max():.4f}")
    print(f"  → 0.04<z<0.10: {((df['z'] > 0.04) & (df['z'] < 0.10)).sum()} galaxies")
    print(f"  → +cone θ<40°: {((df['z'] > 0.04) & (df['z'] < 0.10) & (df['theta_DR'] < 40)).sum()}")
    print(f"  → +Ktmag<11.5: {((df['z'] > 0.04) & (df['z'] < 0.10) & (df['theta_DR'] < 40) & (df['Ktmag'] < 11.5)).sum()}")
    print(f"  → +e_Ktmag<0.20: {((df['z'] > 0.04) & (df['z'] < 0.10) & (df['theta_DR'] < 40) & (df['Ktmag'] < 11.5) & (df['e_Ktmag'] < 0.20)).sum()}")

    # Sauvegarde
    df.to_csv(OUTPUT, index=False)
    print(f"\nSaved {len(df)} → {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
