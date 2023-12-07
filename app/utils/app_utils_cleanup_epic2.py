import csv
import tempfile
import datetime
import re
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pyodbc
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import nltk

# disable dtype warning
pd.options.mode.chained_assignment = None  # default='warn'
# other warnings
import warnings
warnings.filterwarnings("ignore")

# Connect to database
DWH_NAME = st.secrets['DWH_NAME']
SERVER_NAME = st.secrets['SERVER_NAME']
SERVER_NAME_REMOTE = st.secrets['SERVER_NAME_REMOTE']
DB_USER = st.secrets['DB_USER']
DB_PASSWORD = st.secrets['DB_PASSWORD']
LOCAL = st.secrets['LOCAL']

def connect_db(local=True, engine=False):
    if local:
        URL_LOCAL = f'mssql+pyodbc://{SERVER_NAME}/{DWH_NAME}?trusted_connection=yes&driver=ODBC+Driver+17 for SQL Server'
        engine = create_engine(URL_LOCAL)
        if engine:
            return engine
        conn = engine.connect()
        return conn
    else:
        URL = f'mssql+pymssql://{DB_USER}:{DB_PASSWORD}@{SERVER_NAME_REMOTE}:1438/{DWH_NAME}'
        engine = create_engine(URL)
        if engine:
            return engine
        conn = engine.connect()
        return conn

def get_data_from_db(table):
    conn = connect_db(LOCAL)
    df = pd.read_sql(f'SELECT * FROM Voka.dbo.{table}', conn)
    return df

# functies voor het cleanen van de keyphrases
def team_name_change(text):
    teams_dict = {
        'jo': ' jong ondernemen ',
        'do': ' duurzaam ondernemen ',
        'in': ' innovatie digitalisering ',
        'io': ' internationaal ondernemen ',
        'ao': ' arbeidsmarkt ',
        'ex': ' expert ',
        'gr': ' groei ',
        'bb': ' belangenbehartiging ',
        'co': ' communicatie ',
        'nw': ' netwerking ',
        'ha': ' haven ',
        'ma': ' match '
    }
    word_tokens = word_tokenize(text, language='dutch')
    result = [teams_dict.get(word, word) for word in word_tokens]
    cleaned_list = ', '.join(result)
    tokenize_list = word_tokenize(cleaned_list, language='dutch')
    tokenize_list_no_comma = [x for x in tokenize_list if x != ',']
    return ', '.join(list(set(tokenize_list_no_comma)))

def remove_stopwords(text):
    stop_words_nl = set(stopwords.words('dutch'))
    word_tokens = word_tokenize(text, language='dutch')
    result = [x for x in word_tokens if x not in stop_words_nl]
    seperator = ', '
    return seperator.join(result)

def stemmer(text):
    stemmer = SnowballStemmer(language='dutch')
    stem_sentence=[]
    for word in text.split(','):
        stem_sentence.append(stemmer.stem(word))
    stem_sentence= ', '.join(stem_sentence)
    return stem_sentence

def clean_text(df, cols):
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)
    df_copy = df.copy()
    for col in cols:
        for row in range(len(df_copy)):
            try:
                name_change = team_name_change(df_copy[col][row])
                no_stopwords = remove_stopwords(name_change)
                tokenize_list = word_tokenize(no_stopwords, language='dutch')
                tokenize_list = [x for x in tokenize_list if x != ',']
                df_copy.at[row, col] = ', '.join(list(set(tokenize_list)))      
                stemmer_list = stemmer(df_copy[col][row])
                df_copy.at[row, col] = stemmer_list
            except KeyError as e:
                print(f"KeyError: {e}")
    return df_copy

# einde functies voor het cleanen van de keyphrases

def remove_duplicate_pk_single(data, col_pk):
    data = data.groupby(col_pk).agg(lambda x: x.tolist())
    data.reset_index(inplace=True)
    columns = list(data.columns)
    columns.remove(col_pk)
    for col in columns:
        data[col] = data[col].apply(lambda x: list(set(x)))
        for row in data[col]:
            if len(row) > 1:
                if 'unknown' in row:
                    row.remove('unknown')
                row.pop(0)
        data[col] = data[col].apply(lambda x: x[0] if len(x) > 0 else 'unknown')
    data.drop_duplicates(inplace=True)
    return data

def fill_na(dataframe):
    numeric = dataframe.select_dtypes(include='number').columns
    non_numeric = dataframe.select_dtypes(exclude=['number']).columns
    dataframe[numeric] = dataframe[numeric].fillna(-1)
    dataframe[non_numeric] = dataframe[non_numeric].fillna('unknown')
    return dataframe

def create_column_names(dataframe, pk):
    columns = dataframe.columns
    columns = [col + '_id' if col == pk else col for col in columns]
    columns = [re.sub(r'\W+', '', col) for col in columns]
    columns = [col.lower() for col in columns]
    dict_columns = dict(zip(dataframe.columns, columns))
    return dict_columns


def column_name_change(data):
    for col in data.columns:
        if col.startswith('crm_') or col.startswith('CDI_'):
            data.columns = data.columns.str.replace('crm_', '')
            data.columns = data.columns.str.replace('CDI_', '')
    return data

def load_unique_values(tablename, column_name):
    data = get_data_from_db(tablename)
    unique_values = data[column_name].unique()
    return unique_values


def remove_non_existing_pk(data, fk_arr, col_name_arr):
    df=data
    for fk, col_name in zip(fk_arr, col_name_arr):
        if fk == 'account':
            acc_unique = load_unique_values('Account', 'account_account_id')
            fk_arr_index = fk_arr.index('account')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(acc_unique)]
            print(f'FK for {fk}: {len(df)} rows left')

        elif fk == 'contact':
            contact_unique = load_unique_values('Contact', 'contact_contactpersoon_id')
            fk_arr_index = fk_arr.index('contact')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(contact_unique)]
            print(f'FK for {fk}: {len(df)} rows left')

        elif fk == 'persoon':
            persoon_unique = load_unique_values('Persoon', 'persoon_persoon_id')
            fk_arr_index = fk_arr.index('persoon')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(persoon_unique)]
            print(f'FK for {fk}: {len(df)} rows left')

        elif fk == 'afspraak':
            afspraak_alle_unique = load_unique_values('Afspraak_alle', 'afspraak_alle_afspraak_id')
            fk_arr_index = fk_arr.index('afspraak')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(afspraak_alle_unique)]
            print(f'FK for {fk}: {len(df)} rows left')

        elif fk == 'campagne':
            campagne_unique = load_unique_values('Campagne', 'campagne_campagne_id')
            fk_arr_index = fk_arr.index('campagne')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(campagne_unique)]
            print(f'FK for {fk}: {len(df)} rows left')

        elif fk == 'mailing':
            mailing_unique = load_unique_values('Cdi_mailing', 'mailing_mailing_id')
            fk_arr_index = fk_arr.index('mailing')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(mailing_unique)]
            print(f'FK for {fk}: {len(df)} rows left')

        elif fk == 'activiteitscode':
            activiteitscode_unique = load_unique_values('Activiteitscode', 'activiteitscode_activiteitscode_id')
            fk_arr_index = fk_arr.index('activiteitscode')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(activiteitscode_unique)]
            print(f'FK for {fk}: {len(df)} rows left')

        elif fk == 'visit':
            visit_unique = load_unique_values('Cdi_visits', 'visit_visit_id')
            fk_arr_index = fk_arr.index('visit')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(visit_unique)]
            print(f'FK for {fk}: {len(df)} rows left')

        elif fk == 'functie':
            functie_unique = load_unique_values('Functie', 'functie_functie_id')
            fk_arr_index = fk_arr.index('functie')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(functie_unique)]
            print(f'FK for {fk}: {len(df)} rows left')

        elif fk == 'gebruiker':
            gebruiker_unique = load_unique_values('Gebruikers', 'gebruikers_crm_user_id_id')
            fk_arr_index = fk_arr.index('gebruiker')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(gebruiker_unique)]
            print(f'FK for {fk}: {len(df)} rows left')

        elif fk == 'sessie':
            sessie_unique = load_unique_values('Sessie', 'sessie_sessie_id')
            fk_arr_index = fk_arr.index('sessie')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(sessie_unique)]
            print(f'FK for {fk}: {len(df)} rows left')

        elif fk == 'inschrijving':
            inschrijving_unique = load_unique_values('Inschrijving', 'inschrijving_inschrijving_id')
            fk_arr_index = fk_arr.index('inschrijving')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(inschrijving_unique)]
            print(f'FK for {fk}: {len(df)} rows left')
            
        elif fk =='pageviews':
            pageviews_unique = load_unique_values('Cdi_pageviews', 'page_view_id')
            fk_arr_index = fk_arr.index('pageviews')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(pageviews_unique)]
            print(f'FK for {fk}: {len(df)} rows left')
    
    return df  


def default_process(data,pk, dropna=False):

    if dropna:
        data.dropna(inplace=True)
        data.reset_index(inplace=True, drop=True)

    data.drop_duplicates(inplace=True)

    numeric = data.select_dtypes(include='number').columns
    non_numeric = data.select_dtypes(exclude='number').columns
    data[numeric] = data[numeric].fillna(-1)
    data[non_numeric] = data[non_numeric].fillna('unknown')

    data.rename(columns=create_column_names(data, pk), inplace=True)

    return data

def parse_date(date_str, DEFAULT):
    try:
        if date_str:
            date = datetime.datetime.strptime(date_str, "%d-%m-%Y").date()
            return date.strftime("%Y-%m-%d")
    except ValueError:
        pass
    return DEFAULT



def parse_datetime(date_str, DEFAULT):
    try: 
        if date_str:
            date_str = date_str.split(' ')[0]
            date = datetime.datetime.strptime(date_str, "%d-%m-%Y").date()
            return date.strftime("%Y-%m-%d")
    except ValueError:
        pass
    return DEFAULT


def parse_number(number_str):
    try:
        if number_str:
            return float(number_str.replace(',', '.'))
        else:
            return -1
    except ValueError:
        pass
    return -1

def account(data):
    data = column_name_change(data)

    data = data[data['Account_Adres_Provincie'] == 'Oost-Vlaanderen']
    data.replace({'Account_Status': {'Actief': 1, 'Inactief': 0}}, inplace=True)
    data.replace({'Account_Is_Voka_entiteit': {'Ja': 1, 'Nee': 0}}, inplace=True)
    
    if 'Account_Hoofd_NaCe_Code' in data.columns:
        data.drop('Account_Hoofd_NaCe_Code', axis=1, inplace=True)

    data['Account_Oprichtingsdatum'] = data['Account_Oprichtingsdatum'].apply(lambda x: parse_date(str(x), "1750-01-01"))
    
    data = default_process(data, 'Account_Account')
    data = remove_duplicate_pk_single(data, 'account_account_id')
    data = fill_na(data)
    return data



def account_activiteitscode(data):
    data = column_name_change(data)

    data = default_process(data, '')
    data = remove_non_existing_pk(data, ['account', 'activiteitscode'], ['account_activiteitscode_account', 'account_activiteitscode_activiteitscode'])
    data = fill_na(data)
    return data
    


def account_financiele_data(data):
    data = column_name_change(data)

    excluded_ids = [
    "02E2C17D-A213-E211-9DAA-005056B06EB4",
    "5C161136-A768-E111-B43A-00505680000A",
    "8AC9D862-9668-E111-B43A-00505680000A",
    "DFAAE601-1969-E111-B43A-00505680000A"
    ]
    data = data[~data['FinancieleData_OndernemingID'].isin(excluded_ids)]

    data['FinancieleData_Gewijzigd_op'] = data['FinancieleData_Gewijzigd_op'].apply(lambda x: parse_datetime(str(x), "2020-01-01"))
    data['FinancieleData_FTE'] = data['FinancieleData_FTE'].apply(parse_number)
    data['FinancieleData_Toegevoegde_waarde'] = data['FinancieleData_Toegevoegde_waarde'].apply(parse_number)

    data = default_process(data, '')
    data = remove_non_existing_pk(data, ['account'], ['financieledata_ondernemingid'])
    data = fill_na(data)
    return data
    

def activiteit_vereist_contact(data):
    data = column_name_change(data)

    data = default_process(data, 'ActiviteitVereistContact_ActivityId')
    data = remove_non_existing_pk(data, ['afspraak', 'contact'], ['activiteitvereistcontact_activityid_id', 'activiteitvereistcontact_reqattendee'])
    data = remove_duplicate_pk_single(data, 'activiteitvereistcontact_activityid_id')
    data = fill_na(data)
    return data


def activiteitscode(data):
    data = column_name_change(data)

    data = default_process(data, 'ActiviteitsCode_Activiteitscode')
    data = remove_duplicate_pk_single(data, 'activiteitscode_activiteitscode_id')
    data = fill_na(data)
    return data


def afspraak_alle(data):
    data = column_name_change(data)

    data = default_process(data , 'Afspraak_ALLE_Afspraak')
    data = remove_duplicate_pk_single(data, 'afspraak_alle_afspraak_id')
    data = fill_na(data)
    return data
    

def afspraak_betreft_account_cleaned(data):
    data = column_name_change(data)

    data['Afspraak_BETREFT_ACCOUNT_KeyPhrases'] = data['Afspraak_BETREFT_ACCOUNT_KeyPhrases'].replace('\[NAME\] ,*', '', regex=True)
    data['Afspraak_BETREFT_ACCOUNT_Eindtijd'] = data['Afspraak_BETREFT_ACCOUNT_Eindtijd'].apply(lambda x: parse_date(str(x), "2020-01-01"))

    cols_to_clean = ["Afspraak_BETREFT_ACCOUNT_KeyPhrases"]
    cols_to_clean = clean_text(data,cols_to_clean)
    data[cols_to_clean.columns] = cols_to_clean

    data = default_process(data, 'Afspraak_BETREFT_ACCOUNT_Afspraak')
    data = remove_non_existing_pk(data, ['account', 'afspraak'], ['afspraak_betreft_account_betreft_id', 'afspraak_betreft_account_afspraak_id'])
    data = remove_duplicate_pk_single(data, 'afspraak_betreft_account_afspraak_id')
    data = fill_na(data)
    return data


def afspraak_betreft_contact_cleaned(data):
    data = column_name_change(data)

    data['Afspraak_BETREFT_CONTACTFICHE_KeyPhrases'] = data['Afspraak_BETREFT_CONTACTFICHE_KeyPhrases'].replace('\[NAME\] ,*', '', regex=True)
    data['Afspraak_BETREFT_CONTACTFICHE_Eindtijd'] = data['Afspraak_BETREFT_CONTACTFICHE_Eindtijd'].apply(lambda x: parse_date(str(x), "2020-01-01"))
    
    cols_to_clean = ["Afspraak_BETREFT_CONTACTFICHE_KeyPhrases"]
    cols_to_clean = clean_text(data,cols_to_clean)
    data[cols_to_clean.columns] = cols_to_clean 

    data = default_process(data, 'Afspraak_BETREFT_CONTACTFICHE_Afspraak')
    data = remove_non_existing_pk(data, ['contact', 'afspraak'], ['afspraak_betreft_contactfiche_betreft_id', 'afspraak_betreft_contactfiche_afspraak_id'])
    data = remove_duplicate_pk_single(data, 'afspraak_betreft_contactfiche_afspraak_id')
    data = fill_na(data)
    return data
    


def afspraak_account_gelinkt_cleaned(data):
    data = column_name_change(data)

    data['Afspraak_ACCOUNT_GELINKT_KeyPhrases'] = data['Afspraak_ACCOUNT_GELINKT_KeyPhrases'].replace('\[NAME\] ,*', '', regex=True)
    data['Afspraak_ACCOUNT_GELINKT_Eindtijd'] = data['Afspraak_ACCOUNT_GELINKT_Eindtijd'].apply(lambda x: parse_date(str(x), "2020-01-01"))

    cols_to_clean = ["Afspraak_ACCOUNT_GELINKT_KeyPhrases"]
    cols_to_clean = clean_text(data,cols_to_clean)
    data[cols_to_clean.columns] = cols_to_clean 

    data = default_process(data, 'Afspraak_ACCOUNT_GELINKT_Afspraak')
    data = remove_non_existing_pk(data, ['account', 'afspraak'], ['afspraak_account_gelinkt_account', 'afspraak_account_gelinkt_afspraak_id'])
    data = remove_duplicate_pk_single(data, 'afspraak_account_gelinkt_afspraak_id')
    data = fill_na(data)
    return data
    


def campagne(data):
    data = column_name_change(data)

    data['Campagne_Einddatum'] = data['Campagne_Einddatum'].apply(lambda x: parse_datetime(str(x), "2026-01-01"))
    data['Campagne_Startdatum'] = data['Campagne_Startdatum'].apply(lambda x: parse_datetime(str(x), "1750-01-01"))
    
    data = default_process(data, 'Campagne_Campagne')
    data = remove_duplicate_pk_single(data, 'campagne_campagne_id')
    data = fill_na(data)
    return data


def mailings(data):
    data = column_name_change(data)

    data = default_process(data ,'Mailing_Mailing')
    data = remove_duplicate_pk_single(data, 'mailing_mailing_id')
    data = fill_na(data)
    return data


def sent_email_clicks(data):
    data = column_name_change(data)

    data = default_process(data, 'SentEmail_kliks_Sent_Email')
    data = remove_non_existing_pk(data, ['mailing', 'contact'], ['sentemail_kliks_e_mail_versturen', 'sentemail_kliks_contact'])
    data = remove_duplicate_pk_single(data, 'sentemail_kliks_sent_email_id')
    data = fill_na(data)
    return data


def pageviews(data):
    data = column_name_change(data)

    data.columns = data.columns.map(lambda x: re.sub(r'^crm CDI_PageView\[(.*)\]$', r'\1', x))
    data.columns = data.columns.map(lambda x: re.sub(r'^crm_CDI_PageView_(.*)$', r'\1', x))

    data['Time'] = data['Time'].apply(lambda x: parse_datetime(str(x), "1950-01-01"))
    data['Viewed_On'] = data['Viewed_On'].apply(lambda x: parse_datetime(str(x), "1950-01-01"))
    data['Aangemaakt_op'] = data['Aangemaakt_op'].apply(lambda x: parse_datetime(str(x), "1750-01-01"))
    data['Gewijzigd_op'] = data['Gewijzigd_op'].apply(lambda x: parse_datetime(str(x), "1750-01-01"))

    if 'Anonymous_Visitor' in data.columns:
        data.drop(['Anonymous_Visitor'], axis=1, inplace=True)
    if 'Visitor_Key' in data.columns:
        data.drop(['Visitor_Key'], axis=1, inplace=True)    
    if 'crm_CDI_PageView_Campagne_Code' in data.columns:
        data.drop('crm_CDI_PageView_Campagne_Code', axis=1, inplace=True)
    
    data.rename(columns=create_column_names(data, 'Page_View'), inplace=True)

    data = remove_non_existing_pk(data, ['contact', 'campagne', 'visit'], ['Contact', 'Campaign', 'Visit'])
    data = remove_duplicate_pk_single(data, 'page_view_id')
    data = fill_na(data)
    return data


def visits(data):
    data = column_name_change(data)

    if 'Visit_Campagne_Code' in data.columns:
        data.drop('Visit_Campagne_Code', axis=1, inplace=True)
    if 'Visit_Time' in data.columns:
        data.drop('Visit_Time', axis=1, inplace=True)

    data.replace({'Visit_Adobe_Reader': {'Ja': 1, 'Nee': 0}}, inplace=True)
    data.replace({'Visit_Bounce': {'Ja': 1, 'Nee': 0}}, inplace=True)
    data.replace({'Visit_containssocialprofile': {'Ja': 1, 'Nee': 0}}, inplace=True)

    data['Visit_Started_On'] = data['Visit_Started_On'].apply(lambda x: parse_datetime(str(x), "1750-01-01"))
    data['Visit_Ended_On'] = data['Visit_Ended_On'].apply(lambda x: parse_datetime(str(x), "2026-01-01"))
    data['Visit_Aangemaakt_op'] = data['Visit_Aangemaakt_op'].apply(lambda x: parse_datetime(str(x), "1750-01-01"))
    data['Visit_Gewijzigd_op'] = data['Visit_Gewijzigd_op'].apply(lambda x: parse_datetime(str(x), "2026-01-01"))
    
    data = default_process(data, 'Visit_Visit')
    data = remove_non_existing_pk(data, ['contact', 'mailing', 'campagne'], ['visit_contact', 'visit_email_send', 'visit_campaign'])
    data = remove_duplicate_pk_single(data, 'visit_visit_id')
    data = fill_na(data)
    return data
    

def contact_functie(data):
    data = column_name_change(data)

    data = default_process(data, '', dropna=True)
    data = remove_non_existing_pk(data, ['contact', 'functie'], ['contactfunctie_contactpersoon', 'contactfunctie_functie']) 
    data = fill_na(data)
    return data
 

def contact(data):
    data = column_name_change(data)

    df_acc = pd.read_csv('../data_clean/Account_fixed.csv', sep=",")
    acc_unique = df_acc['Account_Account'].unique()
    data = data[data['Contact_Account'].isin(acc_unique)]

    data = default_process(data, 'Contact_Contactpersoon')
    data = remove_non_existing_pk(data, ['account', 'persoon'], ['contact_account', 'contact_persoon_id'])
    data = remove_duplicate_pk_single(data, 'contact_contactpersoon_id')
    data = fill_na(data)
    return data
    


def functie(data):
    data = column_name_change(data)

    data = default_process(data, 'Functie_Functie')
    data = remove_duplicate_pk_single(data, 'functie_functie_id')    
    data = fill_na(data)
    return data


def gebruikers(data):
    data = column_name_change(data)

    data = default_process(data, 'Gebruikers_CRM_User_ID')
    data = remove_duplicate_pk_single(data, 'gebruikers_crm_user_id_id')    
    data = fill_na(data)
    return data


def info_en_klachten(data):
    data = column_name_change(data)

    data['Info_en_Klachten_Datum'] = data['Info_en_Klachten_Datum'].apply(lambda x: parse_datetime(str(x), "1750-01-01"))
    data['Info_en_Klachten_Datum_afsluiting'] = data['Info_en_Klachten_Datum_afsluiting'].apply(lambda x: parse_datetime(str(x), "2026-01-01"))
    
    data = default_process(data, 'Info_en_Klachten_Aanvraag')
    data = remove_non_existing_pk(data, ['account', 'gebruiker'], ['info_en_klachten_account', 'info_en_klachten_eigenaar'])
    data = remove_duplicate_pk_single(data, 'info_en_klachten_aanvraag_id')
    data = fill_na(data)
    return data



def inschrijving(data):
    data = column_name_change(data)

    data['Inschrijving_Datum_inschrijving'] = data['Inschrijving_Datum_inschrijving'].apply(lambda x: parse_date(str(x), "2018-05-01"))
    data['Inschrijving_Facturatie_Bedrag'] = data['Inschrijving_Facturatie_Bedrag'].apply(parse_number)
    
    data = default_process(data, 'Inschrijving_Inschrijving')
    data = remove_non_existing_pk(data, ['contact', 'campagne'], ['inschrijving_contactfiche', 'inschrijving_campagne']) 
    data = remove_duplicate_pk_single(data, 'inschrijving_inschrijving_id')
    data = fill_na(data)
    return data
   

def Lidmaatschap(data):
    data = column_name_change(data)

    data['Lidmaatschap_Startdatum'] = data['Lidmaatschap_Startdatum'].apply(lambda x: parse_date(str(x), "1750-01-01"))
    data['Lidmaatschap_Datum_Opzeg'] = data['Lidmaatschap_Datum_Opzeg'].apply(lambda x: parse_date(str(x), "2026-01-01"))

    data = default_process(data, 'Lidmaatschap_Lidmaatschap')
    data = remove_non_existing_pk(data, ['account'], ['lidmaatschap_onderneming'])
    data = remove_duplicate_pk_single(data, 'lidmaatschap_lidmaatschap_id')
    data = fill_na(data)
    return data

    


def persoon(data):
    data = column_name_change(data)

    data.replace('Nee', 0, inplace=True)
    data.replace('Ja', 1, inplace=True)
    
    data = default_process(data, 'Persoon_persoon')
    data = remove_duplicate_pk_single(data, 'persoon_persoon_id')
    data = fill_na(data)
    return data



def sessie_inschrijving(data):
    data = column_name_change(data)

    data = default_process(data, 'SessieInschrijving_SessieInschrijving', dropna=True)
    data = remove_non_existing_pk(data, ['sessie', 'inschrijving'], ['sessieinschrijving_sessie', 'sessieinschrijving_inschrijving'])
    data = remove_duplicate_pk_single(data, 'sessieinschrijving_sessieinschrijving_id')
    data = fill_na(data)
    return data




def sessie(data):
    data = column_name_change(data)

    data['Sessie_Eind_Datum_Tijd'] = data['Sessie_Eind_Datum_Tijd'].apply(lambda x: parse_datetime(str(x), "2026-01-01"))
    data['Sessie_Start_Datum_Tijd'] = data['Sessie_Start_Datum_Tijd'].apply(lambda x: parse_datetime(str(x), "1750-01-01"))

    data = default_process(data, 'Sessie_Sessie')
    data = remove_non_existing_pk(data, ['campagne'], ['sessie_campagne'])
    data = remove_duplicate_pk_single(data, 'sessie_sessie_id')
    data = fill_na(data)
    return data
    



def teams(data):
    data = column_name_change(data)

    data = default_process(data, '')
    data = fill_na(data)
    return data
    

def clean_data(filename, data):

    dict_filename = {
    'Account activiteitscode.csv': account_activiteitscode,
    'Account.csv': account,
    'Account financiële data.csv': account_financiele_data,
    'Activiteitscode.csv': activiteitscode,
    'Activiteit vereist contact.csv': activiteit_vereist_contact,
    'Afspraak account gelinkt_cleaned.csv': afspraak_account_gelinkt_cleaned,
    'Afspraak alle.csv': afspraak_alle,
    'Afspraak betreft_account_cleaned.csv': afspraak_betreft_account_cleaned,
    'Afspraak betreft_contact_cleaned.csv': afspraak_betreft_contact_cleaned,
    'Campagne.csv': campagne,
    'CDI mailing.csv': mailings,
    'cdi pageviews.csv': pageviews,
    'CDI sent email clicks.csv': sent_email_clicks,
    'CDI visits.csv': visits,
    'Contact.csv': contact,
    'Contact functie.csv': contact_functie,
    'Functie.csv': functie,
    'Gebruikers.csv': gebruikers,
    'Info en klachten.csv': info_en_klachten,
    'Inschrijving.csv': inschrijving,
    'Lidmaatschap.csv': Lidmaatschap,
    'Persoon.csv': persoon,
    'Sessie.csv': sessie,
    'Sessie inschrijving.csv': sessie_inschrijving,
    'teams.csv': teams,
    }

    if filename in dict_filename.keys():
        return dict_filename[filename](data)
       

# Function to bulk insert data from CSV into the appropriate model
def bulk_insert_data_from_dataframe(data, model_class):
    engine = connect_db(LOCAL, engine=True)

    data.to_sql(model_class.__tablename__, con=engine, if_exists='replace', index=False)



    # engine = connect_db(LOCAL, engine=True)
    # Session = sessionmaker(bind=engine)
    # session = Session()

    # sql = f'ALTER TABLE Voka.dbo.{model_class.__tablename__} NOCHECK CONSTRAINT ALL'
    # session.execute(text(sql))
    # sql = f'DELETE FROM Voka.dbo.{model_class.__tablename__}'
    # session.execute(text(sql))

    # with tempfile.NamedTemporaryFile(delete=False, suffix='.csv', mode='w') as temp_csv:
    #     data.to_csv(temp_csv.name, index=False)

    #     # Use DictReader to read from the temporary CSV file
    #     with open(temp_csv.name, mode='r') as csv_file:
    #         csv_reader = csv.DictReader(csv_file)
    #         data_to_insert = [row for row in csv_reader]

    # # Perform the bulk insert
    # session.bulk_insert_mappings(model_class, data_to_insert)
    
    # sql = f'ALTER TABLE Voka.dbo.{model_class.__tablename__} CHECK CONSTRAINT ALL'
    # session.execute(text(sql))  
    # session.commit()