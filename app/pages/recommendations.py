import streamlit as st
import requests
import pandas as pd
from utils.app_utils_functions import clean_new_campaign_data

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
                # display the response
                st.write(response.json())
        except:
            st.write('Something went wrong, please try again')

   

