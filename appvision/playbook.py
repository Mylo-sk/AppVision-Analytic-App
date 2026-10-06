"""Playbook: find real apps that resemble a concept, then compare the ones that broke out
(100K+ installs) with the ones that didn't.

The pool keeps every breakout app that had been live for at least a year, plus a random
sample of the rest. `weight` records how many real apps each sampled row stands for, so
breakout rates stay true to the full store.
"""

import numpy as np
import pandas as pd

from . import bands, names

MIN_CLOSE_MATCHES = 40


def _weighted_median(values, weights):
    mask = ~np.isnan(values)
    if not mask.any():
        return np.nan
    v, w = values[mask], weights[mask]
    order = np.argsort(v)
    cum = np.cumsum(w[order])
    return float(v[order][np.searchsorted(cum, cum[-1] / 2)])


# (label, column, kind) — kind "share" compares yes/no rates, "median" compares typical values
ATTRIBUTES = [
    ("Free to download", "free", "share"),
    ("Shows ads", "ad_supported", "share"),
    ("Offers in-app purchases", "in_app_purchases", "share"),
    ("Lists a privacy policy", "has_privacy", "share"),
    ("Lists a studio website", "has_website", "share"),
    ("Studio had published apps before", "has_prior_apps", "share"),
    ("Updated in the 6 months before the snapshot", "updated_recently", "share"),
    ("Rated for everyone", "rated_everyone", "share"),
    ("Download size", "size_mb", "median"),
    ("Minimum Android version", "min_android", "median"),
    ("Star rating", "rating_rated", "median"),
]


class Playbook:
    def __init__(self, pool, name_matrix, idf):
        """pool must be sorted by category; name_matrix rows align with pool rows."""
        self.pool = pool.reset_index(drop=True)
        self.X = name_matrix.tocsr()
        self.idf = idf
        cats = self.pool["category"].astype(str).to_numpy()
        self._slices = {}
        for cat in pd.unique(cats):
            hits = np.flatnonzero(cats == cat)
            self._slices[cat] = (hits[0], hits[-1] + 1)
        p = self.pool
        p["has_prior_apps"] = (p["dev_prior_apps"] > 0).astype("float32")
        p["updated_recently"] = (p["days_since_update"] <= 182).astype("float32")
        p["rated_everyone"] = (p["content_rating"].astype(str) == "Everyone").astype("float32")
        p["rating_rated"] = p["rating"].where(p["rating_count"] >= 10)

    def lookalikes(self, category, description, k=300, min_similarity=0.2):
        """Apps in the same category whose names read most like the description.

        Falls back to the whole category when the description matches too few names.
        Returns (frame, is_close_match).
        """
        start, end = self._slices[category]
        block = self.pool.iloc[start:end]
        sims = np.zeros(end - start, dtype=np.float32)
        if description and description.strip():
            q = names.tfidf([description], self.idf)
            sims = np.asarray((self.X[start:end] @ q.T).todense()).ravel()
        close = sims >= min_similarity
        if close.sum() >= MIN_CLOSE_MATCHES:
            top = np.flatnonzero(close)
            top = top[np.argsort(-sims[top])][:k]
            out = block.iloc[top].copy()
            out["similarity"] = sims[top]
            return out, True
        out = block.copy()
        out["similarity"] = sims
        return out, False

    @staticmethod
    def breakout_rate(frame):
        w = frame["weight"].to_numpy()
        b = frame["breakout"].to_numpy().astype(bool)
        return float(w[b].sum() / w.sum()) if w.sum() else np.nan

    @staticmethod
    def represented_apps(frame):
        return int(round(frame["weight"].sum()))

    @staticmethod
    def compare(frame):
        """Breakouts vs the rest on each attribute, with a plain-language note when the gap is real."""
        b = frame[frame["breakout"]]
        o = frame[~frame["breakout"]]
        rows = []
        for label, col, kind in ATTRIBUTES:
            if kind == "share":
                vb, vo = float(b[col].mean()), float(o[col].mean())
            else:
                vb = _weighted_median(b[col].to_numpy(dtype="float64"), np.ones(len(b)))
                vo = _weighted_median(o[col].to_numpy(dtype="float64"), np.ones(len(o)))
            rows.append({"attribute": label, "column": col, "kind": kind, "breakouts": vb, "others": vo,
                         "note": _note(label, col, kind, vb, vo)})
        return pd.DataFrame(rows)

    @staticmethod
    def top_breakouts(frame, n=10):
        b = frame[frame["breakout"]].sort_values(["similarity", "installs"], ascending=False).head(n)
        return b


SHARE_VERBS = {
    "free": "were free to download",
    "ad_supported": "showed ads",
    "in_app_purchases": "offered in-app purchases",
    "has_privacy": "listed a privacy policy",
    "has_website": "listed a studio website",
    "has_prior_apps": "came from a studio with earlier apps",
    "updated_recently": "had been updated in the six months before the snapshot",
    "rated_everyone": "were rated for everyone",
}


def _note(label, col, kind, vb, vo):
    if np.isnan(vb) or np.isnan(vo):
        return ""
    if kind == "share":
        gap = vb - vo
        if abs(gap) < 0.08 or max(vb, vo) / max(min(vb, vo), 1e-6) < 1.25:
            return ""
        return f"{vb:.0%} of breakouts {SHARE_VERBS[col]}, against {vo:.0%} of the rest."
    if col == "size_mb":
        if max(vb, vo) / max(min(vb, vo), 1e-6) < 1.3:
            return ""
        word = "larger" if vb > vo else "smaller"
        return f"Breakouts tended to be {word}: about {vb:,.0f} MB vs {vo:,.0f} MB."
    if col == "rating_rated":
        if abs(vb - vo) < 0.2:
            return ""
        word = "higher" if vb > vo else "lower"
        return f"Breakouts were rated {word}: {vb:.1f} vs {vo:.1f} stars."
    if col == "min_android":
        if abs(vb - vo) < 0.5:
            return ""
        word = "newer" if vb > vo else "older"
        return f"Breakouts required {word} Android versions: {vb:.1f} vs {vo:.1f}."
    return ""


def installs_label(installs_floor):
    v = float(installs_floor)
    for div, suffix in [(1e9, "B"), (1e6, "M"), (1e3, "K")]:
        if v >= div:
            return f"{v / div:g}{suffix}+"
    return f"{v:,.0f}+"


def setup_label(row):
    parts = ["Free" if row["free"] else f"${row['price_usd']:.2f}"]
    if row["ad_supported"]:
        parts.append("ads")
    if row["in_app_purchases"]:
        parts.append("in-app purchases")
    return " · ".join(parts)


def store_link(app_id):
    return f"https://play.google.com/store/apps/details?id={app_id}"
