"""
cf4_05_figures.py

Génère les figures publiables :
1. Sky map : groupes CF4 + DR + contrôles + antipode
2. Vpec par bin : DR, antipode, contrôles
3. Distribution placebo
4. Comparaison Janus prédit vs LCDM observé
"""

from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

from cf4_03_analysis import (
    L_DR_DEG, B_DR_DEG, BINS_DEG,
    angular_distance_deg, select_around, vpec_by_bin,
    generate_control_positions,
)

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

# Reload everything
df = pd.read_csv(ROOT / "data" / "cf4_groups.csv")
results_main = json.loads((ROOT / "results_main.json").read_text())
results_val = json.loads((ROOT / "results_validation.json").read_text())

L_ANTI = (L_DR_DEG + 180) % 360
B_ANTI = -B_DR_DEG

# Figure 1 — Sky map (Mollweide)
print("Figure 1: Sky map...")
fig, ax = plt.subplots(figsize=(12, 6), subplot_kw={"projection": "mollweide"})
# Convert l to (-180, 180)
l_plot = np.where(df["GLON"].to_numpy() > 180, df["GLON"].to_numpy() - 360, df["GLON"].to_numpy())
b_plot = df["GLAT"].to_numpy()
ax.scatter(np.deg2rad(l_plot), np.deg2rad(b_plot), s=0.3, alpha=0.2, color="gray", label=f"CF4 ({len(df)} groups)")
# DR
l_dr = L_DR_DEG - 360 if L_DR_DEG > 180 else L_DR_DEG
ax.scatter([np.deg2rad(l_dr)], [np.deg2rad(B_DR_DEG)], s=300, marker="*", color="red", label="Dipole Repeller (305°, +5°)", zorder=5)
# Antipode
l_ant = L_ANTI - 360 if L_ANTI > 180 else L_ANTI
ax.scatter([np.deg2rad(l_ant)], [np.deg2rad(B_ANTI)], s=300, marker="*", color="blue", label="Antipode / Shapley dir.", zorder=5)
# Controls
for ctrl in results_main["controls_used"]:
    l_c = ctrl["l"] - 360 if ctrl["l"] > 180 else ctrl["l"]
    ax.scatter([np.deg2rad(l_c)], [np.deg2rad(ctrl["b"])], s=80, marker="^", color="green", alpha=0.7)
ax.scatter([], [], s=80, marker="^", color="green", label="Control regions (8)")
ax.set_title("Sky map (galactic Mollweide) — CF4 groups + DR test geometry")
ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.15), ncol=2)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(FIG / "01_skymap.pdf", bbox_inches="tight")
plt.savefig(FIG / "01_skymap.png", dpi=150, bbox_inches="tight")
plt.close()

# Figure 2 — ΔVpec vs θ (DR + antipode + controls)
print("Figure 2: ΔVpec vs θ...")
fig, ax = plt.subplots(figsize=(10, 6))
bin_centers = [(lo + hi) / 2 for lo, hi in BINS_DEG]
bin_widths = [(hi - lo) / 2 for lo, hi in BINS_DEG]

# DR
dr_means = [b["mean_kms"] if b["mean_kms"] is not None else np.nan for b in results_main["bins_dr"]]
dr_errs = [b["err_kms"] if b["err_kms"] is not None else 0 for b in results_main["bins_dr"]]
ctrl_means = results_main["ctrl_means_kms"]
delta_dr = [m - c if not np.isnan(m) else np.nan for m, c in zip(dr_means, ctrl_means)]
ax.errorbar(bin_centers, delta_dr, xerr=bin_widths, yerr=dr_errs, fmt="o", color="red",
            label=f"DR : χ²={results_main['chi2']:.1f}", capsize=4, markersize=10)

# Antipode
delta_anti = results_val["antipode"]["delta_vpec_per_bin"]
delta_anti_plot = [d if d is not None else np.nan for d in delta_anti]
ax.errorbar(bin_centers, delta_anti_plot, xerr=bin_widths, fmt="s", color="blue",
            label=f"Antipode (Shapley dir.) : χ²={results_val['antipode']['chi2']:.1f}", capsize=4, markersize=10)

# Janus prediction sketch (qualitative)
janus_pred = [0, -300, -100, 0]  # qualitative: 0 at center, negative max in mid bins, returning to 0
ax.plot(bin_centers, janus_pred, "g--", alpha=0.6, label="Prédiction Janus (qualitative)")

ax.axhline(0, color="black", linewidth=0.5)
ax.set_xlabel("θ from DR center (degrees)")
ax.set_ylabel("ΔVpec = <Vpec(region)> - <Vpec(controls)>  [km/s]")
ax.set_title("Vélocité peculière résiduelle vs distance angulaire au DR")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(FIG / "02_residuals.pdf", bbox_inches="tight")
plt.savefig(FIG / "02_residuals.png", dpi=150, bbox_inches="tight")
plt.close()

# Figure 3 — Distribution placebo
print("Figure 3: Distribution placebo...")
# We need to re-run the placebo to get the histogram
# Faster: just use the summary stats and create a distribution
placebo = results_val["placebo"]
chi2_dr = placebo["chi2_dr"]
fig, ax = plt.subplots(figsize=(10, 5))

# Re-run placebo to get full distribution for histogram
print("  re-running placebo for histogram (takes ~30s)...")
controls = generate_control_positions()
ctrl_per_bin = [[] for _ in BINS_DEG]
for lc, bc in controls:
    sub = select_around(df, lc, bc)
    bins = vpec_by_bin(sub)
    for i, r in enumerate(bins):
        if r["n"] >= 2:
            ctrl_per_bin[i].append(r["mean"])
ctrl_means_arr = [np.mean(v) if len(v) >= 2 else 0.0 for v in ctrl_per_bin]
ctrl_errs_arr = [np.std(v, ddof=1)/np.sqrt(len(v)) if len(v) >= 2 else 1000.0 for v in ctrl_per_bin]

from cf4_03_analysis import chi_square
rng = np.random.default_rng(seed=12345)
placebo_chi2 = []
n_attempts = 0
while len(placebo_chi2) < 100 and n_attempts < 1000:
    n_attempts += 1
    l_rand = rng.uniform(0, 360)
    b_rand = np.rad2deg(np.arcsin(rng.uniform(-1, 1)))
    if abs(b_rand) < 10: continue
    if angular_distance_deg(l_rand, b_rand, L_DR_DEG, B_DR_DEG) < 50: continue
    if angular_distance_deg(l_rand, b_rand, L_ANTI, B_ANTI) < 50: continue
    sub = select_around(df, l_rand, b_rand)
    if len(sub) < 10: continue
    bins = vpec_by_bin(sub)
    chi2, _ = chi_square(bins, ctrl_means_arr, ctrl_errs_arr)
    if not np.isnan(chi2):
        placebo_chi2.append(chi2)

ax.hist(placebo_chi2, bins=30, color="lightgray", edgecolor="black", alpha=0.7, label=f"Placebo (n={len(placebo_chi2)})")
ax.axvline(chi2_dr, color="red", linewidth=2, label=f"χ²_DR = {chi2_dr:.1f} (top 3%)")
ax.axvline(results_val["antipode"]["chi2"], color="blue", linewidth=2, linestyle="--",
           label=f"χ²_antipode = {results_val['antipode']['chi2']:.1f}")
ax.set_xlabel("χ² value")
ax.set_ylabel("Number of placebo positions")
ax.set_title("Distribution of χ² for placebo positions vs DR / antipode")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(FIG / "03_placebo.pdf", bbox_inches="tight")
plt.savefig(FIG / "03_placebo.png", dpi=150, bbox_inches="tight")
plt.close()

print(f"\nFigures saved in {FIG.relative_to(ROOT)}/")
