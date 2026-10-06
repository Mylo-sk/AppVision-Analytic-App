import html

import numpy as np
import streamlit as st

from appvision import bands, features, resources, ui
from appvision.client import CONCEPTS, STUDIO
from appvision.outlook import Concept, median_band, one_in, per_hundred

HORIZONS = {"6 months": 182, "1 year": 365, "2 years": 730, "3 years": 1095}
TEN_K = 1  # index of the 10K+ milestone, the headline number used to compare concepts

model = resources.outlook()
meta = resources.meta()

ui.eyebrow("Launch Outlook")
st.title("What could each concept realistically reach?")
ui.lede("Describe up to three app ideas. For each, the model looks at real Play Store apps set up the same way "
        "and shows what happened to them, in plain numbers out of 100.")

# ---------------------------------------------------------------- studio inputs
if "concepts" not in st.session_state:
    st.session_state.concepts = dict(CONCEPTS)

with st.container(border=True):
    st.markdown("#### Your studio")
    c1, c2, c3, c4 = st.columns([0.8, 1.05, 0.85, 2.0])
    prior_apps = c1.number_input("Apps published before", 0, 500, STUDIO["prior_apps"], step=1,
                                 help="Count every app your studio has released on Google Play.")
    band_names = ["Under 1,000", "1,000–10,000", "10,000–100,000", "100,000–1 million", "Over 1 million"]
    prior_band = c2.selectbox("Typical installs of those apps", range(5), index=STUDIO["prior_typical_band"],
                              format_func=lambda i: band_names[i], disabled=prior_apps == 0)
    has_website = c3.toggle("Studio website on the listing", value=STUDIO["has_website"])
    horizon_label = c4.segmented_control("Look ahead", list(HORIZONS), default="1 year")
    horizon = HORIZONS[horizon_label or "1 year"]

# ---------------------------------------------------------------- concept inputs
st.markdown("#### Your concepts")
tabs = st.tabs([f"Concept {k}" for k in st.session_state.concepts])
concepts = {}
for (key, base), tab in zip(st.session_state.concepts.items(), tabs):
    with tab:
        a, b, c = st.columns([1.6, 1, 1])
        title = a.text_input("Working title or a few words about the app", base.title, key=f"title_{key}",
                             help="Names and wording carry signal: apps described like yours tend to perform alike.")
        category = b.selectbox("Category", features.CATEGORIES, index=features.CATEGORIES.index(base.category),
                               key=f"cat_{key}")
        rating = c.selectbox("Age rating", features.CONTENT_RATINGS,
                             index=features.CONTENT_RATINGS.index(base.content_rating), key=f"cr_{key}")
        d, e, f, g = st.columns(4)
        paid = d.toggle("Charge to download", value=base.price_usd > 0, key=f"paid_{key}")
        price = d.number_input("Price (USD)", 0.49, 49.99, max(base.price_usd, 2.99), step=0.5,
                               key=f"price_{key}") if paid else 0.0
        ads = e.toggle("Shows ads", value=base.ad_supported, key=f"ads_{key}")
        iap = e.toggle("In-app purchases", value=base.in_app_purchases, key=f"iap_{key}")
        size = f.number_input("Download size (MB)", 1, 2000, int(base.size_mb or 25), step=1,
                              key=f"size_{key}")
        privacy = f.toggle("Privacy policy on the listing", value=base.has_privacy, key=f"pp_{key}")
        min_android = g.selectbox("Minimum Android version", [4.1, 4.4, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
                                  index=[4.1, 4.4, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0].index(base.min_android or 6.0),
                                  key=f"and_{key}")
        concepts[key] = Concept(
            title=title, category=category, price_usd=price, ad_supported=ads, in_app_purchases=iap,
            size_mb=size, content_rating=rating, min_android=min_android, has_website=has_website,
            has_privacy=privacy, prior_apps=int(prior_apps), prior_typical_band=prior_band if prior_apps else None,
            horizon_days=horizon)
st.session_state.concepts = concepts

# ---------------------------------------------------------------- scoring
keys = list(concepts)
probs = model.band_probs([concepts[k] for k in keys])
odds = bands.reach_odds(probs)

st.divider()
ui.eyebrow(f"After {ui.horizon_phrase(horizon)} on the store")
st.subheader("How the concepts compare")

ranked = sorted(keys, key=lambda k: -odds[keys.index(k), TEN_K])
best, rest = ranked[0], ranked[1:]
best_n = per_hundred(probs[keys.index(best)])[2:].sum()
others = " and ".join(f"{per_hundred(probs[keys.index(k)])[2:].sum()}" for k in rest)
st.markdown(
    f'<p class="av-headline">Concept {best} has the strongest outlook: <em>{best_n} in 100</em> apps like it '
    f'passed 10,000 installs, against {others} for the others.</p>', unsafe_allow_html=True)

cols = st.columns(len(keys))
for col, k in zip(cols, keys):
    p = probs[keys.index(k)]
    with col:
        with st.container(border=True):
            st.markdown(f'<p class="av-eyebrow">Concept {k} · {html.escape(concepts[k].category)}</p>'
                        f'<p style="font-weight:700;margin:0 0 .7rem 0">{html.escape(concepts[k].title)}</p>'
                        f'{ui.hundred_grid_html(p, small=True)}'
                        f'<p class="av-note" style="margin-top:.8rem"><b>{per_hundred(p)[2:].sum()} in 100</b> passed 10K · '
                        f'typical result: {ui.band_label_phrase(median_band(p))}</p>', unsafe_allow_html=True)

# ---------------------------------------------------------------- detail for one concept
st.divider()
focus = st.radio("Look closer at", keys, format_func=lambda k: f"Concept {k}: {concepts[k].title}",
                 horizontal=True, index=keys.index(best))
c, p, o = concepts[focus], probs[keys.index(focus)], odds[keys.index(focus)]
typical = model.typical(c.category, horizon)
typical_odds = bands.reach_odds(typical)[0]

left, right = st.columns([1, 1.25], gap="large")
with left:
    ui.eyebrow("100 apps like this one")
    st.markdown(ui.hundred_grid_html(p), unsafe_allow_html=True)
with right:
    counts = per_hundred(p)
    st.markdown(
        f'<p class="av-headline">Picture 100 apps set up like “{html.escape(c.title)}”. After '
        f'{ui.horizon_phrase(horizon)}, <em>{counts[0]}</em> would still be under 1,000 installs and '
        f'<em>{counts[3:].sum()}</em> would have passed 100,000.</p>', unsafe_allow_html=True)
    st.markdown(ui.legend_html(p), unsafe_allow_html=True)

st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)
ui.eyebrow("Chance of reaching each milestone")
st.markdown(ui.milestones_html(o, typical_odds, c.category), unsafe_allow_html=True)
diff = o[TEN_K] - typical_odds[TEN_K]
compare_word = "better than" if diff > 0.02 else "worse than" if diff < -0.02 else "about the same as"
st.caption(f"“Typical {c.category}” is every {c.category} app that had been live about as long. "
           f"This concept's chance of 10K+ is {compare_word} that baseline.")

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
left, right = st.columns([1.15, 1], gap="large")
with left:
    ui.eyebrow("What-if: one change at a time")
    st.markdown(ui.whatif_html(model.what_if(c), TEN_K), unsafe_allow_html=True)
    st.caption("Each line changes one thing and keeps everything else the same. These show how similar apps "
               "differed, not a guarantee of cause and effect.")
with right:
    m = meta["metrics"]["model"]
    bl = meta["metrics"]["baseline_category_age"]
    ui.eyebrow("How much to trust this")
    st.markdown(
        f'<div class="av-card"><p class="av-note" style="margin-top:0">'
        f'Tested on <b>{meta["metrics"]["test_apps"]:,}</b> apps from developers the model never saw. '
        f'It ranks apps that pass 10K above apps that don’t <b>{m["auc_10k"]:.0%}</b> of the time '
        f'(a guess from category and age alone manages {bl["auc_10k"]:.0%}). '
        f'When it says “30 in 100”, about 30 in 100 such apps really got there.</p>'
        f'<p class="av-note">It can’t see marketing spend, app quality, reviews or luck. Those explain much of the '
        f'rest. Treat it as the base rate to plan around, then beat it.</p></div>',
        unsafe_allow_html=True)
    st.page_link("views/playbook.py", label="Open the Playbook for this niche",
                 icon=":material/menu_book:")
