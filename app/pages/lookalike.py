import streamlit as st
import pandas as pd
from datetime import date

from utils.app_utils_lookalike_functions import clean_new_contact_data, recommend_lookalikes_CONTACT, get_hulp_df

# Streamlit UI
st.title('Check out the tabs, starting with the data tab')

# Tabs
data_tab, rec_tab = st.tabs(['Data', 'Lookalike recommendations'])

# Data tab

with data_tab:
  csv_file = st.file_uploader('Upload a csv file for contact')
  df_contact_clean = pd.DataFrame()
  contact_id = None

  if csv_file is not None:

    df_contact = pd.read_csv(csv_file)

    try:
      df_contact_clean = clean_new_contact_data(df_contact)
    except Exception as e:
      error_type = e.__getattribute__('__class__').__name__
      if error_type == 'KeyError':
        st.write(f"{error_type}: {e} not found in the csv file")
      else:
        st.write(f"{error_type}: {e}")
    
    if df_contact_clean.empty:
      st.write('Something went wrong, please check the error message above')
    else:
      st.dataframe(df_contact_clean)
    
    contact_id = st.text_input("Enter a contact ID for recommendation of lookalikes")

    if contact_id:
      df_contact_clean[df_contact_clean['contact_contactpersoon_id'] == contact_id]
      if df_contact_clean.empty:
        st.write('Contact ID not found')
      else:
        st.write('Contact ID found, please go to the lookalike recommendations tab to see the recommendations')

# Lookalike recommendations tab

with rec_tab:
  top_n = st.text_input('How many recommendations do you want?', value=10)
  # make sure the input is a number
  try:
      top_n = int(top_n)
  except:
      st.write('Please enter a number')
      top_n = 10
  
  df_hulp = get_hulp_df()

  response_list = recommend_lookalikes_CONTACT(df_hulp,df_contact_clean,contact_id,top_n)

  response_df = pd.DataFrame(response_list)

  st.write('The top ' + str(top_n) + ' lookalikes for contact ' + str(contact_id) + ' are: ')
  st.dataframe(response_df)

  csv = response_df.to_csv(index=False)
  st.download_button(
      label='Download the recommendations',
      data=csv,
      file_name=f'recommendations_{date.today()}.csv',
      mime='text/csv'
  )