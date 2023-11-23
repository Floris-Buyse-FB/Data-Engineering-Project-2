import streamlit as st
import pandas as pd
from datetime import date

from utils.app_utils_lookalike_epic4 import recommend_lookalikes, connect_db, merge_all, clean_merged

# Streamlit UI
st.title('Create lookalikes for a contact')

# Get the contact ID
st.write('Write the contact id of the contact you want to find lookalikes for')
contact_id = st.text_input('Contact ID', value='0542DA63-2C64-ED11-9561-6045BD895B5A')

top_n = st.text_input('How many lookalikes do you want?', value=10)
# make sure the input is a number

try:
    top_n = int(top_n)
except:
    st.write('Please enter a number')
    top_n = 10

# Connect to the database
conn = connect_db(local=True)

# Get the data from the database

df = merge_all(conn)

# Clean the data
df_clean, original = clean_merged(df)

# Get the recommendations
recommendations = recommend_lookalikes(df_clean,contact_id,top_n)

st.write('The top ' + str(top_n) + ' lookalikes for contact ' + str(contact_id) + ' are: ')
st.dataframe(recommendations)

# show the recommendations with the original data
st.write('The top ' + str(top_n) + ' lookalikes for contact ' + str(contact_id) + ' are: ')
st.dataframe(pd.merge(recommendations['contactID'], original, on='contactID', how='inner'))