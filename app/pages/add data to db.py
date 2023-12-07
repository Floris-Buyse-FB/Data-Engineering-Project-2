import streamlit as st
import pandas as pd
from utils.app_utils_cleanup_epic2 import clean_data, bulk_insert_data_from_dataframe
from utils.orm_model import *

# Streamlit app
def main():
    st.title("CSV Data Upload to Database, with correct filename.")

    # Upload CSV file
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file:
        filename = uploaded_file.name

    if uploaded_file is not None:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)

        # Display the uploaded data
        st.write("Uploaded Data:")
        st.write(df)

        # Button to add data to the database
        if st.button("Add Data to Database"):
            add_data_to_database(filename, df)

# Function to add data to the database (replace this with your database integration logic)
def add_data_to_database(filename, data):
    # clean the data ...
    cleaned_data = clean_data(filename, data)

    # Add the data to the database
    csv_model_mapping = {
    'Account.csv': Account,
    'Account financiële data.csv': Account_financiële_data,
    'Afspraak alle.csv': Afspraak_alle,
    'Persoon.csv': Persoon,
    'Contact.csv': Contact,
    'Activiteit vereist contact.csv': Activiteit_vereist_contact,
    'Activiteitscode.csv': Activiteitscode,
    'Account activiteitscode.csv': Account_activiteitscode,                   
    'Afspraak betreft account_cleaned.csv': Afspraak_betreft_account_cleaned,
    'Afspraak betreft contact_cleaned.csv': Afspraak_betreft_contact_cleaned,   
    'Afspraak_account_gelinkt_cleaned.csv': Afspraak_account_gelinkt_cleaned,
    'Campagne.csv': Campagne,
    'CDI mailing.csv': Cdi_mailing,
    'CDI sent email clicks.csv': Cdi_sent_email_clicks,
    'CDI visits.csv': Cdi_visits,
    'cdi pageviews.csv': Cdi_pageviews,
    'Functie.csv': Functie,
    'Contact functie.csv': Contact_functie,
    'Gebruikers.csv': Gebruikers,
    'Info en klachten.csv': Info_en_klachten,
    'Inschrijving.csv': Inschrijving,
    'Lidmaatschap.csv': Lidmaatschap,
    'Sessie.csv': Sessie,
    'Sessie inschrijving.csv': Sessie_inschrijving,
    'teams.csv': Teams
    }

    bulk_insert_data_from_dataframe(cleaned_data, csv_model_mapping[filename])

    # Placeholder message for demonstration
    st.success(f"Successfully added {filename} to the database!")


if __name__ == "__main__":
    main()
