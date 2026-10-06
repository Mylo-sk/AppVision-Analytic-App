"""Re-check a sample of 2021 apps on Google Play today, to test the Launch Outlook against real outcomes.

Samples apps that were 30–365 days old in June 2021 (stratified by their 2021 install band),
then looks up each app's public listing and records whether it is still live and its install
count now. Only public listing fields are stored; no personal data.

Polite by design: one request at a time with a randomised 1.5–3 s pause, and it resumes from
where it stopped if interrupted.

    pip install google-play-scraper
    python scripts/rescrape_sample.py --n 5000
"""

import argparse
import random
import time
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parent.parent
SOURCE = REPO / "data" / "v2" / "apps_2021.parquet"
OUT = REPO / "data" / "v2" / "rescrape_sample.parquet"


def pick_sample(n, seed=2026):
    df = pd.read_parquet(SOURCE, columns=["app_id", "band", "age_days", "in_model"])
    young = df[(df["in_model"] == 1) & df["age_days"].between(30, 365)]
    per_band = n // 5
    parts = [g.sample(min(per_band, len(g)), random_state=seed) for _, g in young.groupby("band")]
    return pd.concat(parts)["app_id"].astype(str).tolist()


def main():
    from google_play_scraper import app as fetch
    from google_play_scraper.exceptions import NotFoundError

    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=5000)
    args = ap.parse_args()

    ids = pick_sample(args.n)
    done = pd.read_parquet(OUT) if OUT.exists() else pd.DataFrame(columns=["app_id"])
    todo = [i for i in ids if i not in set(done["app_id"])]
    print(f"{len(ids):,} sampled · {len(done):,} already checked · {len(todo):,} to go")

    rows = done.to_dict("records")
    for k, app_id in enumerate(todo, 1):
        rec = {"app_id": app_id, "checked_at": pd.Timestamp.utcnow().isoformat()}
        try:
            d = fetch(app_id, lang="en", country="us")
            rec.update(status="live", installs_now=d.get("realInstalls"), installs_label_now=d.get("installs"),
                       rating_now=d.get("score"), ratings_now=d.get("ratings"), updated_now=d.get("updated"))
        except NotFoundError:
            rec.update(status="removed")
        except Exception as e:  # network hiccups etc.: record and move on, retried on the next run
            print(f"  {app_id}: {type(e).__name__}")
            continue
        rows.append(rec)
        if k % 50 == 0 or k == len(todo):
            pd.DataFrame(rows).to_parquet(OUT, index=False)
            print(f"  {len(rows):,}/{len(ids):,} checked")
        time.sleep(random.uniform(1.5, 3.0))


if __name__ == "__main__":
    main()
