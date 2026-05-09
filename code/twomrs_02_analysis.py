"""
twomrs_02_analysis.py

Sprint 4 — analyse principale photométrique 2MRS selon protocole v3 (commit bcdc0e1).

Deux observables figées:
  A) Médiane M_Kt_app par bin angulaire
  B) Comptage à magnitude limite Kt<11.0 par bin angulaire

Pour chacun: comparaison DR vs 8 régions de contrôle, χ², placebo, antipode.
"""

from pathlib import Path
import json
import numpy as np
import pandas as pd
import scipy.stats

# Constantes figées par protocole v3
L_DR_DEG = 305.0
B_DR_DEG = 5.0
BINS_DEG = [(0, 8), (8, 18), (18, 28), (28, 40)]
CONE_DEG = 40.0
Z_MIN, Z_MAX = 0.04, 0.10
KT_MAX = 11.5  # main sample
KT_LIM_COUNT = 11.0  # for counting test
E_KT_MAX = 0.20
ABS_B_MIN = 5.0
CONTROL_SEED = 42
N_CONTROL = 8

ROOT = Path(__file__).resolve().parents[1]


def angular_distance_deg(l1, b1, l2, b2):
    l1r = np.deg2rad(l1)
    b1r = np.deg2rad(b1)
    l2r = np.deg2rad(l2)
    b2r = np.deg2rad(b2)
    cos_d = np.sin(b1r) * np.sin(b2r) + np.cos(b1r) * np.cos(b2r) * np.cos(l1r - l2r)
    return np.rad2deg(np.arccos(np.clip(cos_d, -1.0, 1.0)))


def select_around(df, l_center, b_center,
                  cone=CONE_DEG, z_min=Z_MIN, z_max=Z_MAX,
                  kt_max=KT_MAX, e_kt_max=E_KT_MAX, min_abs_b=ABS_B_MIN):
    theta = angular_distance_deg(df["GLON"].to_numpy(), df["GLAT"].to_numpy(), l_center, b_center)
    mask = (
        (theta < cone) &
        (df["z"] > z_min) & (df["z"] < z_max) &
        (df["Ktmag"] <= kt_max) &
        (df["e_Ktmag"] < e_kt_max) &
        (df["GLAT"].abs() > min_abs_b)
    )
    sub = df[mask].copy()
    sub["theta"] = theta[mask]
    return sub


def median_M_per_bin(sub):
    """Observable A: médiane de M_Kt_app par bin avec err par bootstrap."""
    results = []
    for lo, hi in BINS_DEG:
        m = (sub["theta"] >= lo) & (sub["theta"] < hi) & sub["M_Kt_app"].notna()
        sl = sub[m]
        n = len(sl)
        if n >= 2:
            median = float(sl["M_Kt_app"].median())
            # Bootstrap error (1000 iterations)
            rng = np.random.default_rng(seed=hash((lo, hi, n)) % (2**31))
            boot_medians = []
            for _ in range(1000):
                idx = rng.integers(0, n, size=n)
                boot_medians.append(np.median(sl["M_Kt_app"].iloc[idx]))
            err = float(np.std(boot_medians, ddof=1))
        elif n == 1:
            median = float(sl["M_Kt_app"].iloc[0])
            err = 1.0
        else:
            median = np.nan
            err = np.nan
        results.append({"lo": lo, "hi": hi, "n": int(n),
                        "median": float(median) if not np.isnan(median) else None,
                        "err": float(err) if not np.isnan(err) else None})
    return results


def count_per_bin(sub, kt_lim=KT_LIM_COUNT):
    """Observable B: comptage de galaxies avec Kt<kt_lim par bin angulaire."""
    results = []
    for lo, hi in BINS_DEG:
        m = (sub["theta"] >= lo) & (sub["theta"] < hi) & (sub["Ktmag"] < kt_lim)
        n = int(m.sum())
        # Surface du bin (sphère: dΩ = 2π(cos(θ_lo) - cos(θ_hi)))
        area = 2*np.pi*(np.cos(np.deg2rad(lo)) - np.cos(np.deg2rad(hi)))
        results.append({"lo": lo, "hi": hi, "n": n, "area_sr": float(area)})
    return results


def chi_square_A(dr_results, ctrl_means, ctrl_errs):
    chi2 = 0.0
    df_used = 0
    for i, r in enumerate(dr_results):
        if r["n"] < 2 or r["median"] is None:
            continue
        delta = r["median"] - ctrl_means[i]
        var = (r["err"] or 0.0) ** 2 + ctrl_errs[i] ** 2
        if var > 0:
            chi2 += (delta ** 2) / var
            df_used += 1
    return chi2, df_used


def chi_square_B(dr_counts, ctrl_means_counts):
    """Test χ² Poisson pour comptage."""
    chi2 = 0.0
    df_used = 0
    for i, r in enumerate(dr_counts):
        if r["n"] >= 1 and ctrl_means_counts[i] > 0:
            delta = r["n"] - ctrl_means_counts[i]
            var = ctrl_means_counts[i]  # Poisson: variance ≈ moyenne
            chi2 += (delta ** 2) / var
            df_used += 1
    return chi2, df_used


def generate_control_positions(seed=CONTROL_SEED, n=N_CONTROL):
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
    print("=== Sprint 4 — Test photométrique 2MRS ===\n")
    df = pd.read_csv(ROOT / "data" / "2mrs_with_galactic.csv")
    print(f"2MRS chargé: {len(df)} galaxies")

    # Région DR
    print(f"\n--- Région DR (l={L_DR_DEG}, b={B_DR_DEG}) ---")
    dr = select_around(df, L_DR_DEG, B_DR_DEG)
    print(f"Sample DR: {len(dr)} galaxies")

    # Observable A: médiane M_Kt_app par bin
    dr_A = median_M_per_bin(dr)
    print(f"\nObservable A — Médiane M_Kt_app par bin:")
    print(f"{'Bin':<12s} {'N':>5s} {'median M':>12s} {'err':>10s}")
    for r in dr_A:
        n_str = str(r["n"])
        m_str = f"{r['median']:.3f}" if r["median"] is not None else "—"
        e_str = f"±{r['err']:.3f}" if r["err"] is not None else "—"
        print(f"  [{r['lo']:>2d}°,{r['hi']:>2d}°) {n_str:>5s} {m_str:>12s} {e_str:>10s}")

    # Observable B: comptage Kt<11.0
    dr_B = count_per_bin(dr)
    print(f"\nObservable B — Comptage Kt<{KT_LIM_COUNT}:")
    print(f"{'Bin':<12s} {'N':>5s} {'Density (gal/sr)':>18s}")
    for r in dr_B:
        density = r["n"] / r["area_sr"] if r["area_sr"] > 0 else 0
        print(f"  [{r['lo']:>2d}°,{r['hi']:>2d}°) {r['n']:>5d} {density:>18.0f}")

    # Régions de contrôle
    print(f"\n--- 8 régions de contrôle (seed=42) ---")
    controls = generate_control_positions()
    A_per_bin = [[] for _ in BINS_DEG]
    B_per_bin = [[] for _ in BINS_DEG]
    for j, (lc, bc) in enumerate(controls):
        sub = select_around(df, lc, bc)
        a_bins = median_M_per_bin(sub)
        b_bins = count_per_bin(sub)
        print(f"  Ctrl {j}: ({lc:5.1f}, {bc:+5.1f}) N={len(sub)} (Kt<{KT_LIM_COUNT}: {sum(b['n'] for b in b_bins)})")
        for i, r in enumerate(a_bins):
            if r["n"] >= 5 and r["median"] is not None:
                A_per_bin[i].append(r["median"])
        for i, r in enumerate(b_bins):
            B_per_bin[i].append(r["n"])

    # Stats contrôles
    A_means = []
    A_errs = []
    for vals in A_per_bin:
        if len(vals) >= 2:
            A_means.append(float(np.mean(vals)))
            A_errs.append(float(np.std(vals, ddof=1) / np.sqrt(len(vals))))
        else:
            A_means.append(0.0)
            A_errs.append(1.0)
    B_means = [float(np.mean(vals)) if len(vals) >= 1 else 0.0 for vals in B_per_bin]

    # Test A χ²
    print(f"\n--- Test A: ΔM_Kt_app(DR) vs <M_Kt_app>(contrôles) ---")
    print(f"{'Bin':<12s} {'DR':>10s} {'Ctrl':>10s} {'ΔM':>10s}")
    for i, r in enumerate(dr_A):
        if r["median"] is not None:
            d = r["median"] - A_means[i]
            print(f"  [{r['lo']:>2d}°,{r['hi']:>2d}°) {r['median']:>10.3f} {A_means[i]:>10.3f} {d:>+10.3f}")

    chi2_A, df_A = chi_square_A(dr_A, A_means, A_errs)
    p_A = 1 - scipy.stats.chi2.cdf(chi2_A, df=df_A) if df_A > 0 else np.nan
    print(f"\nχ²_A = {chi2_A:.2f}, df = {df_A}, p = {p_A:.4f}")

    # Test B χ² Poisson
    print(f"\n--- Test B: comptage DR vs <comptage>(contrôles) ---")
    print(f"{'Bin':<12s} {'DR':>6s} {'Ctrl':>10s} {'Δ':>10s}")
    for i, r in enumerate(dr_B):
        d = r["n"] - B_means[i]
        print(f"  [{r['lo']:>2d}°,{r['hi']:>2d}°) {r['n']:>6d} {B_means[i]:>10.1f} {d:>+10.1f}")

    chi2_B, df_B = chi_square_B(dr_B, B_means)
    p_B = 1 - scipy.stats.chi2.cdf(chi2_B, df=df_B) if df_B > 0 else np.nan
    print(f"\nχ²_B = {chi2_B:.2f}, df = {df_B}, p = {p_B:.4f}")

    # Verdict combiné
    if p_A < 0.01 or p_B < 0.01:
        verdict = "signal_significatif"
    elif p_A < 0.05 or p_B < 0.05:
        verdict = "suggestif"
    else:
        verdict = "non_discriminant"
    print(f"\nVerdict combiné: {verdict}")

    # Sauvegarde
    results = {
        "protocol_version": "v3.0",
        "protocol_commit": "bcdc0e176b0fdc0c8b79220c9d55ade595b79be7",
        "test": "2MRS K-band photometric",
        "n_dr_total": int(len(dr)),
        "observable_A": {
            "name": "median M_Kt_app per bin",
            "dr_bins": dr_A,
            "ctrl_means": A_means,
            "ctrl_errs": A_errs,
            "chi2": float(chi2_A),
            "df": int(df_A),
            "pvalue": float(p_A) if not np.isnan(p_A) else None,
        },
        "observable_B": {
            "name": f"galaxy count Kt<{KT_LIM_COUNT}",
            "dr_bins": dr_B,
            "ctrl_means": B_means,
            "chi2": float(chi2_B),
            "df": int(df_B),
            "pvalue": float(p_B) if not np.isnan(p_B) else None,
        },
        "verdict": verdict,
    }
    out = ROOT / "results_v3_main.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved → {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
