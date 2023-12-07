import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import numpy as np
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import optparse
import nltk
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import roc_auc_score, roc_curve, precision_recall_curve, auc
import seaborn as sns
import matplotlib.pyplot as plt


SERVER_NAME_REMOTE="localhost"
DB_USER="sa"
DB_PASSWORD="Dep2Groep2-VIC"
DWH_NAME="Voka_DWH"

def connect_db(local=True):
    if local:
        URL_LOCAL = f'mssql+pyodbc://{SERVER_NAME}/{DWH_NAME}?trusted_connection=yes&driver=ODBC+Driver+17 for SQL Server'
        engine = create_engine(URL_LOCAL)
        conn = engine.connect()
        return conn
    else:
        URL = f'mssql+pymssql://{DB_USER}:{DB_PASSWORD}@{SERVER_NAME_REMOTE}:1438/{DWH_NAME}'
        engine = create_engine(URL)
        conn = engine.connect()
        return conn
    
conn = connect_db(local=False)

#####################################################################################################################################################

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

#####################################################################################################################################################

def load_inschrijving():
    #Inschrijving Data
    #needed Inschrijving columns
    inschrijving_col = ['contactID', 'campagneID', 'inschrijvingsDatumID', 'facturatieBedrag']

    #create query
    inschrijving_query = create_query('FactInschrijving', inschrijving_col)
    df_inschrijving = pd.read_sql(inschrijving_query, conn)

    #needed contact col
    contact_col = ['contactID', 'accountID']

    #create query
    contact_query = create_query('DimContact', contact_col)
    df_contact = pd.read_sql(contact_query, conn)

    #merge inschrijving en contact
    df_inschrijving = df_inschrijving.merge(df_contact, on='contactID', how='left')
    
    #needed datum col
    datum_col = ['dateID', 'fullDate']

    #create query
    datum_query = create_query('DimDate', datum_col)
    df_datum = pd.read_sql(datum_query, conn)

    #merge inschrijving en datum
    df_inschrijving = df_inschrijving.merge(df_datum, left_on='inschrijvingsDatumID', right_on='dateID', how='left')
    df_inschrijving.drop(columns=['dateID', 'inschrijvingsDatumID'], inplace=True)
    df_inschrijving.drop('contactID', axis=1, inplace=True)

    df_inschrijving['fullDate'] = df_inschrijving['fullDate'].astype(str)
    df_inschrijving['jaar'] = df_inschrijving['fullDate'].str[:4]
    df_inschrijving['jaar'] = df_inschrijving['jaar'].astype(int)

    return df_inschrijving
    
#####################################################################################################################

def load_accounts():
    df_inschrijving = load_inschrijving()
    #ACCOUNT DATA
    #needed Account columns
    account_col = ['accountID', 'plaats', 'isVokaEntiteit', 'accountStatus', 'ondernemingstype', 'ondernemingsaard', 'activiteitNaam']

    #condition
    account_condition = "provincie = 'Oost-Vlaanderen'"

    #create query
    account_query = create_query('DimAccount', account_col, account_condition)
    df_account = pd.read_sql(account_query, conn)
    df_account['plaats'] = df_account['plaats'].str.replace(r'\([a-z.-]+\)', '', regex=True).str.replace('  ', ' ')
    
    #LIDMAATSCHAP DATA
    #needed Lidmaatschap columns
    lidmaatschap_col = ['lidmaatschapID', 'accountID', 'redenAangroei', 'redenVerloop', 'startDatum', 'opzegDatum']

    #create query
    lidmaatschap_query = create_query('DimLidmaatschap', lidmaatschap_col)
    df_lidmaatschap = pd.read_sql(lidmaatschap_query, conn)
    df_account_lid = df_account.merge(df_lidmaatschap, on='accountID', how='inner')
    
    #opslitsten in 2 dataframes (toevoeging aantal inschrijvingen)
    #opzegdatum omzetten naar string
    df_account_lid['opzegDatum'] = df_account_lid['opzegDatum'].astype(str)
    #we splitsen de dataframes in accounts waarvoor de opzegtdatum = 1950-01-01 en accounts waarvoor de opzegdatum != 1950-01-01
    df_account_ACTIEF = df_account_lid[df_account_lid['opzegDatum'] == '2026-01-01']
    df_account_INACTIEF = df_account_lid[df_account_lid['opzegDatum'] != '2026-01-01']

    #jaar voor opzegDatum per acountID bepalen
    df_account_INACTIEF['jaar'] = df_account_INACTIEF['opzegDatum'].str[:4] 
    df_account_INACTIEF['voorbije_jaar'] = df_account_INACTIEF['jaar'].astype(int) - 1
    df_account_INACTIEF.drop('jaar', axis=1, inplace=True)

    for i, row in df_account_INACTIEF.iterrows():
        accountID = row['accountID']
        voorbije_jaar = row['voorbije_jaar']
        df_account_INACTIEF.loc[i, 'aantal_inschrijvingen'] = df_inschrijving[(df_inschrijving['accountID'] == accountID) & (df_inschrijving['jaar'] == voorbije_jaar)]['accountID'].count()


    df_account_ACTIEF['voorbije_jaar'] = 2022
    for i, row in df_account_ACTIEF.iterrows():
        accountID = row['accountID']
        voorbije_jaar = row['voorbije_jaar']
        df_account_ACTIEF.loc[i, 'aantal_inschrijvingen'] = df_inschrijving[(df_inschrijving['accountID'] == accountID) & (df_inschrijving['jaar'] == voorbije_jaar)]['accountID'].count()

    df_account_ACTIEF['lidmaatschap_actief'] = 1
    df_account_INACTIEF['lidmaatschap_actief'] = 0

    df = pd.concat([df_account_INACTIEF, df_account_ACTIEF], axis=0)
    df.drop('accountStatus', axis=1, inplace=True)
    df.drop('ondernemingsaard', axis=1, inplace=True)

    return df
    
#############################################################################################################################

def one_hot_encoding(df, col):
    df = load_accounts()

    from sklearn.preprocessing import OneHotEncoder

    redenAangroei_cat = ['unknown', 'Actieve werving: koude prospectie',
       'Lead van een collega nalv contact of deelname',
       'Overzetting lidmaatschap', 'Spontane aanvraag via de website',
       'Actieve werving: tip van een collega',
       'Actieve werving: marketingcampagne',
       'Lead van een andere Voka entiteit',
       'Leden maken leden: Lead van een Voka lid',
       'Spontane aanvraag via mail']
    redenVerloop_cat = ['unknown', 'Geen gebruik', 'Prijs', 'Overname', 'Stopzetting',
       'Wanbetaler', 'Ontevreden/klacht', 'Overzetting lidmaatschap',
       'Geen meerwaarde', 'Faillissement', 'FinanciÃ«le moeilijkheden']
    
    # Ondernemingstype
    ondernemingstype_categories = [
    {'categorie': 'unknown', 'binary': None},
    {'categorie': 'Beroepsorganisatie', 'binary': None},
    {'categorie': 'Vakbonden', 'binary': None},
    {'categorie': 'Eenmanszaak', 'binary': None},
    {'categorie': 'Multinational', 'binary': None},
    {'categorie': 'Sociale organisatie', 'binary': None},
    {'categorie': 'Werkgeversorganisaties', 'binary': None},
    {'categorie': 'Pers/Media', 'binary': None},
    {'categorie': 'Overheid', 'binary': None},
    {'categorie': 'Onderwijs', 'binary': None},
    {'categorie': 'Social Profit', 'binary': None},
    {'categorie': 'Vrije beroepen', 'binary': None},
    {'categorie': 'Familiebedrijf', 'binary': None},
    {'categorie': 'Bedrijf', 'binary': None}
    ]

    for i, categorie in enumerate(ondernemingstype_categories):
        categorie['binary'] = str(bin(i)[2:].zfill(4))

    category_to_binary = {categorie['categorie']: categorie['binary'] for categorie in ondernemingstype_categories}
    df['ondernemingstype'] = df['ondernemingstype'].map(category_to_binary)

    for i in range(1, 5):
        df[f'ondernemingstype_{i}'] = df['ondernemingstype'].apply(lambda x: int(str(x)[i-1]))