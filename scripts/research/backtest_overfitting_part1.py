"""
Figures for the post "Backtest Overfitting, Part 1".

Everything here is simulation — no market data. Four experiments:

  1. selection_bias.png  — E[max SR] under a null of zero skill, MC vs the
                           sqrt(2 ln N) and Gumbel (Bailey-Lopez de Prado)
                           approximations, then in annualized-Sharpe units.
  2. pbo.png             — CSCV probability of backtest overfitting for a
                           skilled and an overfit strategy family.
  3. psr.png             — probabilistic Sharpe ratio and the minimum track
                           record length, under normal and fat-tailed returns.
  4. dsr.png             — deflated Sharpe ratio: the threshold a selected
                           Sharpe must clear as the trial count grows.

Run:  python3 scripts/research/backtest_overfitting_part1.py
Out:  src/assets/research/backtest-overfitting-part-1/*.png
"""

from itertools import combinations
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

OUT = Path(__file__).resolve().parents[2] / "src/assets/research/backtest-overfitting-part-1"
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "figure.dpi": 130, "savefig.dpi": 130, "savefig.bbox": "tight",
    "figure.facecolor": "white", "axes.facecolor": "white", "axes.axisbelow": True,
    "axes.grid": True, "grid.alpha": 0.30, "grid.linewidth": 0.6, "grid.color": "#c8c8c8",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#666666", "axes.linewidth": 0.9,
    "axes.titlesize": 12, "axes.titleweight": "bold", "axes.titlepad": 10,
    "axes.labelsize": 10.5, "axes.labelcolor": "#333333",
    "xtick.color": "#666666", "ytick.color": "#666666",
    "xtick.labelsize": 9.5, "ytick.labelsize": 9.5,
    "font.size": 10, "legend.frameon": False, "legend.fontsize": 9,
})
BLUE, ORANGE, GREEN, RED, PURPLE, GRAY = (
    "#2c6fbb", "#e8833a", "#3c9a5f", "#c83e4d", "#7d5ba6", "#8c8c8c")
NAVY = "#1f3b73"

GAMMA = 0.5772156649015329          # Euler-Mascheroni
ANN = np.sqrt(252)                  # daily -> annual Sharpe
T_DAYS = 1260                       # 5 years of daily observations
RNG = np.random.default_rng(20260817)


# --------------------------------------------------------------------------
# 1. Selection bias: the expected maximum Sharpe under a null of no skill
# --------------------------------------------------------------------------
def expected_max_gumbel(n):
    """E[max of n iid standard normals], Bailey & Lopez de Prado's Gumbel
    approximation: (1-g)*z(1 - 1/n) + g*z(1 - 1/(n*e))."""
    n = np.asarray(n, dtype=float)
    return (1 - GAMMA) * norm.ppf(1 - 1 / n) + GAMMA * norm.ppf(1 - 1 / (n * np.e))


def mc_expected_max(n_grid, t=T_DAYS, reps=3000):
    """Monte-Carlo E[max SR] over n independent zero-edge backtests of length t,
    expressed in units of the standard deviation of the trial-SR distribution."""
    out = []
    for n in n_grid:
        best = np.empty(reps)
        for r in range(reps):
            x = RNG.standard_normal((t, n))
            sr = x.mean(0) / x.std(0, ddof=1)          # per-observation Sharpe
            best[r] = sr.max()
        out.append(best.mean() * np.sqrt(t))            # standardize: sd(SR) ~ 1/sqrt(t)
    return np.array(out)


def fig_selection_bias():
    n_mc = np.array([2, 5, 10, 25, 50, 100, 250, 500, 1000])
    mc = mc_expected_max(n_mc)
    n_fine = np.logspace(np.log10(2), np.log10(5000), 200)

    fig, ax = plt.subplots(1, 2, figsize=(12.5, 4.4))

    ax[0].plot(n_fine, np.sqrt(2 * np.log(n_fine)), color=GRAY, ls="--", lw=1.4,
               label=r"$\sqrt{2\ln N}$  (asymptotic)")
    ax[0].plot(n_fine, expected_max_gumbel(n_fine), color=BLUE, lw=1.8,
               label="Gumbel approximation")
    ax[0].scatter(n_mc, mc, s=34, color=RED, zorder=3, label="Monte Carlo (3k reps)")
    ax[0].set_xscale("log")
    ax[0].set_title("Expected maximum Sharpe under a null of zero skill")
    ax[0].set_xlabel("N — number of independent configurations tried")
    ax[0].set_ylabel(r"E[max SR]  /  sd(SR)")
    ax[0].legend(loc="upper left")

    # Same curve in annualized-Sharpe units for a 5-year daily backtest.
    sd_ann = ANN / np.sqrt(T_DAYS)                      # sd of the annualized trial SR
    ann = expected_max_gumbel(n_fine) * sd_ann
    ax[1].plot(n_fine, ann, color=NAVY, lw=1.9)
    ax[1].fill_between(n_fine, 0, ann, color=NAVY, alpha=0.08)
    for level, lab in [(0.5, "0.5 — 'promising'"), (1.0, "1.0 — 'hireable'")]:
        ax[1].axhline(level, color=ORANGE, ls=":", lw=1.3)
        n_star = np.interp(level, ann, n_fine)          # invert the Gumbel curve
        ax[1].annotate(f"{lab}\nreached by chance at N ≈ {n_star:,.0f}",
                       xy=(n_fine[-1], level), xytext=(-6, 6), textcoords="offset points",
                       ha="right", va="bottom", fontsize=9, color="#444444")
    ax[1].set_xscale("log")
    ax[1].set_title(f"...in annualized Sharpe, {T_DAYS//252}-year daily backtest")
    ax[1].set_xlabel("N — number of independent configurations tried")
    ax[1].set_ylabel("expected best annualized Sharpe")
    ax[1].set_ylim(0, None)

    fig.tight_layout()
    fig.savefig(OUT / "selection_bias.png")
    plt.close(fig)

    print("[1] selection bias — E[max SR]/sd at N=1000:",
          f"MC {mc[-1]:.2f}, Gumbel {expected_max_gumbel(1000):.2f}, "
          f"sqrt(2lnN) {np.sqrt(2*np.log(1000)):.2f}")
    print("    annualized best-by-luck Sharpe at N=1000:",
          f"{expected_max_gumbel(1000)*sd_ann:.2f}")


# --------------------------------------------------------------------------
# 2. CSCV / probability of backtest overfitting
# --------------------------------------------------------------------------
def cscv(m, s=10):
    """Combinatorially symmetric cross-validation (Bailey et al. 2016).

    m : (T, N) matrix of per-period returns, one column per configuration.
    s : number of contiguous row blocks; every combination of s/2 blocks is
        used as the in-sample set and its complement as out-of-sample.

    Returns (lambdas, is_sr, oos_sr) where lambdas are the logits of the
    out-of-sample relative rank of the in-sample-optimal configuration.
    """
    t, n = m.shape
    blocks = np.array_split(np.arange(t), s)
    lam, is_sr_sel, oos_sr_sel = [], [], []
    for combo in combinations(range(s), s // 2):
        rows_is = np.concatenate([blocks[b] for b in combo])
        rows_oos = np.concatenate([blocks[b] for b in range(s) if b not in combo])
        j, jbar = m[rows_is], m[rows_oos]
        sr_is = j.mean(0) / j.std(0, ddof=1)
        sr_oos = jbar.mean(0) / jbar.std(0, ddof=1)
        n_star = int(np.argmax(sr_is))
        # relative rank of the selected config among the OOS Sharpes, in (0,1)
        rank = float((sr_oos <= sr_oos[n_star]).sum())
        omega = rank / (n + 1)
        lam.append(np.log(omega / (1 - omega)))
        is_sr_sel.append(sr_is[n_star] * ANN)
        oos_sr_sel.append(sr_oos[n_star] * ANN)
    return np.array(lam), np.array(is_sr_sel), np.array(oos_sr_sel)


def make_family(n_cfg=50, t=T_DAYS, best_ann_sr=0.0, decay=1.5):
    """N configurations of daily returns. `best_ann_sr` is the true annualized
    Sharpe of the strongest configuration and skill decays geometrically across
    the rest, so config 0 is genuinely the best. best_ann_sr = 0 gives a
    pure-noise family in which no configuration has any edge at all."""
    true_sr = best_ann_sr * np.exp(-np.arange(n_cfg) / decay) / ANN
    # common market factor + idiosyncratic noise, so configurations correlate
    common = RNG.standard_normal((t, 1)) * 0.5
    idio = RNG.standard_normal((t, n_cfg))
    x = common + idio
    x = x / x.std(0, ddof=1)
    return x + true_sr


def fig_pbo():
    overfit = make_family(best_ann_sr=0.0)
    skilled = make_family(best_ann_sr=2.0)

    lam_o, is_o, oos_o = cscv(overfit)
    lam_s, _, _ = cscv(skilled)
    pbo_o, pbo_s = (lam_o < 0).mean(), (lam_s < 0).mean()

    fig, ax = plt.subplots(1, 2, figsize=(12.5, 4.4))

    bins = np.linspace(-5, 5, 41)
    ax[0].hist(lam_s, bins=bins, color=GREEN, alpha=0.65,
               label=f"skilled family — PBO = {pbo_s:.0%}")
    ax[0].hist(lam_o, bins=bins, color=RED, alpha=0.60,
               label=f"overfit family — PBO = {pbo_o:.0%}")
    ax[0].axvline(0, color="#333333", lw=1.2)
    ax[0].set_title("CSCV logit distribution — mass below zero is PBO")
    ax[0].set_xlabel(r"$\lambda = \log[\omega/(1-\omega)]$   (OOS rank logit of the IS winner)")
    ax[0].set_ylabel("CSCV splits")
    ax[0].legend(loc="upper left")

    ax[1].scatter(is_o, oos_o, s=16, color=RED, alpha=0.45, edgecolor="none")
    lo, hi = is_o.min(), is_o.max()
    pad = 0.05 * (hi - lo)
    xs = np.linspace(lo - pad, hi + pad, 50)
    ax[1].plot(xs, xs, color=GRAY, ls="--", lw=1.2, label="no degradation")
    slope, intercept = np.polyfit(is_o, oos_o, 1)
    ax[1].plot(xs, slope * xs + intercept, color=NAVY, lw=1.8,
               label=f"fitted slope = {slope:+.2f}")
    ax[1].axhline(0, color="#333333", lw=1.0)
    ax[1].set_xlim(lo - pad, hi + pad)
    ax[1].set_title("Overfit family: the in-sample winner degrades out of sample")
    ax[1].set_xlabel("in-sample Sharpe of the selected configuration (annualized)")
    ax[1].set_ylabel("its out-of-sample Sharpe")
    ax[1].legend(loc="upper right")

    fig.tight_layout()
    fig.savefig(OUT / "pbo.png")
    plt.close(fig)

    print(f"[2] PBO — skilled {pbo_s:.1%}, overfit {pbo_o:.1%}; "
          f"overfit IS->OOS slope {slope:+.2f}, median OOS SR {np.median(oos_o):+.2f}")
    return pbo_s, pbo_o, slope, np.median(oos_o)


# --------------------------------------------------------------------------
# 3. Probabilistic Sharpe ratio
# --------------------------------------------------------------------------
def psr(sr_hat, t, sr_star=0.0, skew=0.0, kurt=3.0):
    """Probability that the true Sharpe exceeds sr_star. All Sharpes are
    per-observation; `kurt` is the raw (not excess) kurtosis."""
    denom = np.sqrt(1 - skew * sr_hat + (kurt - 1) / 4 * sr_hat ** 2)
    return norm.cdf((sr_hat - sr_star) * np.sqrt(t - 1) / denom)


def min_trl(sr_hat, sr_star=0.0, skew=0.0, kurt=3.0, alpha=0.95):
    """Minimum track record length (observations) for PSR(sr_star) >= alpha."""
    return 1 + (1 - skew * sr_hat + (kurt - 1) / 4 * sr_hat ** 2) * \
        (norm.ppf(alpha) / (sr_hat - sr_star)) ** 2


def fig_psr():
    # Monthly observations: the higher-moment terms scale with SR_hat^2, so at
    # daily frequency (SR_hat ~ 0.06) they are numerically invisible. A monthly
    # track record is also how allocators actually see a Sharpe reported.
    ann_m = np.sqrt(12)
    t_grid = np.arange(6, 181)
    cases = [
        ("normal returns  (γ₃ = 0, γ₄ = 3)", 0.0, 3.0, BLUE),
        ("fat tails  (γ₃ = 0, γ₄ = 8)", 0.0, 8.0, PURPLE),
        ("negative skew + fat tails  (γ₃ = −1.5, γ₄ = 8)", -1.5, 8.0, RED),
    ]
    sr_ann = 1.0
    sr_hat = sr_ann / ann_m

    fig, ax = plt.subplots(1, 2, figsize=(12.5, 4.4))

    for lab, sk, ku, c in cases:
        ax[0].plot(t_grid, psr(sr_hat, t_grid, 0.0, sk, ku), color=c, lw=1.8, label=lab)
        trl = min_trl(sr_hat, 0.0, sk, ku)
        ax[0].scatter([trl], [0.95], s=32, color=c, zorder=3)
    ax[0].axhline(0.95, color=ORANGE, ls=":", lw=1.3)
    ax[0].annotate("95% confidence", xy=(t_grid[-1], 0.95), xytext=(-6, -15),
                   textcoords="offset points", ha="right", fontsize=9, color="#444444")
    ax[0].set_title(f"PSR(0) for an observed annualized Sharpe of {sr_ann:.1f}")
    ax[0].set_xlabel("track record length T (months)")
    ax[0].set_ylabel("P(true Sharpe > 0)")
    ax[0].set_ylim(0.4, 1.02)
    ax[0].legend(loc="lower right")

    sr_grid_ann = np.linspace(0.4, 2.5, 120)
    for lab, sk, ku, c in cases:
        ax[1].plot(sr_grid_ann, min_trl(sr_grid_ann / ann_m, 0.0, sk, ku),
                   color=c, lw=1.8, label=lab)
    ax[1].axhline(60, color=GRAY, ls="--", lw=1.2)
    ax[1].annotate("a 5-year track record", xy=(2.5, 60), xytext=(-6, 5),
                   textcoords="offset points", ha="right", fontsize=9, color="#444444")
    ax[1].set_yscale("log")
    ax[1].set_title("Minimum track record length for 95% confidence")
    ax[1].set_xlabel("observed annualized Sharpe")
    ax[1].set_ylabel("months of returns required")
    ax[1].legend(loc="upper right")

    fig.tight_layout()
    fig.savefig(OUT / "psr.png")
    plt.close(fig)

    for lab, sk, ku, _ in cases:
        print(f"[3] MinTRL @ SR=1.0, {lab}: {min_trl(sr_hat, 0, sk, ku):.0f} months "
              f"| PSR at 36m = {psr(sr_hat, 36, 0, sk, ku):.3f}")


# --------------------------------------------------------------------------
# 4. Deflated Sharpe ratio
# --------------------------------------------------------------------------
def sr_star(n_trials, sr_var, t):
    """The benchmark a selected Sharpe must beat: the expected maximum Sharpe
    across n_trials under the null. sr_var = variance of the trial Sharpes
    (per-observation units)."""
    return np.sqrt(sr_var) * expected_max_gumbel(n_trials)


def dsr(sr_hat, n_trials, sr_var, t, skew=0.0, kurt=3.0):
    return psr(sr_hat, t, sr_star(n_trials, sr_var, t), skew, kurt)


def fig_dsr():
    n_grid = np.logspace(np.log10(2), 3.7, 200)
    sr_var = 1 / T_DAYS                      # null: sd(SR) = 1/sqrt(T)
    observed_ann = 1.5
    sr_hat = observed_ann / ANN

    fig, ax = plt.subplots(1, 2, figsize=(12.5, 4.4))

    thr = sr_star(n_grid, sr_var, T_DAYS) * ANN
    ax[0].plot(n_grid, thr, color=NAVY, lw=1.9, label="deflated threshold SR*")
    ax[0].fill_between(n_grid, 0, thr, color=NAVY, alpha=0.08)
    ax[0].axhline(observed_ann, color=RED, lw=1.6, ls="--",
                  label=f"observed selected Sharpe = {observed_ann}")
    cross = np.interp(observed_ann, thr, n_grid)
    ax[0].axvline(cross, color=GRAY, ls=":", lw=1.2)
    ax[0].annotate(f"at N ≈ {cross:,.0f} the threshold\nreaches the observed Sharpe\n(DSR = 0.50 — a coin flip)",
                   xy=(cross, observed_ann), xytext=(-12, -92), textcoords="offset points",
                   ha="right", fontsize=9, color="#444444")
    ax[0].set_xscale("log")
    ax[0].set_title("The bar rises with the size of the search")
    ax[0].set_xlabel("N — effective number of trials")
    ax[0].set_ylabel("annualized Sharpe")
    ax[0].legend(loc="upper left")

    n95 = None
    for lab, sk, ku, c in [("normal returns", 0.0, 3.0, BLUE),
                           ("γ₃ = −1.5, γ₄ = 8", -1.5, 8.0, RED)]:
        d = dsr(sr_hat, n_grid, sr_var, T_DAYS, sk, ku)
        ax[1].plot(n_grid, d, color=c, lw=1.8, label=lab)
        if n95 is None:
            n95 = np.interp(-0.95, -d, n_grid)   # d is decreasing; negate to sort
            ax[1].scatter([n95], [0.95], s=34, color=c, zorder=3)
            ax[1].annotate(f"significant at 95%\nonly up to N ≈ {n95:,.0f}",
                           xy=(n95, 0.95), xytext=(-8, -66), textcoords="offset points",
                           ha="right", fontsize=9, color="#444444")
    ax[1].axhline(0.95, color=ORANGE, ls=":", lw=1.3)
    ax[1].annotate("95%", xy=(n_grid[-1], 0.95), xytext=(-6, 5),
                   textcoords="offset points", ha="right", fontsize=9, color="#444444")
    ax[1].set_xscale("log")
    ax[1].set_title(f"DSR of a Sharpe-{observed_ann} strategy vs. trials run")
    ax[1].set_xlabel("N — effective number of trials")
    ax[1].set_ylabel("deflated Sharpe ratio")
    ax[1].set_ylim(0, 1.02)
    ax[1].legend(loc="lower left")

    fig.tight_layout()
    fig.savefig(OUT / "dsr.png")
    plt.close(fig)

    for n in (2, 10, 100, 1000):
        print(f"[4] N={n:>5}: SR* = {sr_star(n, sr_var, T_DAYS)*ANN:.2f} ann, "
              f"DSR(normal) = {dsr(sr_hat, n, sr_var, T_DAYS):.3f}, "
              f"DSR(fat/skew) = {dsr(sr_hat, n, sr_var, T_DAYS, -1.5, 8.0):.3f}")
    print(f"    breakeven N for SR={observed_ann}: {cross:,.0f}")


if __name__ == "__main__":
    fig_selection_bias()
    fig_pbo()
    fig_psr()
    fig_dsr()
    print("\nfigures written to", OUT)
