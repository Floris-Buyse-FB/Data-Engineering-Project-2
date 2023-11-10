import argparse
import datetime
from json import load
import re
import pandas as pd
import os
import time
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import nltk
# disable dtype warning
pd.options.mode.chained_assignment = None  # default='warn'
# other warnings
import warnings
warnings.filterwarnings("ignore")
DATA_FOLDER = '../data'
CLEAN_DATA_FOLDER = '../data_clean'


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
    nltk.download('stopwords')
    nltk.download('punkt')
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

def remove_duplicate_pk_single(file, col_pk):
    url = os.path.join(CLEAN_DATA_FOLDER, file)
    data = pd.read_csv(url)
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
    if os.path.exists(url):
        os.replace(url, url)
    data.to_csv(url, index=False)


def remove_duplicate_pk_all():
    pk_dict = {
    'Account_activiteitscode_fixed.csv': '',
    'Account_financiële_data_fixed.csv': '',
    'Account_fixed.csv': 'Account_Account',
    'Activiteitscode_fixed.csv': 'ActiviteitsCode_Activiteitscode',
    'Activiteit_vereist_contact_fixed.csv': 'ActiviteitVereistContact_ActivityId',
    'Afspraak_account_gelinkt_cleaned_fixed.csv': 'Afspraak_ACCOUNT_GELINKT_Afspraak',
    'Afspraak_alle_fixed.csv': 'Afspraak_ALLE_Afspraak',
    'Afspraak_betreft_account_cleaned_fixed.csv': 'Afspraak_BETREFT_ACCOUNT_Afspraak',
    'Afspraak_betreft_contact_cleaned_fixed.csv': 'Afspraak_BETREFT_CONTACTFICHE_Afspraak',
    'Campagne_fixed.csv': 'Campagne_Campagne',
    'CDI_mailing_fixed.csv': 'Mailing_Mailing',
    'CDI_pageviews_fixed.csv': 'Page_View',
    'CDI_sent_email_clicks_fixed.csv': 'SentEmail_kliks_Sent_Email',
    'CDI_visits_fixed.csv': 'Visit_Visit',
    'Contact_fixed.csv': 'Contact_Contactpersoon',
    'Contact_functie_fixed.csv': '',
    'Functie_fixed.csv': 'Functie_Functie',
    'Gebruikers_fixed.csv': 'Gebruikers_CRM_User_ID',
    'Info_en_klachten_fixed.csv': 'Info_en_Klachten_Aanvraag',
    'Inschrijving_fixed.csv': 'Inschrijving_Inschrijving',
    'Lidmaatschap_fixed.csv': 'Lidmaatschap_Lidmaatschap',
    'Persoon_fixed.csv': 'Persoon_persoon',
    'Sessie_fixed.csv': 'Sessie_Sessie',
    'Sessie_inschrijving_fixed.csv': 'SessieInschrijving_SessieInschrijving',
    'Teams_fixed.csv': '',
    }

    for file_name, pk in pk_dict.items():
        if pk != '':
            try:
                print(f'currently removing pk duplicates for {file_name}')
                new_pk = pk.lower() + '_id'
                remove_duplicate_pk_single(file_name, new_pk)
            except:
                pass


def fill_na():
    for file in os.listdir(CLEAN_DATA_FOLDER):
        dataframe = pd.read_csv(os.path.join(CLEAN_DATA_FOLDER, file))
        numeric = dataframe.select_dtypes(include='number').columns
        non_numeric = dataframe.select_dtypes(exclude=['number']).columns
        dataframe[numeric] = dataframe[numeric].fillna(-1)
        dataframe[non_numeric] = dataframe[non_numeric].fillna('unknown')
        dataframe.to_csv(os.path.join(CLEAN_DATA_FOLDER, file), index=False)


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


def column_name_change_V2():
    pk_dict = {
    'Account_activiteitscode_fixed.csv': '',
    'Account_financiële_data_fixed.csv': '',
    'Account_fixed.csv': 'Account_Account',
    'Activiteitscode_fixed.csv': 'ActiviteitsCode_Activiteitscode',
    'Activiteit_vereist_contact_fixed.csv': 'ActiviteitVereistContact_ActivityId',
    'Afspraak_account_gelinkt_cleaned_fixed.csv': 'Afspraak_ACCOUNT_GELINKT_Afspraak',
    'Afspraak_alle_fixed.csv': 'Afspraak_ALLE_Afspraak',
    'Afspraak_betreft_account_cleaned_fixed.csv': 'Afspraak_BETREFT_ACCOUNT_Afspraak',
    'Afspraak_betreft_contact_cleaned_fixed.csv': 'Afspraak_BETREFT_CONTACTFICHE_Afspraak',
    'Campagne_fixed.csv': 'Campagne_Campagne',
    'CDI_mailing_fixed.csv': 'Mailing_Mailing',
    'cdi_pageviews_fixed.csv': 'Page_View',
    'CDI_sent_email_clicks_fixed.csv': 'SentEmail_kliks_Sent_Email',
    'CDI_visits_fixed.csv': 'Visit_Visit',
    'Contact_fixed.csv': 'Contact_Contactpersoon',
    'Contact_functie_fixed.csv': '',
    'Functie_fixed.csv': 'Functie_Functie',
    'Gebruikers_fixed.csv': 'Gebruikers_CRM_User_ID',
    'Info_en_klachten_fixed.csv': 'Info_en_Klachten_Aanvraag',
    'Inschrijving_fixed.csv': 'Inschrijving_Inschrijving',
    'Lidmaatschap_fixed.csv': 'Lidmaatschap_Lidmaatschap',
    'Persoon_fixed.csv': 'Persoon_persoon',
    'Sessie_fixed.csv': 'Sessie_Sessie',
    'Sessie_inschrijving_fixed.csv': 'SessieInschrijving_SessieInschrijving',
    'Teams_fixed.csv': '',
    }
    
    for file_name, pk in pk_dict.items():
        try:
            URL = os.path.join(CLEAN_DATA_FOLDER, file_name)
            data = pd.read_csv(URL)
            cols = create_column_names(data, pk)
            data.rename(columns=cols, inplace=True)
            data.to_csv(URL, index=False)
        except:
            pass


def load_unique_values(file_name, column_name):
    df = pd.read_csv(os.path.join(CLEAN_DATA_FOLDER, file_name), sep=",")
    unique_values = df[column_name].unique()
    del df  # Release DataFrame from memory
    return unique_values


def remove_non_existing_pk(file, fk_arr, col_name_arr):

    df = pd.read_csv(os.path.join(CLEAN_DATA_FOLDER, file), sep=",")

    for fk, col_name in zip(fk_arr, col_name_arr):
        if fk == 'account':
            acc_unique = load_unique_values('Account_fixed.csv', 'account_account_id')
            fk_arr_index = fk_arr.index('account')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(acc_unique)]
            print(f'FK for {fk}: {len(df)} rows left')

        elif fk == 'contact':
            contact_unique = load_unique_values('Contact_fixed.csv', 'contact_contactpersoon_id')
            fk_arr_index = fk_arr.index('contact')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(contact_unique)]
            print(f'FK for {fk}: {len(df)} rows left')

        elif fk == 'persoon':
            persoon_unique = load_unique_values('Persoon_fixed.csv', 'persoon_persoon_id')
            fk_arr_index = fk_arr.index('persoon')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(persoon_unique)]
            print(f'FK for {fk}: {len(df)} rows left')

        elif fk == 'afspraak':
            afspraak_alle_unique = load_unique_values('Afspraak_alle_fixed.csv', 'afspraak_alle_afspraak_id')
            fk_arr_index = fk_arr.index('afspraak')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(afspraak_alle_unique)]
            print(f'FK for {fk}: {len(df)} rows left')

        elif fk == 'campagne':
            campagne_unique = load_unique_values('Campagne_fixed.csv', 'campagne_campagne_id')
            fk_arr_index = fk_arr.index('campagne')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(campagne_unique)]
            print(f'FK for {fk}: {len(df)} rows left')

        elif fk == 'mailing':
            mailing_unique = load_unique_values('CDI_mailing_fixed.csv', 'mailing_mailing_id')
            fk_arr_index = fk_arr.index('mailing')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(mailing_unique)]
            print(f'FK for {fk}: {len(df)} rows left')

        elif fk == 'activiteitscode':
            activiteitscode_unique = load_unique_values('Activiteitscode_fixed.csv', 'activiteitscode_activiteitscode_id')
            fk_arr_index = fk_arr.index('activiteitscode')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(activiteitscode_unique)]
            print(f'FK for {fk}: {len(df)} rows left')

        elif fk == 'visit':
            visit_unique = load_unique_values('CDI_visits_fixed.csv', 'visit_visit_id')
            fk_arr_index = fk_arr.index('visit')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(visit_unique)]
            print(f'FK for {fk}: {len(df)} rows left')

        elif fk == 'functie':
            functie_unique = load_unique_values('Functie_fixed.csv', 'functie_functie_id')
            fk_arr_index = fk_arr.index('functie')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(functie_unique)]
            print(f'FK for {fk}: {len(df)} rows left')

        elif fk == 'gebruiker':
            gebruiker_unique = load_unique_values('Gebruikers_fixed.csv', 'gebruikers_crm_user_id_id')
            fk_arr_index = fk_arr.index('gebruiker')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(gebruiker_unique)]
            print(f'FK for {fk}: {len(df)} rows left')

        elif fk == 'sessie':
            sessie_unique = load_unique_values('Sessie_fixed.csv', 'sessie_sessie_id')
            fk_arr_index = fk_arr.index('sessie')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(sessie_unique)]
            print(f'FK for {fk}: {len(df)} rows left')

        elif fk == 'inschrijving':
            inschrijving_unique = load_unique_values('Inschrijving_fixed.csv', 'inschrijving_inschrijving_id')
            fk_arr_index = fk_arr.index('inschrijving')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(inschrijving_unique)]
            print(f'FK for {fk}: {len(df)} rows left')
            
        elif fk =='pageviews':
            pageviews_unique = load_unique_values('CDI_pageviews_fixed.csv', 'page_view_id')
            fk_arr_index = fk_arr.index('pageviews')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(pageviews_unique)]
            print(f'FK for {fk}: {len(df)} rows left')
    
    print(f'{file} has {len(df)} rows left, writing to csv\n=========================================\n')
    df.to_csv(os.path.join(CLEAN_DATA_FOLDER, file), index=False)
    return df  


def default_process(filename, datafolder=DATA_FOLDER, dropna=False):

    print(f'currently working on {filename}')

    data = pd.read_csv(os.path.join(datafolder, filename))
    
    column_name_change(data)

    if dropna:
        data.dropna(inplace=True)
        data.reset_index(inplace=True, drop=True)

    data.drop_duplicates(inplace=True)

    numeric = data.select_dtypes(include='number').columns
    non_numeric = data.select_dtypes(exclude='number').columns
    data[numeric] = data[numeric].fillna(-1)
    data[non_numeric] = data[non_numeric].fillna('unknown')

    return data


def create_new_file_name(filename):
    new_filename = filename[:-4]
    new_filename = new_filename.replace(' ', '_')
    new_filename = f'{new_filename}_fixed.csv'
    return new_filename


def new_to_csv(filename, data, cleandatafolder=CLEAN_DATA_FOLDER):
    new_filename = filename[:-4]
    new_filename = new_filename.replace(' ', '_')
    new_filename = f'{new_filename}_fixed.csv'

    path = os.path.join(cleandatafolder, new_filename)
    if os.path.exists(path):
        os.remove(path)
    data.to_csv(path, index=False)


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


def ChangeAllData():
    account()
    account_financiele_data()
    afspraak_alle()
    persoon()
    contact()
    activiteit_vereist_contact()
    activiteitscode()
    account_activiteitscode()    
    afspraak_betreft_account_cleaned()
    afspraak_betreft_contact_cleaned()
    afspraak_account_gelinkt_cleaned()
    campagne()
    mailings()
    sent_email_clicks()
    visits()
    pageviews()
    functie()
    contact_functie()
    gebruikers()
    info_en_klachten()
    inschrijving()
    Lidmaatschap()
    sessie()
    sessie_inschrijving()   
    teams()

    print('changing column names...')
    column_name_change_V2()

    print('removing non existing primary keys...')
    remove_non_existing_pk('Account_financiële_data_fixed.csv', ['account'], ['financieledata_ondernemingid'])
    remove_non_existing_pk('Contact_fixed.csv', ['account', 'persoon'], ['contact_account', 'contact_persoon_id'])
    remove_non_existing_pk('Activiteit_vereist_contact_fixed.csv', ['afspraak', 'contact'], ['activiteitvereistcontact_activityid_id', 'activiteitvereistcontact_reqattendee'])
    remove_non_existing_pk('Account_activiteitscode_fixed.csv', ['account', 'activiteitscode'], ['account_activiteitscode_account', 'account_activiteitscode_activiteitscode'])
    remove_non_existing_pk('Afspraak_betreft_account_cleaned_fixed.csv', ['account', 'afspraak'], ['afspraak_betreft_account_betreft_id', 'afspraak_betreft_account_afspraak_id'])
    remove_non_existing_pk('Afspraak_betreft_contact_cleaned_fixed.csv', ['contact', 'afspraak'], ['afspraak_betreft_contactfiche_betreft_id', 'afspraak_betreft_contactfiche_afspraak_id'])
    remove_non_existing_pk('Afspraak_account_gelinkt_cleaned_fixed.csv', ['account', 'afspraak'], ['afspraak_account_gelinkt_account', 'afspraak_account_gelinkt_afspraak_id'])
    remove_non_existing_pk('CDI_sent_email_clicks_fixed.csv', ['mailing', 'contact'], ['sentemail_kliks_e_mail_versturen', 'sentemail_kliks_contact'])
    remove_non_existing_pk('CDI_visits_fixed.csv', ['contact', 'mailing', 'campagne'], ['visit_contact', 'visit_email_send', 'visit_campaign'])
    remove_non_existing_pk('CDI_pageviews_fixed.csv', ['contact', 'campagne', 'visit'], ['contact', 'campaign', 'visit'])
    remove_non_existing_pk('Contact_functie_fixed.csv', ['contact', 'functie'], ['contactfunctie_contactpersoon', 'contactfunctie_functie']) 
    remove_non_existing_pk('Info_en_klachten_fixed.csv', ['account', 'gebruiker'], ['info_en_klachten_account', 'info_en_klachten_eigenaar'])
    remove_non_existing_pk('Inschrijving_fixed.csv', ['contact', 'campagne'], ['inschrijving_contactfiche', 'inschrijving_campagne']) 
    remove_non_existing_pk('Lidmaatschap_fixed.csv', ['account'], ['lidmaatschap_onderneming'])
    remove_non_existing_pk('Sessie_fixed.csv', ['campagne'], ['sessie_campagne'])
    remove_non_existing_pk('Sessie_inschrijving_fixed.csv', ['sessie', 'inschrijving'], ['sessieinschrijving_sessie', 'sessieinschrijving_inschrijving'])

    print('removing duplicate primary keys, this might take a while...')
    remove_duplicate_pk_all()

    print('filling na values...')
    fill_na()

def account():
    FILENAME = 'Account.csv'
    data = default_process(FILENAME)
    print(data.shape)
    data = data[data['Account_Adres_Provincie'] == 'Oost-Vlaanderen']
    print(data.shape)
    data.replace({'Account_Status': {'Actief': 1, 'Inactief': 0}}, inplace=True)
    data.replace({'Account_Is_Voka_entiteit': {'Ja': 1, 'Nee': 0}}, inplace=True)
    
    if 'Account_Hoofd_NaCe_Code' in data.columns:
        data.drop('Account_Hoofd_NaCe_Code', axis=1, inplace=True)

    data['Account_Oprichtingsdatum'] = data['Account_Oprichtingsdatum'].apply(parse_date("1750-01-01"))
    new_to_csv(FILENAME, data)


def account_activiteitscode():
    FILENAME = 'Account activiteitscode.csv'
    data = default_process(FILENAME)
    new_to_csv(FILENAME, data)


def account_financiele_data():
    FILENAME = 'Account financiële data.csv'
    data = default_process(FILENAME)

    excluded_ids = [
    "02E2C17D-A213-E211-9DAA-005056B06EB4",
    "5C161136-A768-E111-B43A-00505680000A",
    "8AC9D862-9668-E111-B43A-00505680000A",
    "DFAAE601-1969-E111-B43A-00505680000A"
    ]
    data = data[~data['FinancieleData_OndernemingID'].isin(excluded_ids)]

    data['FinancieleData_Gewijzigd_op'] = data['FinancieleData_Gewijzigd_op'].apply(parse_datetime("2020-01-01"))
    
    new_to_csv(FILENAME, data)

def activiteit_vereist_contact():
    FILENAME = 'Activiteit vereist contact.csv'
    data = default_process(FILENAME)
    new_to_csv(FILENAME, data)


def activiteitscode():
    FILENAME = 'Activiteitscode.csv'
    data = default_process(FILENAME)
    new_to_csv(FILENAME, data)


def afspraak_alle():
    FILENAME = 'Afspraak alle.csv'
    data = default_process(FILENAME)
    new_to_csv(FILENAME, data)
    

def afspraak_betreft_account_cleaned():
    FILENAME = 'Afspraak betreft account_cleaned.csv'
    data = default_process(FILENAME)
    
    data['Afspraak_BETREFT_ACCOUNT_KeyPhrases'] = data['Afspraak_BETREFT_ACCOUNT_KeyPhrases'].replace('\[NAME\] ,*', '', regex=True)
    data['Afspraak_BETREFT_ACCOUNT_Eindtijd'] = data['Afspraak_BETREFT_ACCOUNT_Eindtijd'].apply(parse_date("2020-01-01"))

    cols_to_clean = ["Afspraak_BETREFT_ACCOUNT_KeyPhrases"]
    cols_to_clean = clean_text(data,cols_to_clean)
    data[cols_to_clean.columns] = cols_to_clean

    new_to_csv(FILENAME, data)


def afspraak_betreft_contact_cleaned():
    FILENAME = 'Afspraak betreft contact_cleaned.csv'
    data = default_process(FILENAME)

    data['Afspraak_BETREFT_CONTACTFICHE_KeyPhrases'] = data['Afspraak_BETREFT_CONTACTFICHE_KeyPhrases'].replace('\[NAME\] ,*', '', regex=True)
    data['Afspraak_BETREFT_CONTACTFICHE_Eindtijd'] = data['Afspraak_BETREFT_CONTACTFICHE_Eindtijd'].apply(parse_date("2020-01-01"))
    
    cols_to_clean = ["Afspraak_BETREFT_CONTACTFICHE_KeyPhrases"]
    cols_to_clean = clean_text(data,cols_to_clean)
    data[cols_to_clean.columns] = cols_to_clean 

    new_to_csv(FILENAME, data)


def afspraak_account_gelinkt_cleaned():
    FILENAME = 'Afspraak_account_gelinkt_cleaned.csv'
    data = default_process(FILENAME)

    data['Afspraak_ACCOUNT_GELINKT_KeyPhrases'] = data['Afspraak_ACCOUNT_GELINKT_KeyPhrases'].replace('\[NAME\] ,*', '', regex=True)
    data['Afspraak_ACCOUNT_GELINKT_Eindtijd'] = data['Afspraak_ACCOUNT_GELINKT_Eindtijd'].apply(parse_date("2020-01-01"))

    cols_to_clean = ["Afspraak_ACCOUNT_GELINKT_KeyPhrases"]
    cols_to_clean = clean_text(data,cols_to_clean)
    data[cols_to_clean.columns] = cols_to_clean 

    new_to_csv(FILENAME, data)


def campagne():
    FILENAME = 'Campagne.csv'
    data = default_process(FILENAME)
    data['Campagne_Einddatum'] = data['Campagne_Einddatum'].apply(parse_datetime("2026-01-01"))
    data['Campagne_Startdatum'] = data['Campagne_Startdatum'].apply(parse_datetime("1750-01-01"))
    new_to_csv(FILENAME, data)


def mailings():
    FILENAME = 'CDI mailing.csv'
    data = default_process(FILENAME)
    new_to_csv(FILENAME, data)


def sent_email_clicks():
    FILENAME = 'CDI sent email clicks.csv'
    data = default_process(FILENAME)
    new_to_csv(FILENAME, data)


def pageviews():
    print('currently working on Pageviews')

    FILENAME = 'CDI pageviews.csv'
    
    data = pd.read_csv('../data/cdi pageviews.csv', encoding="latin-1", sep=",")

    data.columns = data.columns.map(lambda x: re.sub(r'^crm CDI_PageView\[(.*)\]$', r'\1', x))
    data.columns = data.columns.map(lambda x: re.sub(r'^crm_CDI_PageView_(.*)$', r'\1', x))

    data['Time'] = data['Time'].apply(parse_datetime("1950-01-01"))
    data['Viewed_On'] = data['Viewed_On'].apply(parse_datetime("1950-01-01"))
    data['Aangemaakt_op'] = data['Aangemaakt_op'].apply(parse_datetime("1750-01-01"))
    data['Gewijzigd_op'] = data['Gewijzigd_op'].apply(parse_datetime("1750-01-01"))

    if 'Anonymous_Visitor' in data.columns:
        data.drop(['Anonymous_Visitor'], axis=1, inplace=True)
    if 'Visitor_Key' in data.columns:
        data.drop(['Visitor_Key'], axis=1, inplace=True)    
    if 'crm_CDI_PageView_Campagne_Code' in data.columns:
        data.drop('crm_CDI_PageView_Campagne_Code', axis=1, inplace=True)
    
    new_to_csv(FILENAME, data)


def visits():
    FILENAME = 'CDI visits.csv'
    data = default_process(FILENAME)

    if 'Visit_Campagne_Code' in data.columns:
        data.drop('Visit_Campagne_Code', axis=1, inplace=True)
    if 'Visit_Time' in data.columns:
        data.drop('Visit_Time', axis=1, inplace=True)

    data.replace({'Visit_Adobe_Reader': {'Ja': 1, 'Nee': 0}}, inplace=True)
    data.replace({'Visit_Bounce': {'Ja': 1, 'Nee': 0}}, inplace=True)
    data.replace({'Visit_containssocialprofile': {'Ja': 1, 'Nee': 0}}, inplace=True)

    data['Visit_Started_On'] = data['Visit_Started_On'].apply(parse_datetime("1750-01-01"))
    data['Visit_Ended_On'] = data['Visit_Ended_On'].apply(parse_datetime("2026-01-01"))
    data['Visit_Aangemaakt_op'] = data['Visit_Aangemaakt_op'].apply(parse_datetime("1750-01-01"))
    data['Visit_Gewijzigd_op'] = data['Visit_Gewijzigd_op'].apply(parse_datetime("2026-01-01"))
    
    new_to_csv(FILENAME, data)
    

def contact_functie():
    FILENAME = 'Contact functie.csv'
    data = default_process(FILENAME, dropna=True)
    new_to_csv(FILENAME, data)
 

def contact():
    FILENAME = 'Contact.csv'
    data = default_process(FILENAME)
    df_acc = pd.read_csv('../data_clean/Account_fixed.csv', sep=",")
    acc_unique = df_acc['Account_Account'].unique()
    data = data[data['Contact_Account'].isin(acc_unique)]
    new_to_csv(FILENAME, data)


def functie():
    FILENAME = 'Functie.csv'
    data = default_process(FILENAME)
    new_to_csv(FILENAME, data)


def gebruikers():
    FILENAME = 'Gebruikers.csv'
    data = default_process(FILENAME)
    new_to_csv(FILENAME, data)


def info_en_klachten():
    FILENAME = 'Info en klachten.csv'
    data = default_process(FILENAME)
    data['Info_en_Klachten_Datum'] = data['Info_en_Klachten_Datum'].apply(parse_datetime("1750-01-01"))
    data['Info_en_Klachten_Datum_afsluiting'] = data['Info_en_Klachten_Datum_afsluiting'].apply(parse_datetime("2026-01-01"))
    new_to_csv(FILENAME, data)


def inschrijving():
    FILENAME = 'Inschrijving.csv'
    data = default_process(FILENAME)
    data['Inschrijving_Datum_inschrijving'] = data['Inschrijving_Datum_inschrijving'].apply(parse_date("2018-05-01"))
    new_to_csv(FILENAME, data)
    

def Lidmaatschap():
    FILENAME = 'Lidmaatschap.csv'
    data = default_process(FILENAME)
    data['Lidmaatschap_Startdatum'] = data['Lidmaatschap_Startdatum'].apply(parse_date("1750-01-01"))
    data['Lidmaatschap_Datum_Opzeg'] = data['Lidmaatschap_Datum_Opzeg'].apply(parse_date("2026-01-01"))
    new_to_csv(FILENAME, data)
    


def persoon():
    FILENAME = 'Persoon.csv'
    data = default_process(FILENAME)
    data.replace('Nee', 0, inplace=True)
    data.replace('Ja', 1, inplace=True)
    new_to_csv(FILENAME, data)


def sessie_inschrijving():
    FILENAME = 'Sessie inschrijving.csv'
    data = default_process(FILENAME, dropna=True)
    new_to_csv(FILENAME, data)



def sessie():
    FILENAME = 'Sessie.csv'
    data = default_process(FILENAME)
    data['Sessie_Eind_Datum_Tijd'] = data['Sessie_Eind_Datum_Tijd'].apply(parse_datetime("2026-01-01"))
    data['Sessie_Start_Datum_Tijd'] = data['Sessie_Start_Datum_Tijd'].apply(parse_datetime("1750-01-01"))
    new_to_csv(FILENAME, data)



def teams():
    FILENAME = 'Teams.csv'
    data = default_process(FILENAME)
    new_to_csv(FILENAME, data)


# Define a dictionary mapping subcommands to functions
subcommands = {
    'all': ChangeAllData,
    '': ChangeAllData,
    'account_activiteitscode': account_activiteitscode,
    'account_financiele_data': account_financiele_data,
    'account': account,
    'activiteit_vereist_contact': activiteit_vereist_contact,
    'activiteitscode': activiteitscode,
    'afspraak_alle': afspraak_alle,
    'afspraak_betreft_account_cleaned': afspraak_betreft_account_cleaned,
    'afspraak_betreft_contact_cleaned': afspraak_betreft_contact_cleaned,
    'afspraak_account_gelinkt_cleaned': afspraak_account_gelinkt_cleaned,
    'campagne': campagne,
    'mailings': mailings,
    'sent_email_clicks': sent_email_clicks,
    'pageviews': pageviews,
    'visits': visits,
    'contact_functie': contact_functie,
    'contact': contact,
    'functie': functie,
    'gebruikers': gebruikers,
    'info_en_klachten': info_en_klachten,
    'inschrijving': inschrijving,
    'lidmaatschap': Lidmaatschap,
    'persoon': persoon,
    'sessie_inschrijving': sessie_inschrijving,
    'sessie': sessie,
    'teams': teams
    # Add more subcommands here...
}

"""
USE
python3 cleanup_script.py [NAAM SUBCOMMAND]
"""

parser = argparse.ArgumentParser(description="Process data files")

subparsers = parser.add_subparsers(dest='subcommand', title='Subcommands')
for subcommand, func in subcommands.items():
    subparser = subparsers.add_parser(subcommand)
    subparser.set_defaults(func=func)

args = parser.parse_args()

if hasattr(args, 'func'):
    print("Processing data for subcommand '{}'".format(args.subcommand))
    args.func()
    print("Done.")

else:
    print("Please specify a valid subcommand.")


