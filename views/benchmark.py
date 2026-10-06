import html

import numpy as np
import streamlit as st

from appvision import features, resources, ui
from appvision.benchmark import AGE_BANDS, AGE_LABELS
from appvision.style import BAND_COLORS, BLUE, INK_2

bench = resources.benchmarks()

ui.eyebrow("Benchmark")
st.title("Already live? See where you stand.")
ui.lede("Compare your app with every app in the same category that had been live about as long. "
        "This page doesn't predict anything. It shows where real apps your age landed.")

with st.container(border=True):
    a, b, c = st.columns([1.3, 1, 1])
    category = a.selectbox("Category", features.CATEGORIES, index=features.CATEGORIES.index("Finance"))
    months = b.number_input("Months on Google Play", 1, 60, 8, step=1)
    installs = c.number_input("Installs so far", 0, 5_000_000_000, 4_000, step=500,
                              help="The real number from your Play Console, not the public '1,000+' label.")
    d, e, _ = st.columns([1.3, 1, 1])
    ratings = d.number_input("Number of ratings", 0, 100_000_000, 25, step=5)
    stars = e.number_input("Average star rating", 1.0, 5.0, 4.2, step=0.1, format="%.1f")

age_days = months * 30.4
age_band = next((i for i, (lo, hi, _) in enumerate(AGE_BANDS) if lo <= age_days < hi), len(AGE_BANDS) - 1)
peer_label = f"{category} apps live {AGE_LABELS[age_band]}"

pct, peers = bench.percentile(category, age_band, "installs", installs)
st.divider()
if pct is None:
    st.warning(f"Fewer than 30 {peer_label.lower()} exist in the data, too few for a fair comparison. "
               "Try a neighbouring category.")
    st.stop()

ahead = int(round(pct))
ui.eyebrow(f"Compared with {peers:,} {peer_label}")
st.markdown(f'<p class="av-headline">With {installs:,} installs you are ahead of <em>{ahead} in 100</em> '
            f'{html.escape(peer_label)}.</p>', unsafe_allow_html=True)

curve, _ = bench.curve(category, age_band, "installs")
marks = {"Bottom quarter": curve[24], "Middle (half do better)": curve[49], "Top quarter": curve[74], "Top 10%": curve[89]}

# percentile strip: where you sit among peers, 0 → 100
st.markdown(
    f"""<div class="av-card" role="img" aria-label="You are at the {ahead}th percentile of peers">
    <div style="position:relative;height:46px;margin:.4rem 0 .2rem 0">
      <div style="position:absolute;top:18px;left:0;right:0;height:10px;border-radius:5px;
        background:linear-gradient(90deg,{BAND_COLORS[0]} 0%,{BAND_COLORS[0]} 25%,{BAND_COLORS[1]} 25%,{BAND_COLORS[1]} 50%,
        {BAND_COLORS[2]} 50%,{BAND_COLORS[2]} 75%,{BAND_COLORS[4]} 75%)"></div>
      <div style="position:absolute;left:calc({min(max(pct, 1), 99)}% - 9px);top:11px;width:18px;height:24px;
        border-radius:6px;background:#151922;border:3px solid #fff;box-shadow:0 1px 3px rgba(0,0,0,.25)"></div>
    </div>
    <div style="display:flex;justify-content:space-between;font-family:var(--mono);font-size:.74rem;color:{INK_2}">
      <span>behind everyone</span><span>middle</span><span>ahead of everyone</span></div></div>""",
    unsafe_allow_html=True)

cols = st.columns(4)
for col, (label, value) in zip(cols, marks.items()):
    col.metric(label, f"{value:,.0f}+", help=f"Installs needed to be in the {label.lower()} of {peer_label.lower()}.")

next_goal = next(((label, v) for label, v in marks.items() if installs < v), None)
if next_goal:
    st.caption(f"Next marker: {next_goal[0].lower()} of {peer_label.lower()} starts at about {next_goal[1]:,.0f} installs.")
else:
    st.caption(f"You're in the top 10% of {peer_label.lower()}.")

st.divider()
left, right = st.columns(2, gap="large")
with left:
    ui.eyebrow("Are people leaving ratings?")
    per_k = ratings / max(installs, 1) * 1000
    med, _ = bench.median(category, age_band, "ratings_per_1k")
    if installs >= 100 and med is not None:
        rp, _ = bench.percentile(category, age_band, "ratings_per_1k", per_k)
        verdict = ("more than most" if per_k > med * 1.2 else "fewer than most" if per_k < med * 0.8 else "about the usual number")
        st.markdown(
            f'<p class="av-headline" style="font-size:1.2rem">You get about <em>{per_k:.0f}</em> ratings per 1,000 installs. '
            f'A typical peer gets {med:.0f}, so you get {verdict}.</p>', unsafe_allow_html=True)
        st.markdown('<p class="av-note">Ratings are how the store and new visitors judge an app at a glance. If few '
                    'people leave one, asking at a good moment (after a success, never mid-task) usually helps more '
                    'than anything else on this page.</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="av-note">Once you pass 100 installs, this compares how often your users leave a '
                    'rating with apps your age.</p>', unsafe_allow_html=True)
with right:
    ui.eyebrow("How does your star rating compare?")
    med_r, _ = bench.median(category, age_band, "rating")
    if ratings >= 10 and med_r is not None:
        sp, _ = bench.percentile(category, age_band, "rating", stars)
        st.markdown(
            f'<p class="av-headline" style="font-size:1.2rem">At <em>{stars:.1f} ★</em> you rate higher than '
            f'about {int(round(sp))} in 100 peers (typical: {med_r:.1f} ★).</p>', unsafe_allow_html=True)
        st.markdown('<p class="av-note">Compared only with peers that have at least 10 ratings, since a handful of '
                    'early ratings swing averages a lot.</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="av-note">With fewer than 10 ratings an average isn’t stable enough to compare. '
                    'Collect a few more first.</p>', unsafe_allow_html=True)
