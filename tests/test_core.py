import numpy as np
import pandas as pd

from appvision import bands, features
from appvision.outlook import one_in, per_hundred


def test_band_edges():
    assert list(bands.band_of([0, 999, 1_000, 9_999, 10_000, 99_999, 100_000, 1_000_000, 5e9])) == [0, 0, 1, 1, 2, 2, 3, 4, 4]


def test_reach_odds_are_cumulative():
    p = np.array([[0.5, 0.2, 0.15, 0.1, 0.05]])
    np.testing.assert_allclose(bands.reach_odds(p)[0], [0.5, 0.3, 0.15, 0.05])


def test_size_parsing():
    out = features.parse_size_mb(["10M", "512k", "1.5G", "Varies with device", None]).tolist()
    assert out[:3] == [10.0, 0.5, 1536.0]
    assert np.isnan(out[3]) and np.isnan(out[4])


def test_min_android_parsing():
    out = features.parse_min_android(["4.0.3 and up", "8.0 and up", "Varies with device"]).tolist()
    assert out[:2] == [4.0, 8.0]
    assert np.isnan(out[2])


def test_track_record_only_counts_strictly_earlier_apps():
    n, mean_log = features.developer_track_record(
        dev_id=["a", "a", "a", "b"],
        released=pd.to_datetime(["2019-01-01", "2020-01-01", "2020-01-01", "2020-01-01"]),
        installs=[999, 9, 99, 5],
    )
    assert n.tolist() == [0, 1, 1, 0]          # same-day releases don't count as each other's history
    assert np.isnan(mean_log[0]) and np.isnan(mean_log[3])
    np.testing.assert_allclose(mean_log[1:3], [3.0, 3.0])


def test_per_hundred_always_sums_to_100():
    rng = np.random.default_rng(0)
    for _ in range(200):
        p = rng.dirichlet(np.ones(5))
        assert per_hundred(p).sum() == 100


def test_one_in_phrasing():
    assert one_in(0.7) == "about 7 in 10"
    assert one_in(0.125) == "about 1 in 8"
    assert one_in(0.0001) == "fewer than 1 in 2,000"


def test_model_frame_types():
    row = {c: 0.0 for c in features.NUMERIC} | {"category": "Finance", "content_rating": "Teen"}
    X = features.to_model_frame(pd.DataFrame([row]))
    assert list(X.columns) == features.FEATURES
    assert X["category"].cat.categories.tolist() == features.CATEGORIES
