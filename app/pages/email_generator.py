import streamlit as st
import pandas as pd
from datetime import date

from utils.app_utils_email_epic7 import generate_personalized_email

# Streamlit UI
st.title('Generate a personalized email')

naam = st.text_input('naar wie wil je de mail sturen?', value='0542DA63-2C64-ED11-9561-6045BD895B5A')
campagnes = ["Campagne 1", "Campagne 2", "Campagne 3"]
campagne_doelen = ["Awareness", "Consideration", "Conversion"]
campagne_strategieen = ["Google Ads", "Facebook Ads", "LinkedIn Ads"]

if 'handtekening' not in st.session_state:
    # If not, set a default value
    default_handtekening = '[Je Naam] \n[Je Titel] \n[Bedrijfsnaam] \n[Contactgegevens]'
    st.session_state.handtekening = default_handtekening
else:
    # If it's already stored, use the stored value
    default_handtekening = st.session_state.handtekening

# Create a text area with the default value
handtekening = st.text_area('handtekening', value=default_handtekening, height=120)

# Update the session state with the new value
st.session_state.handtekening = handtekening

if st.button('Generate email'):
  personalized_email = generate_personalized_email(naam, campagnes, campagne_doelen, campagne_strategieen,handtekening)
  st.text_area('Personalized email', personalized_email, height=500)
# Toon de gegenereerde e-mail
