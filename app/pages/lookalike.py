import streamlit as st
import pandas as pd
from datetime import date

from utils.app_utils_lookalike_functions import recommend_lookalikes, get_hulp_df

# Streamlit UI
st.title('Create lookalikes for a contact')

# Get the contact ID
st.write('Write the contact id of the contact you want to find lookalikes for')
contact_id = st.text_input('Contact ID', value='10446D11-F363-ED11-9561-6045BD895B5A')

top_n = st.text_input('How many lookalikes do you want?', value=10)
# make sure the input is a number

try:
    top_n = int(top_n)
except:
    st.write('Please enter a number')
    top_n = 10

df_hulp = get_hulp_df()

response_list = recommend_lookalikes(df_hulp,contact_id,top_n)

response_df = pd.DataFrame(response_list)

st.write('The top ' + str(top_n) + ' lookalikes for contact ' + str(contact_id) + ' are: ')
st.dataframe(response_df)

# give the option to download the response
csv = response_df.to_csv(index=False)
st.download_button(
    label='Download the recommendations',
    data=csv,
    file_name=f'recommendations_{date.today()}.csv',
    mime='text/csv'
)