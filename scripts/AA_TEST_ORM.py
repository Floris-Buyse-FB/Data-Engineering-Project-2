import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from AA_ORM_models import (
    Account_activiteitscode,
    Account,
    Account_financiële_data,
    Afspraak_alle,
    Persoon,
    Contact,
    Activiteit_vereist_contact,
    Activiteitscode,
    Afspraak_betreft_account_cleaned,
    Afspraak_betreft_contact_cleaned,
    Afspraak_account_gelinkt_cleaned,
    Campagne,
    CDI_mailing,
    CDI_visits,
    CDI_web_content,
    cdi_pageviews,
    CDI_sent_email_clicks,
    Functie,
    Contact_functie,
    Gebruikers,
    Info_en_klachten,
    Inschrijving,
    Lidmaatschap,
    Sessie,
    Sessie_inschrijving,
    Teams
)

# Database URL
DB_NAME = 'Voka'
SERVER_NAME = 'ASUS_FLORIS'
URL = f'mssql+pyodbc://{SERVER_NAME}/{DB_NAME}?trusted_connection=yes&driver=ODBC+Driver+17 for SQL Server'
DATA_DIR = os.path.join(os.getcwd(), 'data_clean')

# Define your database engine
engine = create_engine(URL)
Session = sessionmaker(bind=engine)
session = Session()

# Function to bulk insert data from CSV into the appropriate model
def bulk_insert_data_from_csv(file_name, model_class):
    with open(os.path.join(DATA_DIR, file_name), 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        data_to_insert = [row for row in csv_reader]

        print(f'\n\n=========================================\nInserting {len(data_to_insert)} rows into {model_class.__name__}\n\n=========================================\n')
        session.bulk_insert_mappings(model_class, data_to_insert)

bulk_insert_data_from_csv('Contact_functie_fixed.csv', Contact_functie)
# # CSV file paths and corresponding model classes
# csv_model_mapping = {
#     'Account_activiteitscode_fixed.csv': Account_activiteitscode,
#     'Account_fixed.csv': Account,
#     'Account_financiële_data_fixed.csv': Account_financiële_data,
#     'Afspraak_alle_fixed.csv': Afspraak_alle,
#     'Persoon_fixed.csv': Persoon,
#     'Contact_fixed.csv': Contact,
#     'Activiteit_vereist_contact_fixed.csv': Activiteit_vereist_contact,
#     'Activiteitscode_fixed.csv': Activiteitscode,
#     'Afspraak_betreft_account_cleaned_fixed.csv': Afspraak_betreft_account_cleaned,
#     'Afspraak_betreft_contact_cleaned_fixed.csv': Afspraak_betreft_contact_cleaned,
#     'Afspraak_account_gelinkt_cleaned_fixed.csv': Afspraak_account_gelinkt_cleaned,
#     'Campagne_fixed.csv': Campagne,
#     'CDI_mailing_fixed.csv': CDI_mailing,
#     'CDI_visits_fixed.csv': CDI_visits,
#     'CDI_web_content_fixed.csv': CDI_web_content,
#     'cdi_pageviews_fixed.csv': cdi_pageviews,
#     'CDI_sent_email_clicks_fixed.csv': CDI_sent_email_clicks,
#     'Functie_fixed.csv': Functie,
#     'Contact_functie_fixed.csv': Contact_functie,
#     'Gebruikers_fixed.csv': Gebruikers,
#     'Info_en_klachten_fixed.csv': Info_en_klachten,
#     'Inschrijving_fixed.csv': Inschrijving,
#     'Lidmaatschap_fixed.csv': Lidmaatschap,
#     'Sessie_fixed.csv': Sessie,
#     'Sessie_inschrijving_fixed.csv': Sessie_inschrijving,
#     'Teams_fixed.csv': Teams
# }


# # Insert data from CSV into the corresponding models
# for csv_file, model_class in csv_model_mapping.items():
#     bulk_insert_data_from_csv(csv_file, model_class)

# Commit the changes
session.commit()

