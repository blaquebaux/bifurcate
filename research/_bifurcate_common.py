#!/usr/bin/python3
# =============================================================================
# _bifurcate_common.py — shared helpers for Blaque Baux BIFURCATE (capital-structure divergence: equity vs credit).
# Alpaca SIP daily bars (adjustment=all → total return); env keys. Read-only.
#
# Capital-structure RV: when the credit market signals distress (spreads widening) but equity stays buoyant, short the
# equity / long the bond, betting on convergence. BIFURCATE tests Kareem's null: bond markets are less liquid and
# often price distress EARLIER — so is the "divergence" a RATIONAL bond-market LEAD, meaning the EQUITY SHORT is the
# only leg with alpha while the LONG-bond leg is dead weight with negative carry? HARD LIMIT: no single-name CDS or
# corporate bonds in Alpaca, so issuer-level divergence is out of reach (= bifurcate_2). We test the AGGREGATE version
# — HY credit (HYG vs IG LQD) vs equity (SPY) — asking (1) does credit LEAD equity, and (2) in the convergence trade,
# which leg carries the P&L: the equity short (alpha) or the long credit/bond (dead weight)? basic covers convert-arb;
# this is the debt-vs-equity-pricing angle it didn't.
# =============================================================================
import os, json, urllib.request, math
import numpy as np

H = {"APCA-API-KEY-ID": os.environ["ALPACA_KEY_ID"], "APCA-API-SECRET-KEY": os.environ["ALPACA_SECRET_KEY"]}
START, END = "2016-01-01", "2026-08-01"
_cache = {}

def bars(s):
    if s in _cache: return _cache[s]
    u = (f"https://data.alpaca.markets/v2/stocks/bars?symbols={s}&timeframe=1Day"
         f"&start={START}&end={END}&adjustment=all&feed=sip&limit=10000")
    try:
        d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=40))
        _cache[s] = {b["t"][:10]: b["c"] for b in d.get("bars", {}).get(s, [])}
    except Exception:
        _cache[s] = {}
    return _cache[s]

def panel(syms):
    D = {s: bars(s) for s in syms}; D = {s: v for s, v in D.items() if len(v) > 250}
    if not D: return {}, []
    u = [s for s in syms if s in D]; dates = sorted(set.intersection(*[set(D[s]) for s in u]))
    return {s: np.array([D[s][d] for d in dates], float) for s in u}, dates

def rets(px): return px[1:] / px[:-1] - 1

def stats(r):
    r = np.asarray(r, float); r = r[np.isfinite(r)]
    if len(r) < 20 or r.std() == 0: return dict(sh=float('nan'), cagr=float('nan'), dd=float('nan'), vol=float('nan'))
    cum = np.cumprod(1 + r)
    return dict(sh=r.mean()/r.std()*math.sqrt(252), cagr=cum[-1]**(252/len(r))-1,
                dd=float((cum/np.maximum.accumulate(cum)-1).min()), vol=r.std()*math.sqrt(252))

def corr(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float); m = np.isfinite(a) & np.isfinite(b)
    return float(np.corrcoef(a[m], b[m])[0, 1]) if m.sum() > 30 else float('nan')

def roll(x, w):
    x = np.asarray(x, float); n = len(x); o = np.full(n, np.nan)
    for t in range(w, n): o[t] = x[t-w:t].sum()
    return o
