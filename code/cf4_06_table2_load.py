"""
cf4_06_table2_load.py

Sprint 3 — extension à table2 (55877 galaxies individuelles) pour combler caveat 3.
Note: table2 ne contient PAS Vpec directement (contrairement à table4).
On doit calculer Vpec à partir de DM (distance modulus) et zCMB.

table2 fields (selon ReadMe):
  PGC, 1PGC, T17, Vcmb, DM, e_DM, [DM par méthode], RA, DEC, GLON, GLAT, SGL, SGB

Note structurelle: Vpec n'est pas explicitement dans table2 (qui se concentre sur DM individuel).
On le calcule: Vpec = c*z_cmb - H0*d_lum, où d_lum = 10^((DM-25)/5) Mpc.
"""

from pathlib import Path
import numpy as np
import pandas as pd

L_DR_DEG = 305.0
B_DR_DEG = 5.0
H0 = 70.0  # km/s/Mpc, identique au protocole v2

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "cosmicflows-4" / "table2.dat"
OUTPUT = ROOT / "data" / "cf4_table2_individuals.csv"


def angular_distance_deg(l1, b1, l2, b2):
    l1r = np.deg2rad(l1)
    b1r = np.deg2rad(b1)
    l2r = np.deg2rad(l2)
    b2r = np.deg2rad(b2)
    cos_d = np.sin(b1r) * np.sin(b2r) + np.cos(b1r) * np.cos(b2r) * np.cos(l1r - l2r)
    return np.rad2deg(np.arccos(np.clip(cos_d, -1.0, 1.0)))


def parse_table2(path):
    """Parse table2.dat fixed-width selon ReadMe.

    Bytes (1-indexed) → Python slice (0-indexed):
      1-7   PGC
      9-15  1PGC (group dominant)
      17-21 T17 (Tempel id)
      23-27 Vcmb (km/s)
      29-34 DM (mag)
      36-40 e_DM
      42-47 DMsnIa
      ... (méthodes)
      138-145 RAdeg
      147-154 DEdeg
      156-163 GLON
      165-172 GLAT
      174-181 SGL
      183-190 SGB
    """
    rows = []
    with open(path, "r") as f:
        for line in f:
            try:
                vcmb_s = line[22:27].strip()
                dm_s = line[28:34].strip()
                edm_s = line[35:40].strip()
                if not (dm_s and edm_s):
                    continue
                row = {
                    "PGC": int(line[0:7].strip()),
                    "Vcmb": int(vcmb_s) if vcmb_s else np.nan,
                    "DM": float(dm_s),
                    "e_DM": float(edm_s),
                    "RAdeg": float(line[137:145].strip()),
                    "DEdeg": float(line[146:154].strip()),
                    "GLON": float(line[155:163].strip()),
                    "GLAT": float(line[164:172].strip()),
                    "SGL": float(line[173:181].strip()),
                    "SGB": float(line[182:190].strip()),
                }
                rows.append(row)
            except (ValueError, IndexError):
                continue
    return pd.DataFrame(rows)


def main():
    print(f"Loading {INPUT.name}...")
    df = parse_table2(INPUT)
    print(f"  parsed {len(df)} galaxies")

    # Distance luminosity (Mpc) à partir de DM
    df["Dist_Mpc"] = 10 ** ((df["DM"] - 25) / 5)

    # Vpec = c*z - H0*d (approximation au premier ordre pour z<<1)
    # Vcmb est en km/s (= c*z_cmb)
    df["Vpec_calc"] = df["Vcmb"] - H0 * df["Dist_Mpc"]

    # θ au DR
    df["theta_DR"] = angular_distance_deg(df["GLON"].to_numpy(), df["GLAT"].to_numpy(),
                                          L_DR_DEG, B_DR_DEG)

    print(f"\nDistance range: {df['Dist_Mpc'].min():.1f} to {df['Dist_Mpc'].max():.1f} Mpc")
    print(f"Vpec_calc range: {df['Vpec_calc'].min():.0f} to {df['Vpec_calc'].max():.0f} km/s")
    print(f"e_DM median: {df['e_DM'].median():.3f}")

    df.to_csv(OUTPUT, index=False)
    print(f"\nSaved {len(df)} galaxies → {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
