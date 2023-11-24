import time
import pandas as pd
import streamlit as st
from datetime import date
from utils.app_utils_rec_epic_5 import *

# Streamlit UI
st.title('Recommendations - Epic 3')
st.subheader('Follow the instructions given in the tab. Start with the data tab')
# Tabs
data_tab, rec_tab = st.tabs(['Data', 'Recommendations'])

# Tab finish vars
col_chose_finished = False


@st.cache_data
def get_data():
    st.write('Setting up database connection and preloading data, please wait a moment')
    conn = connect_db()
    final_no_mp = get_final_no_mp(conn)
    results_df = get_results_df(conn)
    return final_no_mp, results_df


# Data tab
with data_tab:

    data_tab_done = False

    st.info('Upload a txt file with contact id\'s seperated by just a \',\' . Wait for everything to load, then enter a contact ID when prompted.')
    txt_file = st.file_uploader('Upload a csv file with contact id\'s')

    if txt_file is not None:

        with st.status('Data tab status', expanded=True) as status:
            
            # init the data
            final_no_mp, results_df = get_data()
            st.success('Database connection and preloading data successful')

            contactids = txt_file.read().decode('utf-8').split(',')
            contactids = [contactid.strip() for contactid in contactids]

            try:
                st.write('Fetching the data from the database, please wait a moment')
                df_contacts_cleaned = get_df_contact_clean(contactids, results_df)
            except Exception as e:
                error_type = e.__getattribute__('__class__').__name__
                if error_type == 'KeyError':
                    st.error(f"{error_type}: {e} not found in the database.")
                    status.update(label='Something went wrong', state='error', expanded=True)
                    st.stop()
                else:
                    st.error(f"{error_type}: {e}. Make sure the txt file contains the right format")
                    status.update(label='Something went wrong', state='error', expanded=True)
                    st.stop()
            st.success('Fetching the data was successful')

            status.update(label='Done processing data', state='complete', expanded=False)


        with st.status('CampagneID status', expanded=True, state='error') as campagne_status:

            # display the dataframe
            if contactids.empty:
                st.write('Something went wrong, please check the error message above')
            else:
                st.dataframe(contactids)
            # type a campaign id to give recommendations for
            campaign_id = st.text_input("Enter a campaign ID for recommendation", value='')
            
            campagne_status.update(label='Please enter a campaign ID', state='error', expanded=True)
            
            if campaign_id != '':
                try:
                    df_campagne_clean = df_campagne_clean[df_campagne_clean['campagne_campagne_id'] == campaign_id]
                    if df_campagne_clean.empty:
                        st.write('Not found, please check the campaign ID')
                    else:
                        data_tab_done = True
                        campagne_status.update(label='Done', state='complete', expanded=False)

                except Exception as e:
                    st.write('Something went wrong, please try again\n', e)
        
        if data_tab_done:
            st.success('Success, proceed to the "Settings" tab')

# Recommendations tab
with rec_tab:

    st.info('This tab will give you the recommendations for the campaign you selected in the data tab.')
    if not col_chose_finished:
        st.error('Please go back to the previous tab and make sure you inserted the right contact IDs')

    if col_chose_finished:
        
        st.write("The recommendations might take a while to load, please be patient")
        # get the hulp dataframe
        df_hulp = final_no_mp.copy()

        # remove the columns that are not chosen for marketing pressure
        remove_cols = [col for col in mp_cols if col not in mp_cols_chosen]
        df_hulp.drop(columns=remove_cols, inplace=True)

        # calc the marketing pressure
        df_hulp_mp_calc = calc_marketing_pressure(df_hulp, mp_cols_chosen, weights_dict, date_range)
        df_hulp_mp_calc.drop(['fullDate'], axis=1, inplace=True)

        # preprocess the dataframe
        df_hulp_prep = preproces_df(df_hulp_mp_calc)

        # turn df_campagne_clean which is only 1 row into a dataframe, into a string
        df_campagne_clean = df_campagne_clean.to_string(header=False, index=False, index_names=False)

        # get the recommendations
        response_list = recommend(df_hulp_prep, df_campagne_clean, top_n=n_rec)

        # turn into dataframe
        response_df = pd.DataFrame(response_list)

        # rename columns
        response_df.rename(columns={0: 'contactID', 1: 'marketing_pressure', 2: 'similarity score'}, inplace=True)

        # getting other information about the contact persons
        fill_up_df = results_df.copy()
        response_df = response_df.merge(fill_up_df, on='contactID', how='inner')
        response_df['marketing_pressure'] = response_df['marketing_pressure_x']
        response_df.drop(columns=['marketing_pressure_x', 'marketing_pressure_y'], inplace=True)

        # display the response
        st.write('Recommended contact persons')
        st.dataframe(response_df)

        # give the option to download the response
        csv = response_df.to_csv(index=False)
        st.download_button(
            label='Download the recommendations',
            data=csv,
            file_name=f'recommendations_{date.today()}.csv',
            mime='text/csv'
        )