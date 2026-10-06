"""Install bands: the single definition used for training, benchmarks and every label in the app."""

import numpy as np

BAND_EDGES = [0, 1_000, 10_000, 100_000, 1_000_000]
BAND_LABELS = ["Under 1K", "1K–10K", "10K–100K", "100K–1M", "1M+"]
N_BANDS = len(BAND_LABELS)

# "Chance of reaching X installs" thresholds shown in the app (one per band boundary)
THRESHOLDS = BAND_EDGES[1:]
THRESHOLD_LABELS = ["1K+", "10K+", "100K+", "1M+"]

# An app counts as a breakout once it passes 100K installs (roughly the top 8% of the store)
BREAKOUT_MIN = 100_000

# Typical installs inside each band (geometric midpoint), used when a user picks a band as an input
BAND_TYPICAL = [200, 3_000, 30_000, 300_000, 3_000_000]


def band_of(installs):
    """Band index (0-4) for one value or an array of install counts."""
    return np.searchsorted(BAND_EDGES, np.asarray(installs, dtype="float64"), side="right") - 1


def reach_odds(band_probs):
    """Turn per-band probabilities (n, 5) into chance of reaching each threshold (n, 4)."""
    p = np.atleast_2d(band_probs)
    return np.cumsum(p[:, ::-1], axis=1)[:, ::-1][:, 1:]
