import time
import pandas as pd
import streamlit as st
from datetime import date
from utils.app_utils_lidmaatschap import *

# Streamlit UI
st.title('Voorspelling lidmaatschap - Epic 8')
st.subheader('Follow the instructions.')
# Tabs
data_tab, rec_tab = st.tabs(['Data', 'Recommendations'])

# Tab finish vars
merged_total = None
df_inschrijving = None
contactids = None

@st.cache_data
def get_data():
    st.write('Setting up database connection and preloading data, please wait a moment')
    conn = connect_db(local=False)
    df = one_hot_encoding(conn)
    return df


# Data tab
with data_tab:

    data_tab_done = False

    with st.form(key='accountID'):
        st.info('Seperate the accountIDs with a comma.')
        accountID = st.text_area('What is the accountID(\'s)?')
        submit_button = st.form_submit_button(label='Submit')

    lijst = accountID.split(',')
    lijst = [x.strip() for x in lijst]
    st.write(lijst)
    
    if accountID is not None and accountID != '':

        with st.status('Data tab status', expanded=True) as status:
            try:
            # init the data
                df = get_data()
                st.write(df.drop(['lidmaatschap_actief'], axis=1))
                st.success('Database connection and preloading data successful')
                status.update(label='Done processing data', state='complete', expanded=False)
                data_tab_done = True
            except Exception as e:
                st.error(f"{e}. Make sure the given accountID is correct and try again.")
                status.update(label='Something went wrong', state='error', expanded=True)
                st.stop()
        
        if data_tab_done:
            st.success('Success, go to the next tab')

# Recommendations tab
with rec_tab:

    rec_tab_done = False
    
    st.info('This tab will give you the prediction whether an account will continue (1) its subscription or not (0).')
    recommended = False
    st.write("The prediction might take a while to load, please be patient")
    if data_tab_done:   
        prediction = get_recommendations(lijst, df)
        
        st.write('Prediction about subscription renewal:')
        prediction = ['Will CONTINUE subscription' if x == 1 else 'Will CANCEL subscription' for x in prediction]
        data = {'accountID': lijst, 'prediction': prediction}
        st.write(pd.DataFrame(data))
        print(prediction)
        rec_tab_done = True
