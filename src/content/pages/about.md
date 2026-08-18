---
title: "About"
description: "Jiawen Yan — systematic quant researcher building and publishing a fund-grade research platform, negative results included."
---

I’m a quant guy interested in systematic investing, portfolio construction,
financial planning and the occasional optimization problem that behaves nicely.

By day, I work on turning noisy financial data into models and hopefully useful
decisions. By night, I read papers, build side projects, and convince myself that
one more backtest is statistically justified.

Outside of work, I like to keep things equally structured and competitive: I
enjoy long, intensive 70-mile road bike rides on Saturday mornings up 9W, have
played soccer since I was a kid, and got completely obsessed with tennis about
four years ago.

This site is where I keep research notes, experiments, and ideas on quantitative
investing, optimization, factor models, simulation, and whatever else I’m
currently overthinking.

## The positioning

The quant-content space has two saturated modes: backtest porn (fake Sharpes,
selling courses) and academic papers (rigorous but unreadable). The empty seat in
the middle is the practitioner voice that says: *I built the full stack, ran the
honest tests, and here is what died — with the deflation math.*

That's the whole brand. Every finding here is either a mechanism that survived
scrutiny or a plausible edge that didn't — reported with the statistics that tell
the two apart (deflated Sharpe, PBO, out-of-sample gates). Publishing negatives is
free; any signal that ever survives the harness stays private.

## The platform

Behind the posts is a layered, tested research stack — the kind of thing that's
rare outside institutional settings — built from scratch:

- **Risk** — a Barra-style structural factor risk model (`Σ = B·F·Bᵀ + Δ`),
  point-in-time exposures, WLS factor returns, shrinkage factor covariance.
- **Construction** — decay-aware signal weighting, a cost-penalised QP with
  optional multi-period look-ahead, constraint shadow prices, and return/risk
  attribution that reconciles to machine precision.
- **Validation** — an anti-overfit harness: freeze-date holdout, walk-forward
  folds, probabilistic & deflated Sharpe, and PBO via CSCV. A trials ledger charges
  the honesty bar for every backtest run.
- **Capacity & regimes** — strategy capacity curves under a calibrated cost model,
  and a from-scratch Gaussian HMM for regime-conditional risk control.
- **Execution** — backtest/paper parity: the same decision code runs in both, with
  only the data source and broker swapped.

## Elsewhere

- GitHub — [@jiawenyannyc](https://github.com/jiawenyannyc)
- LinkedIn — [Gavin Yan](https://www.linkedin.com/in/jiawen-gavin-yan-8364a0144/)
- Email — [jiawenyannyc@gmail.com](mailto:jiawenyannyc@gmail.com)

*Views are my own. Results, unfortunately, are also my own. Nothing here is
investment advice or a solicitation — it’s research and education.*
