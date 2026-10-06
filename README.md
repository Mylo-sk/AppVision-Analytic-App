# AppVision Analytics · Launch Readiness

**Honest launch odds for Android app ideas, built on 2.3 million Google Play apps.**

Most apps never reach 1,000 installs. AppVision tells a studio, before it builds anything, what happened to real apps set up like its idea, in numbers anyone can read ("28 out of 100 apps like this passed 10,000 installs"). It also shows what the apps that broke out in that niche had in common.

> v2 is a rebuild. An audit of the first version found that its headline 96.5% accuracy came from target leakage. The story of finding and fixing that is in [What changed in v2](#what-changed-in-v2-and-why).

---

## The engagement

**Client:** Osu Lane Studio *(fictional)*, a five-person indie studio in Accra with budget to build one Android app this year, choosing between three concepts: a budget tracker, an offline word puzzle and an exam-prep flashcards app.

| The founder asked | Answered by |
|---|---|
| Which of our three concepts has the best realistic odds? | **Launch Outlook** page · notebook 03 |
| What install number should year one be planned around? | **Launch Outlook** page · notebook 03 |
| What do the apps that broke out in each niche have in common? | **Playbook** page · notebook 04 |
| Once we launch, how do we tell whether we're on track? | **Benchmark** page · notebook 04 |

## What the app does

- **Launch Outlook:** compares up to three concepts side by side. For each, it shows "100 apps like this one" as a 10 × 10 grid shaded by install band, the chance of reaching 1K / 10K / 100K / 1M installs (as a percentage and as "about 1 in N"), how that compares with a typical app in the category, and a what-if panel (add in-app purchases, drop ads, halve the download size…).
- **Playbook:** finds real apps whose names read like the concept within its category, then compares the ones that passed 100K installs with the ones that didn't, and lists breakouts worth studying.
- **Benchmark:** for a live app, shows where its installs, rating volume and star rating sit among apps of the same category and age. Descriptive only, no model.
- **How it works:** the model card, covering data, inputs, tested performance against baselines, calibration, the v1 audit and limitations. Every number on it is read from a file the notebooks write.

## Results

Tested on **397,435 apps from developers the model never saw in training**:

| | Launch Outlook model | Category + age baseline | Always guess "under 1K" |
|---|---|---|---|
| Ranks a 10K+ app above one that isn't (AUC) | **0.89** | 0.71 | 0.50 |
| Ranks a 100K+ app above one that isn't (AUC) | **0.93** | 0.75 | 0.50 |
| Exact install band | **65%** | 57% | 57% |
| Within one band | **93%** | 82% | 80% |

Exact-band accuracy looks modest because more than half of all apps sit in the lowest band. Always guessing "under 1K" already scores 57%. That's why the app reports **odds**, not a single verdict, and why the odds were checked for calibration: when the model says 30%, about 30% of such apps got there.

### Checked again five years later

The test above uses the same June 2021 snapshot the model learned from. To see whether the forecasts hold up over time, re-checked 5,000 apps on Google Play in October 2026: apps that were 1–12 months old in 2021, 1,000 from each install band. Then compared where they ended up with what the model would have forecast for them in 2021 ([notebook 05](notebooks/05_out_of_time_check.ipynb)).

| Apps from unseen developers, still listed in 2026 | Launch Outlook | Category + age baseline | 2021 test |
|---|---|---|---|
| Ranks a 10K+ app above one that isn't (AUC) | **0.86** | 0.56 | 0.89 |
| Ranks a 100K+ app above one that isn't (AUC) | **0.87** | 0.65 | 0.93 |
| Exact install band | **44%** | 37% | 65% |
| Within one band | **87%** | 70% | 93% |

- **The ranking held up.** Comparing concepts against each other, which is how the app is used, still works five years out. For apps still listed, the odds stayed calibrated (forecast 51% → 49% actual, 81% → 81%).
- **Survival was the miss.** 81% of those apps had been removed from Google Play by 2026, including 46% of apps that already had 1M+ installs. Launch-time inputs didn't predict which ones. Removal ran at 74–85% across every forecast group. Every Launch Outlook number therefore means *the odds if the app stays listed and maintained*.

## The answer for Osu Lane Studio

| Concept | Passed 10K installs within a year (out of 100 similar apps) | Typical app in the category | Breakout rate among look-alikes (100K+) |
|---|---|---|---|
| **B · Offline word puzzle** | **32** | 22 | 24.5% |
| A · Budget and expense tracker | 16 | 17 | 14.4% |
| C · Exam-prep flashcards | 9 | 10 | 4.2% |

- **Recommended concept B.** It's the only concept that beats its category average. Year one should be planned around 1,000–10,000 installs, its typical outcome, not the best case.
- **Keep B's free + ads + in-app purchases setup.** Among comparable apps, charging $2.99 up front went with a 12% chance of 10K+ instead of 32%.
- **Copy what the niche's breakouts had in common.** 83% offered in-app purchases (vs 52% of the rest), they were fuller downloads (about 35 MB vs 22 MB), and they kept shipping updates.
- **On-track marker after launch:** at 6–12 months, a Word game in the top quarter has about 5,800+ installs.

## What changed in v2 and why

Audited the v1 models before giving the client any numbers ([notebook 02](notebooks/02_v1_audit.ipynb)):

- **Found target leakage.** v1's *Rating Density* was `ratings ÷ (install bucket + 1)`, and the install bucket is the thing being predicted. Rebuilt every rated app's install bucket exactly from two model inputs (100.00% match). With only launch-time information, v1's recipe fell from 96% to 63% accuracy, and 97% of its remaining mistakes were on zero-rating apps, where the shortcut stops working.
- **Found a training–serving mismatch.** The web app computed inputs differently from training (ratings per *day* instead of per install, star rating instead of the quality score, a fixed $2.99 price). The same real app flipped from "Emerging" (100% sure) to "Low" (99% sure) depending on which definition was used.
- **Found the recommender matched release dates.** Min–max scaling squashed rating counts to about 0, so similarity came down to category and app age.
- **Found biased cleaning.** Dropping every row with a blank field removed 44% of apps (mostly those without a developer website), and those apps perform worse.

**Rebuilt:**
- Cleaned the raw 2.3M-app data again, keeping every app and storing no emails or URLs ([notebook 01](notebooks/01_data_rebuild.ipynb)).
- Trained a launch-time-only model, tested it on unseen developers and compared it with baselines ([notebook 03](notebooks/03_launch_outlook_model.ipynb)).
- Replaced the recommender with a name-based Playbook that separates breakouts from the rest, and added percentile benchmarks ([notebook 04](notebooks/04_playbook_and_benchmarks.ipynb)).
- Moved every feature definition into one shared package (`appvision/`) that both the notebooks and the app import, so they can't drift apart again.
- Re-checked 5,000 of the 2021 apps on the live store in 2026 to test the forecasts out of time ([notebook 05](notebooks/05_out_of_time_check.ipynb)).

## Repository layout

```
app.py                     Streamlit entry point (navigation)
views/                     The five pages
appvision/                 Shared code: bands, features, name signal, outlook, playbook, benchmarks, UI
artifacts/                 Model and data files (written by notebooks 03–05, no pickles)
notebooks/                 01 data rebuild · 02 v1 audit · 03 Launch Outlook model · 04 Playbook & benchmarks · 05 out-of-time check
scripts/rescrape_sample.py Re-checks a sample of 2021 apps on Google Play today (feeds notebook 05)
tests/                     Checks on the shared definitions
```

## Running it

```bash
pip install -r requirements.txt
streamlit run app.py
```

To rebuild everything from scratch, download the *Google Play Store Apps* dataset (Gautham Prakash, 2.3M apps, June 2021) and set `RAW_DIR` in notebook 01. Then run notebooks 01 → 04 in order. Notebook 05 also needs `pip install google-play-scraper` and `python scripts/rescrape_sample.py --n 5000` (about 5 hours with its built-in pauses between requests).

## Limits worth knowing

- **2021 snapshot.** The numbers describe the shape of the market, not today's exact odds.
- **No marketing, quality or review data.** Those explain much of what the model can't.
- **Survivors only.** Apps removed before June 2021 are missing, and removal is common. 81% of young 2021 apps were gone five years later (notebook 05), so the odds describe apps that stay listed.
- **Studio track record** uses earlier apps' installs as measured in 2021, which slightly flatters studios whose catalogue kept growing.
- **Patterns, not causes.** The what-if panel and Playbook show how similar apps differed, not guaranteed effects.

## Data and licence

Data: [Google Play Store Apps](https://www.kaggle.com/gauthamp10/google-playstore-apps) by Gautham Prakash (MIT licence, [backup repo](https://github.com/gauthamp10/Google-Playstore-Dataset)). Code: MIT (see `LICENSE`).
