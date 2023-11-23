import os
import re
import nltk
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from nltk.corpus import stopwords
from sqlalchemy import create_engine
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

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


# Calculate the marketing pressure


def default_mp_cols(df):
    mp_cols = [col for col in df.columns if col.__contains__('persoon_mail_type') 
                           or col.__contains__('persoon_mail_thema') or col.__contains__('persoon_marketingcommunicatie')]
    mp_cols.append('bron')
    mp_cols.append('visit_first_visit')
    mp_cols.append('visit_total_pages')
    mp_cols.append('mail_click_freq')

    return mp_cols


def calc_marketing_pressure(df, mp_cols, weights_dict=None, date_range=None):
    
    if date_range is not None:
        start_date = np.datetime64(date_range[0])
        end_date = np.datetime64(date_range[1])

        df = df[(df['fullDate'] >= start_date) & (df['fullDate'] <= end_date)]

    if len(mp_cols) == 0:

        mp_cols = default_mp_cols(df)

        if weights_dict is not None:
            for col in mp_cols:
                df[col] = df[col].apply(lambda x: x * weights_dict[col] if x > 0 else x)
            df['marketing_pressure'] = df[mp_cols].sum(axis=1)
            df['marketing_pressure'] = df['marketing_pressure'].astype(int)

        else:
            df['marketing_pressure'] = df[mp_cols].sum(axis=1)
            df['marketing_pressure'] = df['marketing_pressure'].astype(int)

        df.drop(mp_cols, axis=1, inplace=True)
        return df
    
    else:

        if weights_dict is not None:
            for col in mp_cols:
                df[col] = df[col].apply(lambda x: x * weights_dict[col] if x > 0 else x)
            df['marketing_pressure'] = df[mp_cols].sum(axis=1)
            df['marketing_pressure'] = df['marketing_pressure'].astype(int)
        else:
            df['marketing_pressure'] = df[mp_cols].sum(axis=1)
            df['marketing_pressure'] = df['marketing_pressure'].astype(int)

        df.drop(mp_cols, axis=1, inplace=True)
        return df


# Helper function for text cleaning


def remove_stopwords(text):
    stop_words_nl = set(stopwords.words('dutch'))
    
    word_tokens = word_tokenize(text, language='dutch')

    result = [x for x in word_tokens if x not in stop_words_nl]

    seperator = ', '
    return seperator.join(result)


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
    # apply dict to list
    result = [teams_dict.get(word, word) for word in word_tokens]
    # join list to string
    cleaned_list = ', '.join(result)
    # tokenize string
    tokenize_list = word_tokenize(cleaned_list, language='dutch')
    # remove comma
    tokenize_list_no_comma = [x for x in tokenize_list if x != ',']
    # join list to string and remove duplicates from list
    return ', '.join(list(set(tokenize_list_no_comma)))


def stemmer(text):
    stemmer = SnowballStemmer(language='dutch')
    stem_sentence=[]
    for word in text.split(','):
        stem_sentence.append(stemmer.stem(word))
    stem_sentence= ', '.join(stem_sentence)
    return stem_sentence


def clean_text(df, col='keyphrase'):

    df_copy = df.copy()

    for row in range(len(df_copy)):
        name_change = team_name_change(df_copy[col][row])
        no_stopwords = remove_stopwords(name_change)
        tokenize_list = word_tokenize(no_stopwords, language='dutch')
        tokenize_list = [x for x in tokenize_list if x != ',']
        df_copy.at[row, col] = ', '.join(list(set(tokenize_list)))
        stemmer_list= stemmer(df_copy[col][row])
        df_copy.at[row, col] = stemmer_list
    
    df_copy[col] = df_copy[col].str.replace('voka', ' ') \
        .str.replace('ov', '').str.replace('unknown', '').str.replace(r'\b\w{1,3}\b', '', regex=True).str.replace(r'\d+', '', regex=True) \
        .str.replace(r'(\s{2},\s{2}),*', '', regex=True).str.replace(' ', '').str.replace(r'^,+|,+$', '', regex=True) \
        .str.replace(r',,+', ',', regex=True)

    return df_copy


## Clean new campaign data (new data which is uploaded by the user)


def titelChange(data):
    for col in data.columns:
        if col.startswith('crm_') or col.startswith('CDI_'):
            data.columns = data.columns.str.replace('crm_', '')
            data.columns = data.columns.str.replace('CDI_', '')


def create_column_names(dataframe, pk='Campagne_Campagne'):
    columns = dataframe.columns
    columns = [col + '_id' if col == pk else col for col in columns]
    columns = [re.sub(r'\W+', '', col) for col in columns]
    columns = [col.lower() for col in columns]
    dict_columns = dict(zip(dataframe.columns, columns))
    return dict_columns


def basic_clean(df):
    data = df.copy()
    data.drop_duplicates(inplace=True)
    numeric = data.select_dtypes(include='number').columns
    non_numeric = data.select_dtypes(exclude='number').columns
    data[numeric] = data[numeric].fillna(-1)
    data[non_numeric] = data[non_numeric].fillna('unknown')
    return data


def clean_new_campaign_data(df):

    preclean_df = df.copy()

    titelChange(preclean_df)

    preclean_df.rename(columns=create_column_names(preclean_df), inplace=True)

    df_campagne = basic_clean(preclean_df)

    # campagne naam cleanen
    df_campagne['campagne_naam'] = df_campagne['campagne_naam'].str.replace('OV-', '').str.replace('ov-', '') \
                                                            .str.replace('-', ' ').str.replace(r'[^\w\s]', '', regex=True) \
                                                            .str.replace('  ', ' ').str.strip().str.lower().str.replace('  ', ' ')

    # Drop kolommen
    df_campagne.drop(['campagne_einddatum', 'campagne_startdatum', 'campagne_campagne_nr', 
                  'campagne_naam_in_email', 'campagne_reden_van_status', 'campagne_status',
                  'campagne_url_voka_be'
                  ], axis=1, inplace=True)

    # Create keyphrase column
    cols_for_key = ['campagne_naam', 'campagne_type_campagne', 'campagne_soort_campagne']

    for col in cols_for_key:
        df_campagne[col] = df_campagne[col].astype(str).str.split().str.join(', ')

    df_campagne['keyphrase'] = df_campagne[cols_for_key].apply(lambda x: ', '.join(x), axis=1)

    # keyphrases cleanen
    df_campagne['keyphrase'] = df_campagne['keyphrase'].str.replace(', ,', ',').str.replace(r'(\s{2},\s{2}),*+', '') \
        .str.replace('  ', ' ').str.replace(r'[^\w\s]', '', regex=True).str.replace('  ', ' ').str.strip().str.lower()
    
    final_df = clean_text(df_campagne, 'keyphrase') 

    return final_df


# get the data from the database


def get_acc(conn):
    acc_cols = ['accountID', 'plaats', 'subregio', 'ondernemingstype', 'ondernemingsaard', 'activiteitNaam']
    # account conditie
    acc_condition = "accountStatus = 1 AND provincie = 'Oost-Vlaanderen'"
    # create query
    acc_query = create_query('DimAccount', acc_cols, acc_condition)
    # read sql
    df_account = pd.read_sql(acc_query, conn)

    df_account['plaats'] = df_account['plaats'].str.replace(r'\([a-z.-]+\)', '', regex=True).str.replace('  ', ' ')
    df_account['plaats'] = df_account['plaats'] + ' ' + df_account['subregio']

    # account ondernemingstype samenvoegen
    df_account['onderneming'] = df_account['ondernemingstype'] + ' ' \
                                + df_account['ondernemingsaard'] + ' ' \
                                + df_account['activiteitNaam']

    df_account['onderneming'] = df_account['onderneming'].str.replace('unknown', '').str.replace(', , ', '') \
                                                                .str.strip().str.lower() \
                                                                .str.replace(r',$|^,', '', regex=True) \
                                                                .str.replace('&', '').str.replace('-', '')                                                      
    # gebruikte kolommen droppen
    df_account.drop(columns=['ondernemingstype', 
                'ondernemingsaard', 'activiteitNaam', 'subregio'], inplace=True)
    
    return df_account


def get_contact(conn):
    contact_cols = ['contactID', 'accountID', 'functietitel', 
    'persoon_mail_thema_duurzaamheid', 'persoon_mail_thema_financieel_fiscaal', 'persoon_mail_thema_innovatie',
    'persoon_mail_thema_internationaal_ondernemen', 'persoon_mail_thema_mobiliteit', 'persoon_mail_thema_omgeving',
    'persoon_mail_thema_sales_marketing_communicatie', 'persoon_mail_thema_strategie_en_algemeen_management',
    'persoon_mail_thema_talent', 'persoon_mail_thema_welzijn', 'persoon_mail_type_bevraging', 'persoon_mail_type_communities_en_projecten',
    'persoon_mail_type_netwerkevenementen', 'persoon_mail_type_nieuwsbrieven', 'persoon_mail_type_opleidingen',
    'persoon_mail_type_persberichten_belangrijke_meldingen', 'persoon_marketingcommunicatie',]

    contact_condition = "contactStatus = 'Actief'"
    contact_query = create_query('DimContact', contact_cols, contact_condition)
    df_contact = pd.read_sql(contact_query, conn)

    df_contact['functietitel'] = df_contact['functietitel'].str.lower()
    df_contact['persoon_marketingcommunicatie'] = df_contact['persoon_marketingcommunicatie'].fillna('-1')
    df_contact['persoon_marketingcommunicatie'] = df_contact['persoon_marketingcommunicatie'] \
                                                                .str.replace('Strikt', '0').str.replace('Flexibel', '1') \
                                                                .str.replace('Uitgeschreven', '-1').str.replace('unknown', '-1').astype(int)
    
    return df_contact


def get_acc_cont(conn):
    df_contact = get_contact(conn)
    df_account = get_acc(conn)

    df_acc_cont = pd.merge(df_contact, df_account, on='accountID', how='inner')
    df_acc_cont.drop_duplicates(inplace=True)
    return df_acc_cont


def get_afspraak_contact(conn):
    afspraak_cols = ['subthema', 'onderwerp', 'keyphrases', 'contactID']

    afspraak_condition = "contactID is not null"
    afspraak_query = create_query('DimAfspraak', afspraak_cols, afspraak_condition)
    df_afspraak = pd.read_sql(afspraak_query, conn)

    df_afspraak['thema'] = df_afspraak['subthema'].str.replace('\(', '', regex=True)

    df_afspraak['thema'] = df_afspraak['thema'].str.replace('\)', '', regex=True).str.lower() \
            .str.replace(r'[^\w\s]', '', regex=True).str.replace('  ', ' ').str.strip()

    df_afspraak['onderwerp'] = df_afspraak['onderwerp'].str.lower().astype(str).str.replace('ov-', '') \
            .str.replace('ov -', '').str.replace('ov ', '').str.replace('-', ' ') \
            .str.replace(r'[^\w\s]', '', regex=True).str.replace('  ', ' ').str.strip()

    df_afspraak['keyphrases'] = df_afspraak['keyphrases'].str.lower().str.replace(r'[^\w\s]', '', regex=True) \
                                                                                .str.replace('  ', ' ').str.strip()

    df_afspraak.drop(['subthema'], axis=1, inplace=True)
    df_afspraak.drop_duplicates(inplace=True)

    return df_afspraak


def get_afspraak_account(conn):
    
    afspraak_cols1 = ['subthema', 'onderwerp', 'keyphrases', 'accountID']

    afspraak_condition1 = "accountID is not null"
    afspraak_query1 = create_query('DimAfspraak', afspraak_cols1, afspraak_condition1)
    df_afspraak1 = pd.read_sql(afspraak_query1, conn)

    df_afspraak1['thema'] = df_afspraak1['subthema'].str.replace('\(', '', regex=True)

    df_afspraak1['thema'] = df_afspraak1['thema'].str.replace('\)', '', regex=True).str.lower() \
            .str.replace(r'[^\w\s]', '', regex=True).str.replace('  ', ' ').str.strip()

    df_afspraak1['onderwerp'] = df_afspraak1['onderwerp'].str.lower().astype(str).str.replace('ov-', '') \
            .str.replace('ov -', '').str.replace('ov ', '').str.replace('-', ' ') \
            .str.replace(r'[^\w\s]', '', regex=True).str.replace('  ', ' ').str.strip()

    df_afspraak1['keyphrases'] = df_afspraak1['keyphrases'].str.lower().str.replace(r'[^\w\s]', '', regex=True) \
                                                                                .str.replace('  ', ' ').str.strip()

    df_afspraak1.drop(['subthema'], axis=1, inplace=True)
    df_afspraak1.drop_duplicates(inplace=True)

    return df_afspraak1


def get_acc_cont_afs(conn):
    df_acc_cont = get_acc_cont(conn)
    df_afspraak = get_afspraak_contact(conn)
    df_afspraak1 = get_afspraak_account(conn)

    df_acc_cont_afs = df_acc_cont.merge(df_afspraak, on=['contactID'], how='left')
    df_acc_cont_afs = df_acc_cont_afs.merge(df_afspraak1, on=['accountID'], how='left')

    df_acc_cont_afs['onderwerp_x'] = df_acc_cont_afs['onderwerp_x'].fillna('')
    df_acc_cont_afs['onderwerp_y'] = df_acc_cont_afs['onderwerp_y'].fillna('')
    df_acc_cont_afs['keyphrases_x'] = df_acc_cont_afs['keyphrases_x'].fillna('')
    df_acc_cont_afs['keyphrases_y'] = df_acc_cont_afs['keyphrases_y'].fillna('')
    df_acc_cont_afs['thema_x'] = df_acc_cont_afs['thema_x'].fillna('')
    df_acc_cont_afs['thema_y'] = df_acc_cont_afs['thema_y'].fillna('')

    df_acc_cont_afs['onderwerp'] = df_acc_cont_afs['onderwerp_x'] + ' ' + df_acc_cont_afs['onderwerp_y']
    df_acc_cont_afs['keyphrases'] = df_acc_cont_afs['keyphrases_x'] + ' ' + df_acc_cont_afs['keyphrases_y']
    df_acc_cont_afs['thema'] = df_acc_cont_afs['thema_x'] + ' ' + df_acc_cont_afs['thema_y']

    df_acc_cont_afs['onderwerp'] = df_acc_cont_afs['onderwerp'].str.strip().apply(lambda x: ' '.join(list(set(x.replace('  ', ' ').split(' ')))))
    df_acc_cont_afs['keyphrases'] = df_acc_cont_afs['keyphrases'].str.strip().apply(lambda x: ' '.join(list(set(x.replace('  ', ' ').split(' ')))))
    df_acc_cont_afs['thema'] = df_acc_cont_afs['thema'].str.strip().apply(lambda x: ' '.join(list(set(x.replace('  ', ' ').split(' ')))))

    df_acc_cont_afs.drop(['onderwerp_x', 'onderwerp_y', 'keyphrases_x', 'keyphrases_y', 'thema_x', 'thema_y'], axis=1, inplace=True)
    df_acc_cont_afs.drop_duplicates(inplace=True)

    return df_acc_cont_afs


def get_campagne(conn):
    campagne_cols = ['campagneID', 'campagneNaam', 'campagneType', 'campagneSoort']

    campagne_query = create_query('DimCampagne', campagne_cols)
    df_campagne = pd.read_sql(campagne_query, conn)

    df_campagne['campagneNaam'] = df_campagne['campagneNaam'].str.replace('OV-', '').str.replace('ov-', '') \
                                        .str.replace('-', ' ').str.replace(r'[^\w\s]', '', regex=True) \
                                        .str.replace('  ', ' ').str.strip().str.lower().str.replace('  ', ' ')

    return df_campagne
    

def get_inschrijving(conn):

    inschrijving_cols = ['campagneID', 'contactID', 'bron', 'inschrijvingsDatumID']

    inschrijving_query = create_query('FactInschrijving', inschrijving_cols)
    df_inschrijving = pd.read_sql(inschrijving_query, conn)

    df_inschrijving['bron'] = df_inschrijving['bron'].astype(str).str.replace('unknown', '-1') \
                                .str.replace('Website', '0').str.replace('Email', '1').astype(int)

    return df_inschrijving


def get_date(conn):
    date_cols = ['dateID', 'fullDate']
    date_query = create_query('DimDate', date_cols)
    df_date = pd.read_sql(date_query, conn)
    return df_date


def get_campagne_inschrijving(conn):
    df_campagne = get_campagne(conn)
    df_inschrijving = get_inschrijving(conn)

    df_campagne_inschrijving = pd.merge(df_campagne, df_inschrijving, on='campagneID', how='inner')
    df_campagne_inschrijving.drop_duplicates(inplace=True)

    df_date = get_date(conn)
    df_campagne_inschrijving = pd.merge(df_campagne_inschrijving, df_date, left_on='inschrijvingsDatumID', right_on='dateID', how='inner')
    df_campagne_inschrijving.drop(['dateID', 'inschrijvingsDatumID'], axis=1, inplace=True)
    df_campagne_inschrijving.drop_duplicates(inplace=True)

    return df_campagne_inschrijving


def get_sessie(conn):

    sessie_cols = ['campaignID', 'themaNaam']

    sessie_query = create_query('DimSessie', sessie_cols)
    df_sessie = pd.read_sql(sessie_query, conn)

    df_sessie = df_sessie.groupby('campaignID')['themaNaam'].apply(list).reset_index()
    df_sessie['themaNaam'] = df_sessie['themaNaam'].apply(lambda x: ', '.join(list(set(x))))
    df_sessie['themaNaam'] = df_sessie['themaNaam'].str.replace('OV-', '').str.replace('ov-', '') \
                                                                .str.replace('-', ' ').str.replace(r'[^\w\s]', '', regex=True) \
                                                                .str.replace('  ', ' ').str.strip().str.lower().str.replace('  ', ' ')
    
    return df_sessie


def get_campagne_inschrijving_sessie(conn):
    df_campagne_inschrijving = get_campagne_inschrijving(conn)
    df_sessie = get_sessie(conn)

    df_campagne_inschrijving_sessie = pd.merge(df_campagne_inschrijving, df_sessie, left_on='campagneID', right_on='campaignID', how='inner')
    df_campagne_inschrijving_sessie.drop(['campaignID', 'campagneID'], axis=1, inplace=True)
    df_campagne_inschrijving_sessie.drop_duplicates(inplace=True)

    return df_campagne_inschrijving_sessie


def get_acc_cont_afs_camp_insch_sessie(conn):
    df_acc_cont_afs = get_acc_cont_afs(conn)
    df_campagne_inschrijving_sessie = get_campagne_inschrijving_sessie(conn)

    df_merge = pd.merge(df_acc_cont_afs, df_campagne_inschrijving_sessie, on='contactID', how='left')
    df_merge['bron'].fillna(-1, inplace=True)
    df_merge.fillna('unknown', inplace=True)

    return df_merge


def get_visit(conn):
    visit_cols = ['contactID', 'visit_first_visit', 'visit_total_pages', 'mailing_onderwerp', 'mailing_name', 'mailSent_clicks', 'mailSent']

    visit_query = create_query('DimVisit', visit_cols)
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

    df_visit['mailing_name'] = df_visit['mailing_name'].str.replace('OV-', '') \
                                                .str.replace('OV ', '').str.replace('OV -', '') \
                                                .str.replace('-', ' ').str.replace(r'[^\w\s]', ' ', regex=True) \
                                                .str.replace('  ', ' ').str.strip().str.lower().str.replace('  ', ' ')

    df_visit['mailing_onderwerp'] = df_visit['mailing_onderwerp'] \
                                                .str.replace('-', ' ').str.replace(r'[^\w\s]', ' ', regex=True) \
                                                .str.replace('  ', ' ').str.strip().str.lower().str.replace('  ', ' ')

    df_visit['mail_click_freq'] = np.round(df_visit['clicks_total'] / df_visit['aantal_mails'], 0)
    df_visit['mail_click_freq'] = df_visit['mail_click_freq'].fillna(-1).astype(int)

    df_visit.drop(['mailSent', 'mailSent_clicks', 'clicks_total', 'aantal_mails'], axis=1, inplace=True)
    df_visit.drop_duplicates(inplace=True)

    return df_visit


def calc_marketing_pressure_normal(df):
    marketing_pressure_cols = [col for col in df.columns if col.__contains__('persoon_mail_type') 
                           or col.__contains__('persoon_mail_thema') or col.__contains__('persoon_marketingcommunicatie')]

    marketing_pressure_cols.append('bron')
    marketing_pressure_cols.append('visit_first_visit')
    marketing_pressure_cols.append('visit_total_pages')
    marketing_pressure_cols.append('mail_click_freq')

    df['marketing_pressure'] = df[marketing_pressure_cols].sum(axis=1)
    df['marketing_pressure'] = df['marketing_pressure'].astype(int)
    df.drop(marketing_pressure_cols, axis=1, inplace=True)

    return df


def get_final_no_mp(conn):
    df_merge = get_acc_cont_afs_camp_insch_sessie(conn)
    df_visit = get_visit(conn)

    df = pd.merge(df_merge, df_visit, on='contactID', how='left')

    df = df[df['fullDate'] != 'unknown']
    df['fullDate'] = pd.to_datetime(df['fullDate'])

    df['visit_first_visit'] = df['visit_first_visit'].fillna(-1).astype(int)
    df['visit_total_pages'] = df['visit_total_pages'].fillna(-1).astype(int)
    df['mail_click_freq'] = df['mail_click_freq'].fillna(-1).astype(int)
    df['mailing_onderwerp'] = df['mailing_onderwerp'].fillna('unknown')
    df['mailing_name'] = df['mailing_name'].fillna('unknown')

    int_cols = df.select_dtypes(include=['int64', 'int32']).columns
    df[int_cols] = df[int_cols].astype('int8')

    df['keyphrases'] += ' ' + df['plaats'] + ' ' + df['onderneming'] + ' ' + df['functietitel'] \
                    + ' ' + df['onderwerp'] + ' ' + df['thema'] + ' ' + df['campagneNaam'] \
                    + ' ' + df['campagneType'] + ' ' + df['campagneSoort'] + ' ' + df['themaNaam'] \
                    + ' ' + df['mailing_onderwerp'] + ' ' + df['mailing_name']

    df.drop(['plaats', 'onderneming', 'functietitel', 'onderwerp', 'thema', 'campagneNaam', 'campagneType', 'campagneSoort', 
            'themaNaam', 'mailing_onderwerp', 'mailing_name'], axis=1, inplace=True)

    df['keyphrases'] = df['keyphrases'].str.replace(', ,', ',').str.replace(r'(\s{2},\s{2}),*+', '').str.replace('unknown', ' ') \
        .str.replace('  ', ' ').str.replace(r'[^\w\s]', '', regex=True).str.replace(r'\d+', '', regex=True) \
        .str.replace('ov', '').str.replace('  ', ' ').str.strip().str.lower() \

    df.drop_duplicates(inplace=True)

    return df


def preproces_df(df):
    df = df.groupby('contactID').agg(list)
    df['marketing_pressure'] = df['marketing_pressure'].apply(lambda x: np.mean(x).round(0).astype(int))
    df['accountID'] = df['accountID'].apply(lambda x: list(set(x)))
    df['accountID'] = df['accountID'].apply(lambda x: x[0])
    df['keyphrases'] = df['keyphrases'].apply(lambda x: ', '.join(list(set(x))))
    df['keyphrases'] = df['keyphrases'].apply(lambda x: remove_stopwords(x))
    df['keyphrases'] = df['keyphrases'].apply(lambda x: team_name_change(x))
    df['keyphrases'] = df['keyphrases'].apply(lambda x: ', '.join(sorted(x.split(', '))))

    df.reset_index(inplace=True)
    df.drop_duplicates(inplace=True)

    return df


def get_final_df(conn):
    df_merge = get_acc_cont_afs_camp_insch_sessie(conn)
    df_visit = get_visit(conn)

    df = pd.merge(df_merge, df_visit, on='contactID', how='left')

    df['visit_first_visit'] = df['visit_first_visit'].fillna(-1).astype(int)
    df['visit_total_pages'] = df['visit_total_pages'].fillna(-1).astype(int)
    df['mail_click_freq'] = df['mail_click_freq'].fillna(-1).astype(int)
    df['mailing_onderwerp'] = df['mailing_onderwerp'].fillna('unknown')
    df['mailing_name'] = df['mailing_name'].fillna('unknown')

    int_cols = df.select_dtypes(include=['int64', 'int32']).columns
    df[int_cols] = df[int_cols].astype('int8')

    df = calc_marketing_pressure_normal(df)

    df['keyphrases'] += ' ' + df['plaats'] + ' ' + df['onderneming'] + ' ' + df['functietitel'] \
                    + ' ' + df['onderwerp'] + ' ' + df['thema'] + ' ' + df['campagneNaam'] \
                    + ' ' + df['campagneType'] + ' ' + df['campagneSoort'] + ' ' + df['themaNaam'] \
                    + ' ' + df['mailing_onderwerp'] + ' ' + df['mailing_name']

    df.drop(['plaats', 'onderneming', 'functietitel', 'onderwerp', 'thema', 'campagneNaam', 'campagneType', 'campagneSoort', 
            'themaNaam', 'mailing_onderwerp', 'mailing_name'], axis=1, inplace=True)

    df['keyphrases'] = df['keyphrases'].str.replace(', ,', ',').str.replace(r'(\s{2},\s{2}),*+', '').str.replace('unknown', ' ') \
        .str.replace('  ', ' ').str.replace(r'[^\w\s]', '', regex=True).str.replace(r'\d+', '', regex=True) \
        .str.replace('ov', '').str.replace('  ', ' ').str.strip().str.lower() \

    df = df.groupby('contactID').agg(list)

    df['marketing_pressure'] = df['marketing_pressure'].apply(lambda x: np.mean(x).round(0).astype(int))
    df['accountID'] = df['accountID'].apply(lambda x: list(set(x)))
    df['accountID'] = df['accountID'].apply(lambda x: x[0])
    df['keyphrases'] = df['keyphrases'].apply(lambda x: ', '.join(list(set(x))))
    df['keyphrases'] = df['keyphrases'].apply(lambda x: remove_stopwords(x))
    df['keyphrases'] = df['keyphrases'].apply(lambda x: team_name_change(x))
    df['keyphrases'] = df['keyphrases'].apply(lambda x: ', '.join(sorted(x.split(', '))))

    df.reset_index(inplace=True)
    df.drop_duplicates(inplace=True)

    return df


def get_results_df(conn):
    df_merge = get_acc_cont_afs_camp_insch_sessie(conn)
    df_visit = get_visit(conn)

    df = pd.merge(df_merge, df_visit, on='contactID', how='left')
    df.drop(['fullDate'], axis=1, inplace=True)

    df['visit_first_visit'] = df['visit_first_visit'].fillna(-1).astype(int)
    df['visit_total_pages'] = df['visit_total_pages'].fillna(-1).astype(int)
    df['mail_click_freq'] = df['mail_click_freq'].fillna(-1).astype(int)
    df['mailing_onderwerp'] = df['mailing_onderwerp'].fillna('unknown')
    df['mailing_name'] = df['mailing_name'].fillna('unknown')

    int_cols = df.select_dtypes(include=['int64', 'int32']).columns
    df[int_cols] = df[int_cols].astype('int8')

    df = calc_marketing_pressure_normal(df)

    df = df.groupby('contactID').agg(list)

    df['marketing_pressure'] = df['marketing_pressure'].apply(lambda x: np.mean(x).round(0).astype(int))
    df['accountID'] = df['accountID'].apply(lambda x: list(set(x)))
    df['accountID'] = df['accountID'].apply(lambda x: x[0])
    df['keyphrases'] = df['keyphrases'].apply(lambda x: ', '.join(list(set(x))))
    df['functietitel'] = df['functietitel'].apply(lambda x: ', '.join(list(set(x))))
    df['plaats'] = df['plaats'].apply(lambda x: ', '.join(list(set(x)))).str.lower().apply(lambda x: ', '.join(list(set(x.split(' ')))))
    df['onderneming'] = df['onderneming'].apply(lambda x: ', '.join(list(set(x))))
    df['onderwerp'] = df['onderwerp'].apply(lambda x: ', '.join(list(set(x))))
    df['thema'] = df['thema'].apply(lambda x: ', '.join(list(set(x))))
    df['campagneNaam'] = df['campagneNaam'].apply(lambda x: ', '.join(list(set(x))))
    df['campagneType'] = df['campagneType'].apply(lambda x: ', '.join(list(set(x))))
    df['campagneSoort'] = df['campagneSoort'].apply(lambda x: ', '.join(list(set(x))))
    df['themaNaam'] = df['themaNaam'].apply(lambda x: ', '.join(list(set(x))))
    df['mailing_onderwerp'] = df['mailing_onderwerp'].apply(lambda x: ', '.join(list(set(x))))
    df['mailing_name'] = df['mailing_name'].apply(lambda x: ', '.join(list(set(x))))

    df.reset_index(inplace=True)
    df.drop_duplicates(inplace=True)    

    return df


def recommend(df, new_keyphrase: str, top_n=10):
    # preprocessing
    scaler = MinMaxScaler()
    df['marketing_pressure'] = scaler.fit_transform(df[['marketing_pressure']])

    # vectorization
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(df['keyphrases'])

    # vectorize the new keyphrase and calculate similarity
    new_keyphrase_tfidf = tfidf.transform([new_keyphrase])
    sim_score_new = cosine_similarity(new_keyphrase_tfidf, tfidf_matrix)

    # Create a new column for similarity scores in the DataFrame
    df['similarity_score'] = sim_score_new[0]

    # sort the similarity scores
    contact_person_similarity = list(enumerate(sim_score_new[0]))
    sorted_contact_persons = sorted(contact_person_similarity, key=lambda x: x[1], reverse=True)

    # get the top n similar contact persons
    top_contact_persons = sorted_contact_persons[:top_n]

    # Create a set to keep track of recommended contact IDs
    recommended_contact_ids = set()

    # Iterate through the sorted contact persons and add unique contact IDs to the set
    for index, _ in top_contact_persons:
        contact_id = df['contactID'][index]
        recommended_contact_ids.add(contact_id)

    # Convert the set back to a list
    recommended_contact_ids = list(recommended_contact_ids)

    # sort the contact ids by marketing pressure
    recommended_contact_ids = sorted(recommended_contact_ids, key=lambda x: df[df['contactID'] == x]['marketing_pressure'].values[0], reverse=False)

    # result
    results_list = []
    for contact_id in recommended_contact_ids:
        marketing_pressure = df[df['contactID'] == contact_id]['marketing_pressure'].values[0]
        similarity_score = df[df['contactID'] == contact_id]['similarity_score'].values[0]
        results_list.append((contact_id, marketing_pressure, similarity_score))
    return results_list
