import streamlit as st
import pandas as pd
from datetime import date

from utils.app_utils_lookalike_epic4 import recommend_lookalikes, connect_db, merge_all, clean_merged

# Streamlit UI
st.title('Create lookalikes for a contact')

# Get the contact ID
st.write('Write the contact id of the contact you want to find lookalikes for')
contact_id = st.text_input('Contact ID', value='0542DA63-2C64-ED11-9561-6045BD895B5A')


# Connect to the database
conn = connect_db(local=True)

# Get the data from the database

df = merge_all(conn)

# Clean the data
df_clean, original = clean_merged(df)

st.write('choose on what campaign you want to base the lookalikes on')

campagnes = st.selectbox('Select a campaign or choose all', options=['All'] + list(df_clean[df_clean['contactID'] == contact_id]['campagneNaam'])+ ['None'])
st.write('You selected:', campagnes)


if campagnes == 'All':
    df_all = df_clean.groupby(['contactID','plaats','subregio','ondernemingsaard','ondernemingstype','activiteitNaam','functieNaam','functietitel','keyphrases']).agg(list).reset_index()
    df_all['campagneType'] = df_all['campagneType'].apply(lambda x: ', '.join(list(set(x))))
    df_all['campagneNaam'] = df_all['campagneNaam'].apply(lambda x: ', '.join(list(set(x))))
    df_all['campagneSoort'] = df_all['campagneSoort'].apply(lambda x: ', '.join(list(set(x))))
elif campagnes == 'None':
    df_None = df_clean.drop(columns=['campagneNaam','campagneSoort','campagneType'])
    df_None = df_None.drop_duplicates(subset=['contactID'], keep='first')
else:
    contact_id = df_clean[(df_clean['contactID'] == contact_id) & (df_clean['campagneNaam'] == campagnes)]
    #df_clean = df_clean[df_clean['campagneNaam'] == campagnes]

st.write('The contact you want lookalikes for: ')
if campagnes == 'None':
    st.dataframe(df_None[df_None['contactID']==contact_id])
else:
    st.dataframe(df_clean[df_clean['contactID']==contact_id])

if campagnes == 'All':
    if  st.toggle('look how we train the data', key='show_data'):
        st.write('The data we use to train the model: ')
        st.dataframe(df_all[df_all['contactID']==contact_id])

top_n = st.text_input('How many lookalikes do you want?', value=10)
# make sure the input is a number
try:
    top_n = int(top_n)
except:
    st.write('Please enter a number')
    top_n = 10

if st.button('Create lookalikes', key='lookalikes'):
    with st.status('Creating lookalikes...'):

        # Get the recommendations
        if campagnes == 'All':
            recommendations = recommend_lookalikes(df_all,contact_id,top_n)
        elif campagnes == 'None':
            recommendations = recommend_lookalikes(df_None,contact_id,top_n)
        else:
            recommendations = recommend_lookalikes(df_clean,contact_id,top_n)

    st.write('The top ' + str(top_n) + ' lookalikes for contact ' + str(contact_id) + ' are: ')
    st.dataframe(recommendations)

    # show the recommendations with the original data
    st.write('The top ' + str(top_n) + ' lookalikes for contact ' + str(contact_id) + ' are: ')
    st.dataframe(pd.merge(recommendations['contactID'], original, on='contactID', how='inner'))    
