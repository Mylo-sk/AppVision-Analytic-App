"""Launch Outlook: score app concepts with the trained model and express the answer plainly."""

import json
from dataclasses import dataclass, replace
from pathlib import Path

import numpy as np
import pandas as pd
import xgboost as xgb

from . import bands, features, names


@dataclass(frozen=True)
class Concept:
    """An app idea described with things a studio knows before launch."""
    title: str
    category: str
    price_usd: float = 0.0
    ad_supported: bool = False
    in_app_purchases: bool = False
    size_mb: float | None = 25.0
    content_rating: str = "Everyone"
    min_android: float | None = 6.0
    has_website: bool = True
    has_privacy: bool = True
    prior_apps: int = 0
    prior_typical_band: int | None = None
    horizon_days: int = 365

    def to_row(self, idf, coef, intercept):
        prior_log = (np.log10(bands.BAND_TYPICAL[self.prior_typical_band] + 1)
                     if self.prior_apps > 0 and self.prior_typical_band is not None else np.nan)
        return {
            "category": self.category,
            "content_rating": self.content_rating,
            "free": float(self.price_usd <= 0),
            "price_usd": float(max(self.price_usd, 0.0)),
            "ad_supported": float(self.ad_supported),
            "in_app_purchases": float(self.in_app_purchases),
            "size_mb": np.nan if self.size_mb is None else float(self.size_mb),
            "size_varies": float(self.size_mb is None),
            "min_android": np.nan if self.min_android is None else float(self.min_android),
            "min_android_varies": float(self.min_android is None),
            "has_website": float(self.has_website),
            "has_privacy": float(self.has_privacy),
            "dev_prior_apps": float(self.prior_apps),
            "dev_prior_log_installs": prior_log,
            "name_signal": float(names.name_signal([self.title], idf, coef, intercept)[0]),
            "name_words": float(names.word_count([self.title])[0]),
            "age_days": float(self.horizon_days),
        }


# Single changes a studio could actually make, used by the what-if panel
def what_if_variants(c: Concept):
    out = []
    if c.price_usd > 0:
        out.append(("Make it free to download", replace(c, price_usd=0.0)))
    else:
        out.append(("Charge $2.99 up front", replace(c, price_usd=2.99)))
    out.append(("Remove ads" if c.ad_supported else "Add ads", replace(c, ad_supported=not c.ad_supported)))
    out.append(("Remove in-app purchases" if c.in_app_purchases else "Add in-app purchases",
                replace(c, in_app_purchases=not c.in_app_purchases)))
    if c.size_mb is not None and c.size_mb > 10:
        out.append((f"Cut the download to {c.size_mb / 2:.0f} MB", replace(c, size_mb=c.size_mb / 2)))
    if not c.has_privacy:
        out.append(("List a privacy policy", replace(c, has_privacy=True)))
    if not c.has_website:
        out.append(("List a studio website", replace(c, has_website=True)))
    return out


class LaunchOutlook:
    def __init__(self, artifacts_dir):
        d = Path(artifacts_dir)
        self.booster = xgb.Booster()
        self.booster.load_model(d / "outlook_model.ubj")
        self.meta = json.loads((d / "outlook_meta.json").read_text(encoding="utf-8"))
        self.idf = np.load(d / "name_idf.npy")
        self.coef = np.load(d / "name_coef.npy")
        self.intercept = float(self.meta["name_model"]["intercept"])

    def band_probs(self, concepts):
        rows = pd.DataFrame([c.to_row(self.idf, self.coef, self.intercept) for c in concepts])
        X = features.to_model_frame(rows)
        return self.booster.predict(xgb.DMatrix(X, enable_categorical=True))

    def typical(self, category, horizon_days):
        """Band mix of apps in the same category at the same age (the 'just ask the store' baseline)."""
        age_idx = int(np.searchsorted(self.meta["base_rates"]["age_edges"], horizon_days, side="right") - 1)
        age_idx = min(max(age_idx, 0), len(self.meta["base_rates"]["age_edges"]) - 2)
        table = self.meta["base_rates"]["by_category"]
        return np.array(table.get(category, table["__all__"])[age_idx])

    def what_if(self, concept):
        variants = what_if_variants(concept)
        probs = self.band_probs([concept] + [v for _, v in variants])
        base = bands.reach_odds(probs[:1])[0]
        rows = []
        for (label, _), p in zip(variants, probs[1:]):
            odds = bands.reach_odds(p[None, :])[0]
            rows.append({"change": label, "before": base, "after": odds})
        return rows


def per_hundred(p):
    """Probabilities to whole apps out of 100 that sum to exactly 100 (largest remainder)."""
    raw = np.asarray(p, dtype="float64") * 100
    base = np.floor(raw).astype(int)
    short = 100 - base.sum()
    order = np.argsort(-(raw - base))
    base[order[:short]] += 1
    return base


def one_in(p):
    """'about 1 in 8' phrasing for a probability."""
    if p >= 0.5:
        return f"about {round(p * 10)} in 10"
    if p <= 0.0005:
        return "fewer than 1 in 2,000"
    n = 1 / p
    if n < 10:
        return f"about 1 in {n:.0f}"
    step = 5 if n < 50 else 10 if n < 200 else 50 if n < 1000 else 100
    return f"about 1 in {int(round(n / step) * step):,}"


def most_likely_band(p):
    return int(np.argmax(p))


def median_band(p):
    """Band where the cumulative chance first passes 50% (the 'typical outcome')."""
    return int(np.searchsorted(np.cumsum(p), 0.5))
