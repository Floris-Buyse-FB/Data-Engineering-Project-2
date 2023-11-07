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
                if col in df_copy.columns:
                    name_change = team_name_change(df_copy[col][row])
                    no_stopwords = remove_stopwords(name_change)
                    tokenize_list = word_tokenize(no_stopwords, language='dutch')
                    tokenize_list = [x for x in tokenize_list if x != ',']
                    df_copy.at[row, col] = ', '.join(list(set(tokenize_list)))
                    stemmer_list = stemmer(df_copy[col][row])
                    df_copy.at[row, col] = stemmer_list
                else:
                    print(f"Column '{col}' does not exist in the DataFrame.")
            except KeyError as e:
                print(f"KeyError: {e}")
    return df_copy

# einde functies voor het cleanen van de keyphrases

def parse_date(date_str):
    try:
        if date_str:
            return datetime.datetime.strptime(date_str, "%d-%m-%Y").date()
    except ValueError:
        pass
    return None  # Leave empty values as None

def parse_datetime(date_str):
    try: 
        if date_str:
            date_str = date_str.split(' ')[0]
            return datetime.datetime.strptime(date_str, "%d-%m-%Y").date()
    except ValueError:
        pass
    return None  # Leave empty values as None

def titelChange(data):
    for col in data.columns:
        if col.startswith('crm_') or col.startswith('CDI_'):
            data.columns = data.columns.str.replace('crm_', '')
            data.columns = data.columns.str.replace('CDI_', '')


def load_unique_values(file_name, column_name):
    df = pd.read_csv(os.path.join(CLEAN_DATA_FOLDER, file_name), sep=",")
    unique_values = df[column_name].unique()
    del df  # Release DataFrame from memory
    return unique_values


def remove_non_existing_pk(file, fk_arr, col_name_arr):

    df = pd.read_csv(os.path.join(CLEAN_DATA_FOLDER, file), sep=",")
    print(f'Loaded {file} with {len(df)} rows\n')

    for fk, col_name in zip(fk_arr, col_name_arr):
        if fk == 'account':
            acc_unique = load_unique_values('Account_fixed.csv', 'account_account_id')
            fk_arr_index = fk_arr.index('account')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(acc_unique)]
            print(f'{file}: FK for {fk}: {len(df)} rows left\n')

        elif fk == 'contact':
            contact_unique = load_unique_values('Contact_fixed.csv', 'contact_contactpersoon_id')
            fk_arr_index = fk_arr.index('contact')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(contact_unique)]
            print(f'{file}: FK for {fk}: {len(df)} rows left\n')

        elif fk == 'afspraak':
            afspraak_alle_unique = load_unique_values('Afspraak_alle_fixed.csv', 'afspraak_alle_afspraak_id')
            fk_arr_index = fk_arr.index('afspraak')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(afspraak_alle_unique)]
            print(f'{file}: FK for {fk}: {len(df)} rows left\n')

        elif fk == 'campagne':
            campagne_unique = load_unique_values('Campagne_fixed.csv', 'campagne_campagne_id')
            fk_arr_index = fk_arr.index('campagne')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(campagne_unique)]
            print(f'{file}: FK for {fk}: {len(df)} rows left\n')

        elif fk == 'mailing':
            mailing_unique = load_unique_values('CDI_mailing_fixed.csv', 'mailing_mailing_id')
            fk_arr_index = fk_arr.index('mailing')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(mailing_unique)]
            print(f'{file}: FK for {fk}: {len(df)} rows left\n')

        elif fk == 'activiteitscode':
            activiteitscode_unique = load_unique_values('Activiteitscode_fixed.csv', 'activiteitscode_activiteitscode_id')
            fk_arr_index = fk_arr.index('activiteitscode')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(activiteitscode_unique)]
            print(f'{file}: FK for {fk}: {len(df)} rows left\n')

        # elif fk == 'webcontent':
        #     webcontent_unique = load_unique_values('CDI_web_content_fixed.csv', 'webcontent_web_content_id')
        #     fk_arr_index = fk_arr.index('webcontent')
        #     col_name = col_name_arr[fk_arr_index]
        #     df = df[df[col_name].isin(webcontent_unique)]
        #     print(f'{file}: FK for {fk}: {len(df)} rows left\n')

        elif fk == 'visit':
            visit_unique = load_unique_values('CDI_visits_fixed.csv', 'visit_visit_id')
            fk_arr_index = fk_arr.index('visit')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(visit_unique)]
            print(f'{file}: FK for {fk}: {len(df)} rows left\n')

        elif fk == 'functie':
            functie_unique = load_unique_values('Functie_fixed.csv', 'functie_functie_id')
            fk_arr_index = fk_arr.index('functie')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(functie_unique)]
            print(f'{file}: FK for {fk}: {len(df)} rows left\n')

        elif fk == 'gebruiker':
            gebruiker_unique = load_unique_values('Gebruikers_fixed.csv', 'gebruikers_crm_user_id_id')
            fk_arr_index = fk_arr.index('gebruiker')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(gebruiker_unique)]
            print(f'{file}: FK for {fk}: {len(df)} rows left\n')

        elif fk == 'sessie':
            sessie_unique = load_unique_values('Sessie_fixed.csv', 'sessie_sessie_id')
            fk_arr_index = fk_arr.index('sessie')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(sessie_unique)]
            print(f'{file}: FK for {fk}: {len(df)} rows left\n')

        elif fk == 'inschrijving':
            inschrijving_unique = load_unique_values('Inschrijving_fixed.csv', 'inschrijving_inschrijving_id')
            fk_arr_index = fk_arr.index('inschrijving')
            col_name = col_name_arr[fk_arr_index]
            df = df[df[col_name].isin(inschrijving_unique)]
            print(f'{file}: FK for {fk}: {len(df)} rows left\n')
    
    print(f'Writing {file} to csv, {file} has {len(df)} rows left\n\n=========================================\n\n')
    df.to_csv(os.path.join(CLEAN_DATA_FOLDER, file), index=False)     


def default_process(filename, datafolder=DATA_FOLDER, dropna=False):

    print(f'currently working on {filename}')

    data = pd.read_csv(os.path.join(datafolder, filename))
    
    titelChange(data)

    if dropna:
        data.dropna(inplace=True)
        data.reset_index(inplace=True, drop=True)

    data.drop_duplicates(inplace=True)

    numeric = data.select_dtypes(include='number').columns
    non_numeric = data.select_dtypes(exclude='number').columns
    data[numeric] = data[numeric].fillna(-1)
    data[non_numeric] = data[non_numeric].fillna('unknown')

    return data


def new_to_csv(filename, data, cleandatafolder=CLEAN_DATA_FOLDER):
    new_filename = filename[:-4]
    new_filename = new_filename.replace(' ', '_')
    new_filename = f'{new_filename}_fixed.csv'

    path = os.path.join(cleandatafolder, new_filename)
    if os.path.exists(path):
        os.remove(path)
    data.to_csv(path, index=False)

def parse_date(date_str):
    try:
        if date_str:
            return datetime.datetime.strptime(date_str, "%d-%m-%Y").date()
    except ValueError:
        pass
    return None  # Leave empty values as None

def parse_datetime(date_str):
    try: 
        if date_str:
            date_str = date_str.split(' ')[0]
            return datetime.datetime.strptime(date_str, "%d-%m-%Y").date()
    except ValueError:
        pass
    return None  # Leave empty values as None

def create_column_names(dataframe, pk):
    columns = dataframe.columns
    columns = [col + '_id' if col == pk else col for col in columns]
    columns = [re.sub(r'\W+', '', col) for col in columns]
    columns = [col.lower() for col in columns]
    dict_columns = dict(zip(dataframe.columns, columns))
    return dict_columns


def columnNameChangeBis():

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
    'cdi_pageviews_fixed.csv': 'Page View',
    'CDI_sent_email_clicks_fixed.csv': 'SentEmail_kliks_Sent_Email',
    'CDI_visits_fixed.csv': 'Visit_Visit',
    'CDI_web_content_fixed.csv': 'WebContent_Web_Content',
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
        URL = os.path.join(CLEAN_DATA_FOLDER, file_name)
        data = pd.read_csv(URL)
        cols = create_column_names(data, pk)
        data.rename(columns=cols, inplace=True)
        data.to_csv(URL, index=False)


def ChangeAllData():
    account_activiteitscode()
    account_financiele_data()
    account()
    activiteit_vereist_contact()
    activiteitscode()
    afspraak_alle()
    afspraak_betreft_account_cleaned()
    afspraak_betreft_contact_cleaned()
    afspraak_account_gelinkt_cleaned()
    campagne()
    mailings()
    sent_email_clicks()
    pageviews()
    visits()
    web_content()
    contact_functie()
    contact()
    functie()
    gebruikers()
    info_en_klachten()
    inschrijving()
    Lidmaatschap()
    persoon()
    sessie_inschrijving()
    sessie()
    teams()

    print("Changing column names again...\nThis might take some time...")
    time.sleep(2)

    columnNameChangeBis()
    print("Column names changed successfully!\n")

    time.sleep(2)

    print("Removing non existing primary key references...\nThis might take some time...")

    remove_non_existing_pk('Account_financiële_data_fixed.csv', ['account'], ['financieledata_ondernemingid']) # niets veranderd
    remove_non_existing_pk('Contact_fixed.csv', ['account'], ['contact_account']) # niets veranderd
    remove_non_existing_pk('Activiteit_vereist_contact_fixed.csv', ['afspraak', 'contact'], ['activiteitvereistcontact_activityid_id', 'activiteitvereistcontact_reqattendee']) # veranderd veel
    remove_non_existing_pk('Account_activiteitscode_fixed.csv', ['account', 'activiteitscode'], ['account_activiteitscode_account', 'account_activiteitscode_activiteitscode']) # er gaat 1 rij weg
    remove_non_existing_pk('Afspraak_betreft_account_cleaned_fixed.csv', ['account', 'afspraak'], ['afspraak_betreft_account_betreft_id', 'afspraak_betreft_account_afspraak_id'])
    remove_non_existing_pk('Afspraak_betreft_contact_cleaned_fixed.csv', ['contact', 'afspraak'], ['afspraak_betreft_contactfiche_betreft_id', 'afspraak_betreft_contactfiche_afspraak_id'])
    remove_non_existing_pk('Afspraak_account_gelinkt_cleaned_fixed.csv', ['account', 'afspraak'], ['afspraak_account_gelinkt_account', 'afspraak_account_gelinkt_afspraak_id'])
    remove_non_existing_pk('CDI_sent_email_clicks_fixed.csv', ['mailing', 'contact'], ['sentemail_kliks_e_mail_versturen', 'sentemail_kliks_contact'])
    remove_non_existing_pk('CDI_visits_fixed.csv', ['contact', 'mailing', 'campagne'], ['visit_contact', 'visit_email_send', 'visit_campaign'])
    ### remove_non_existing_pk('Cdi_web_content_fixed.csv', ['campagne'], ['webcontent_campaign'])
    remove_non_existing_pk('CDI_pageviews_fixed.csv', ['contact', 'campagne', 'visit'], ['contact', 'campaign', 'visit']) # normaal gezien is webcontent ook FK
    remove_non_existing_pk('Contact_functie_fixed.csv', ['contact', 'functie'], ['contactfunctie_contactpersoon', 'contactfunctie_functie']) # weinig veranderd
    remove_non_existing_pk('Info_en_klachten_fixed.csv', ['account', 'gebruiker'], ['info_en_klachten_account', 'info_en_klachten_eigenaar']) # veel onbestaande gebruikers
    remove_non_existing_pk('Inschrijving_fixed.csv', ['contact', 'campagne'], ['inschrijving_contactfiche', 'inschrijving_campagne']) # ongv 10k vd 300k weg
    remove_non_existing_pk('Lidmaatschap_fixed.csv', ['account'], ['lidmaatschap_onderneming']) # veranderd niks
    remove_non_existing_pk('Sessie_fixed.csv', ['campagne'], ['sessie_campagne']) #
    remove_non_existing_pk('Sessie_inschrijving_fixed.csv', ['sessie', 'inschrijving'], ['sessieinschrijving_sessie', 'sessieinschrijving_inschrijving']) # 1/2 weg

    print("Non existing primary key references removed successfully!\n")
    print("Last cleanup for CDI_pageveiw_fixed.csv...\n")
    pv = pd.read_csv('../data_clean/CDI_pageviews_fixed.csv', sep=",", encoding="latin-1")
    zero_cols = pv.columns[pv.notnull().sum() == 0]
    pv.drop(zero_cols, axis=1, inplace=True)
    pv.to_csv('../data_clean/CDI_pageviews_fixed.csv', index=False)

def account():
    FILENAME = 'Account.csv'
    data = default_process(FILENAME)

    data.replace({'Account_Status': {'Actief': 1, 'Inactief': 0}}, inplace=True)
    data.replace({'Account_Is_Voka_entiteit': {'Ja': 1, 'Nee': 0}}, inplace=True)
    
    if 'Account_Hoofd_NaCe_Code' in data.columns:
        data.drop('Account_Hoofd_NaCe_Code', axis=1, inplace=True)

    data['Account_Oprichtingsdatum'] = data['Account_Oprichtingsdatum'].apply(parse_date)
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
    
    data['FinancieleData_Gewijzigd_op'] = data['FinancieleData_Gewijzigd_op'].apply(parse_datetime)
    
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
    data['Afspraak_BETREFT_ACCOUNT_Eindtijd'] = data['Afspraak_BETREFT_ACCOUNT_Eindtijd'].apply(parse_date)

    cols_to_clean = ["Afspraak_BETREFT_ACCOUNT_KeyPhrases"]
    cols_to_clean = clean_text(data,cols_to_clean)
    data[cols_to_clean.columns] = cols_to_clean
    new_to_csv(FILENAME, data)


def afspraak_betreft_contact_cleaned():
    FILENAME = 'Afspraak betreft contact_cleaned.csv'
    data = default_process(FILENAME)

    data['Afspraak_BETREFT_CONTACTFICHE_KeyPhrases'] = data['Afspraak_BETREFT_CONTACTFICHE_KeyPhrases'].replace('\[NAME\] ,*', '', regex=True)
    data['Afspraak_BETREFT_CONTACTFICHE_Eindtijd'] = data['Afspraak_BETREFT_CONTACTFICHE_Eindtijd'].apply(parse_date) 
    cols_to_clean = ["Afspraak_BETREFT_CONTACTFICHE_KeyPhrases"]
    cols_to_clean = clean_text(data,cols_to_clean)
    data[cols_to_clean.columns] = cols_to_clean   
    new_to_csv(FILENAME, data)
    

def afspraak_account_gelinkt_cleaned():
    FILENAME = 'Afspraak_account_gelinkt_cleaned.csv'
    data = default_process(FILENAME)

    data['Afspraak_ACCOUNT_GELINKT_KeyPhrases'] = data['Afspraak_ACCOUNT_GELINKT_KeyPhrases'].replace('\[NAME\] ,*', '', regex=True)
    data['Afspraak_ACCOUNT_GELINKT_Eindtijd'] = data['Afspraak_ACCOUNT_GELINKT_Eindtijd'].apply(parse_date)
    cols_to_clean = ["Afspraak_ACCOUNT_GELINKT_KeyPhrases"]
    cols_to_clean = clean_text(data,cols_to_clean)
    data[cols_to_clean.columns] = cols_to_clean 
    new_to_csv(FILENAME, data)


def campagne():
    FILENAME = 'Campagne.csv'
    data = default_process(FILENAME)

    data['Campagne_Einddatum'] = data['Campagne_Einddatum'].apply(parse_datetime)
    data['Campagne_Startdatum'] = data['Campagne_Startdatum'].apply(parse_datetime)
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

    if 'Anonymous Visitor' in data.columns:
        data.drop(['Anonymous Visitor'], axis=1, inplace=True)
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

    data['Visit_Started_On'] = data['Visit_Started_On'].apply(parse_datetime)
    data['Visit_Ended_On'] = data['Visit_Ended_On'].apply(parse_datetime)
    data['Visit_Aangemaakt_op'] = data['Visit_Aangemaakt_op'].apply(parse_datetime)
    data['Visit_Gewijzigd_op'] = data['Visit_Gewijzigd_op'].apply(parse_datetime)
    new_to_csv(FILENAME, data)


def web_content():
    FILENAME = 'CDI web content.csv'
    data = default_process(FILENAME)
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

    data['Info_en_Klachten_Datum'] = data['Info_en_Klachten_Datum'].apply(parse_datetime)
    data['Info_en_Klachten_Datum_afsluiting'] = data['Info_en_Klachten_Datum_afsluiting'].apply(parse_datetime)
    new_to_csv(FILENAME, data)


def gebruikers():
    FILENAME = 'Gebruikers.csv'
    data = default_process(FILENAME)
    new_to_csv(FILENAME, data)


def info_en_klachten():
    FILENAME = 'Info en klachten.csv'
    data = default_process(FILENAME)

    data['Info_en_Klachten_Datum'] = data['Info_en_Klachten_Datum'].apply(lambda date_str: datetime.datetime.strptime(date_str, "%d-%m-%Y %H:%M:%S").date())
    data['Info_en_Klachten_Datum'] = data['Info_en_Klachten_Datum'].dt.strftime('%d-%m-%Y')

    data['Info_en_Klachten_Datum_afsluiting'] = data['Info_en_Klachten_Datum_afsluiting'].apply(lambda date_str: datetime.datetime.strptime(date_str, "%d-%m-%Y %H:%M:%S").date())
    data['Info_en_Klachten_Datum_afsluiting'] = data['Info_en_Klachten_Datum_afsluiting'].dt.strftime('%d-%m-%Y')

    new_to_csv(FILENAME, data)


def inschrijving():
    FILENAME = 'Inschrijving.csv'
    data = default_process(FILENAME)

    data['Inschrijving_Datum_inschrijving'] = data['Inschrijving_Datum_inschrijving'].apply(parse_date)
    new_to_csv(FILENAME, data)


def Lidmaatschap():
    FILENAME = 'Lidmaatschap.csv'
    data = default_process(FILENAME)

    data['Lidmaatschap_Startdatum'] = data['Lidmaatschap_Startdatum'].apply(parse_date)
    data['Lidmaatschap_Datum_Opzeg'] = data['Lidmaatschap_Datum_Opzeg'].apply(parse_date)
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
    data['Sessie_Eind_Datum_Tijd'] = data['Sessie_Eind_Datum_Tijd'].apply(parse_datetime)
    data['Sessie_Start_Datum_Tijd'] = data['Sessie_Start_Datum_Tijd'].apply(parse_datetime)
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
    'web_content': web_content,
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


