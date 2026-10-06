import html

import pandas as pd
import streamlit as st

from appvision import features, resources, ui
from appvision.client import CONCEPTS
from appvision.playbook import installs_label, setup_label, store_link
from appvision.style import BLUE

book = resources.playbook()

ui.eyebrow("Playbook")
st.title("What did the apps that broke out do differently?")
ui.lede("Pick a concept. The Playbook finds real apps in the same category whose names read like it, then "
        "puts the ones that passed 100,000 installs next to the ones that didn't.")

concepts = st.session_state.get("concepts", CONCEPTS)
options = {f"Concept {k}: {c.title}": c for k, c in concepts.items()}
options["Something else…"] = None

with st.container(border=True):
    a, b, c = st.columns([1.4, 1.4, 1])
    choice = a.selectbox("Concept", list(options))
    picked = options[choice]
    default_text = picked.title if picked else ""
    default_cat = picked.category if picked else "Tools"
    text = b.text_input("Describe it in a few words", default_text, key=f"pb_text_{choice}",
                        placeholder="e.g. habit tracker, offline chess, recipe planner")
    category = c.selectbox("Category", features.CATEGORIES, index=features.CATEGORIES.index(default_cat),
                           key=f"pb_cat_{choice}")

frame, close = book.lookalikes(category, text)
rate = book.breakout_rate(frame)
n_break = int(frame["breakout"].sum())

st.divider()
if close:
    ui.eyebrow(f"Closest matches in {category}: about {book.represented_apps(frame):,} apps")
    st.markdown(
        f'<p class="av-headline">Of the {category} apps that read most like “{html.escape(text)}”, '
        f'<em>{rate:.0%}</em> broke out and passed 100,000 installs.</p>', unsafe_allow_html=True)
    st.caption(f"Every breakout among them is kept for comparison ({n_break:,} apps); the rest are a random "
               "sample weighted to stand for the full store.")
else:
    ui.eyebrow(f"All of {category}")
    st.markdown(
        f'<p class="av-headline">Too few {category} app names read like “{html.escape(text)}”, so this compares '
        f'the whole category instead: <em>{rate:.0%}</em> of {category} apps live a year or more broke out.</p>',
        unsafe_allow_html=True)
    st.caption("Try broader words (for example “budget” instead of a brand-style title) to get closer matches.")

if n_break < 5:
    st.info("Fewer than five breakouts match this description, which is too few to compare. "
            "Try broader words or a neighbouring category.")
    st.stop()

cmp = book.compare(frame)
notes = [n for n in cmp["note"] if n]

left, right = st.columns([1, 1.2], gap="large")
with left:
    ui.eyebrow("What stood out")
    if notes:
        st.markdown("".join(f'<p class="av-note" style="font-size:1.02rem;color:var(--ink)">• {html.escape(n)}</p>'
                            for n in notes), unsafe_allow_html=True)
    else:
        st.markdown('<p class="av-note">No setup choice clearly separated breakouts from the rest here. '
                    'What set them apart was probably product quality, marketing or timing, which this data '
                    'can\'t see.</p>', unsafe_allow_html=True)
    st.caption("Breakouts are apps that passed 100,000 installs. Differences show what was common among them, "
               "not proof that copying one choice causes success. Recent updates partly reflect success: "
               "popular apps get maintained.")
with right:
    ui.eyebrow("Side by side")
    rows = []
    for r in cmp.itertuples():
        if r.kind == "share":
            fb, fo = f"{r.breakouts:.0%}", f"{r.others:.0%}"
        elif r.column == "size_mb":
            fb, fo = f"{r.breakouts:,.0f} MB", f"{r.others:,.0f} MB"
        elif r.column == "rating_rated":
            fb, fo = f"{r.breakouts:.1f} ★", f"{r.others:.1f} ★"
        else:
            fb, fo = f"{r.breakouts:.1f}", f"{r.others:.1f}"
        mark = ' <span class="av-pill">stands out</span>' if r.note else ""
        rows.append(f"<tr><td>{html.escape(r.attribute)}{mark}</td><td class='num' style='color:{BLUE};font-weight:700'>"
                    f"{fb}</td><td class='num'>{fo}</td></tr>")
    st.markdown("<table class='av-compare'><thead><tr><th>Among the matches</th><th>Breakouts</th><th>The rest</th>"
                f"</tr></thead><tbody>{''.join(rows)}</tbody></table>", unsafe_allow_html=True)

st.divider()
ui.eyebrow("Breakouts worth studying")
top = book.top_breakouts(frame, n=12)
table = pd.DataFrame({
    "App": top["app_name"].astype(str).str.slice(0, 60),
    "Installs (June 2021)": top["installs_floor"].map(installs_label),
    "Rating": top["rating"].map(lambda v: f"{v:.1f} ★" if v and v > 0 else "—"),
    "Setup": top.apply(setup_label, axis=1),
    "Launched": pd.to_datetime(top["released"]).dt.year.astype("Int64").astype(str),
    "Store page": top["app_id"].map(store_link),
})
st.dataframe(table, hide_index=True, width="stretch",
             column_config={"Store page": st.column_config.LinkColumn("Store page", display_text="Open")})
st.caption("Store pages are from the June 2021 snapshot. Some of these apps have since been renamed or removed.")
