import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from appvision import resources, ui
from appvision.style import AXIS, BLUE, GRID, INK, INK_2, MUTED

meta = resources.meta()
m = meta["metrics"]

ui.eyebrow("How it works")
st.title("What's behind the numbers, and what isn't")
ui.lede("Every figure in this tool comes from the notebooks in the repository. This page explains the data, "
        "what the model can and can't see, and how well it held up on apps it had never seen.")

# ---------------------------------------------------------------- data and inputs
left, right = st.columns(2, gap="large")
with left:
    st.subheader("The data")
    st.markdown(
        f"- **{meta['store_stats']['apps']:,} Google Play apps**, scraped on 15–16 June 2021 "
        "(*Google Play Store Apps* dataset, Gautham Prakash).\n"
        "- **Outcome:** the Play Store's own approximate install count, grouped into five bands "
        "(under 1K, 1K–10K, 10K–100K, 100K–1M, 1M+).\n"
        f"- **Model trained on** {m['train_apps']:,} apps and **tested on** {m['test_apps']:,} apps from "
        f"{m['test_developers']:,} developers it never saw during training.\n"
        "- Developer emails and URLs were never loaded or stored.")
with right:
    st.subheader("What the model looks at")
    st.markdown(
        "Only things a studio knows **before launch**: category, age rating, price, ads, in-app purchases, "
        "download size, minimum Android version, whether a website and privacy policy are listed, the studio's "
        "earlier apps, the wording of the app's name, and how long it has been live.\n\n"
        "**Deliberately left out:** ratings, reviews, Editors' Choice and update history. They only exist after "
        "launch, and in the first version of this tool they leaked the answer (see below).")

# ---------------------------------------------------------------- performance
st.divider()
st.subheader("How well it works")
rows = [("This model", m["model"]),
        ("Guess from category and app age only", m["baseline_category_age"]),
        ("Always guess “under 1K”", m["baseline_majority"])]
perf = pd.DataFrame({
    "": [r[0] for r in rows],
    "Ranks a 10K+ app above one that isn't": [f"{r[1]['auc_10k']:.0%}" if r[1].get("auc_10k") else "50%" for r in rows],
    "Ranks a 100K+ app above one that isn't": [f"{r[1]['auc_100k']:.0%}" if r[1].get("auc_100k") else "50%" for r in rows],
    "Exact band right": [f"{r[1]['accuracy']:.0%}" for r in rows],
    "Within one band": [f"{r[1]['within_one']:.0%}" for r in rows],
})
st.dataframe(perf, hide_index=True, width="stretch")
st.markdown(
    f"**How to read this:** the useful question is not “which exact band?” but “how likely is each milestone?”. "
    f"On that, the model ranks apps that pass 10,000 installs above apps that don't **{m['model']['auc_10k']:.0%}** "
    f"of the time. Exact-band accuracy looks modest (**{m['model']['accuracy']:.0%}**) because more than half of all "
    "apps sit in the lowest band, so even always guessing “under 1K” scores "
    f"{m['baseline_majority']['accuracy']:.0%}. That's also why the tool shows odds out of 100 instead of a single "
    "verdict.")

left, right = st.columns(2, gap="large")
with left:
    cal = pd.DataFrame(m["calibration_10k"], columns=["predicted", "observed", "apps"])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", line=dict(color=AXIS, width=1),
                             hoverinfo="skip", showlegend=False))
    fig.add_trace(go.Scatter(x=cal["predicted"], y=cal["observed"], mode="lines+markers",
                             line=dict(color=BLUE, width=2), marker=dict(size=8, color=BLUE),
                             customdata=cal["apps"], showlegend=False,
                             hovertemplate="Model said %{x:.0%}<br>Actually reached 10K+: %{y:.0%}"
                                           "<br>%{customdata:,} test apps<extra></extra>"))
    fig.update_layout(title=dict(text="When the model says X%, about X% get there", font=dict(size=15, color=INK)),
                      height=340, margin=dict(l=10, r=10, t=50, b=10), plot_bgcolor="#fcfcfb",
                      paper_bgcolor="rgba(0,0,0,0)", font=dict(family="Atkinson Hyperlegible, sans-serif", color=INK_2))
    fig.update_xaxes(title="Model's chance of 10K+", tickformat=".0%", range=[0, 1], gridcolor=GRID, linecolor=AXIS)
    fig.update_yaxes(title="Share that actually got there", tickformat=".0%", range=[0, 1], gridcolor=GRID, linecolor=AXIS)
    st.plotly_chart(fig, config={"displayModeBar": False})
    st.caption("Test apps grouped by the model's predicted chance of passing 10,000 installs. Points near the grey "
               "diagonal mean the stated odds can be taken at face value.")
with right:
    imp = pd.DataFrame(meta["importance"]).head(10).iloc[::-1]
    fig = go.Figure(go.Bar(x=imp["share"], y=imp["label"], orientation="h", marker=dict(color=BLUE),
                           hovertemplate="%{y}: %{x:.0%} of the model's total gain<extra></extra>"))
    fig.update_layout(title=dict(text="What moves the outlook most", font=dict(size=15, color=INK)),
                      height=340, margin=dict(l=10, r=10, t=50, b=10), plot_bgcolor="#fcfcfb",
                      paper_bgcolor="rgba(0,0,0,0)", bargap=0.35,
                      font=dict(family="Atkinson Hyperlegible, sans-serif", color=INK_2))
    fig.update_xaxes(tickformat=".0%", gridcolor=GRID, linecolor=AXIS, title="Share of the model's total gain")
    fig.update_yaxes(linecolor=AXIS)
    st.plotly_chart(fig, config={"displayModeBar": False})
    st.caption("Gain: how much each input improved the model's predictions during training.")

# ---------------------------------------------------------------- v1
st.divider()
st.subheader("What changed from the first version")
st.markdown(
    "The first AppVision reported **96.5% accuracy**. An audit (notebook 02) found three problems:\n"
    "1. **The answer leaked into the inputs.** One input, *rating density*, was calculated by dividing ratings by "
    "the app's install bucket, which is the very thing being predicted. The install bucket could be rebuilt exactly "
    "from two inputs for every app with a rating. With only launch-time information, the same recipe scored "
    "about 63%.\n"
    "2. **The web app sent different inputs from the ones the model learned on.** For example, ratings per day "
    "instead of ratings per install. The same app could flip from “Emerging” to “Low”.\n"
    "3. **The recommender mostly matched apps by release date,** not by what they were or whether they succeeded.\n\n"
    "Version 2 uses only launch-time information, shares one feature definition between training and the app, "
    "tests on unseen developers, and reports itself against simple baselines.")

st.divider()
st.subheader("Limits worth knowing")
st.markdown(
    "- **2021 snapshot.** The store has changed since; treat the numbers as the shape of the market, not today's exact odds.\n"
    "- **No marketing, quality or review data.** Those drive much of what the model can't explain.\n"
    "- **Survivors only.** Apps removed before June 2021 are missing, so older cohorts look a little better than they were.\n"
    "- **Studio track record** uses earlier apps' installs as of 2021, which slightly flatters studios whose catalogue kept growing.\n"
    "- **Patterns, not causes.** The what-if panel and Playbook show how similar apps differed, not what would happen if you changed one thing.")
