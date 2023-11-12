import streamlit as st
import pandas as pd
from datetime import date
from utils.app_utils_functions import clean_new_campaign_data, clean_contact_df, recommend, preproces_df, default_mp_cols, get_hulp_df, calc_marketing_pressure

# Streamlit UI
st.title('Check out the tabs, starting with the data tab')

# Tabs
data_tab, cols_tab, weights_tab, rec_tab = st.tabs(['Data', 'Cols', 'Weights', 'Recommendations'])

# Tab finish vars
col_chose_finished = False
weight_finished = False

# Data tab
with data_tab:
    # make it possible to input a csv file
    csv_file = st.file_uploader('Upload a csv file')
    # if a file is uploaded
    if csv_file is not None:
        # read the file
        df_campagne = pd.read_csv(csv_file)
        # clean the dataframe
        df_campagne_clean = pd.DataFrame()
        try:
            df_campagne_clean = clean_new_campaign_data(df_campagne)
        except Exception as e:
            error_type = e.__getattribute__('__class__').__name__
            if error_type == 'KeyError':
                st.write(f"{error_type}: {e} not found in the csv file")
            else:
                st.write(f"{error_type}: {e}")
        # display the dataframe
        if df_campagne_clean.empty:
            st.write('Something went wrong, please check the error message above')
        else:
            st.dataframe(df_campagne_clean)
        # type a campaign id to give recommendations for
        campaign_id = st.text_input("Enter a campaign ID for recommendation")
        if campaign_id:
            try:
                df_campagne_clean = df_campagne_clean[df_campagne_clean['campagne_campagne_id'] == campaign_id]
                if df_campagne_clean.empty:
                    st.write('Campaign ID not found')
                else:
                    # make the tab change to the weights tab automatically
                    st.write('Campaign ID found, please go to the weights tab to set the weights')
            except Exception as e:
                st.write('Something went wrong, please try again\n', e)


# Cols tab
with cols_tab:
    # get the hulp dataframe to use for the weights and recommendations
    df_hulp = get_hulp_df()
    # get default columns for marketing pressure
    mp_cols = default_mp_cols(df_hulp)

    # option to select all columns for marketing pressure
    select_all = st.checkbox('Select all columns for marketing pressure')

    # create a list to store the columns chosen for marketing pressure
    mp_cols_chosen = []
    if select_all:
        mp_cols_chosen = mp_cols
    else:
        # select the columns to use for marketing pressure
        mp_cols_chosen = st.multiselect(
            label='Select the columns you want to use for marketing pressure',
            options=mp_cols)
    
    # display the columns selected
    st.write('The columns you selected are:', mp_cols_chosen)

    # init variable to check if the user is done selecting columns
    col_chose_finished = st.checkbox('Finished choosing columns')

    # if the user has selected columns for marketing pressure
    if col_chose_finished:
        st.write('Please proceed to the next tab to set the weights')
    

# Weights tab
with weights_tab:
    if col_chose_finished:

        # init a dictionary to store the weights
        weights_dict = {}

        for col in mp_cols_chosen:
            weight = st.slider(col, min_value=0.0, max_value=2.0, value=1.0, step=0.1)
            weights_dict[col] = weight
        
        # display the weights
        st.write('The weights you selected are:', weights_dict)

        # init variable to check if the user is done setting the weights
        weight_finished = st.checkbox('Finished setting the weights')

        # if the user has set the weights
        if weight_finished:
            st.write('Please proceed to the next tab to get the recommendations')


# Recommendations tab
with rec_tab:
    if weight_finished:
        # select the top n recommendations
        top_n = st.text_input('How many recommendations do you want?', value=10)
        # make sure the input is a number
        try:
            top_n = int(top_n)
        except:
            st.write('Please enter a number')
            top_n = 10
        
        # get the hulp dataframe
        df_hulp = get_hulp_df()

        # remove the columns that are not chosen for marketing pressure
        remove_cols = [col for col in mp_cols if col not in mp_cols_chosen]
        df_hulp.drop(columns=remove_cols, inplace=True)

        # calc the marketing pressure
        df_hulp_mp_calc = calc_marketing_pressure(df_hulp, mp_cols_chosen, weights_dict)

        # preprocess the dataframe
        df_hulp_prep = preproces_df(df_hulp_mp_calc)

        # turn df_campagne_clean which is only 1 row into a dataframe, into a string
        df_campagne_clean = df_campagne_clean.to_string(header=False, index=False, index_names=False)

        # get the recommendations
        response_list = recommend(df_hulp_prep, df_campagne_clean, top_n=top_n)

        # turn into dataframe
        response_df = pd.DataFrame(response_list)

        # rename columns
        response_df.rename(columns={0: 'contact_contactpersoon_id', 1: 'marketing_pressure'}, inplace=True)

        # getting other information about the contact persons
        response_df = clean_contact_df(response_df['contact_contactpersoon_id'], df_hulp_prep)

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
#                 


   
