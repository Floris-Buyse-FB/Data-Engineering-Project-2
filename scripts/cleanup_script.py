import argparse
import re
import pandas as pd
import os
import time


DATA_FOLDER = '../data'
CLEAN_DATA_FOLDER = '../data_clean'


def titelChange(data):
    for col in data.columns:
        if col.startswith('crm_') or col.startswith('CDI_'):
            data.columns = data.columns.str.replace('crm_', '')
            data.columns = data.columns.str.replace('CDI_', '')


def default_process(filename, datafolder=DATA_FOLDER, cleandatafolder=CLEAN_DATA_FOLDER, dropna=False):

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


def account():
    FILENAME = 'Account.csv'
    data = default_process(FILENAME)

    data.replace({'Account_Status': {'Actief': 1, 'Inactief': 0}}, inplace=True)
    data.replace({'Account_Is_Voka_entiteit': {'Ja': 1, 'Nee': 0}}, inplace=True)
    
    if 'Account_Hoofd_NaCe_Code' in data.columns:
        data.drop('Account_Hoofd_NaCe_Code', axis=1, inplace=True)

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
    
    new_to_csv(FILENAME, data)


def afspraak_betreft_contact_cleaned():
    FILENAME = 'Afspraak betreft contact_cleaned.csv'
    data = default_process(FILENAME)

    data['Afspraak_BETREFT_CONTACTFICHE_KeyPhrases'] = data['Afspraak_BETREFT_CONTACTFICHE_KeyPhrases'].replace('\[NAME\] ,*', '', regex=True)

    new_to_csv(FILENAME, data)
    

def afspraak_account_gelinkt_cleaned():
    FILENAME = 'Afspraak_account_gelinkt_cleaned.csv'
    data = default_process(FILENAME)

    data['Afspraak_ACCOUNT_GELINKT_KeyPhrases'] = data['Afspraak_ACCOUNT_GELINKT_KeyPhrases'].replace('\[NAME\] ,*', '', regex=True)

    new_to_csv(FILENAME, data)


def campagne():
    FILENAME = 'Campagne.csv'
    data = default_process(FILENAME)
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
    
    data = pd.read_csv('../data/cdi pageviews.csv', encoding="latin-1", sep=";")
    
    data.columns = data.columns.map(lambda x: re.sub(r'^crm CDI_PageView\[(.*)\]$', r'\1', x))

    if 'Anonymous Visitor' in data.columns:
        data.drop(['Anonymous Visitor'], axis=1, inplace=True)
    if 'crm_CDI_PageView_Campagne_Code' in data.columns:
        data.drop('crm_CDI_PageView_Campagne_Code', axis=1, inplace=True)
    
    new_to_csv(FILENAME, data)

def visits():
    FILENAME = 'CDI visits.csv'
    data = default_process(FILENAME)

    if 'CDI_Visit_Campagne_Code' in data.columns:
        data.drop('CDI_Visit_Campagne_Code', axis=1, inplace=True)

    data.replace({'CDI_Visit_Adobe_Reader': {'Ja': 1, 'Nee': 0}}, inplace=True)
    data.replace({'CDI_Visit_Bounce': {'Ja': 1, 'Nee': 0}}, inplace=True)
    data.replace({'CDI_Visit_containssocialprofile': {'Ja': 1, 'Nee': 0}}, inplace=True)

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
    new_to_csv(FILENAME, data)


def gebruikers():
    FILENAME = 'Gebruikers.csv'
    data = default_process(FILENAME)
    new_to_csv(FILENAME, data)


def info_en_klachten():
    FILENAME = 'Info en klachten.csv'
    data = default_process(FILENAME)
    new_to_csv(FILENAME, data)


def inschrijving():
    FILENAME = 'Inschrijving.csv'
    data = default_process(FILENAME)
    new_to_csv(FILENAME, data)


def Lidmaatschap():
    FILENAME = 'Lidmaatschap.csv'
    data = default_process(FILENAME)
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


