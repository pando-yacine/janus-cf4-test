"""
cf4_03_analysis.py

Analyse principale du test Janus DR sur CF4.

Calcule les Vpec moyens par bin angulaire dans :
- la région DR (cône 40° autour de (305°, +5°))
- 8 régions de contrôle équiréparties sur le ciel admissible

Calcule ΔVpec (DR - moyenne_contrôles) par bin et le χ² principal.
"""

from pathlib import Path
import json
import numpy as np
import pandas as pd
import scipy.stats

# Constantes figées par protocole v2 (commit b06dfd3)
L_DR_DEG = 305.0
B_DR_DEG = 5.0
BINS_DEG = [(0, 8), (8, 18), (18, 28), (28, 40)]
CONTROL_SEED = 42
N_CONTROL = 8

# Filtres figés
MIN_DIST = 50.0
MAX_DIST = 350.0
MAX_E_DM = 0.30
MIN_ABS_B = 3.0
CONE_DEG = 40.0

ROOT = Path(__file__).resolve().parents[1]


def angular_distance_deg(l1, b1, l2, b2):
    l1r = np.deg2rad(l1)
    b1r = np.deg2rad(b1)
    l2r = np.deg2rad(l2)
    b2r = np.deg2rad(b2)
    cos_d = np.sin(b1r) * np.sin(b2r) + np.cos(b1r) * np.cos(b2r) * np.cos(l1r - l2r)
    return np.rad2deg(np.arccos(np.clip(cos_d, -1.0, 1.0)))


def select_around(df, l_center, b_center):
    """Applique les filtres figés du protocole, centré sur (l_center, b_center)."""
    theta = angular_distance_deg(df["GLON"].to_numpy(), df["GLAT"].to_numpy(), l_center, b_center)
    mask = (
        (theta < CONE_DEG) &
        (df["Dist_Mpc"] > MIN_DIST) & (df["Dist_Mpc"] < MAX_DIST) &
        (df["e_DMzp"] < MAX_E_DM) &
        (df["GLAT"].abs() > MIN_ABS_B)
    )
    sub = df[mask].copy()
    sub["theta"] = theta[mask]
    return sub


def vpec_by_bin(sub):
    """Retourne mean(Vpec), err(Vpec), N par bin angulaire."""
    results = []
    for lo, hi in BINS_DEG:
        m = (sub["theta"] >= lo) & (sub["theta"] < hi) & sub["Vpec"].notna()
        sl = sub[m]
        n = len(sl)
        if n >= 2:
            mean = sl["Vpec"].mean()
            err = sl["Vpec"].std(ddof=1) / np.sqrt(n)
        elif n == 1:
            mean = sl["Vpec"].iloc[0]
            err = 1000.0  # large error placeholder for single point
        else:
            mean = np.nan
            err = np.nan
        results.append({"lo": lo, "hi": hi, "n": n, "mean": mean, "err": err})
    return results


def generate_control_positions(seed=CONTROL_SEED, n=N_CONTROL):
    """Génère N positions de contrôle aléatoires, exclues du DR et de l'antipode et du plan."""
    rng = np.random.default_rng(seed)
    L_ANTI = (L_DR_DEG + 180) % 360
    B_ANTI = -B_DR_DEG
    positions = []
    while len(positions) < n:
        # Sphère uniforme: l ∈ [0, 360), sin(b) ∈ [-1, 1]
        l_rand = rng.uniform(0, 360)
        b_rand = np.rad2deg(np.arcsin(rng.uniform(-1, 1)))
        if abs(b_rand) < 20: continue  # éviter le plan galactique
        if angular_distance_deg(l_rand, b_rand, L_DR_DEG, B_DR_DEG) < 60: continue
        if angular_distance_deg(l_rand, b_rand, L_ANTI, B_ANTI) < 60: continue
        positions.append((l_rand, b_rand))
    return positions


def chi_square(dr_results, ctrl_means, ctrl_errs):
    """χ² test : H0 = ΔVpec compatible avec zéro."""
    chi2 = 0
    df_used = 0
    for i, r in enumerate(dr_results):
        if r["n"] < 2 or np.isnan(r["mean"]):
            continue  # skip bins vides
        delta = r["mean"] - ctrl_means[i]
        var = r["err"] ** 2 + ctrl_errs[i] ** 2  # variance de la différence
        if var > 0:
            chi2 += (delta ** 2) / var
            df_used += 1
    return chi2, df_used


def main():
    print("=== Test principal Janus DR — CF4 ===\n")
    df = pd.read_csv(ROOT / "data" / "cf4_groups.csv")
    print(f"CF4 chargé: {len(df)} groupes\n")

    # 1. Région DR
    print(f"--- Région DR : (l={L_DR_DEG}, b={B_DR_DEG}) ---")
    dr = select_around(df, L_DR_DEG, B_DR_DEG)
    print(f"Sample DR: {len(dr)} groupes")
    dr_bins = vpec_by_bin(dr)
    print(f"\n{'Bin':<10s} {'N':>5s} {'mean Vpec':>12s} {'err':>10s}")
    for r in dr_bins:
        n_str = str(r["n"])
        m_str = f"{r['mean']:.0f} km/s" if not np.isnan(r["mean"]) else "—"
        e_str = f"±{r['err']:.0f}" if not np.isnan(r["err"]) else "—"
        print(f"  [{r['lo']:>2d}°,{r['hi']:>2d}°) {n_str:>5s} {m_str:>12s} {e_str:>10s}")

    # 2. Régions de contrôle
    print(f"\n--- {N_CONTROL} régions de contrôle (seed={CONTROL_SEED}) ---")
    controls = generate_control_positions()
    ctrl_results_per_bin = [[] for _ in BINS_DEG]
    for j, (lc, bc) in enumerate(controls):
        sub = select_around(df, lc, bc)
        bins = vpec_by_bin(sub)
        print(f"  Ctrl {j}: (l={lc:5.1f}, b={bc:+5.1f}) N={len(sub):>3d}")
        for i, r in enumerate(bins):
            if r["n"] >= 2:
                ctrl_results_per_bin[i].append(r["mean"])

    # 3. Statistiques de contrôle par bin
    ctrl_means = []
    ctrl_errs = []
    for i, vals in enumerate(ctrl_results_per_bin):
        if len(vals) >= 2:
            m = np.mean(vals)
            e = np.std(vals, ddof=1) / np.sqrt(len(vals))
        elif len(vals) == 1:
            m = vals[0]
            e = 1000.0
        else:
            m = 0.0
            e = 1000.0
        ctrl_means.append(m)
        ctrl_errs.append(e)

    # 4. Test χ²
    print(f"\n--- Test principal : ΔVpec(DR) vs <Vpec>(contrôles) ---")
    print(f"{'Bin':<12s} {'DR mean':>10s} {'Ctrl mean':>10s} {'ΔVpec':>10s}")
    for i, r in enumerate(dr_bins):
        if not np.isnan(r["mean"]):
            delta = r["mean"] - ctrl_means[i]
            print(f"  [{r['lo']:>2d}°,{r['hi']:>2d}°) {r['mean']:>10.0f} {ctrl_means[i]:>10.0f} {delta:>+10.0f}")
        else:
            print(f"  [{r['lo']:>2d}°,{r['hi']:>2d}°)        —          —          —")

    chi2, df_used = chi_square(dr_bins, ctrl_means, ctrl_errs)
    if df_used > 0:
        pvalue = 1 - scipy.stats.chi2.cdf(chi2, df=df_used)
        print(f"\nχ² = {chi2:.2f}, df = {df_used}, p-value = {pvalue:.4f}")
        # Seuils
        crit_05 = scipy.stats.chi2.ppf(0.95, df=df_used)
        crit_01 = scipy.stats.chi2.ppf(0.99, df=df_used)
        print(f"Seuils df={df_used}: p<0.05 si χ²>{crit_05:.2f} ; p<0.01 si χ²>{crit_01:.2f}")
        if pvalue < 0.01:
            verdict = "signal_significatif (p<0.01)"
        elif pvalue < 0.05:
            verdict = "suggestif (0.01<p<0.05)"
        else:
            verdict = "non_discriminant (p>0.05)"
        print(f"\nVerdict provisoire: {verdict}")
    else:
        chi2 = np.nan
        pvalue = np.nan
        verdict = "test_impossible"
        print(f"\nχ² impossible : aucun bin valide.")

    # Sauvegarder résultats
    results = {
        "protocol_version": "v2.0",
        "protocol_commit": "b06dfd379b0c14c2e99b0544aaeb537a9c6a15d1",
        "dr_position": {"l": L_DR_DEG, "b": B_DR_DEG},
        "n_dr_total": len(dr),
        "bins_dr": [{"lo": r["lo"], "hi": r["hi"], "n": int(r["n"]),
                     "mean_kms": float(r["mean"]) if not np.isnan(r["mean"]) else None,
                     "err_kms": float(r["err"]) if not np.isnan(r["err"]) else None} for r in dr_bins],
        "controls_used": [{"l": float(l), "b": float(b)} for l, b in controls],
        "ctrl_means_kms": [float(x) for x in ctrl_means],
        "ctrl_errs_kms": [float(x) for x in ctrl_errs],
        "chi2": float(chi2) if not np.isnan(chi2) else None,
        "df_used": df_used,
        "pvalue": float(pvalue) if not np.isnan(pvalue) else None,
        "verdict_main": verdict,
    }
    out = ROOT / "results_main.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved → {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
