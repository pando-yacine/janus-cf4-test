"""
cf4_04_placebo.py

Test placebo : refait l'analyse à 100 positions aléatoires sur le ciel,
compare la distribution des χ² obtenus à celui de la région DR.

Aussi : test antipode (direction Shapley) et robustesse des bins ±20%.
"""

from pathlib import Path
import json
import numpy as np
import pandas as pd
import scipy.stats

# Imports communs avec analysis script
from cf4_03_analysis import (
    L_DR_DEG, B_DR_DEG, BINS_DEG,
    angular_distance_deg, select_around, vpec_by_bin,
    generate_control_positions, chi_square,
)

ROOT = Path(__file__).resolve().parents[1]


def run_test_at(df, l_center, b_center, ctrl_means, ctrl_errs):
    """Calcule χ² à une position donnée, en utilisant les contrôles déjà calculés."""
    sub = select_around(df, l_center, b_center)
    if len(sub) < 10:
        return np.nan, 0
    bins = vpec_by_bin(sub)
    return chi_square(bins, ctrl_means, ctrl_errs)


def main():
    print("=== Tests de validation ===\n")
    df = pd.read_csv(ROOT / "data" / "cf4_groups.csv")

    # Recalculer les contrôles (mêmes que dans cf4_03)
    print("Calcul des contrôles (seed=42)...")
    controls = generate_control_positions()
    ctrl_results_per_bin = [[] for _ in BINS_DEG]
    for lc, bc in controls:
        sub = select_around(df, lc, bc)
        bins = vpec_by_bin(sub)
        for i, r in enumerate(bins):
            if r["n"] >= 2:
                ctrl_results_per_bin[i].append(r["mean"])
    ctrl_means = []
    ctrl_errs = []
    for vals in ctrl_results_per_bin:
        if len(vals) >= 2:
            ctrl_means.append(np.mean(vals))
            ctrl_errs.append(np.std(vals, ddof=1) / np.sqrt(len(vals)))
        else:
            ctrl_means.append(0.0)
            ctrl_errs.append(1000.0)
    print(f"  done.\n")

    # χ² du DR (référence)
    chi2_dr, df_dr = run_test_at(df, L_DR_DEG, B_DR_DEG, ctrl_means, ctrl_errs)
    print(f"χ² du DR : {chi2_dr:.2f} (df={df_dr})\n")

    # === Test 1 : Placebo 100 positions ===
    print("--- Test placebo 100 positions ---")
    rng = np.random.default_rng(seed=12345)
    placebo_chi2 = []
    L_ANTI = (L_DR_DEG + 180) % 360
    B_ANTI = -B_DR_DEG
    n_attempts = 0
    while len(placebo_chi2) < 100 and n_attempts < 1000:
        n_attempts += 1
        l_rand = rng.uniform(0, 360)
        b_rand = np.rad2deg(np.arcsin(rng.uniform(-1, 1)))
        if abs(b_rand) < 10: continue
        if angular_distance_deg(l_rand, b_rand, L_DR_DEG, B_DR_DEG) < 50: continue
        if angular_distance_deg(l_rand, b_rand, L_ANTI, B_ANTI) < 50: continue
        chi2, _ = run_test_at(df, l_rand, b_rand, ctrl_means, ctrl_errs)
        if not np.isnan(chi2):
            placebo_chi2.append(chi2)

    placebo_chi2 = np.array(placebo_chi2)
    n_above = (placebo_chi2 > chi2_dr).sum()
    percentile = n_above / len(placebo_chi2) * 100
    print(f"Tirages réussis: {len(placebo_chi2)} / {n_attempts} tentatives")
    print(f"χ²_DR ({chi2_dr:.2f}) > {len(placebo_chi2) - n_above}/{len(placebo_chi2)} placebos")
    print(f"DR est dans le top {percentile:.1f}% des placebos")
    print(f"Distribution placebo: median={np.median(placebo_chi2):.2f}, max={placebo_chi2.max():.2f}")
    placebo_verdict = "real_signal" if percentile < 5 else ("borderline" if percentile < 10 else "consistent_with_null")
    print(f"Verdict placebo: {placebo_verdict}")

    # === Test 2 : Antipode (Shapley direction) ===
    print(f"\n--- Test antipode : (l={L_ANTI:.1f}, b={B_ANTI:+.1f}) ---")
    sub_anti = select_around(df, L_ANTI, B_ANTI)
    print(f"Sample antipode: {len(sub_anti)} groupes")
    bins_anti = vpec_by_bin(sub_anti)
    print(f"\n{'Bin':<12s} {'N':>5s} {'mean Vpec':>12s} {'ΔVpec vs ctrl':>16s}")
    for i, r in enumerate(bins_anti):
        if not np.isnan(r["mean"]):
            delta = r["mean"] - ctrl_means[i]
            print(f"  [{r['lo']:>2d}°,{r['hi']:>2d}°) {r['n']:>5d} {r['mean']:>10.0f} km/s {delta:>+13.0f}")
        else:
            print(f"  [{r['lo']:>2d}°,{r['hi']:>2d}°) {r['n']:>5d}            —                —")
    chi2_anti, df_anti = chi_square(bins_anti, ctrl_means, ctrl_errs)
    if df_anti > 0:
        p_anti = 1 - scipy.stats.chi2.cdf(chi2_anti, df=df_anti)
        print(f"χ²_antipode = {chi2_anti:.2f} (df={df_anti}, p={p_anti:.4f})")

    # === Test 3 : Robustesse des bins ±20% ===
    print(f"\n--- Test robustesse bins ±20% ---")
    BINS_PLUS = [(0, 10), (10, 22), (22, 34), (34, 40)]
    BINS_MINUS = [(0, 6), (6, 14), (14, 22), (22, 40)]

    def vpec_by_custom_bins(sub, bins_def):
        results = []
        for lo, hi in bins_def:
            m = (sub["theta"] >= lo) & (sub["theta"] < hi) & sub["Vpec"].notna()
            sl = sub[m]
            n = len(sl)
            if n >= 2:
                mean = sl["Vpec"].mean()
                err = sl["Vpec"].std(ddof=1) / np.sqrt(n)
            elif n == 1:
                mean = sl["Vpec"].iloc[0]
                err = 1000.0
            else:
                mean = np.nan
                err = np.nan
            results.append({"lo": lo, "hi": hi, "n": n, "mean": mean, "err": err})
        return results

    # NOTE: on ré-extrait sub pour DR
    sub_dr = select_around(df, L_DR_DEG, B_DR_DEG)

    for label, bins_alt in [("bins +20%", BINS_PLUS), ("bins -20%", BINS_MINUS)]:
        bins_dr_alt = vpec_by_custom_bins(sub_dr, bins_alt)
        # Calculer ctrl_means/errs dans les nouveaux bins
        ctrl_per_bin_alt = [[] for _ in bins_alt]
        for lc, bc in controls:
            sub_c = select_around(df, lc, bc)
            for i, (lo, hi) in enumerate(bins_alt):
                m = (sub_c["theta"] >= lo) & (sub_c["theta"] < hi) & sub_c["Vpec"].notna()
                if m.sum() >= 2:
                    ctrl_per_bin_alt[i].append(sub_c[m]["Vpec"].mean())
        ctrl_means_alt = [np.mean(v) if len(v) >= 2 else 0.0 for v in ctrl_per_bin_alt]
        ctrl_errs_alt = [np.std(v, ddof=1)/np.sqrt(len(v)) if len(v) >= 2 else 1000.0 for v in ctrl_per_bin_alt]
        chi2_alt, df_alt = chi_square(bins_dr_alt, ctrl_means_alt, ctrl_errs_alt)
        if df_alt > 0:
            p_alt = 1 - scipy.stats.chi2.cdf(chi2_alt, df=df_alt)
            print(f"  {label}: χ² = {chi2_alt:.2f} (df={df_alt}, p={p_alt:.4f})")

    # === Sauvegarde résultats ===
    results = {
        "placebo": {
            "n_trials": int(len(placebo_chi2)),
            "chi2_dr": float(chi2_dr),
            "median_placebo": float(np.median(placebo_chi2)),
            "max_placebo": float(placebo_chi2.max()),
            "n_above_dr": int(n_above),
            "percentile_dr": float(percentile),
            "verdict": placebo_verdict,
        },
        "antipode": {
            "position": {"l": float(L_ANTI), "b": float(B_ANTI)},
            "n_groups": int(len(sub_anti)),
            "chi2": float(chi2_anti) if not np.isnan(chi2_anti) else None,
            "df": int(df_anti),
            "delta_vpec_per_bin": [float(r["mean"] - ctrl_means[i]) if not np.isnan(r["mean"]) else None
                                   for i, r in enumerate(bins_anti)],
        },
    }
    out = ROOT / "results_validation.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved → {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
