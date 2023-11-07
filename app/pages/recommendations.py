import streamlit as st
import requests
import pandas as pd
from utils.app_utils_functions import clean_new_campaign_data, clean_contact_df

API_ENDPOINT = 'http://localhost:5000/post_data'

# Streamlit UI
st.title('Post a csv file and get recommendations')

# make it possible to input a csv file
uploaded_file = st.file_uploader("Choose a file")

# if a file is uploaded
if uploaded_file is not None:
    # read the file
    df = pd.read_csv(uploaded_file)
    # clean the dataframe
    df_clean = clean_new_campaign_data(df)
    # display the dataframe
    st.write(df)
    # type a campaign id to give recommendations for
    campaign_id = st.text_input("Enter a campaign ID for recommendation")
    if campaign_id:
        try:
            df_clean = df_clean[df_clean['campagne_campagne_id'] == campaign_id]
            if df_clean.empty:
                st.write('Campaign ID not found')
            else:
                # convert the dataframe to a dictionary
                data = df_clean.to_dict(orient='records')
                # post the data to the API
                response = requests.post(API_ENDPOINT, json=data)
                # turn response into a dataframe
                response_df = pd.DataFrame(response.json())
                response_df.rename(columns={0: 'contact_contactpersoon_id', 1: 'marketing_pressure'}, inplace=True)
                # getting other information about the contact persons
                response_df = clean_contact_df(response_df['contact_contactpersoon_id'], response_df)
                # display the response
                st.write('Recommended contact persons')
                st.write(response_df)
        except:
            st.write('Something went wrong, please try again')

   

