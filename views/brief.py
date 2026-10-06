import html

import numpy as np
import streamlit as st

from appvision import bands, resources, ui
from appvision.client import CLIENT, CLIENT_BLURB, CONCEPT_PITCH, CONCEPTS
from appvision.outlook import per_hundred

meta = resources.meta()
model = resources.outlook()
store = meta["store_stats"]

ui.eyebrow("AppVision Analytics · Client engagement")
st.title(f"{CLIENT} can build one app this year. Which one?")
ui.lede(f"{CLIENT} is {CLIENT_BLURB}. The founder asked AppVision for an honest read on three concepts before "
        "committing a year of work. This tool is the answer, and any studio can use it the same way.")

st.markdown("<div style='height:.6rem'></div>", unsafe_allow_html=True)
left, right = st.columns([1, 1.35], gap="large")
with left:
    ui.eyebrow("100 apps on Google Play")
    st.markdown(ui.hundred_grid_html(store["band_shares"]), unsafe_allow_html=True)
with right:
    counts = per_hundred(store["band_shares"])
    st.markdown(
        f'<p class="av-headline">Out of every 100 apps on Google Play, <em>{counts[0]}</em> never reach 1,000 '
        f'installs. Only <em>{counts[3:].sum()}</em> pass 100,000.</p>', unsafe_allow_html=True)
    st.markdown(ui.legend_html(store["band_shares"]), unsafe_allow_html=True)
    st.caption(f"All {store['apps']:,} apps in the June 2021 snapshot. The typical app had about "
               f"{store['median_installs']:,.0f} installs.")

st.divider()
ui.eyebrow("What the founder asked, and where to find the answer")
qs = [
    ("Which of our three concepts has the best realistic odds?", "views/launch_outlook.py", "Launch Outlook"),
    ("What install number should year one be planned around?", "views/launch_outlook.py", "Launch Outlook"),
    ("What do the apps that broke out in each niche have in common?", "views/playbook.py", "Playbook"),
    ("Once we launch, how do we tell whether we're on track?", "views/benchmark.py", "Benchmark"),
]
cols = st.columns(4)
for col, (q, page, name) in zip(cols, qs):
    with col:
        with st.container(border=True, height=150):
            st.markdown(f"**{q}**")
            st.page_link(page, label=f"Open {name}", icon=":material/arrow_forward:")

st.divider()
ui.eyebrow("The short answer, after one year on the store")
keys = list(CONCEPTS)
probs = model.band_probs([CONCEPTS[k] for k in keys])
cols = st.columns(3)
for col, k in zip(cols, keys):
    p = probs[keys.index(k)]
    n = per_hundred(p)
    with col:
        with st.container(border=True):
            st.markdown(f'<p class="av-eyebrow">Concept {k} · {html.escape(CONCEPTS[k].category)}</p>'
                        f'<p style="font-weight:700;margin:0">{html.escape(CONCEPTS[k].title)}</p>'
                        f'<p class="av-note" style="margin:.2rem 0 .8rem 0">{html.escape(CONCEPT_PITCH[k])}</p>'
                        f'{ui.hundred_grid_html(p, small=True)}'
                        f'<p class="av-note" style="margin-top:.8rem"><b>{n[2:].sum()} in 100</b> similar apps passed '
                        f'10,000 installs in a year · <b>{n[3:].sum()} in 100</b> passed 100,000</p>',
                        unsafe_allow_html=True)
best = keys[int(np.argmax(bands.reach_odds(probs)[:, 1]))]
st.markdown(f"**Recommendation:** Concept {best} gives the studio the best realistic start. Plan year one around the "
            f"typical outcome shown on the Launch Outlook page, not the best case, and use the Playbook to copy what "
            f"that niche's breakouts had in common.")
st.caption(f"{CLIENT} is fictional; every number comes from real Play Store data. Studio inputs used: two earlier "
           "apps with 1K–10K installs each, a studio website and a privacy policy.")
