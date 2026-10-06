"""AppVision Analytics · Launch Readiness (v2). Run with: streamlit run app.py"""

import streamlit as st

from appvision import ui

st.set_page_config(page_title="AppVision · Launch Readiness", page_icon="📈", layout="wide")
ui.inject_css()

pages = [
    st.Page("views/brief.py", title="The brief", icon=":material/assignment:", default=True),
    st.Page("views/launch_outlook.py", title="Launch Outlook", icon=":material/insights:"),
    st.Page("views/playbook.py", title="Playbook", icon=":material/menu_book:"),
    st.Page("views/benchmark.py", title="Benchmark", icon=":material/speed:"),
    st.Page("views/how_it_works.py", title="How it works", icon=":material/info:"),
]

st.navigation(pages).run()

with st.sidebar:
    st.caption("AppVision Analytics · Google Play data, June 2021 · "
               "Estimates describe what happened to similar apps, not guarantees.")
