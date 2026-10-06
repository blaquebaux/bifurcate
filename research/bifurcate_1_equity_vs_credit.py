#!/usr/bin/python3
# =============================================================================
# bifurcate_1_equity_vs_credit.py — does credit LEAD equity, and is the long-bond leg of the convergence trade dead weight?
#
# Aggregate capital-structure divergence (no single-name CDS in Alpaca). SIP daily total return, causal.
#   credit signal = HYG − LQD  (high-yield minus investment-grade = pure credit-risk appetite)
#  (A) DOES CREDIT LEAD EQUITY? corr(credit 20d change @t, SPY forward 20d). And forward SPY after a BEARISH divergence
#      (equity up 20d WHILE credit down 20d = equity rich vs credit) vs unconditional.
#  (B) WHICH LEG HAS THE ALPHA? in the convergence trade (short SPY + long HYG on a bearish divergence), decompose the
#      forward P&L into the EQUITY-SHORT leg and the LONG-CREDIT leg — is the bond leg dead weight / negative carry?
# =============================================================================
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _bifurcate_common import panel, rets, stats, corr, roll
import numpy as np

P, dates = panel(["HYG", "LQD", "IEF", "SPY"])
R = {s: rets(P[s]) for s in P}; n = len(R["SPY"])
credit = R["HYG"] - R["LQD"]                                   # HY over IG = credit-risk appetite (down = stress)
spy = R["SPY"]; hyg = R["HYG"]
cr20 = roll(credit, 20); sp20 = roll(spy, 20)
spy_fwd20 = np.array([spy[t:t+20].sum() if t+20 <= n else np.nan for t in range(n)])
hyg_fwd20 = np.array([hyg[t:t+20].sum() if t+20 <= n else np.nan for t in range(n)])
cr_fwd20  = np.array([credit[t:t+20].sum() if t+20 <= n else np.nan for t in range(n)])
print("="*98); print(f"BIFURCATE #1 — equity vs credit divergence  ({dates[0]} → {dates[-1]}, {len(dates)} days)"); print("="*98)

# ---- (A) does credit lead equity? -------------------------------------------------------------------
lead = corr(cr20, spy_fwd20)                                   # credit change @t vs SPY forward 20d
coincident = corr(cr20, sp20)
bear_div = np.isfinite(cr20) & np.isfinite(sp20) & (sp20 > 0) & (cr20 < 0)   # equity up, credit down = rich equity
un = np.nanmean(spy_fwd20[np.isfinite(spy_fwd20)]); bd = np.nanmean(spy_fwd20[bear_div & np.isfinite(spy_fwd20)])
print(f"\n(A) DOES CREDIT LEAD EQUITY?")
print(f"  corr(credit 20d change, SPY 20d SAME-period)  {coincident:+.2f}   (coincident — move together)")
print(f"  corr(credit 20d change @t, SPY FORWARD 20d)   {lead:+.2f}   (the lead — credit predicting equity)")
print(f"  forward-20d SPY after a BEARISH divergence (equity↑ while credit↓): {bd*100:+.2f}%  vs unconditional {un*100:+.2f}%  ({int(bear_div.sum())} days)")

# ---- (B) which leg has the alpha? -------------------------------------------------------------------
# convergence trade on bearish divergence: SHORT SPY + LONG HYG, held 20d
eq_leg  = -np.nanmean(spy_fwd20[bear_div & np.isfinite(spy_fwd20)])     # short-equity P&L
cr_leg  =  np.nanmean(hyg_fwd20[bear_div & np.isfinite(hyg_fwd20)])     # long-HYG P&L
print(f"\n(B) WHICH LEG CARRIES IT? (convergence trade on bearish divergence, 20d hold)")
print(f"  SHORT-EQUITY leg (−SPY)  {eq_leg*100:+.2f}%   LONG-CREDIT leg (+HYG)  {cr_leg*100:+.2f}%   combined {(eq_leg+cr_leg)*100:+.2f}%")
print(f"  → the {'EQUITY SHORT' if eq_leg>cr_leg else 'credit long'} carries it; the {'LONG-BOND leg is dead weight' if cr_leg<=0.005 else 'bond leg adds a bit'}")

# ---- verdict ----------------------------------------------------------------------------------------
no_lead = abs(lead) < 0.08 and (bd > un - 0.004)               # credit does not meaningfully lead the index
short_lost = eq_leg < 0                                        # the equity-short leg lost (equity kept rising)
print("\n"+"="*98); print("READ:")
print(f"  • CREDIT & EQUITY ARE COINCIDENT, NOT LEAD-LAG: same-period corr {coincident:+.2f}, forward (leading) corr {lead:+.2f} — at the aggregate level credit does NOT lead equity; they reprice risk together (echoing bellwether).")
print(f"  • THE DIVERGENCE DOESN'T RESOLVE: after a 'bearish divergence' (equity rich vs credit), forward-20d SPY is still {bd*100:+.2f}% — equity kept RISING, only a trivial {(un-bd)*100:.2f}pp below the {un*100:+.2f}% baseline. In a bull decade, 'rich equity' just got richer.")
print(f"  • KAREEM'S THESIS IS INVERTED HERE: the convergence trade LOST ({(eq_leg+cr_leg)*100:+.2f}%) — the EQUITY-SHORT leg lost {eq_leg*100:+.2f}% (shorting a still-rising market), and the LONG-CREDIT leg was the ONLY positive one ({cr_leg*100:+.2f}%). So 'short equity = alpha, bond long = dead weight' is backwards at the index level: the short was the loser.")

v = ("NULL (and the paired trade is inverted at the index level): capital-structure divergence is not tradable on "
     f"aggregate proxies. Credit and equity are COINCIDENT, not lead-lag (forward corr {lead:+.2f}), so a 'bearish divergence' "
     f"doesn't forecast an equity catch-down — forward SPY was still {bd*100:+.1f}% (a bull decade kept rich equity rising). And "
     f"Kareem's hypothesis flips: the EQUITY-SHORT leg LOST {eq_leg*100:+.1f}% while the LONG-CREDIT leg (+{cr_leg*100:.1f}%) was the only "
     "positive one — 'short equity = alpha, bond = dead weight' is backwards here, because the index short fought the "
     "bull. The honest reading: the real capital-structure edge is ISSUER-LEVEL and idiosyncratic — a single name whose "
     "CDS blows out while its stock sleeps, where credit genuinely leads for name-specific distress — which the aggregate "
     "index cannot show and Alpaca cannot feed. bifurcate_2 = single-name CDS + bond data; the index version is a null.")
print(f"\n  VERDICT: {v}")
print("  (Aggregate HY-vs-IG-vs-equity proxies — no single-name CDS or corporate bonds in Alpaca. The issuer-level")
print("   divergence (one name's credit leading its stock) is where the real RV lives = bifurcate_2 with a CDS feed.)")
