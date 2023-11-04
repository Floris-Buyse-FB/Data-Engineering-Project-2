import streamlit as st
import requests
import pandas as pd

# Streamlit UI
st.title('Post a csv file and get recommendations')

# make it possible to input a csv file
uploaded_file = st.file_uploader("Choose a file")

# if a file is uploaded
if uploaded_file is not None:
    # read the file
    df = pd.read_csv(uploaded_file)
    # display the dataframe
    st.write(df)
    # convert the dataframe to a dictionary
    data = df.to_dict(orient='records')
    # post the data to the API
    response = requests.post('http://localhost:5000/post_data', json=data)
    # display the response
    st.write(response.json())

