import streamlit as st
import pandas as pd
from datetime import date

from utils.app_utils_ep

campagnes = ["Campagne 1", "Campagne 2", "Campagne 3"]
campagne_doelen = ["Awareness", "Consideration", "Conversion"]
campagne_strategieen = ["Google Ads", "Facebook Ads", "LinkedIn Ads"]

naam = input("Wat is je naam? ")


personalized_email = generate_personalized_email(naam, campagnes, campagne_doelen, campagne_strategieen)

# Toon de gegenereerde e-mail
print(personalized_email)