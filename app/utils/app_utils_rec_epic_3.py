import os
import re
import nltk
import numpy as np
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sklearn.preprocessing import OneHotEncoder

ENV_URL = os.path.join(os.getcwd(), '.env')
load_dotenv(ENV_URL)

DWH_NAME = st.secrets['DWH_NAME']
SERVER_NAME = st.secrets['SERVER_NAME']
DB_USER = st.secrets['DB_USER']
DB_PASSWORD = st.secrets['DB_PASSWORD']
MODEL_PATH = st.secrets['MODEL_PATH']
SERVER_NAME_REMOTE = st.secrets['SERVER_NAME_REMOTE']

def connect_db(local=False):
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

####################################################################################################################################################

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

####################################################################################################################################################

def load_accounts(contactids, conn):
    # Load contacts
    contact_cols = ['contactID', 'accountID']
    if len(contactids) > 1:
        contact_condition = f"contactID IN {tuple(contactids)}"
    else:
        contact_condition = f"contactID = '{contactids[0]}'"
    contact_query = create_query('DimContact', contact_cols, contact_condition)
    df_contact = pd.read_sql(contact_query, conn)
    # Load accounts
    acc_cols = ['accountID', 'subregio', 'ondernemingstype', 'ondernemingsaard', 'activiteitNaam']
    acc_query = create_query('DimAccount', acc_cols)
    df_account = pd.read_sql(acc_query, conn)
    # Merge contacts and accounts
    accounts_merged = df_contact.merge(df_account, on='accountID', how='inner')
    
    def map_thema(thema):
        for category, themes in grouping_categories.items():
            if thema in themes:
                return category
        return thema
    
    grouping_categories = {
        'afspraak_Lidmaatschap': ['Lidmaatschap'],
        'afspraak_Welt': ['Welt', 'Welt 2.0', 'Welt 2.0-2023'],
        'afspraak_Plato & Bryo': ['Plato', 'Bryo'],
        'afspraak_Internationaal Ondernemen': ['Internationaal Ondernemen', 'Internationaal Ondernemen - voor Info en Advies'],
        'afspraak_Technologie en Innovatie': ['Digitalisering, IT & Technologie', 'Innovatie', 'Veiligheid & Preventie'],
        'afspraak_Groeien en Netwerking': ['Groeien', 'Netwerking', 'Communicatie', 'Starten'],
        'afspraak_Duurzaamheid': ['Duurzaam Ondernemen', 'Mobiliteit'],
        'afspraak_Familiebedrijfsmanagement': ['Familiebedrijven', 'Opvolging en Overname'],
        'afspraak_Arbeidsmarkt': ['Arbeidsmarkt', 'Opleidingen'],
        'afspraak_Bedrijfsbeheer': ['Algemeen Management', 'Bestuurlijke organisaties', 'Human Resources', 'Ruimtelijke ordening en Infrastructuur'],
        'afspraak_Financieel': ['Financieel', 'Marketing & Sales', 'Aankoop'],
        'afspraak_Logistiek en Transport': ['Logistiek en Transport', 'Haven']
    }

    afspraak_cols = ['thema', 'contactID']

    afspraak_condition = "contactID is not null"
    afspraak_query = create_query('DimAfspraak', afspraak_cols, afspraak_condition)
    df_afspraak1 = pd.read_sql(afspraak_query, conn)

    df_afspraak1.drop_duplicates(inplace=True)

    df_afspraak1['thema'] = df_afspraak1['thema'].apply(map_thema)
    df_afspraak1 = df_afspraak1.groupby('contactID')['thema'].value_counts().unstack(fill_value=0)
      
    afspraak_cols = ['thema', 'accountID']

    afspraak_condition = "accountID is not null"
    afspraak_query = create_query('DimAfspraak', afspraak_cols, afspraak_condition)
    df_afspraak2 = pd.read_sql(afspraak_query, conn)

    df_afspraak2.drop_duplicates(inplace=True)

    df_afspraak2['thema'] = df_afspraak2['thema'].apply(map_thema)
    df_afspraak2 = df_afspraak2.groupby('accountID')['thema'].value_counts().unstack(fill_value=0).apply(lambda x: np.int8(x))
    
    accounts_merged = accounts_merged.merge(df_afspraak1, on=['contactID'], how='left')
    accounts_merged = accounts_merged.merge(df_afspraak2, on=['accountID'], how='left')

    columns_to_merge = ['afspraak_Arbeidsmarkt', 'afspraak_Bedrijfsbeheer', 'afspraak_Duurzaamheid', 'afspraak_Familiebedrijfsmanagement',
                        'afspraak_Financieel', 'afspraak_Groeien en Netwerking', 'afspraak_Internationaal Ondernemen',
                        'afspraak_Lidmaatschap', 'afspraak_Logistiek en Transport', 'afspraak_Plato & Bryo',
                        'afspraak_Technologie en Innovatie', 'afspraak_Welt']

    for column in columns_to_merge:
        accounts_merged[column] = accounts_merged[f'{column}_x'].combine_first(accounts_merged[f'{column}_y'])

    accounts_merged = accounts_merged.drop(columns=[f'{column}_x' for column in columns_to_merge] + [f'{column}_y' for column in columns_to_merge]).fillna(0)
    return accounts_merged
    
####################################################################################################################################################

def load_campaigns(conn):
    campagne_cols = ['campagneID', 'campagneNaam', 'campagneType', 'campagneSoort']
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
               .reset_index())

    unique_categories = set(category for row in df_sessie['themaNaam_list'] for category in row)

    for category in unique_categories:
        df_sessie[category] = df_sessie['themaNaam_list'].apply(lambda x: np.int8(category in x))

    df_sessie.drop('themaNaam_list', axis=1, inplace=True)
    
    campagnes_merged = pd.merge(df_campagne, df_sessie, left_on='campagneID', right_on='campaignID', how='left').fillna(0)
    campagnes_merged.drop_duplicates(keep='first',inplace=True)
    campagnes_merged.drop(['campaignID'], axis=1, inplace=True)
    return campagnes_merged

####################################################################################################################################################

def load_visits(contactids, conn):
    visit_cols = ['contactID', 'visit_first_visit', 'visit_total_pages', 'mailSent_clicks', 'mailSent', 'campaignID']
    if len(contactids) > 1:
        visit_condition = f"contactID IN {tuple(contactids)}"
    else:
        visit_condition = f"contactID = '{contactids[0]}'"
    visit_query = create_query('DimVisit', visit_cols, visit_condition)
    df_visit = pd.read_sql(visit_query, conn)
    df_visit.drop_duplicates(inplace=True)
    
    df_visit['visit_first_visit'] = df_visit['visit_first_visit'] \
      .str.replace('Ja', '0').str.replace('Nee', '1') \
      .str.replace('unknown', '-1').astype(int)

    df_visit['visit_total_pages'] = df_visit['visit_total_pages']\
          .replace('unknown', '-1.0').astype(float)

    df_visit['aantal_mails'] = df_visit.groupby(
        ['contactID'])['mailSent'].transform('nunique')

    df_visit['clicks_total'] = df_visit.groupby(
        ['contactID'])['mailSent_clicks'].transform('sum')

    df_visit['visit_total_pages'] = df_visit.groupby(
        ['contactID'])['visit_total_pages'].transform('sum').astype(int)

    df_visit['visit_first_visit'] = df_visit.groupby(
        ['contactID'])['visit_first_visit'].transform('sum').astype(int)

    df_visit['mail_click_freq'] = np.round(df_visit['clicks_total'] / df_visit['aantal_mails'], 0)
    df_visit['mail_click_freq'] = df_visit['mail_click_freq'].fillna(-1).astype(int)

    df_visit.drop(['mailSent', 'mailSent_clicks', 'clicks_total', 'aantal_mails'], axis=1, inplace=True)
    df_visit.drop_duplicates(inplace=True)

    int_cols = df_visit.select_dtypes(include=['int64', 'int32']).columns
    df_visit[int_cols] = df_visit[int_cols].astype('int8')

    df_visit.reset_index(inplace=True)
    df_visit.drop_duplicates(inplace=True)
    return df_visit

####################################################################################################################################################

def calc_marketing_pressure(row):
    marketing_pressure_cols = ['visit_first_visit', 'visit_total_pages', 'mail_click_freq']
    return int(row[marketing_pressure_cols].sum())

####################################################################################################################################################
  
def cross_merge(contactids, conn):
    accounts_merged = load_accounts(contactids, conn)
    campagnes_merged = load_campaigns(conn)

    numeric_cols = accounts_merged.select_dtypes(include=np.number).columns
    accounts_merged[numeric_cols] = accounts_merged[numeric_cols].astype('int8')

    numeric_cols = campagnes_merged.select_dtypes(include=np.number).columns
    campagnes_merged[numeric_cols] = campagnes_merged[numeric_cols].astype('int8')
    
    merged_total = pd.merge(accounts_merged.assign(key=1), campagnes_merged.assign(key=1), on='key').drop('key', axis=1)
    return merged_total
      
####################################################################################################################################################  

def get_model():
    model = pd.read_pickle(MODEL_PATH)
    return model

####################################################################################################################################################

def add_marketing_pressure(merged_total, df_visit):
    def calc_marketing_pressure(row):
        marketing_pressure_cols = ['visit_first_visit', 'visit_total_pages', 'mail_click_freq']
        return int(row[marketing_pressure_cols].sum())
    df_visit['marketing_pressure'] = df_visit.apply(calc_marketing_pressure, axis=1)
    merged_total = pd.merge(merged_total, df_visit[['contactID', 'campaignID', 'marketing_pressure']], 
                            left_on=['contactID', 'campagneID'], right_on=['contactID', 'campaignID'], how='left')
    merged_total['marketing_pressure'] = merged_total['marketing_pressure'].fillna(-1).apply(lambda x: np.int8(x))
    merged_total.drop(['campaignID'], axis=1, inplace=True)
    return merged_total

####################################################################################################################################################

def get_inschrijvingen(contactids, conn):
    inschrijving_cols = ['campagneID', 'contactID', 'facturatieBedrag']
    if len(contactids) > 1:
        inschrijving_condition = f"contactID IN {tuple(contactids)}"
    else:
        inschrijving_condition = f"contactID = '{contactids[0]}'"
    inschrijving_query = create_query('FactInschrijving', inschrijving_cols, inschrijving_condition)
    df_inschrijving = pd.read_sql(inschrijving_query, conn)
    return df_inschrijving

####################################################################################################################################################

def get_recommendations(contactids, merged_total, df_inschrijving,top_n=10):
    model = get_model()
    recommendations = []
    custom_order = ['contactID', 'campagneID', 'campagneNaam', 'afspraak_Arbeidsmarkt', 'afspraak_Bedrijfsbeheer', 'afspraak_Duurzaamheid', 'afspraak_Familiebedrijfsmanagement', 'afspraak_Financieel', 'afspraak_Groeien en Netwerking', 'afspraak_Internationaal Ondernemen', 'afspraak_Lidmaatschap', 'afspraak_Logistiek en Transport', 'afspraak_Plato & Bryo', 'afspraak_Technologie en Innovatie', 'afspraak_Welt', 'sessie_ondernemen', 'sessie_logistiek', 'sessie_onderwijs', 'sessie_duurzaamheid', 'sessie_welt', 'sessie_lidmaatschap', 'sessie_innovatie en Technologie', 'sessie_netwerking', 'sessie_algemeen', 'sessie_juridisch', 'sessie_bryo', 'sessie_economie', 'sessie_veiligheid en communicatie', 'sessie_andere', 'marketing_pressure', 'ondernemingstype_1', 'ondernemingstype_2', 'ondernemingstype_3', 'ondernemingstype_4', 'activiteitNaam_1', 'activiteitNaam_2', 'activiteitNaam_3', 'activiteitNaam_4', 'activiteitNaam_5', 'activiteitNaam_6', 'Diensten', 'Productie', '0', '1', '2', '3', '4', '5', '0_campagne_type', '1_campagne_type', '2_campagne_type', '3_campagne_type', '4_campagne_type', '5_campagne_type', 'Online', 'Offline']
    merged_total = merged_total[custom_order]
    extra_info = pd.DataFrame(columns=['contactID', 'campagneID', 'campagneNaam', 'zekerheid'])
    
    for i in contactids:
        df_hulp = merged_total[merged_total['contactID'] == i]
        campaign_ids = df_hulp[['campagneID', 'campagneNaam']]
        df_hulp = df_hulp.drop(['contactID', 'campagneID', 'campagneNaam'], axis=1)
        predictions = model.predict(df_hulp)
        predict_proba = model.predict_proba(df_hulp)
        df_hulp[['campagneID', 'campagneNaam']] = campaign_ids
        df_hulp['contactID'] = i
        df_hulp['predictions'] = predictions
        df_hulp['predict_proba'] = predict_proba[:, 1]
        df_hulp = df_hulp[~df_hulp[['campagneID', 'contactID']].isin(df_inschrijving[['campagneID', 'contactID']]).all(axis=1)]
        
        top_n_recommendations = df_hulp.sort_values(by=['predictions', 'predict_proba'], ascending=False).head(top_n)
        
        extra_info = pd.concat([extra_info, top_n_recommendations[['contactID', 'campagneID', 'campagneNaam', 'predict_proba']]], ignore_index=True)
        
        recommendations.append({
            'contactID': i,
            'recommendations': top_n_recommendations['campagneID'].tolist()
        })
        
    return recommendations, extra_info

####################################################################################################################################################

def get_all_data(contactids, conn):
    df_visit = load_visits(contactids, conn)
    merged_total = cross_merge(contactids, conn)
    merged_total = add_marketing_pressure(merged_total, df_visit)
    df_inschrijving = get_inschrijvingen(contactids, conn)
    merged_total = merged_total.drop(['accountID'], axis=1)
    
    return merged_total, df_inschrijving

####################################################################################################################################################

def one_hot_encoding(merged_total):
    subregio_cat = ['Gent', 'Leiestreek-Meetjesland', 'Dendermonde', 'Aalst', 'Oudenaarde', 'Waasland']
    campagnetype_cat = ['Project', 'Projectgebonden', 'Campagne', 'Opleiding', 'Netwerkevenement', 'Infosessie']

    oneHot_subregio = OneHotEncoder(sparse=False, categories=[subregio_cat])
    oneHot_campagnetype = OneHotEncoder(sparse=False, categories=[campagnetype_cat])
    
    subregio_1hot = oneHot_subregio.fit_transform(merged_total[['subregio']])
    
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
    merged_total['ondernemingstype'] = merged_total['ondernemingstype'].map(category_to_binary)

    for i in range(1, 5):
        merged_total[f'ondernemingstype_{i}'] = merged_total['ondernemingstype'].apply(lambda x: int(str(x)[i-1]))
    
    merged_total['activiteitNaam'] = merged_total['activiteitNaam'].apply(lambda x: 'unknown' if x == 'Luchthavengerelateerd' else x)
    
    # Primaire activiteit
    activiteitNaam_categories = [
      {'categorie': 'unknown', 'binary': None},
      {'categorie': 'Farmacie', 'binary': None},
      {'categorie': 'Diamant, edelstenen, juwelen', 'binary': None},
      {'categorie': 'Havengerelateerd', 'binary': None},
      {'categorie': 'Media', 'binary': None},
      {'categorie': 'Overheid', 'binary': None},
      {'categorie': 'Verenigingen en maatschappelijke organisaties', 'binary': None},
      {'categorie': 'Onderwijs', 'binary': None},
      {'categorie': 'Milieu', 'binary': None},
      {'categorie': 'Vrije beroepen', 'binary': None},
      {'categorie': 'Agrarische & bio-industrie', 'binary': None},
      {'categorie': 'Hout- en meubelindustrie', 'binary': None},
      {'categorie': 'Accountancy & boekhouding', 'binary': None},
      {'categorie': 'Vastgoed', 'binary': None},
      {'categorie': 'Verzekering', 'binary': None},
      {'categorie': 'Financiële diensten', 'binary': None},
      {'categorie': 'Grafische industrie en diensten', 'binary': None},
      {'categorie': 'Automobiel- en Tweewielerindustrie', 'binary': None},
      {'categorie': 'Textiel, kleding en confectie', 'binary': None},
      {'categorie': 'Horeca & toerisme', 'binary': None},
      {'categorie': 'Technologische industrie & diensten', 'binary': None},
      {'categorie': 'Zorg', 'binary': None},
      {'categorie': 'Detailhandel', 'binary': None},
      {'categorie': 'Groothandel', 'binary': None},
      {'categorie': 'Bouw', 'binary': None},
      {'categorie': 'Energie', 'binary': None},
      {'categorie': 'Consultancy', 'binary': None},
      {'categorie': 'Papier & karton', 'binary': None},
      {'categorie': 'Human capital', 'binary': None},
      {'categorie': 'Chemie, petrochemie', 'binary': None},
      {'categorie': 'Distributie, logistiek en transport', 'binary': None},
      {'categorie': 'Telecom & IT', 'binary': None},
      {'categorie': 'Ijzer en staal', 'binary': None},
      {'categorie': 'Voeding', 'binary': None},
      {'categorie': 'Overige industrie & diensten', 'binary': None}
    ]
    
    merged_total['activiteitNaam'] = merged_total['activiteitNaam'].apply(lambda x: 'unknown' if x not in [categorie['categorie'] for categorie in activiteitNaam_categories] else x)

    for i, categorie in enumerate(activiteitNaam_categories):
        categorie['binary'] = str(bin(i)[2:].zfill(6))

    category_to_binary = {categorie['categorie']: categorie['binary'] for categorie in activiteitNaam_categories}
    merged_total['activiteitNaam'] = merged_total['activiteitNaam'].map(category_to_binary)

    for i in range(1, 7):
        merged_total[f'activiteitNaam_{i}'] = merged_total['activiteitNaam'].apply(lambda x: int(str(x)[i-1]))
    
    # Ondernemingsaard
    diensten_column = []
    productie_column = []

    for label in merged_total["ondernemingsaard"]:
        if label == "Productie & Diensten":
            diensten_column.append(1)
            productie_column.append(1)
        elif label == "Diensten":
            diensten_column.append(1)
            productie_column.append(0)
        elif label == "Productie":
            diensten_column.append(0)
            productie_column.append(1)
        else:
            diensten_column.append(0)
            productie_column.append(0)

    ondernemingsaard_multihot = pd.DataFrame({"Diensten": diensten_column, "Productie": productie_column})
    merged_total = merged_total.join(ondernemingsaard_multihot, rsuffix='_ondernemingsaard')
    
    # Campagne soort
    online_column = []
    offline_column = []

    for label in merged_total["campagneSoort"]:
        if label == "On en Offline":
            online_column.append(1)
            offline_column.append(1)
        elif label == "Offline":
            online_column.append(0)
            offline_column.append(1)
        elif label == "Online":
            online_column.append(1)
            offline_column.append(0)
        else:
            online_column.append(0)
            offline_column.append(1)

    campagne_soort_multihot = pd.DataFrame({"Online": online_column, "Offline": offline_column})
    
    # Campagne type
    campagne_type_1hot = oneHot_campagnetype.fit_transform(merged_total[['campagneType']])
    
    merged_total = merged_total.drop(['subregio', 'ondernemingstype', 'activiteitNaam', 'ondernemingsaard', 'campagneSoort', 'campagneType', 'unknown'], axis=1)
    
    # Al de one hot encodings samenvoegen
    merged_total = merged_total.join(pd.DataFrame(subregio_1hot), rsuffix='_subregio')
    merged_total = merged_total.join(pd.DataFrame(campagne_type_1hot), rsuffix='_campagne_type')
    merged_total = merged_total.join(campagne_soort_multihot, rsuffix='_campagneSoort')
    
    int_cols = merged_total.select_dtypes(include=['int64', 'int32', 'float32', 'float64']).columns
    merged_total[int_cols] = merged_total[int_cols].apply(lambda x: np.int8(x))
    
    return merged_total
