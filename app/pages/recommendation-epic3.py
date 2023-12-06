import time
import pandas as pd
import streamlit as st
from datetime import date
from utils.app_utils_rec_epic_3 import *

# Streamlit UI
st.title('Recommendations - Epic 3')
st.subheader('Follow the instructions.')
# Tabs
data_tab, rec_tab, download_tab = st.tabs(['Data', 'Recommendations', 'Download'])

# Tab finish vars
merged_total = None
df_inschrijving = None
contactids = None

@st.cache_data
def get_data(contactids):
    st.write('Setting up database connection and preloading data, please wait a moment')
    conn = connect_db()
    merged_total, df_inschrijving = get_all_data(contactids, conn)
    return merged_total, df_inschrijving


# Data tab
with data_tab:

    data_tab_done = False

    st.info('1. Fill in howmany campaigns you want to recommend per contact.\n2. Upload a txt file with contact id\'s seperated by just a comma.\n3. Wait for everything to load and go to the next tab when instructed.')
    top_n = st.number_input('How many campaigns do you want to recommend per contact ID?', min_value=1, max_value=1000, value=10)
    txt_file = st.file_uploader('Upload a txt file with contact id\'s seperated by just a comma')
    st.write("Tip: you can use the following website https://arraythis.com/ to seperate a list of contact id's with commas")

    if txt_file is not None:

        with st.status('Data tab status', expanded=True) as status:
            try:
            # init the data
                contactids = str(txt_file.read().decode('utf-8'))
                if ',' in contactids:
                    contactids = contactids.split(',')
                    contactids = [contactid.strip() for contactid in contactids]
                else:
                    contactids = [contactids.strip()]
                merged_total, df_inschrijving = get_data(contactids)
                st.success('Database connection and preloading data successful')
                status.update(label='Done processing data', state='complete', expanded=False)
                data_tab_done = True
            except Exception as e:
                st.error(f"{e}. Make sure the txt file contains the right data")
                status.update(label='Something went wrong', state='error', expanded=True)
                st.stop()
        
        if data_tab_done:
            st.success('Success, go to the next tab')

# Recommendations tab
with rec_tab:

    rec_tab_done = False
    
    st.info('This tab will give you the recommendations for the contacts you gave through.')
    recommended = False
    st.write("The recommendations might take a while to load, please be patient")
    if data_tab_done and txt_file is not None:
        merged_total = one_hot_encoding(merged_total)
        recommendations_list, extra_info = get_recommendations(contactids, merged_total, df_inschrijving, top_n)
        
        st.write('Recommended campaigns')
        
        unique_contact_ids = extra_info['contactID'].unique()

        for contact_id in unique_contact_ids:
            st.write(f"ContactID: {contact_id}")
            
            contact_data = extra_info[extra_info['contactID'] == contact_id].drop(columns=['contactID', 'zekerheid'])
            contact_data['zekerheid'] = (contact_data['predict_proba'] * 100).round(2)
            # add a % sign to the zekerheid column
            contact_data['zekerheid'] = contact_data['zekerheid'].astype(str) + '%'

            contact_data = contact_data.drop(columns=['predict_proba'])
            reversed_columns = contact_data.columns[::-1]
            
            st.dataframe(contact_data[reversed_columns].reset_index(drop=True), use_container_width=True)
            
            st.markdown("---")
        
        rec_tab_done = True

with download_tab:
    
    st.info("Here you can download the recommended campaigns.")

    if rec_tab_done: 

        df = pd.DataFrame()
        df['contactID'] = [item['contactID'] for item in recommendations_list]
        max_recommendations = max(len(item['recommendations']) for item in recommendations_list)
        for i in range(1, max_recommendations + 1):
            df[f'recommended_campaign_{i}'] = [item['recommendations'][i - 1] if len(item['recommendations']) >= i else None for item in recommendations_list]
        
        csv = df.to_csv(index=False)
        st.download_button(
            label='Download the recommendations',
            data=csv,
            file_name=f'recommendations_{date.today()}.csv',
            mime='text/csv',
        )
        
        st.json(recommendations_list)