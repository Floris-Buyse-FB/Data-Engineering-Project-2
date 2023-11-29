import time
import pandas as pd
import streamlit as st
from datetime import date
from utils.app_utils_rec_epic_3 import *

# Streamlit UI
st.title('Recommendations - Epic 3')
st.subheader('Follow the instructions.')
# Tabs
data_tab, rec_tab = st.tabs(['Data', 'Recommendations'])

# Tab finish vars
col_chose_finished = False
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

    st.info('1. Fill in howmany campaign IDs you want to recommend per contact ID.\n2. Upload a txt file with contact id\'s seperated by just a \',\'.\n3. Wait for everything to load.')
    top_n = st.number_input('How many campaign IDs do you want to recommend per contact ID?', min_value=1, max_value=1000, value=10)
    txt_file = st.file_uploader('Upload a csv file with contact id\'s')

    if txt_file is not None:

        with st.status('Data tab status', expanded=True) as status:
            try:
            # init the data
                contactids = str(txt_file.read().decode('utf-8')).split(',')
                contactids = [contactid.strip() for contactid in contactids]
                merged_total, df_inschrijving = get_data(contactids)
                st.success('Database connection and preloading data successful')
                st.write(merged_total.columns)
                status.update(label='Done processing data', state='complete', expanded=False)
                data_tab_done = True
            except Exception as e:
                st.error(f"{e}. Make sure the txt file contains the right data")
                status.update(label='Something went wrong', state='error', expanded=True)
                st.stop()
        
        if data_tab_done:
            st.success('Success, proceed to the "Recommendations" tab')

# Recommendations tab
with rec_tab:

    st.info('This tab will give you the recommendations for the contacts you gave through.')
    
    st.write("The recommendations might take a while to load, please be patient")
    if data_tab_done:
        
        merged_total = one_hot_encoding(merged_total)
        recommendations_list = get_recommendations(contactids, merged_total, df_inschrijving, top_n)
        # display the response
        st.write('Recommended contact persons')
        st.json(recommendations_list)

        df = pd.DataFrame()
        df['contactID'] = [item['contactID'] for item in recommendations_list]
        max_recommendations = max(len(item['recommendations']) for item in recommendations_list)
        for i in range(1, max_recommendations + 1):
            df[f'recommended_campaign_{i}'] = [item['recommendations'][i - 1] if len(item['recommendations']) >= i else None for item in recommendations_list]

        # give the option to download the response
        csv = df.to_csv(index=False)
        st.download_button(
            label='Download the recommendations',
            data=csv,
            file_name=f'recommendations_{date.today()}.csv',
            mime='text/csv'
        )
