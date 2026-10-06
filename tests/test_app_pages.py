"""Smoke test: every page renders without an exception (needs the files in artifacts/)."""

from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parent.parent / "app.py")
PAGES = ["views/launch_outlook.py", "views/playbook.py", "views/benchmark.py", "views/how_it_works.py"]


def test_every_page_renders():
    at = AppTest.from_file(APP, default_timeout=180).run()
    assert not at.exception, at.exception
    for page in PAGES:
        # a fresh session per page: AppTest can't carry segmented-control state across page switches
        at = AppTest.from_file(APP, default_timeout=180).run()
        at.switch_page(page).run()
        assert not at.exception, f"{page}: {at.exception}"
