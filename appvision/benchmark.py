"""Benchmark: where a live app stands against apps of the same category and age.

Purely descriptive (percentiles from the June 2021 snapshot), so it needs no model and
makes no prediction.
"""

import numpy as np
import pandas as pd

AGE_BANDS = [
    (0, 91, "0–3 months"),
    (91, 183, "3–6 months"),
    (183, 366, "6–12 months"),
    (366, 731, "1–2 years"),
    (731, 1096, "2–3 years"),
    (1096, 1826, "3–5 years"),
]
AGE_LABELS = [label for _, _, label in AGE_BANDS]
PERCENTILES = np.arange(1, 100)

METRICS = {
    "installs": "Installs",
    "ratings_per_1k": "Ratings per 1,000 installs",
    "rating": "Star rating",
}


def age_band_of(days):
    for i, (lo, hi, _) in enumerate(AGE_BANDS):
        if lo <= days < hi:
            return i
    return len(AGE_BANDS) - 1 if days >= AGE_BANDS[-1][0] else 0


class Benchmarks:
    def __init__(self, table):
        """table columns: category, age_band (index), metric, peers, p1 … p99."""
        self.table = table.set_index(["category", "age_band", "metric"]).sort_index()

    def curve(self, category, age_band, metric):
        key = (category, age_band, metric)
        if key not in self.table.index:
            return None, 0
        row = self.table.loc[key]
        values = row[[f"p{p}" for p in PERCENTILES]].to_numpy(dtype="float64")
        return values, int(row["peers"])

    def percentile(self, category, age_band, metric, value):
        """Share of peers (0-100) with a lower value. None when there are too few peers."""
        values, peers = self.curve(category, age_band, metric)
        if values is None or peers < 30:
            return None, peers
        if metric == "installs":
            values, value = np.log10(values + 1), np.log10(value + 1)
        if value <= values[0]:
            return float(PERCENTILES[0] / 2), peers
        if value >= values[-1]:
            return 99.5, peers
        # collapse ties so interpolation stays well defined on flat stretches of the curve
        uniq, idx = np.unique(values, return_index=True)
        return float(np.interp(value, uniq, PERCENTILES[idx])), peers

    def median(self, category, age_band, metric):
        values, peers = self.curve(category, age_band, metric)
        return (None, peers) if values is None else (float(values[49]), peers)


def build_table(df, categories, min_peers=30):
    """Percentile curves per category × age band for each metric (used by notebook 04)."""
    age_idx = df["age_days"].apply(age_band_of) if len(df) < 1000 else pd.cut(
        df["age_days"], [lo for lo, _, _ in AGE_BANDS] + [AGE_BANDS[-1][1]], right=False, labels=False)
    work = pd.DataFrame({
        "category": df["category"].astype(str).to_numpy(),
        "age_band": age_idx.to_numpy(),
        "installs": df["installs"].to_numpy(dtype="float64"),
        "ratings_per_1k": np.where(df["installs"] >= 100, df["rating_count"] / df["installs"].clip(lower=1) * 1000, np.nan),
        "rating": np.where(df["rating_count"] >= 10, df["rating"], np.nan),
    }).dropna(subset=["age_band"])
    rows = []
    for (cat, band), grp in work.groupby(["category", "age_band"], sort=True):
        for metric in METRICS:
            vals = grp[metric].dropna().to_numpy()
            if len(vals) < min_peers:
                continue
            q = np.percentile(vals, PERCENTILES)
            rows.append({"category": cat, "age_band": int(band), "metric": metric, "peers": len(vals),
                         **{f"p{p}": float(v) for p, v in zip(PERCENTILES, q)}})
    return pd.DataFrame(rows)
