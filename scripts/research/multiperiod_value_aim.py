"""Figure for the post "Is Multi-Period Optimization Worth It?".

The mechanism figure: in the linear-quadratic trading problem both the myopic
and the dynamic-programming policies are "trade a fixed fraction of the way to
somewhere" rules.  They differ in the fraction and in the somewhere:

  myopic :  trade rate 1 - lam/(gamma+lam),  destination = the Markowitz target
  DP     :  trade rate 1 - c,                destination = the *aim*, an
            exponentially-weighted average of current and expected future
            Markowitz targets, which shrinks each alpha factor by
                (1-c) / (1 - c(1-phi))
            with phi the factor's per-period mean-reversion rate.

Both quantities are computed here from a scalar value iteration on the LQ
Bellman equation -- no closed form assumed.  With a diagonal, homogeneous
covariance the full n-asset recursion collapses to this scalar one exactly
(verified against quantlib.simulate.solve_dp: c = 0.6417424305 at gamma = 10,
lam/gamma = 5).

Run:  python3 scripts/research/multiperiod_value_aim.py
Out:  src/assets/research/multiperiod-value/aim_mechanism.png
"""

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parents[2] / "src/assets/research/multiperiod-value"
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
BLUE, PURPLE, GREEN, ORANGE, GRAY = "#2c6fbb", "#7d5ba6", "#3c9a5f", "#e8833a", "#8c8c8c"

GAMMA = 10.0            # risk aversion of the central calibration
CENTRAL_COST = 5.0      # lam / gamma
HL_FAST, HL_SLOW = 5.0, 30.0


def dp_persistence(cost_mult, gamma=GAMMA, tol=1e-14, max_iter=100_000):
    """Diagonal of the DP policy matrix P = c*I, by value iteration on the
    scalar LQ Bellman equation.  The value function is V = -(1/2) a x^2 + ...;
    iterating a to its fixed point gives c = lam / (gamma + lam + a)."""
    lam = cost_mult * gamma
    a = 0.0
    for _ in range(max_iter):
        c = lam / (gamma + lam + a)
        a_new = gamma * c**2 + lam * (c - 1) ** 2 + a * c**2
        if abs(a_new - a) < tol:
            a = a_new
            break
        a = a_new
    return lam / (gamma + lam + a)


def aim_shrinkage(c, half_life_d):
    """Weight the DP aim puts on a factor with the given half-life, relative to
    that factor's weight in the cost-free Markowitz target."""
    phi = 1 - np.exp(-np.log(2) / np.asarray(half_life_d, dtype=float))
    return (1 - c) / (1 - c * (1 - phi))


fig, axes = plt.subplots(1, 2, figsize=(12.4, 4.9))

# -- left: how hard each factor is discounted, by speed and by cost level ----
ax = axes[0]
hl = np.logspace(np.log10(0.7), np.log10(120), 400)
for cost_mult, color in ((1.0, GREEN), (CENTRAL_COST, PURPLE), (20.0, ORANGE)):
    c = dp_persistence(cost_mult)
    ax.plot(hl, aim_shrinkage(c, hl), color=color, lw=2.2,
            label=rf"$\lambda/\gamma$ = {cost_mult:g}  (trade rate {1-c:.2f}/day)")
c_central = dp_persistence(CENTRAL_COST)
for h, name, off, ha in ((HL_FAST, "fast factor, HL 5d", (-10, 10), "right"),
                         (HL_SLOW, "slow factor, HL 30d", (-4, 12), "right")):
    s = float(aim_shrinkage(c_central, h))
    ax.scatter([h], [s], s=60, color=PURPLE, zorder=5)
    ax.annotate(f"{name}\n{s:.2f}", (h, s), xytext=off, textcoords="offset points",
                ha=ha, fontsize=9, color=PURPLE)
ax.axhline(1.0, color=GRAY, ls="--", lw=1.2)
ax.text(0.85, 1.008, "myopic policy: every factor at full weight",
        fontsize=9, color=GRAY)
ax.set_xscale("log")
ax.set_xticks([1, 2, 5, 10, 20, 50, 100])
ax.set_xticklabels([1, 2, 5, 10, 20, 50, 100])
ax.set_xlim(0.8, 120)
ax.set_ylim(0, 1.12)
ax.set_xlabel("alpha factor half-life (trading days)")
ax.set_ylabel("weight in the DP aim ÷ weight in the Markowitz target")
ax.set_title("The DP mutes fast alpha")
ax.legend(loc="lower right")

# -- right: how fast each policy closes the gap to its destination -----------
ax = axes[1]
cm = np.logspace(np.log10(0.2), np.log10(50), 200)
dp_rate = np.array([1 - dp_persistence(x) for x in cm])
my_rate = 1 / (1 + cm)                       # 1 - lam/(gamma+lam)
ax.plot(cm, 100 * dp_rate, color=PURPLE, lw=2.4, label="DP (toward its aim)")
ax.plot(cm, 100 * my_rate, color=BLUE, lw=2.4,
        label="myopic (toward the full target)")
ax.fill_between(cm, 100 * my_rate, 100 * dp_rate, color=PURPLE, alpha=0.10)
ax.axvline(CENTRAL_COST, color=GRAY, ls=":", lw=1.2)
ax.annotate(f"central calibration\nDP {100*(1-c_central):.0f}%/day vs myopic "
            f"{100/(1+CENTRAL_COST):.0f}%/day",
            (CENTRAL_COST, 100 * (1 - c_central)), xytext=(8, 26),
            textcoords="offset points", fontsize=9, color="#444444",
            arrowprops=dict(arrowstyle="->", color="#888888", lw=0.9))
ax.set_xscale("log")
ax.set_xticks([0.2, 0.5, 1, 2, 5, 10, 20, 50])
ax.set_xticklabels([0.2, 0.5, 1, 2, 5, 10, 20, 50])
ax.set_yscale("log")
ax.set_yticks([2, 5, 10, 20, 50, 100])
ax.set_yticklabels(["2%", "5%", "10%", "20%", "50%", "100%"])
ax.set_xlabel(r"transaction-cost scale  $\lambda/\gamma$")
ax.set_ylabel("share of the gap closed per day")
ax.set_title("…and gets there faster")
ax.legend(loc="lower left")

fig.suptitle("Two 'trade partway there' rules: the DP trades faster, toward a nearer "
             "destination", fontsize=13, y=1.03)
fig.tight_layout()
path = OUT / "aim_mechanism.png"
fig.savefig(path)
print("wrote", path)

# -- numbers quoted in the post ---------------------------------------------
print(f"c (lam/gamma={CENTRAL_COST:g}) = {c_central:.10f}  "
      f"DP trade rate = {1-c_central:.4f}, myopic = {1/(1+CENTRAL_COST):.4f}")
for h in (HL_FAST, HL_SLOW):
    print(f"  aim shrinkage at HL {h:g}d: {float(aim_shrinkage(c_central, h)):.4f}")
