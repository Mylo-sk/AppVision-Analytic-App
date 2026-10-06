"""AppVision v2: shared code used by both the training notebooks and the Streamlit app.

Keeping feature definitions in one place means the app can never feed the model
something defined differently from what it was trained on (the main v1 failure).
"""
