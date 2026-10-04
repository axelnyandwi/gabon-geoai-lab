"""Point d’entrée de la plateforme expérimentale Gabon GeoAI Lab."""

import streamlit as st

from src.config import APP_TITLE, PROJECT_STATUS, TAGLINE

st.set_page_config(page_title=APP_TITLE, layout="wide")
st.title(APP_TITLE)
st.markdown(TAGLINE)
st.info(PROJECT_STATUS)
