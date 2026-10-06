"""The engagement: Osu Lane Studio (fictional) and the three concepts it is choosing between.

Used by the notebooks and as the app's starting example, so both tell the same story.
"""

from .outlook import Concept

CLIENT = "Osu Lane Studio"
CLIENT_BLURB = "a five-person indie studio in Accra with budget to build one new Android app this year"

# The studio's track record: two earlier apps that typically reached 1K–10K installs
STUDIO = dict(prior_apps=2, prior_typical_band=1, has_website=True, has_privacy=True)

CONCEPTS = {
    "A": Concept(
        title="Budget and expense tracker", category="Finance",
        price_usd=0.0, ad_supported=False, in_app_purchases=True, size_mb=18.0,
        content_rating="Everyone", min_android=6.0, **STUDIO),
    "B": Concept(
        title="Offline word puzzle game", category="Word",
        price_usd=0.0, ad_supported=True, in_app_purchases=True, size_mb=45.0,
        content_rating="Everyone", min_android=5.0, **STUDIO),
    "C": Concept(
        title="Exam prep flashcards quiz", category="Education",
        price_usd=0.0, ad_supported=True, in_app_purchases=False, size_mb=22.0,
        content_rating="Everyone", min_android=5.0, **STUDIO),
}

CONCEPT_PITCH = {
    "A": "Track spending and set monthly budgets; free with a paid premium tier.",
    "B": "Daily word puzzles that work without a connection; free with ads and a remove-ads purchase.",
    "C": "Flashcards and timed quizzes for secondary-school exams; free with ads.",
}
