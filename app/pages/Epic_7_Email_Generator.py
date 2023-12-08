import streamlit as st
import pandas as pd
from datetime import date

from utils.app_utils_email_epic7 import *
from utils.app_utils_rec_epic_3 import *
from utils.app_utils_lookalike_epic4 import *
# Streamlit UI
st.title('Generate a personalized email')

contactid = st.text_input('naar wie wil je de mail sturen?', value='0542DA63-2C64-ED11-9561-6045BD895B5A')
naam=contactid
        
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

top_n = st.number_input('How many campaigns do you want to recommend per contact ID?', min_value=1, max_value=1000, value=3)

contactid = [contactid.strip()]
merged_total, df_inschrijving,conn = get_data(contactid)
merged_total = one_hot_encoding(merged_total)
recommendations_list, extra_info = get_recommendations(contactid, merged_total, df_inschrijving, top_n)

unique_contact_ids = extra_info['contactID'].unique()

for contact_id in unique_contact_ids:
  st.write(f"ContactID: {contact_id}")
            
  contact_data = extra_info[extra_info['contactID'] == contact_id].drop(columns=['contactID', 'Certainty'])
  contact_data['Certainty'] = (contact_data['predict_proba'] * 100).round(2)
            # add a % sign to the zekerheid column
  contact_data['Certainty'] = contact_data['Certainty'].astype(str) + '%'

  contact_data = contact_data.drop(columns=['predict_proba'])
  reversed_columns = contact_data.columns[::-1] 
              
campagne_cols = [ 'campagneNaam', 'campagneType', 'campagneSoort']
campagne_query = create_query('DimCampagne', campagne_cols)
df_campagne = pd.read_sql(campagne_query, conn)
df= pd.merge(contact_data['campagneNaam'], df_campagne, on='campagneNaam', how='inner')

st.dataframe(df)
campagnes=df['campagneNaam'].tolist()
campagne_doelen=df['campagneType'].tolist()
campagne_strategieen=df['campagneSoort'].tolist()

if st.button('Generate email'):
  personalized_email = generate_personalized_email(naam, campagnes, campagne_doelen, campagne_strategieen,handtekening,lengte=len(campagnes))
  st.text_area('Personalized email', personalized_email, height=500)
# Toon de gegenereerde e-mail
