"""Launch-time feature contract.

Every input here is something a studio knows before its app goes live. Ratings, rating
counts, Editors' Choice and update history only exist after launch, so they are kept out
of the Launch Outlook model on purpose (they power the Benchmark page instead).
"""

import numpy as np
import pandas as pd

CATEGORIES = [
    "Action", "Adventure", "Arcade", "Art & Design", "Auto & Vehicles", "Beauty", "Board",
    "Books & Reference", "Business", "Card", "Casino", "Casual", "Comics", "Communication",
    "Dating", "Education", "Educational", "Entertainment", "Events", "Finance", "Food & Drink",
    "Health & Fitness", "House & Home", "Libraries & Demo", "Lifestyle", "Maps & Navigation",
    "Medical", "Music", "Music & Audio", "News & Magazines", "Parenting", "Personalization",
    "Photography", "Productivity", "Puzzle", "Racing", "Role Playing", "Shopping", "Simulation",
    "Social", "Sports", "Strategy", "Tools", "Travel & Local", "Trivia",
    "Video Players & Editors", "Weather", "Word",
]

CONTENT_RATINGS = ["Everyone", "Everyone 10+", "Teen", "Mature 17+", "Adults only 18+"]

CATEGORICAL = ["category", "content_rating"]
NUMERIC = [
    "free", "price_usd", "ad_supported", "in_app_purchases",
    "size_mb", "size_varies", "min_android", "min_android_varies",
    "has_website", "has_privacy",
    "dev_prior_apps", "dev_prior_log_installs",
    "name_signal", "name_words",
    "age_days",
]
FEATURES = CATEGORICAL + NUMERIC

# Plain-language names for charts and the app
FEATURE_LABELS = {
    "category": "Category",
    "content_rating": "Age rating",
    "free": "Free to download",
    "price_usd": "Price",
    "ad_supported": "Shows ads",
    "in_app_purchases": "In-app purchases",
    "size_mb": "Download size",
    "size_varies": "Size varies by device",
    "min_android": "Minimum Android version",
    "min_android_varies": "Android version varies by device",
    "has_website": "Studio website listed",
    "has_privacy": "Privacy policy listed",
    "dev_prior_apps": "Apps the studio published before",
    "dev_prior_log_installs": "Typical installs of the studio's earlier apps",
    "name_signal": "Wording of the app name",
    "name_words": "Words in the app name",
    "age_days": "Time on the store",
}

FX_TO_USD = {
    "USD": 1.00, "EUR": 1.10, "INR": 0.012, "GBP": 1.29, "CAD": 0.73, "VND": 0.000042,
    "BRL": 0.19, "KRW": 0.00077, "TRY": 0.033, "RUB": 0.011, "SGD": 0.74, "AUD": 0.67,
    "PKR": 0.0036, "ZAR": 0.055,
}


def parse_size_mb(size):
    """'10M' -> 10.0, '512k' -> 0.5, '1.2G' -> 1228.8, 'Varies with device' -> NaN."""
    s = pd.Series(size, dtype="string").str.strip().str.replace(",", "", regex=False).fillna("")
    num = pd.to_numeric(s.str[:-1], errors="coerce")
    unit = s.str[-1:]
    scale = unit.map({"M": 1.0, "k": 1 / 1024, "K": 1 / 1024, "G": 1024.0})
    return (num * scale).astype("float32")


def parse_min_android(version):
    """'4.0.3 and up' -> 4.0, '8.0 and up' -> 8.0, 'Varies with device' -> NaN."""
    s = pd.Series(version, dtype="string").fillna("")
    parts = s.str.extract(r"^(\d+)(?:\.(\d))?")
    major = pd.to_numeric(parts[0], errors="coerce")
    minor = pd.to_numeric(parts[1], errors="coerce").fillna(0)
    return (major + minor / 10).astype("float32")


def developer_track_record(dev_id, released, installs):
    """For each app: how many apps the same developer released strictly earlier, and the
    mean log10 installs of those earlier apps (NaN when there are none).

    Apps released on the same day as each other do not count as each other's history.
    """
    frame = pd.DataFrame({
        "dev": pd.Series(dev_id).astype("string").fillna("(unknown)").values,
        "day": pd.to_datetime(released).values,
        "log_inst": np.log10(pd.Series(installs, dtype="float64").clip(lower=0).values + 1),
    })
    daily = frame.groupby(["dev", "day"], sort=True).agg(n=("log_inst", "size"), s=("log_inst", "sum"))
    grp = daily.groupby(level="dev")
    daily["prior_n"] = grp["n"].cumsum() - daily["n"]
    daily["prior_s"] = grp["s"].cumsum() - daily["s"]
    looked_up = frame.join(daily[["prior_n", "prior_s"]], on=["dev", "day"])
    prior_n = looked_up["prior_n"].to_numpy(dtype="float32")
    with np.errstate(invalid="ignore", divide="ignore"):
        prior_mean = np.where(prior_n > 0, looked_up["prior_s"].to_numpy() / prior_n, np.nan)
    return prior_n, prior_mean.astype("float32")


def to_model_frame(df):
    """Select and type the model columns exactly the way the model was trained."""
    out = pd.DataFrame(index=df.index)
    out["category"] = pd.Categorical(df["category"], categories=CATEGORIES)
    out["content_rating"] = pd.Categorical(df["content_rating"], categories=CONTENT_RATINGS)
    for col in NUMERIC:
        out[col] = pd.to_numeric(df[col], errors="coerce").astype("float32")
    return out[FEATURES]
