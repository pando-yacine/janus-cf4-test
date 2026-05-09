"""
cf4_07_lcdm_subtract.py

Sprint 3 — soustraction du Vpec prédit par 2M++ (Carrick et al. 2015) via pvhub.
Pour chaque galaxie/groupe dans l'échantillon, on calcule:
    V_pec_residual = V_pec_observed - V_pec_LCDM_predicted

Le test χ² est ensuite refait sur les résidus. Si LCDM explique tout,
les résidus doivent être compatibles avec zéro dans tous les bins.
Si Janus apporte quelque chose en plus, il pourrait subsister un signal.

Note: pvhub utilise RA/DEC (pas galactique) et z_CMB (pas distance).
"""

import os
import sys
from pathlib import Path
import json
import warnings

import numpy as np
import pandas as pd
import scipy.stats

warnings.filterwarnings("ignore", category=SyntaxWarning)

# Ajouter pvhub au path
PVHUB_DIR = "/tmp/pvhub-repo"
if PVHUB_DIR not in sys.path:
    sys.path.insert(0, PVHUB_DIR)

import pvhub  # noqa: E402

# Constantes du protocole v2
L_DR_DEG = 305.0
B_DR_DEG = 5.0
BINS_DEG = [(0, 8), (8, 18), (18, 28), (28, 40)]
H0 = 70.0
C_KMS = 299792.458

ROOT = Path(__file__).resolve().parents[1]


def angular_distance_deg(l1, b1, l2, b2):
    l1r = np.deg2rad(l1)
    b1r = np.deg2rad(b1)
    l2r = np.deg2rad(l2)
    b2r = np.deg2rad(b2)
    cos_d = np.sin(b1r) * np.sin(b2r) + np.cos(b1r) * np.cos(b2r) * np.cos(l1r - l2r)
    return np.rad2deg(np.arccos(np.clip(cos_d, -1.0, 1.0)))


def select_around(df, l_center, b_center,
                  cone=40.0, dmin=50.0, dmax=350.0, max_edm=0.30, min_abs_b=3.0):
    theta = angular_distance_deg(df["GLON"].to_numpy(), df["GLAT"].to_numpy(), l_center, b_center)
    mask = (
        (theta < cone) &
        (df["Dist_Mpc"] > dmin) & (df["Dist_Mpc"] < dmax) &
        (df["e_DM"] < max_edm) &
        (df["GLAT"].abs() > min_abs_b)
    )
    sub = df[mask].copy()
    sub["theta"] = theta[mask]
    return sub


def add_vpec_lcdm(df, recon):
    """Ajoute la colonne Vpec_LCDM en utilisant pvhub."""
    z_cmb = df["Vcmb"].to_numpy() / C_KMS
    pv = recon.calculate_pv(df["RAdeg"].to_numpy(), df["DEdeg"].to_numpy(), z_cmb)
    df["Vpec_LCDM"] = pv
    df["Vpec_residual"] = df["Vpec_calc"] - df["Vpec_LCDM"]
    return df


def vpec_by_bin(sub, col="Vpec_residual"):
    results = []
    for lo, hi in BINS_DEG:
        m = (sub["theta"] >= lo) & (sub["theta"] < hi) & sub[col].notna()
        sl = sub[m]
        n = len(sl)
        if n >= 2:
            mean = sl[col].mean()
            err = sl[col].std(ddof=1) / np.sqrt(n)
        elif n == 1:
            mean = float(sl[col].iloc[0])
            err = 1000.0
        else:
            mean = np.nan
            err = np.nan
        results.append({"lo": lo, "hi": hi, "n": int(n), "mean": float(mean) if not np.isnan(mean) else None, "err": float(err) if not np.isnan(err) else None})
    return results


def chi_square(dr_results, ctrl_means, ctrl_errs):
    chi2 = 0.0
    df_used = 0
    for i, r in enumerate(dr_results):
        if r["n"] < 2 or r["mean"] is None:
            continue
        delta = r["mean"] - ctrl_means[i]
        var = (r["err"] or 0.0) ** 2 + ctrl_errs[i] ** 2
        if var > 0:
            chi2 += (delta ** 2) / var
            df_used += 1
    return chi2, df_used


def generate_control_positions(seed=42, n=8):
    rng = np.random.default_rng(seed)
    L_ANTI = (L_DR_DEG + 180) % 360
    B_ANTI = -B_DR_DEG
    positions = []
    while len(positions) < n:
        l_rand = rng.uniform(0, 360)
        b_rand = np.rad2deg(np.arcsin(rng.uniform(-1, 1)))
        if abs(b_rand) < 20: continue
        if angular_distance_deg(l_rand, b_rand, L_DR_DEG, B_DR_DEG) < 60: continue
        if angular_distance_deg(l_rand, b_rand, L_ANTI, B_ANTI) < 60: continue
        positions.append((l_rand, b_rand))
    return positions


def main():
    print("=== Sprint 3 — Test sur résidus Vpec - VLCDM ===\n")

    # Charger table2 (galaxies individuelles)
    df = pd.read_csv(ROOT / "data" / "cf4_table2_individuals.csv")
    print(f"Loaded {len(df)} galaxies from table2")

    # Charger pvhub
    print("Loading 2M++ SDSS reconstruction (Carrick 2015)...")
    recon = pvhub.TwoMPP_SDSS()

    # Calculer Vpec LCDM pour TOUTES les galaxies
    print("Computing Vpec_LCDM for all 55877 galaxies...")
    df = add_vpec_lcdm(df, recon)
    print(f"  Vpec_LCDM range: {df['Vpec_LCDM'].min():.0f} to {df['Vpec_LCDM'].max():.0f} km/s")
    print(f"  Vpec_residual range: {df['Vpec_residual'].min():.0f} to {df['Vpec_residual'].max():.0f} km/s")

    # 1. Région DR
    print(f"\n--- Région DR (l={L_DR_DEG}, b={B_DR_DEG}) ---")
    dr = select_around(df, L_DR_DEG, B_DR_DEG)
    print(f"Sample DR: {len(dr)} galaxies")
    dr_bins = vpec_by_bin(dr, col="Vpec_residual")
    print(f"\n{'Bin':<12s} {'N':>5s} {'mean residual':>16s} {'err':>10s}")
    for r in dr_bins:
        n_str = str(r["n"])
        m_str = f"{r['mean']:.0f} km/s" if r["mean"] is not None else "—"
        e_str = f"±{r['err']:.0f}" if r["err"] is not None else "—"
        print(f"  [{r['lo']:>2d}°,{r['hi']:>2d}°) {n_str:>5s} {m_str:>16s} {e_str:>10s}")

    # 2. Régions de contrôle
    print(f"\n--- 8 contrôles ---")
    controls = generate_control_positions()
    ctrl_per_bin = [[] for _ in BINS_DEG]
    for j, (lc, bc) in enumerate(controls):
        sub = select_around(df, lc, bc)
        bins = vpec_by_bin(sub, col="Vpec_residual")
        n = len(sub)
        print(f"  Ctrl {j}: ({lc:5.1f}, {bc:+5.1f}) N={n}")
        for i, r in enumerate(bins):
            if r["n"] >= 2:
                ctrl_per_bin[i].append(r["mean"])

    ctrl_means = []
    ctrl_errs = []
    for vals in ctrl_per_bin:
        if len(vals) >= 2:
            ctrl_means.append(float(np.mean(vals)))
            ctrl_errs.append(float(np.std(vals, ddof=1) / np.sqrt(len(vals))))
        else:
            ctrl_means.append(0.0)
            ctrl_errs.append(1000.0)

    # 3. Test principal
    print(f"\n--- Test principal sur résidus ---")
    print(f"{'Bin':<12s} {'DR mean':>12s} {'Ctrl mean':>12s} {'ΔVpec_res':>12s}")
    for i, r in enumerate(dr_bins):
        if r["mean"] is not None:
            delta = r["mean"] - ctrl_means[i]
            print(f"  [{r['lo']:>2d}°,{r['hi']:>2d}°) {r['mean']:>10.0f} {ctrl_means[i]:>10.0f} {delta:>+12.0f}")

    chi2, df_used = chi_square(dr_bins, ctrl_means, ctrl_errs)
    if df_used > 0:
        pvalue = 1 - scipy.stats.chi2.cdf(chi2, df=df_used)
        print(f"\nχ² (résidus) = {chi2:.2f}, df = {df_used}, p = {pvalue:.4f}")
        if pvalue < 0.01:
            verdict = "signal_residual_significatif"
        elif pvalue < 0.05:
            verdict = "suggestif"
        else:
            verdict = "non_discriminant_apres_LCDM"
        print(f"Verdict (sur résidus): {verdict}")
    else:
        chi2 = np.nan
        pvalue = np.nan
        verdict = "test_impossible"

    # 4. Antipode (Shapley)
    L_ANTI = (L_DR_DEG + 180) % 360
    B_ANTI = -B_DR_DEG
    print(f"\n--- Antipode (Shapley): ({L_ANTI}, {B_ANTI}) ---")
    sub_anti = select_around(df, L_ANTI, B_ANTI)
    bins_anti = vpec_by_bin(sub_anti, col="Vpec_residual")
    print(f"Sample antipode: {len(sub_anti)} galaxies")
    print(f"{'Bin':<12s} {'N':>5s} {'mean residual':>16s}")
    for r in bins_anti:
        m_str = f"{r['mean']:.0f} km/s" if r["mean"] is not None else "—"
        print(f"  [{r['lo']:>2d}°,{r['hi']:>2d}°) {r['n']:>5d} {m_str:>16s}")
    chi2_anti, df_anti = chi_square(bins_anti, ctrl_means, ctrl_errs)
    p_anti = 1 - scipy.stats.chi2.cdf(chi2_anti, df=df_anti) if df_anti > 0 else np.nan

    # 5. Sauvegarde
    results = {
        "protocol_version": "v2.0_extension_sprint3",
        "test_type": "residuals after 2M++ LCDM subtraction",
        "lcdm_model": "TwoMPP_SDSS (Carrick et al. 2015 / Said et al. 2020)",
        "dr_position": {"l": L_DR_DEG, "b": B_DR_DEG},
        "n_dr_total": int(len(dr)),
        "n_anti_total": int(len(sub_anti)),
        "bins_dr_residual": dr_bins,
        "bins_anti_residual": bins_anti,
        "ctrl_means": ctrl_means,
        "ctrl_errs": ctrl_errs,
        "chi2_dr_residual": float(chi2) if not np.isnan(chi2) else None,
        "chi2_anti_residual": float(chi2_anti) if not np.isnan(chi2_anti) else None,
        "df_used": df_used,
        "pvalue_dr": float(pvalue) if not np.isnan(pvalue) else None,
        "pvalue_anti": float(p_anti) if not np.isnan(p_anti) else None,
        "verdict": verdict,
    }
    out = ROOT / "results_sprint3_residuals.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved → {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
