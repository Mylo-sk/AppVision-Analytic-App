# v1 (archived)

The first AppVision app, kept for reference and for the audit in [`notebooks/02_v1_audit.ipynb`](../notebooks/02_v1_audit.ipynb).

- `pages/`, `utils/`: the v1 Streamlit pages and helpers (they no longer run from here)
- `models/`: the v1 regressor, classifier and recommender preprocessors, loaded by the audit

v1's large data and FAISS index were removed from this branch; they remain in the `main` branch history. See the main README's "What changed in v2" for why v1 was replaced.
