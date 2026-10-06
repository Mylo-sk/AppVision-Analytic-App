"""Cached loaders for the app's model and data files (all produced by the notebooks)."""

import json
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
from scipy import sparse

ARTIFACTS = Path(__file__).resolve().parent.parent / "artifacts"


@st.cache_resource(show_spinner="Loading the Launch Outlook model…")
def outlook():
    from .outlook import LaunchOutlook
    return LaunchOutlook(ARTIFACTS)


@st.cache_resource(show_spinner="Loading the Playbook…")
def playbook():
    from .playbook import Playbook
    pool = pd.read_parquet(ARTIFACTS / "playbook_pool.parquet")
    matrix = sparse.load_npz(ARTIFACTS / "playbook_names.npz")
    return Playbook(pool, matrix, np.load(ARTIFACTS / "name_idf.npy"))


@st.cache_resource(show_spinner="Loading benchmarks…")
def benchmarks():
    from .benchmark import Benchmarks
    return Benchmarks(pd.read_parquet(ARTIFACTS / "benchmarks.parquet"))


@st.cache_data
def meta():
    return json.loads((ARTIFACTS / "outlook_meta.json").read_text(encoding="utf-8"))
