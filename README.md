# Blaque Baux Bifurcate

**Capital-structure divergence (equity vs credit) — is the divergence a rational bond-market lead where only the equity short has alpha? At the index level it's a null, and the thesis actually inverts.**

Capital-structure RV: when credit signals distress but equity stays buoyant, short equity / long bond on convergence.
Bifurcate tests Kareem's null: bonds often price distress earlier, so is the "divergence" a *rational bond lead* —
meaning the **equity short is the only leg with alpha** and the **long-bond leg is dead weight**? **Hard limit:** no
single-name CDS or corporate bonds in Alpaca, so issuer-level divergence is out of reach; we test the **aggregate**
version (HY credit via HYG−LQD vs equity SPY). `basic` covers convert-arb; this is the debt-vs-equity-pricing angle.

> **Not investment advice.** Educational/research software. See [DISCLAIMER](DISCLAIMER.md) and [LICENSE](LICENSE).

```bash
python3 research/bifurcate_1_equity_vs_credit.py   # needs Alpaca data keys in the environment
```

## The finding (null — and the thesis inverts)

[`research/bifurcate_1_equity_vs_credit.py`](research/bifurcate_1_equity_vs_credit.py) — SIP daily total return, causal.

- **Credit & equity are coincident, not lead-lag** — same-day corr **+0.25**, forward (leading) corr **−0.06**. At the
  aggregate level credit does *not* lead equity (echoing `bellwether`).
- **The divergence doesn't resolve** — after a "bearish divergence" (equity rich vs credit), forward-20d SPY was still
  **+1.01%**, only a trivial 0.27pp below the +1.27% baseline. In a bull decade, rich equity just got richer.
- **Kareem's thesis inverts here** — the convergence trade **lost (−0.54%)**: the equity-short leg lost **−1.01%**
  (shorting a still-rising market) while the long-credit leg was the *only positive one* (**+0.47%**). "Short equity =
  alpha, bond = dead weight" is *backwards* at the index level — the short was the loser, because it fought the bull.

## Verdict

**NULL — not tradable on aggregate proxies, and the paired trade inverts.** Credit and equity reprice risk *together*,
so a bearish divergence doesn't forecast an equity catch-down, and shorting the index just fought a bull market. The real
capital-structure edge is **issuer-level and idiosyncratic** — a single name whose CDS blows out while its stock sleeps,
where credit genuinely leads for name-specific distress — which the aggregate index can't show and Alpaca can't feed. A
`bifurcate_2` needs single-name CDS + bond data; the index version is a null.

## Status

**Research.** Honest null — a capital-structure thesis tested at the only level the data allows (aggregate), found
non-predictive, with the paired-trade inversion and the issuer-level data gap stated plainly. Lead-lag correlation,
divergence-conditional forward returns, leg decomposition, Alpaca SIP daily total return. No live capital.
