import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DWH_NAME = st.secrets["DWH_NAME"]
SERVER_NAME = st.secrets["SERVER_NAME"]
DB_USER = st.secrets["DB_USER"]
DB_PASSWORD = st.secrets["DB_PASSWORD"]


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

def get_account(conn):
    acc_cols = ['accountID', 'plaats','subregio','ondernemingsaard','ondernemingstype','activiteitNaam']
    # account conditie
    acc_condition = "provincie = 'Oost-Vlaanderen'"
    # create query
    acc_query = create_query('DimAccount', acc_cols, acc_condition)
    # read sql
    df_account = pd.read_sql(acc_query, conn)
    
    return df_account

def get_contact(conn):
    contact_cols = ['contactID', 'accountID', 'functietitel','functieNaam']

    contact_query = create_query('DimContact', contact_cols)
    df_contact = pd.read_sql(contact_query, conn)

    df_contact['functietitel'] = df_contact['functietitel'].str.lower()

    df_contact['functieNaam'] = df_contact['functieNaam'].str.lower()

    return df_contact

def get_afspraak(conn):
    afspraak_cols = ['accountID', 'keyphrases']

    afspraak_query = create_query('DimAfspraak', afspraak_cols)

    df_afspraak = pd.read_sql(afspraak_query, conn)

    return df_afspraak

def get_campagne(conn):
    campagne_cols = ['campagneID','campagneType','campagneNaam','campagneSoort']

    campagne_query = create_query('DimCampagne', campagne_cols)

    df_campagne = pd.read_sql(campagne_query, conn)

    return df_campagne

def get_factInschrijving(conn):
    factInschrijving_cols = ['campagneID','contactID']

    factInschrijving_query = create_query('FactInschrijving', factInschrijving_cols)

    df_factInschrijving = pd.read_sql(factInschrijving_query, conn)

    return df_factInschrijving

def merge_all(conn):
    #merge account en contact
    df_account = get_account(conn)
    df_contact = get_contact(conn)

    accounts_merged = pd.merge(df_contact, df_account, on='accountID', how='inner')

    #merge afspraak en accounts_merged
    df_afspraak = get_afspraak(conn)

    acc_con_afs = pd.merge(accounts_merged, df_afspraak, on='accountID', how='inner')

    #merge campagne en factInschrijving
    df_campagne = get_campagne(conn)
    df_factInschrijving = get_factInschrijving(conn)

    camp_fact = pd.merge(df_campagne, df_factInschrijving, on='campagneID', how='inner')

    #merge acc_con_afs en camp_fact
    df_all = pd.merge(acc_con_afs, camp_fact, on='contactID', how='inner')

    return df_all

def clean_merged(df):
    df_clean = df.drop_duplicates(subset=['contactID','campagneID'], keep='first')
    df_clean = df_clean[['contactID','plaats','subregio','ondernemingsaard','ondernemingstype','activiteitNaam','campagneID','campagneType','campagneNaam','campagneSoort','keyphrases','functietitel','functieNaam']]
    
    original = df_clean.copy()
    
    return (df_clean, original)

def vectorizing(df):
  df2 = df
  df2['data'] = df[df.columns[1:]].apply(lambda x: ','.join(x.dropna().astype(str)),axis=1)

  vectorizer = CountVectorizer()
  vectorized = vectorizer.fit_transform(df2['data'])
  return vectorized

def lookalike_matrix(df):
  vectorized = vectorizing(df)

  similarities = cosine_similarity(vectorized)

  matrix = pd.DataFrame(similarities,columns=df['contactID'],index=df['contactID']).reset_index()

  return matrix

def recommend_lookalikes(df, input_contactid, top_n=10):
  matrix = lookalike_matrix(df)
  top_recommendations = matrix.nlargest(40,input_contactid)
  recommendations = pd.DataFrame({
      'contactID': top_recommendations['contactID'],
      'score': top_recommendations[input_contactid]
  })
  recommendations = recommendations[recommendations['contactID']!=input_contactid]
  recommendations = recommendations.drop_duplicates(subset=['contactID'], keep='first').reset_index(drop=True)

  return recommendations.head(top_n)
    