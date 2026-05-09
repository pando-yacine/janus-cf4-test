"""
twomrs_03_validation.py

Sprint 4 — placebo (100 positions) + antipode + robustesse pour le test 2MRS.
"""

from pathlib import Path
import json
import numpy as np
import pandas as pd
import scipy.stats

from twomrs_02_analysis import (
    L_DR_DEG, B_DR_DEG, BINS_DEG, CONE_DEG, CONTROL_SEED, N_CONTROL,
    angular_distance_deg, select_around, median_M_per_bin, count_per_bin,
    chi_square_A, chi_square_B, generate_control_positions,
    KT_LIM_COUNT,
)

ROOT = Path(__file__).resolve().parents[1]


def main():
    print("=== Sprint 4 — Validation 2MRS ===\n")
    df = pd.read_csv(ROOT / "data" / "2mrs_with_galactic.csv")

    # Recalculer contrôles
    print("Contrôles...")
    controls = generate_control_positions()
    A_per_bin = [[] for _ in BINS_DEG]
    B_per_bin = [[] for _ in BINS_DEG]
    for lc, bc in controls:
        sub = select_around(df, lc, bc)
        for i, r in enumerate(median_M_per_bin(sub)):
            if r["n"] >= 5 and r["median"] is not None:
                A_per_bin[i].append(r["median"])
        for i, r in enumerate(count_per_bin(sub)):
            B_per_bin[i].append(r["n"])
    A_means = [float(np.mean(v)) if len(v) >= 2 else 0.0 for v in A_per_bin]
    A_errs = [float(np.std(v, ddof=1)/np.sqrt(len(v))) if len(v) >= 2 else 1.0 for v in A_per_bin]
    B_means = [float(np.mean(v)) for v in B_per_bin]

    # χ² du DR
    dr = select_around(df, L_DR_DEG, B_DR_DEG)
    dr_A = median_M_per_bin(dr)
    dr_B = count_per_bin(dr)
    chi2_A_dr, df_A_dr = chi_square_A(dr_A, A_means, A_errs)
    chi2_B_dr, df_B_dr = chi_square_B(dr_B, B_means)
    print(f"DR: χ²_A = {chi2_A_dr:.2f}, χ²_B = {chi2_B_dr:.2f}")

    # === Test 1: Placebo 100 positions ===
    print("\n--- Placebo 100 positions ---")
    rng = np.random.default_rng(seed=12345)
    L_ANTI = (L_DR_DEG + 180) % 360
    B_ANTI = -B_DR_DEG
    placebo_chi2_A = []
    placebo_chi2_B = []
    n_attempts = 0
    while (len(placebo_chi2_A) < 100 or len(placebo_chi2_B) < 100) and n_attempts < 1500:
        n_attempts += 1
        l_rand = rng.uniform(0, 360)
        b_rand = np.rad2deg(np.arcsin(rng.uniform(-1, 1)))
        if abs(b_rand) < 10: continue
        if angular_distance_deg(l_rand, b_rand, L_DR_DEG, B_DR_DEG) < 50: continue
        if angular_distance_deg(l_rand, b_rand, L_ANTI, B_ANTI) < 50: continue
        sub = select_around(df, l_rand, b_rand)
        if len(sub) < 50: continue
        a_bins = median_M_per_bin(sub)
        b_bins = count_per_bin(sub)
        chi2_A, _ = chi_square_A(a_bins, A_means, A_errs)
        chi2_B, _ = chi_square_B(b_bins, B_means)
        if not np.isnan(chi2_A):
            placebo_chi2_A.append(chi2_A)
        if not np.isnan(chi2_B):
            placebo_chi2_B.append(chi2_B)

    placebo_chi2_A = np.array(placebo_chi2_A)
    placebo_chi2_B = np.array(placebo_chi2_B)
    pct_A = (placebo_chi2_A > chi2_A_dr).sum() / len(placebo_chi2_A) * 100
    pct_B = (placebo_chi2_B > chi2_B_dr).sum() / len(placebo_chi2_B) * 100
    print(f"Tirages: {len(placebo_chi2_A)} (A), {len(placebo_chi2_B)} (B)")
    print(f"Observable A: DR top {pct_A:.1f}% — median placebo χ² = {np.median(placebo_chi2_A):.2f}")
    print(f"Observable B: DR top {pct_B:.1f}% — median placebo χ² = {np.median(placebo_chi2_B):.2f}")

    # === Test 2: Antipode ===
    print(f"\n--- Antipode (l={L_ANTI}, b={B_ANTI}) ---")
    sub_anti = select_around(df, L_ANTI, B_ANTI)
    print(f"Sample antipode: {len(sub_anti)} galaxies")
    anti_A = median_M_per_bin(sub_anti)
    anti_B = count_per_bin(sub_anti)
    chi2_A_anti, df_A_anti = chi_square_A(anti_A, A_means, A_errs)
    chi2_B_anti, df_B_anti = chi_square_B(anti_B, B_means)
    p_A_anti = 1 - scipy.stats.chi2.cdf(chi2_A_anti, df=df_A_anti) if df_A_anti > 0 else np.nan
    p_B_anti = 1 - scipy.stats.chi2.cdf(chi2_B_anti, df=df_B_anti) if df_B_anti > 0 else np.nan
    print(f"χ²_A antipode = {chi2_A_anti:.2f} (df={df_A_anti}, p={p_A_anti:.4f})")
    print(f"χ²_B antipode = {chi2_B_anti:.2f} (df={df_B_anti}, p={p_B_anti:.4f})")

    # Détails antipode
    print(f"\n{'Bin':<12s} {'DR ΔM':>10s} {'Anti ΔM':>10s} {'DR Δcount':>12s} {'Anti Δcount':>13s}")
    for i, lo_hi in enumerate(BINS_DEG):
        lo, hi = lo_hi
        dr_dm = (dr_A[i]["median"] - A_means[i]) if dr_A[i]["median"] is not None else None
        anti_dm = (anti_A[i]["median"] - A_means[i]) if anti_A[i]["median"] is not None else None
        dr_dc = dr_B[i]["n"] - B_means[i]
        anti_dc = anti_B[i]["n"] - B_means[i]
        s1 = f"{dr_dm:+.3f}" if dr_dm is not None else "—"
        s2 = f"{anti_dm:+.3f}" if anti_dm is not None else "—"
        print(f"  [{lo:>2d}°,{hi:>2d}°) {s1:>10s} {s2:>10s} {dr_dc:>+12.1f} {anti_dc:>+13.1f}")

    # === Test 3: Robustesse ±20% sur les bins ===
    print(f"\n--- Robustesse bins ±20% ---")
    BINS_PLUS = [(0, 10), (10, 22), (22, 34), (34, 40)]
    BINS_MINUS = [(0, 6), (6, 14), (14, 22), (22, 40)]

    def test_with_bins(bins_def):
        # DR
        dr_a = []
        dr_b_counts = []
        for lo, hi in bins_def:
            m = (dr["theta"] >= lo) & (dr["theta"] < hi) & dr["M_Kt_app"].notna()
            sl = dr[m]
            n = len(sl)
            if n >= 2:
                med = float(sl["M_Kt_app"].median())
                rng2 = np.random.default_rng(seed=hash((lo, hi, n)) % (2**31))
                boots = [np.median(sl["M_Kt_app"].iloc[rng2.integers(0, n, size=n)]) for _ in range(500)]
                err = float(np.std(boots, ddof=1))
            else:
                med, err = (None, None)
            dr_a.append({"n": n, "median": med, "err": err})
            n_count = ((dr["theta"] >= lo) & (dr["theta"] < hi) & (dr["Ktmag"] < KT_LIM_COUNT)).sum()
            dr_b_counts.append({"n": int(n_count)})
        # Contrôles
        ctrl_A = [[] for _ in bins_def]
        ctrl_B = [[] for _ in bins_def]
        for lc, bc in controls:
            sub = select_around(df, lc, bc)
            for i, (lo, hi) in enumerate(bins_def):
                m = (sub["theta"] >= lo) & (sub["theta"] < hi) & sub["M_Kt_app"].notna()
                sl = sub[m]
                if len(sl) >= 5:
                    ctrl_A[i].append(float(sl["M_Kt_app"].median()))
                ctrl_B[i].append(int(((sub["theta"] >= lo) & (sub["theta"] < hi) & (sub["Ktmag"] < KT_LIM_COUNT)).sum()))
        cA_means = [np.mean(v) if len(v) >= 2 else 0.0 for v in ctrl_A]
        cA_errs = [np.std(v, ddof=1)/np.sqrt(len(v)) if len(v) >= 2 else 1.0 for v in ctrl_A]
        cB_means = [np.mean(v) for v in ctrl_B]
        # χ²
        c2A = sum(((r["median"] - cA_means[i])**2)/((r["err"] or 0)**2 + cA_errs[i]**2)
                  for i, r in enumerate(dr_a) if r["median"] is not None)
        c2B = sum(((r["n"] - cB_means[i])**2)/cB_means[i]
                  for i, r in enumerate(dr_b_counts) if cB_means[i] > 0 and r["n"] >= 1)
        return c2A, c2B

    for label, bins_alt in [("bins +20%", BINS_PLUS), ("bins -20%", BINS_MINUS)]:
        c2A, c2B = test_with_bins(bins_alt)
        print(f"  {label}: χ²_A = {c2A:.2f}, χ²_B = {c2B:.2f}")

    # Sauvegarde
    results = {
        "placebo": {
            "n_trials_A": int(len(placebo_chi2_A)),
            "n_trials_B": int(len(placebo_chi2_B)),
            "chi2_A_dr": float(chi2_A_dr),
            "chi2_B_dr": float(chi2_B_dr),
            "median_placebo_A": float(np.median(placebo_chi2_A)),
            "median_placebo_B": float(np.median(placebo_chi2_B)),
            "max_placebo_A": float(placebo_chi2_A.max()),
            "max_placebo_B": float(placebo_chi2_B.max()),
            "percentile_dr_A": float(pct_A),
            "percentile_dr_B": float(pct_B),
        },
        "antipode": {
            "position": {"l": float(L_ANTI), "b": float(B_ANTI)},
            "n_galaxies": int(len(sub_anti)),
            "chi2_A": float(chi2_A_anti),
            "chi2_B": float(chi2_B_anti),
            "pvalue_A": float(p_A_anti) if not np.isnan(p_A_anti) else None,
            "pvalue_B": float(p_B_anti) if not np.isnan(p_B_anti) else None,
            "delta_M_per_bin": [(anti_A[i]["median"] - A_means[i]) if anti_A[i]["median"] is not None else None
                                 for i in range(len(BINS_DEG))],
            "delta_count_per_bin": [int(anti_B[i]["n"] - B_means[i]) for i in range(len(BINS_DEG))],
        },
    }
    out = ROOT / "results_v3_validation.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2, default=float)
    print(f"\nSaved → {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
