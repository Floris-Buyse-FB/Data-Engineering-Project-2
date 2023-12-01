import streamlit as st
import pandas as pd
from datetime import date

from utils.app_utils_email_epic7 import generate_personalized_email

# Streamlit UI
st.title('Generate a personalized email')

naam = st.text_input('naar wie wil je de mail sturen?')


campagnes = ["Campagne 1", "Campagne 2", "Campagne 3"]
campagne_doelen = ["Awareness", "Consideration", "Conversion"]
campagne_strategieen = ["Google Ads", "Facebook Ads", "LinkedIn Ads"]


personalized_email = generate_personalized_email(naam, campagnes, campagne_doelen, campagne_strategieen)

st.text_area('Personalized email', personalized_email, height=500)
# Toon de gegenereerde e-mail
