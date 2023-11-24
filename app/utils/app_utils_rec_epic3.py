import os
import re
import nltk
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)


ENV_URL = os.path.join(os.getcwd(), '.env')
load_dotenv(ENV_URL)

DWH_NAME = os.environ.get('DWH_NAME')
SERVER_NAME = os.environ.get('SERVER_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')


def connect_db(local=True):
    if local:
        URL_LOCAL = f'mssql+pyodbc://{SERVER_NAME}/{DWH_NAME}?trusted_connection=yes&driver=ODBC+Driver+17 for SQL Server'
        engine = create_engine(URL_LOCAL)
        conn = engine.connect()
        return conn
    else:
        URL = f'mssql+pymssql://{DB_USER}:{DB_PASSWORD}@{SERVER_NAME}/{DWH_NAME}'
        engine = create_engine(URL)
        conn = engine.connect()
        return conn


def create_query(table_name, columns, condition=None):

    query = f"SELECT "

    for i, column in enumerate(columns):
        if i == 0:
            query += f"[{column}]"
        else:
            query += f", [{column}]"
    
    query += f" FROM [{DWH_NAME}].[dbo].[{table_name}]"
    
    if condition:
        query += f" WHERE {condition}"

    return query

def load_contacts(contactids, conn):
    # Load contacts
    contact_cols = ['contactID', 'accountID']
    contact_condition = f"contactID IN {contactids}"
    contact_query = create_query('DimContact', contact_cols, contact_condition)
    df_contact = pd.read_sql(contact_query, conn)
    
    # Load accounts
    acc_cols = ['accountID', 'subregio', 'ondernemingstype', 'ondernemingsaard', 'activiteitNaam', 'contactID']
    acc_condition = f"contactID IN {contactids}"
    acc_query = create_query('DimAccount', acc_cols, acc_condition)
    df_account = pd.read_sql(acc_query, conn)
    
    # Merge contacts and accounts
    accounts_merged = df_contact.merge(df_account, on='contactID', how='left')
    
def load_campaigns(conn):
    campagne_cols = ['campagneID', 'campagneType', 'campagneSoort']
    campagne_query = create_query('DimCampagne', campagne_cols)
    df_campagne = pd.read_sql(campagne_query, conn)

    sessie_cols = ['campaignID', 'themaNaam']
    sessie_query = create_query('DimSessie', sessie_cols)
    df_sessie = pd.read_sql(sessie_query, conn)
    
    sessie_themes_grouped = {
      'sessie_bryo': ['Bryo'],
      'sessie_algemeen': ['Familiebedrijven','Opvolging en Overname','Algemeen Management','Human Resources','Algemeen Management - Intern','Bestuurlijke organisaties'],
      'sessie_onderwijs': ['Opleidingen','Persoonlijke vaardigheden','Onderwijs'],
      'sessie_logistiek': ['Logistiek en Transport','Haven','Supply Chain','Retail'],
      'sessie_welt': ['Welt', 'Welt 2.0', 'Welt 2.0-2023'],
      'sessie_ondernemen': ['Starten', 'Internationaal Ondernemen', 'Jong Voka', 'Groeien', 'Stille Kampioenen', 'Samen doorgaan', 'Strategie'],
      'sessie_duurzaamheid': ['Energie', 'Duurzaam Ondernemen', 'Milieu', 'Mobiliteit'],
      'sessie_lidmaatschap': ['Lidmaatschap'],
      'sessie_innovatie en Technologie': ['Innovatie', 'Digitalisering, IT & Technologie'],
      'sessie_netwerking': ['Netwerking'],
      'sessie_economie': ['Arbeidsmarkt', 'Economie', 'Fiscaal', 'Financieel', 'Marketing & Sales', 'Jobkanaal'],
      'sessie_juridisch': ['Bedrijfsjuridisch', 'Juridisch'],
      'sessie_veiligheid en communicatie': ['Communicatie', 'Veiligheid & Preventie', 'Welzijn en gezondheidszorg'],
      'sessie_andere': ['Plato', 'Ruimtelijke ordening en Infrastructuur', 'Regeringsvorming', 'Industrie', 'Aankoop', 'Privé&Vrije tijd', 'Aantrekkelijke regio', 'Coronavirus', 'unknown']
    }

    def map_thema(thema):
        for category, themes in sessie_themes_grouped.items():
            if thema in themes:
                return category
        return thema

    df_sessie['themaNaam'] = df_sessie['themaNaam'].apply(map_thema)
    
    df_sessie = (df_sessie.assign(themaNaam_list=df_sessie['themaNaam'].str.split(', '))
               .explode('themaNaam_list')
               .drop_duplicates()
               .groupby('campaignID')['themaNaam_list']
               .agg(lambda x: list(set(x)))
               .reset_index()
               .sort_values(by='themaNaam_list', key=lambda x: x.str.len(), ascending=False))

    unique_categories = set(category for row in df_sessie['themaNaam_list'] for category in row)

    for category in unique_categories:
        df_sessie[category] = df_sessie['themaNaam_list'].apply(lambda x: np.int8(category in x))

    df_sessie.drop('themaNaam_list', axis=1, inplace=True)
    
    campagnes_merged = pd.merge(df_campagne, df_sessie, left_on='campagneID', right_on='campaignID', how='left').fillna(0)
    campagnes_merged.drop(['campaignID'], axis=1, inplace=True)
    campagnes_merged.drop_duplicates(keep='first',inplace=True)
    
    return campagnes_merged
    

def load_visits(conn):
    visit_cols = ['contactID', 'visit_first_visit', 'visit_total_pages', 'mailSent_clicks', 'mailSent', 'campaignID']
    visit_query = create_query('DimVisit', visit_cols)
    df_visit = pd.read_sql(visit_query, conn)
    df_visit.drop_duplicates(inplace=True)
    return df_visit

def get_visits(contactID, campaignID, conn):
    visit_cols = ['contactID', 'visit_first_visit', 'visit_total_pages', 'mailSent_clicks', 'mailSent', 'campaignID']
    visit_query = create_query('DimVisit', visit_cols)
    df_visit = pd.read_sql(visit_query, conn)
    df_visit.drop_duplicates(inplace=True)

    return df
  
def get_df_contact_clean(contactids, results_df):
    df_contacts_cleaned = pd.DataFrame()
    for contactid in contactids:
        df_contact_clean = results_df[results_df['contactID'] == contactid]
        df_contacts_cleaned = pd.concat([df_contacts_cleaned, df_contact_clean])
    return df_contacts_cleaned
  
def get_model():
    # load the model
    model = pd.read_pickle('app/data/model.pkl')
    return model