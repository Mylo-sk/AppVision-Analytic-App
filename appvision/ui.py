"""Shared Streamlit look and the reusable pieces of the AppVision interface."""

import html

import numpy as np
import streamlit as st

from . import bands
from .outlook import one_in, per_hundred
from .style import BAND_COLORS

FONTS = ("https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,500..800"
         "&family=Lexend:wght@300..600&family=IBM+Plex+Mono:wght@400;500&display=swap")

CSS = """
<style>
@import url('__FONTS__');
:root {
  --fog: #f4f6f8; --card: #ffffff; --ink: #151922; --ink-2: #586070; --muted: #8a909c;
  --rule: #dde2e8; --blue: #2a78d6; --blue-deep: #104281;
  --display: 'Archivo', system-ui, sans-serif;
  --body: 'Lexend', system-ui, sans-serif;
  --mono: 'IBM Plex Mono', ui-monospace, monospace;
}
html, body, .stApp, .stMarkdown, .stText, p, li, label, input, textarea, select, button,
[data-testid="stWidgetLabel"], [data-testid="stCaptionContainer"] { font-family: var(--body) !important; }
.stApp { background: var(--fog); color: var(--ink); }
h1, h2, h3, h4 { font-family: var(--display) !important; font-stretch: 112%; letter-spacing: -0.01em; color: var(--ink); }
h1 { font-weight: 800 !important; }
h2, h3 { font-weight: 700 !important; }
.block-container { max-width: 1180px; padding-top: 3.8rem; }
[data-testid="stSidebar"] { background: #eceff3; border-right: 1px solid var(--rule); }
[data-testid="stMetricValue"], [data-testid="stMetricValue"] * { font-family: var(--display) !important;
  font-stretch: 112%; font-weight: 700; }
a { color: var(--blue-deep); }

.stMarkdown p.av-eyebrow, p.av-eyebrow { font-family: var(--mono) !important; font-size: 0.78rem !important;
  letter-spacing: 0.08em; text-transform: uppercase; color: var(--ink-2); margin: 0 0 0.35rem 0; }
.stMarkdown p.av-lede, p.av-lede { font-size: 1.1rem !important; line-height: 1.6 !important; color: var(--ink-2);
  max-width: 46rem; font-weight: 300; }
.av-card { background: var(--card); border: 1px solid var(--rule); border-radius: 14px; padding: 1.25rem 1.4rem; }
.stMarkdown p.av-headline, p.av-headline { font-family: var(--display) !important; font-stretch: 108%; font-weight: 700;
  font-size: 1.45rem !important; line-height: 1.3 !important; color: var(--ink); margin: 0.2rem 0 1rem 0; }
.av-headline em { font-style: normal; color: var(--blue-deep); }
.stMarkdown p.av-note, p.av-note { font-size: 0.92rem !important; color: var(--ink-2); line-height: 1.55 !important; }

/* 100 apps like yours */
.av-hundred { display: grid; grid-template-columns: repeat(10, 1fr); gap: 4px; max-width: 290px; }
.av-hundred span { aspect-ratio: 1 / 1; border-radius: 4px; display: block; }
.av-hundred.small { max-width: 170px; gap: 3px; }
.av-hundred.small span { border-radius: 3px; }
.av-legend { list-style: none; padding: 0; margin: 0; display: grid; gap: 0.45rem; }
.av-legend li { font-family: var(--body) !important; display: grid; grid-template-columns: 14px 2.4rem 1fr; align-items: center; gap: 0.55rem;
  font-size: 0.95rem; color: var(--ink-2); margin: 0; }
.av-legend i { width: 14px; height: 14px; border-radius: 3px; display: block; }
.av-legend b { font-family: var(--display) !important; font-stretch: 112%; font-size: 1.05rem; color: var(--ink); text-align: right; }

/* milestone chances */
.av-milestones { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 0.75rem; }
.av-milestone { background: var(--card); border: 1px solid var(--rule); border-radius: 12px; padding: 0.9rem 1rem 0.85rem; }
.av-milestone .badge { font-family: var(--mono) !important; font-size: 0.78rem; color: var(--ink-2); }
.av-milestone .pct { font-family: var(--display) !important; font-stretch: 115%; font-weight: 800; font-size: 2rem;
  line-height: 1.1; color: var(--ink); margin-top: 0.25rem; }
.av-milestone .freq { font-size: 0.86rem; color: var(--ink-2); }
.av-milestone .bar { height: 6px; border-radius: 3px; background: #e6eaef; margin-top: 0.6rem; overflow: hidden; }
.av-milestone .bar span { display: block; height: 100%; border-radius: 3px; background: var(--blue); }
.av-milestone .vs { font-size: 0.8rem; color: var(--muted); margin-top: 0.4rem; }

.av-whatif { display: grid; grid-template-columns: 1fr auto; gap: 0.2rem 1rem; align-items: baseline;
  padding: 0.6rem 0; border-bottom: 1px solid var(--rule); }
.av-whatif .delta { font-family: var(--display) !important; font-stretch: 112%; font-weight: 700; }
.av-whatif .delta.up { color: #006300; } .av-whatif .delta.down { color: #b42318; } .av-whatif .delta.flat { color: var(--muted); }
.av-whatif small { grid-column: 1 / -1; color: var(--ink-2); }

.av-compare { width: 100%; border-collapse: collapse; font-size: 0.95rem; }
.av-compare th { font-family: var(--mono) !important; font-weight: 500; font-size: 0.74rem; text-transform: uppercase;
  letter-spacing: 0.06em; color: var(--ink-2); text-align: left; padding: 0.4rem 0.5rem; border-bottom: 1px solid var(--rule); }
.av-compare td { padding: 0.55rem 0.5rem; border-bottom: 1px solid var(--rule); vertical-align: top; }
.av-compare td.num { font-variant-numeric: tabular-nums; white-space: nowrap; }
.av-pill { display: inline-block; font-family: var(--mono) !important; font-size: 0.74rem; padding: 0.1rem 0.5rem;
  border-radius: 999px; background: #e3edfa; color: var(--blue-deep); }

@media (max-width: 760px) {
  .av-milestones { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .block-container { padding-left: 1rem; padding-right: 1rem; }
}
@media (prefers-reduced-motion: reduce) { * { transition: none !important; animation: none !important; } }
</style>
""".replace("__FONTS__", FONTS)


def setup_page(title):
    st.set_page_config(page_title=f"{title} · AppVision", page_icon="📈", layout="wide")


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)


def eyebrow(text):
    st.markdown(f'<p class="av-eyebrow">{html.escape(text)}</p>', unsafe_allow_html=True)


def lede(text):
    st.markdown(f'<p class="av-lede">{text}</p>', unsafe_allow_html=True)


def hundred_grid_html(probs, small=False):
    counts = per_hundred(probs)
    cells = "".join(f'<span style="background:{BAND_COLORS[b]}"></span>' for b, n in enumerate(counts) for _ in range(n))
    summary = "; ".join(f"{n} of 100 end up {bands.BAND_LABELS[b]}" for b, n in enumerate(counts) if n)
    cls = "av-hundred small" if small else "av-hundred"
    return f'<div class="{cls}" role="img" aria-label="{html.escape(summary)}">{cells}</div>'


def legend_html(probs):
    counts = per_hundred(probs)
    phrases = ["stay under 1,000 installs", "reach 1,000–10,000", "reach 10,000–100,000",
               "reach 100,000–1 million", "pass 1 million"]
    items = "".join(
        f'<li><i style="background:{BAND_COLORS[b]}"></i><b>{n}</b><span>{phrases[b]}</span></li>'
        for b, n in enumerate(counts))
    return f'<ul class="av-legend">{items}</ul>'


def milestones_html(odds, typical_odds=None, category=None):
    cards = []
    for i, label in enumerate(bands.THRESHOLD_LABELS):
        p = float(odds[i])
        vs = ""
        if typical_odds is not None:
            vs = f'<div class="vs">typical {html.escape(category or "app")}: {typical_odds[i]:.0%}</div>'
        cards.append(
            f'<div class="av-milestone"><div class="badge">{label} installs</div>'
            f'<div class="pct">{p:.0%}</div><div class="freq">{one_in(p)}</div>'
            f'<div class="bar"><span style="width:{max(p, 0.004) * 100:.1f}%"></span></div>{vs}</div>')
    return f'<div class="av-milestones">{"".join(cards)}</div>'


def whatif_html(rows, threshold_index=1):
    label = bands.THRESHOLD_LABELS[threshold_index]
    out = []
    for r in rows:
        before, after = r["before"][threshold_index], r["after"][threshold_index]
        diff = after - before
        cls = "up" if diff > 0.005 else "down" if diff < -0.005 else "flat"
        sign = "+" if diff > 0 else "−" if diff < 0 else "±"
        out.append(
            f'<div class="av-whatif"><span>{html.escape(r["change"])}</span>'
            f'<span class="delta {cls}">{sign}{abs(diff) * 100:.0f} pts</span>'
            f'<small>Chance of {label}: {before:.0%} → {after:.0%}</small></div>')
    return "".join(out)


def band_label_phrase(b):
    return ["under 1,000 installs", "1,000–10,000 installs", "10,000–100,000 installs",
            "100,000–1 million installs", "more than 1 million installs"][b]


def horizon_phrase(days):
    return {182: "6 months", 365: "a year", 730: "two years", 1095: "three years"}.get(days, f"{days} days")


def fmt_int(v):
    return f"{v:,.0f}"


def clamp01(x):
    return float(np.clip(x, 0, 1))
