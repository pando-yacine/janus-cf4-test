"""twomrs_04_figures.py — figures pour Sprint 4."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from twomrs_02_analysis import BINS_DEG, L_DR_DEG, B_DR_DEG

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"

main = json.loads((ROOT / "results_v3_main.json").read_text())
val = json.loads((ROOT / "results_v3_validation.json").read_text())
df = pd.read_csv(ROOT / "data" / "2mrs_with_galactic.csv")

# --- Figure 1: ΔM par bin ---
print("Figure: ΔM par bin")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

bin_centers = [(lo + hi) / 2 for lo, hi in BINS_DEG]
bin_widths = [(hi - lo) / 2 for lo, hi in BINS_DEG]

# Observable A: ΔM
dr_a = main["observable_A"]["dr_bins"]
ctrl_a = main["observable_A"]["ctrl_means"]
delta_dr_A = [r["median"] - ctrl_a[i] if r["median"] is not None else np.nan for i, r in enumerate(dr_a)]
err_dr_A = [r["err"] if r["err"] is not None else 0 for r in dr_a]
axes[0].errorbar(bin_centers, delta_dr_A, xerr=bin_widths, yerr=err_dr_A,
                 fmt="o", color="red", label=f"DR (χ²={main['observable_A']['chi2']:.1f})", capsize=4, markersize=10)
delta_anti_A = val["antipode"]["delta_M_per_bin"]
delta_anti_A_plot = [d if d is not None else np.nan for d in delta_anti_A]
axes[0].errorbar(bin_centers, delta_anti_A_plot, xerr=bin_widths, fmt="s", color="blue",
                 label=f"Antipode (χ²={val['antipode']['chi2_A']:.1f})", capsize=4, markersize=10)
axes[0].plot(bin_centers, [0, -0.10, -0.05, 0], "g--", alpha=0.6, label="Pred. Janus (qualitative)")
axes[0].axhline(0, color="black", lw=0.5)
axes[0].set_xlabel("θ from DR (°)")
axes[0].set_ylabel("Δ median M_K_app  [mag]")
axes[0].set_title(f"Observable A — Magnitude résiduelle\nDR top {val['placebo']['percentile_dr_A']:.0f}% du placebo")
axes[0].legend()
axes[0].grid(alpha=0.3)

# Observable B: comptages
dr_b = main["observable_B"]["dr_bins"]
ctrl_b = main["observable_B"]["ctrl_means"]
delta_dr_B = [r["n"] - ctrl_b[i] for i, r in enumerate(dr_b)]
delta_anti_B = val["antipode"]["delta_count_per_bin"]
axes[1].plot(bin_centers, delta_dr_B, "o-", color="red", label=f"DR (χ²={main['observable_B']['chi2']:.1f})", markersize=10)
axes[1].plot(bin_centers, delta_anti_B, "s-", color="blue", label=f"Antipode (χ²={val['antipode']['chi2_B']:.1f})", markersize=10)
axes[1].plot(bin_centers, [0, -10, -8, 0], "g--", alpha=0.6, label="Pred. Janus (qualitative)")
axes[1].axhline(0, color="black", lw=0.5)
axes[1].set_xlabel("θ from DR (°)")
axes[1].set_ylabel("Δ count")
axes[1].set_title(f"Observable B — Comptage Kt<11.0\nDR top {val['placebo']['percentile_dr_B']:.0f}% du placebo")
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig(FIG / "v3_01_residuals.pdf", bbox_inches="tight")
plt.savefig(FIG / "v3_01_residuals.png", dpi=150, bbox_inches="tight")
plt.close()

# --- Figure 2: 2MRS sky map ---
print("Figure: sky map 2MRS")
fig, ax = plt.subplots(figsize=(12, 6), subplot_kw={"projection": "mollweide"})
l_plot = np.where(df["GLON"].to_numpy() > 180, df["GLON"].to_numpy() - 360, df["GLON"].to_numpy())
ax.scatter(np.deg2rad(l_plot), np.deg2rad(df["GLAT"].to_numpy()), s=0.1, alpha=0.15, color="gray",
           label=f"2MRS ({len(df)} galaxies)")
l_dr = L_DR_DEG - 360 if L_DR_DEG > 180 else L_DR_DEG
ax.scatter([np.deg2rad(l_dr)], [np.deg2rad(B_DR_DEG)], s=400, marker="*", color="red", label="DR (305°, +5°)", zorder=5)
L_ANTI = (L_DR_DEG + 180) % 360
B_ANTI = -B_DR_DEG
l_ant = L_ANTI - 360 if L_ANTI > 180 else L_ANTI
ax.scatter([np.deg2rad(l_ant)], [np.deg2rad(B_ANTI)], s=400, marker="*", color="blue", label="Antipode (Shapley)", zorder=5)
ax.set_title(f"2MRS sky coverage — 91% of sky including avoidance zone")
ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.15), ncol=3)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(FIG / "v3_02_skymap.pdf", bbox_inches="tight")
plt.savefig(FIG / "v3_02_skymap.png", dpi=150, bbox_inches="tight")
plt.close()

# --- Figure 3: distribution placebo ---
print("Figure: placebo distribution")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Placebo distribution se reconstruit en relançant... pas pratique
# On va juste montrer les médianes/maxima
plac = val["placebo"]
axes[0].axvline(plac["chi2_A_dr"], color="red", lw=2, label=f"DR χ²={plac['chi2_A_dr']:.1f} (top {plac['percentile_dr_A']:.0f}%)")
axes[0].axvline(plac["median_placebo_A"], color="black", lw=1, ls="--", label=f"Median placebo = {plac['median_placebo_A']:.1f}")
axes[0].axvline(plac["max_placebo_A"], color="orange", lw=1, ls=":", label=f"Max placebo = {plac['max_placebo_A']:.1f}")
axes[0].set_xlim(0, max(plac["max_placebo_A"], plac["chi2_A_dr"]) * 1.1)
axes[0].set_xlabel("χ²_A value")
axes[0].set_title(f"Observable A — Placebo (n={plac['n_trials_A']})")
axes[0].legend()
axes[0].grid(alpha=0.3)

axes[1].axvline(plac["chi2_B_dr"], color="red", lw=2, label=f"DR χ²={plac['chi2_B_dr']:.1f} (top {plac['percentile_dr_B']:.0f}%)")
axes[1].axvline(plac["median_placebo_B"], color="black", lw=1, ls="--", label=f"Median placebo = {plac['median_placebo_B']:.1f}")
axes[1].axvline(plac["max_placebo_B"], color="orange", lw=1, ls=":", label=f"Max placebo = {plac['max_placebo_B']:.1f}")
axes[1].set_xlim(0, max(plac["max_placebo_B"], plac["chi2_B_dr"]) * 1.1)
axes[1].set_xlabel("χ²_B value")
axes[1].set_title(f"Observable B — Placebo (n={plac['n_trials_B']})")
axes[1].legend()
axes[1].grid(alpha=0.3)
plt.tight_layout()
plt.savefig(FIG / "v3_03_placebo.pdf", bbox_inches="tight")
plt.savefig(FIG / "v3_03_placebo.png", dpi=150, bbox_inches="tight")
plt.close()

print(f"\nDone. Figures in {FIG.relative_to(ROOT)}/")
