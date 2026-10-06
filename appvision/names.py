"""Text features from app names.

A hashed TF-IDF over words and word pairs serves two jobs:
  * the name signal: a linear model that reads a name (or a few keywords) and
    estimates how apps with similar wording tend to perform
  * Playbook look-alikes: cosine similarity between a concept description and real app names

Only plain numpy arrays (idf weights, coefficients) are saved, so nothing depends on
pickled scikit-learn objects.
"""

import numpy as np
from scipy import sparse
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.preprocessing import normalize

N_FEATURES = 2**20

_HASHER = HashingVectorizer(
    n_features=N_FEATURES,
    ngram_range=(1, 2),
    alternate_sign=False,
    norm=None,
    lowercase=True,
    token_pattern=r"(?u)\b\w\w+\b",
    dtype=np.float32,
)


def hashed_counts(texts):
    """Sparse word / word-pair counts for an iterable of strings."""
    return _HASHER.transform(["" if t is None else str(t) for t in texts])


def fit_idf(counts):
    """Smoothed inverse document frequency, same formula as scikit-learn's TfidfTransformer."""
    n = counts.shape[0]
    df = np.bincount(counts.indices, minlength=counts.shape[1])
    return (np.log((1 + n) / (1 + df)) + 1).astype(np.float32)


def tfidf(texts_or_counts, idf):
    """L2-normalised TF-IDF rows, so a dot product between rows is cosine similarity."""
    counts = texts_or_counts if sparse.issparse(texts_or_counts) else hashed_counts(texts_or_counts)
    return normalize(counts @ sparse.diags(idf), norm="l2", copy=False).astype(np.float32)


def name_signal(texts, idf, coef, intercept):
    """Expected log10 installs implied by the wording of each name."""
    return np.asarray(tfidf(texts, idf) @ coef).ravel() + intercept


def word_count(texts):
    return np.array([len(str(t).split()) if t is not None else 0 for t in texts], dtype=np.float32)
