"""
02_diagnose_sample.py

Diagnostique pourquoi l'échantillon principal est si petit.
Inspecte la distribution des SN-Ia autour du Dipole Repeller.
"""

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data" / "pantheon_with_galactic.csv")

print(f"=== Pantheon+ : {len(df)} SN au total ===\n")

# 1. Distribution angulaire au DR
print("Distribution de θ_DR (distance angulaire au Dipole Repeller) :")
bins = [0, 10, 20, 30, 40, 50, 60, 90, 180]
hist, edges = np.histogram(df["theta_DR"], bins=bins)
for lo, hi, n in zip(edges[:-1], edges[1:], hist):
    bar = "█" * int(n / 10)
    print(f"  [{lo:>3.0f}°, {hi:>3.0f}°): {n:>4d}  {bar}")

# 2. Distribution en redshift
print("\nDistribution en zCMB :")
zbins = [0, 0.01, 0.05, 0.10, 0.15, 0.30, 0.50, 1.0, 3.0]
zhist, zedges = np.histogram(df["zCMB"], bins=zbins)
for lo, hi, n in zip(zedges[:-1], zedges[1:], zhist):
    bar = "█" * int(n / 30)
    print(f"  [{lo:.3f}, {hi:.3f}): {n:>4d}  {bar}")

# 3. SN les plus proches du DR
print("\n10 SN les plus proches du Dipole Repeller :")
closest = df.nsmallest(10, "theta_DR")[["CID", "l_gal", "b_gal", "theta_DR", "zCMB", "m_b_corr_err_DIAG"]]
print(closest.to_string(index=False))

# 4. Test élargi : cône plus large
print("\n=== Test exploratoire : effet d'élargir les coupes ===")
configs = [
    ("PROTOCOLE FIGÉ", (df["theta_DR"] < 30) & (df["zCMB"] > 0.05) & (df["zCMB"] < 0.15) & (df["m_b_corr_err_DIAG"] < 0.20)),
    ("Cône 40°", (df["theta_DR"] < 40) & (df["zCMB"] > 0.05) & (df["zCMB"] < 0.15) & (df["m_b_corr_err_DIAG"] < 0.20)),
    ("Cône 50°", (df["theta_DR"] < 50) & (df["zCMB"] > 0.05) & (df["zCMB"] < 0.15) & (df["m_b_corr_err_DIAG"] < 0.20)),
    ("Cône 60°", (df["theta_DR"] < 60) & (df["zCMB"] > 0.05) & (df["zCMB"] < 0.15) & (df["m_b_corr_err_DIAG"] < 0.20)),
    ("z élargi 0.03-0.20, cône 30°", (df["theta_DR"] < 30) & (df["zCMB"] > 0.03) & (df["zCMB"] < 0.20) & (df["m_b_corr_err_DIAG"] < 0.20)),
    ("z élargi 0.02-0.30, cône 60°", (df["theta_DR"] < 60) & (df["zCMB"] > 0.02) & (df["zCMB"] < 0.30) & (df["m_b_corr_err_DIAG"] < 0.20)),
    ("Sans filtre qualité, cône 30°", (df["theta_DR"] < 30) & (df["zCMB"] > 0.05) & (df["zCMB"] < 0.15)),
]

print(f"\n{'Configuration':<40s} {'N':>5s}")
print("-" * 50)
for name, mask in configs:
    print(f"{name:<40s} {mask.sum():>5d}")

# 5. Distribution sur tout le ciel pour voir où est concentré Pantheon+
print("\n=== Pour comparaison : distribution de Pantheon+ sur le ciel galactique ===")
print("Lat. galactique |b| <  5° (plan galactique stricto sensu) : ", (np.abs(df["b_gal"]) < 5).sum(), "SN")
print("Lat. galactique |b| < 10° (zone d'évitement classique)    : ", (np.abs(df["b_gal"]) < 10).sum(), "SN")
print("Lat. galactique |b| > 30° (hors plan galactique)          : ", (np.abs(df["b_gal"]) > 30).sum(), "SN")
print("DR à b=+5°, donc dans zone d'évitement partielle.")
