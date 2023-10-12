import argparse
import re
import pandas as pd
import os
import time


def titelChange(data):
    for col in data.columns:
        if col.startswith('crm_') or col.startswith('CDI_'):
            data.columns = data.columns.str.replace('crm_', '')
            data.columns = data.columns.str.replace('CDI_', '')


# def remove_space_from_filename():
#     for filename in os.listdir('../data_clean'):
#         os.rename(f'../data_clean/{filename}', f'../data_clean/{filename.replace(" ", "_")}')


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


def account_activiteitscode():
    print('currently working on Account activiteitscode')
    data = pd.read_csv(f"../data/Account activiteitscode.csv", sep=",")
    
    data.dropna(inplace=True)
    titelChange(data)

    # fill the empty values with -1 if the column is numeric or with 'unknown' if the column is not numeric
    
    numeric = data.select_dtypes(include='number').columns
    non_numeric = data.select_dtypes(exclude='number').columns
    data[numeric] = data[numeric].fillna(-1)
    data[non_numeric] = data[non_numeric].fillna('unknown')
    data.fillna(-1, inplace=True)
    if os.path.exists(f'../data_clean/Account_activiteitscode_fixed.csv'):
        os.remove(f'../data_clean/Account_activiteitscode_fixed.csv')
    data.to_csv(
        f'../data_clean/Account_activiteitscode_fixed.csv', index=False)

    # Add your code to process 'Account Activiteit' here


def account_financiele_data():
    print('currently working on Account financiele data')
    data = pd.read_csv('../data/Account financiële data.csv', sep=",")
    titelChange(data)
    # data.reset_index(inplace=True)
    # data['index'] = data['index'] + 1
    # data.rename(columns={'index': 'FinancieleData_ID'}, inplace=True)
    excluded_ids = [
    "02E2C17D-A213-E211-9DAA-005056B06EB4",
    "5C161136-A768-E111-B43A-00505680000A",
    "8AC9D862-9668-E111-B43A-00505680000A",
    "DFAAE601-1969-E111-B43A-00505680000A"
    ]

    data = data[~data['FinancieleData_OndernemingID'].isin(excluded_ids)]
    numeric = data.select_dtypes(include='number').columns
    non_numeric = data.select_dtypes(exclude='number').columns
    data[numeric] = data[numeric].fillna(-1)
    data[non_numeric] = data[non_numeric].fillna('unknown')
    data.fillna(-1, inplace=True)
    if os.path.exists('../data_clean/Account_financiële_data_fixed.csv'):
        os.remove('../data_clean/Account_financiële_data_fixed.csv')
    data.to_csv(
        '../data_clean/Account_financiële_data_fixed.csv', index=False)
    # Add your code to process 'Account financiele data' here


def account():
    print('currently working on Account')
    data = pd.read_csv('../data/Account.csv', sep=",")
    titelChange(data)
    data.replace(
        {'Account_Status': {'Actief': 1, 'Inactief': 0}}, inplace=True)
    data.replace({'Account_Is_Voka_entiteit': {
                 'Ja': 1, 'Nee': 0}}, inplace=True)
    # data.reset_index(inplace=True)
    # data['index'] = data['index'] + 1
    if 'Account_Hoofd_NaCe_Code' in data.columns:
        data.drop('Account_Hoofd_NaCe_Code', axis=1, inplace=True)
    numeric = data.select_dtypes(include='number').columns
    non_numeric = data.select_dtypes(exclude='number').columns
    data[numeric] = data[numeric].fillna(-1)
    data[non_numeric] = data[non_numeric].fillna('unknown')
    data.fillna(-1, inplace=True)
    if os.path.exists('../data_clean/Account_fixed.csv'):
        os.remove('../data_clean/Account_fixed.csv')
    data.to_csv('../data_clean/Account_fixed.csv', index=False)

    # Add your code to process 'Account financiele data' here


def activiteit_vereist_contact():
    print('currently working on Activiteit vereist contact')
    data = pd.read_csv('../data/Activiteit vereist contact.csv', sep=",")
    titelChange(data)
    data.drop_duplicates(inplace=True)
    # data.reset_index(inplace=True)
    # data['index'] = data['index'] + 1
    # data.rename(columns={'index': 'Activiteit_vereist_contact_ID'}, inplace=True)
    numeric = data.select_dtypes(include='number').columns
    non_numeric = data.select_dtypes(exclude='number').columns
    data[numeric] = data[numeric].fillna(-1)
    data[non_numeric] = data[non_numeric].fillna('unknown')
    data.fillna(-1, inplace=True)
    if os.path.exists('../data_clean/Activiteit_vereist_contact_fixed.csv'):
        os.remove('../data_clean/Activiteit_vereist_contact_fixed.csv')
    data.to_csv(
        '../data_clean/Activiteit_vereist_contact_fixed.csv', index=False)


def activiteitscode():
    print('currently working on Activiteitscode')
    data = pd.read_csv('../data/Activiteitscode.csv', sep=",")
    titelChange(data)
    numeric = data.select_dtypes(include='number').columns
    non_numeric = data.select_dtypes(exclude='number').columns
    data[numeric] = data[numeric].fillna(-1)
    data[non_numeric] = data[non_numeric].fillna('unknown')
    data.fillna(-1, inplace=True)
    if os.path.exists('../data_clean/Activiteitscode_fixed.csv'):
        os.remove('../data_clean/Activiteitscode_fixed.csv')
    data.to_csv('../data_clean/Activiteitscode_fixed.csv', index=False)


def afspraak_alle():
    print('currently working on Afspraak alle')
    data = pd.read_csv('../data/Afspraak alle.csv', sep=",")
    titelChange(data)
    numeric = data.select_dtypes(include='number').columns
    non_numeric = data.select_dtypes(exclude='number').columns
    data[numeric] = data[numeric].fillna(-1)
    data[non_numeric] = data[non_numeric].fillna('unknown')
    data.fillna(-1, inplace=True)
    if os.path.exists('../data_clean/Afspraak_alle_fixed.csv'):
        os.remove('../data_clean/Afspraak_alle_fixed.csv')
    data.to_csv('../data_clean/Afspraak_alle_fixed.csv', index=False)


def afspraak_betreft_account_cleaned():
    print('currently working on Afspraak betreft account cleaned')
    data = pd.read_csv('../data/Afspraak betreft account_cleaned.csv', sep=",")
    data['crm_Afspraak_BETREFT_ACCOUNT_KeyPhrases'] = data['crm_Afspraak_BETREFT_ACCOUNT_KeyPhrases'].replace(
        '\[NAME\] ,*', '', regex=True)
    titelChange(data)
    # data.reset_index(inplace=True)
    # data['index'] = data['index'] + 1
    # data.rename(columns={'index': 'Afspraak_BETREFT_ACCOUNT_ID'}, inplace=True)
    numeric = data.select_dtypes(include='number').columns
    non_numeric = data.select_dtypes(exclude='number').columns
    data[numeric] = data[numeric].fillna(-1)
    data[non_numeric] = data[non_numeric].fillna('unknown')
    data.fillna(-1, inplace=True)
    if os.path.exists('../data_clean/Afspraak_betreft_account_cleaned_fixed.csv'):
        os.remove('../data_clean/Afspraak_betreft_account_cleaned_fixed.csv')
    data.to_csv(
        '../data_clean/Afspraak_betreft_account_cleaned_fixed.csv', index=False)

    # Add your code to process 'Afspraak betreft account cleaned' here


def afspraak_betreft_contact_cleaned():
    print('currently working on Afspraak betreft contact cleaned')
    data = pd.read_csv('../data/Afspraak betreft contact_cleaned.csv', sep=",")
    data['crm_Afspraak_BETREFT_CONTACTFICHE_KeyPhrases'] = data['crm_Afspraak_BETREFT_CONTACTFICHE_KeyPhrases'].replace(
        '\[NAME\] ,*', '', regex=True)
    titelChange(data)
    # data.reset_index(inplace=True)
    # data['index'] = data['index'] + 1
    # data.rename(columns={'index': 'Afspraak_BETREFT_CONTACTFICHE_ID'}, inplace=True)
    numeric = data.select_dtypes(include='number').columns
    non_numeric = data.select_dtypes(exclude='number').columns
    data[numeric] = data[numeric].fillna(-1)
    data[non_numeric] = data[non_numeric].fillna('unknown')
    data.fillna(-1, inplace=True)
    if os.path.exists('../data_clean/Afspraak_betreft_contact_cleaned_fixed.csv'):
        os.remove('../data_clean/Afspraak_betreft_contact_cleaned_fixed.csv')
    data.to_csv(
        '../data_clean/Afspraak_betreft_contact_cleaned_fixed.csv', index=False)

    # Add your code to process 'Afspraak betreft contact cleaned' here


def afspraak_account_gelinkt_cleaned():
    print('currently working on Afspraak account gelinkt cleaned')
    data = pd.read_csv('../data/Afspraak_account_gelinkt_cleaned.csv', sep=",")
    data['crm_Afspraak_ACCOUNT_GELINKT_KeyPhrases'] = data['crm_Afspraak_ACCOUNT_GELINKT_KeyPhrases'].replace(
        '\[NAME\] ,*', '', regex=True)
    titelChange(data)
    # data.reset_index(inplace=True)
    # data['index'] = data['index'] + 1
    # data.rename(columns={'index': 'Afspraak_ACCOUNT_GELINKT_ID'}, inplace=True)
    numeric = data.select_dtypes(include='number').columns
    non_numeric = data.select_dtypes(exclude='number').columns
    data[numeric] = data[numeric].fillna(-1)
    data[non_numeric] = data[non_numeric].fillna('unknown')
    data.fillna(-1, inplace=True)
    if os.path.exists('../data_clean/Afspraak_account_gelinkt_cleaned_fixed.csv'):
        os.remove('../data_clean/Afspraak_account_gelinkt_cleaned_fixed.csv')
    data.to_csv(
        '../data_clean/Afspraak_account_gelinkt_cleaned_fixed.csv', index=False)
    # Add your code to process 'Afspraak betreft gelinkt cleaned' here


def campagne():
    print('currently working on Campagne')
    data = pd.read_csv('../data/Campagne.csv', sep=",")
    titelChange(data)
    numeric = data.select_dtypes(include='number').columns
    non_numeric = data.select_dtypes(exclude='number').columns
    data[numeric] = data[numeric].fillna(-1)
    data[non_numeric] = data[non_numeric].fillna('unknown')
    data.fillna(-1, inplace=True)
    if os.path.exists('../data_clean/Campagne_fixed.csv'):
        os.remove('../data_clean/Campagne_fixed.csv')
    data.to_csv('../data_clean/Campagne_fixed.csv', index=False)


def mailings():
    print('currently working on Mailings')
    data = pd.read_csv('../data/CDI mailing.csv', sep=",")
    titelChange(data)
    numeric = data.select_dtypes(include='number').columns
    non_numeric = data.select_dtypes(exclude='number').columns
    data[numeric] = data[numeric].fillna(-1)
    data[non_numeric] = data[non_numeric].fillna('unknown')
    data.fillna(-1, inplace=True)
    if os.path.exists('../data_clean/CDI_mailing_fixed.csv'):
        os.remove('../data_clean/CDI_mailing_fixed.csv')
    data.to_csv('../data_clean/CDI_mailing_fixed.csv', index=False)


def sent_email_clicks():
    print('currently working on Sent email clicks')
    data = pd.read_csv('../data/CDI sent email clicks.csv', sep=",")
    titelChange(data)
    numeric = data.select_dtypes(include='number').columns
    non_numeric = data.select_dtypes(exclude='number').columns
    data[numeric] = data[numeric].fillna(-1)
    data[non_numeric] = data[non_numeric].fillna('unknown')
    data.fillna(-1, inplace=True)
    if os.path.exists('../data_clean/CDI_sent_email_clicks_fixed.csv'):
        os.remove('../data_clean/CDI_sent_email_clicks_fixed.csv')
    data.to_csv('../data_clean/CDI_sent_email_clicks_fixed.csv', index=False)


def pageviews():
    print('currently working on Pageviews')
    data = pd.read_csv('../data/cdi pageviews.csv',
                       encoding="latin-1", sep=";")
    data.columns = data.columns.map(lambda x: re.sub(
        r'^crm CDI_PageView\[(.*)\]$', r'\1', x))
    if 'Anonymous Visitor' in data.columns:
        data.drop(['Anonymous Visitor'], axis=1, inplace=True)
    if 'crm_CDI_PageView_Campagne_Code' in data.columns:
        data.drop('crm_CDI_PageView_Campagne_Code', axis=1, inplace=True)
    data.to_csv('../data_clean/cdi_pageviews_fixed.csv', index=False)
    # Add your code to process 'CDI pageviews' here


def visits():
    print('currently working on Visits')
    data = pd.read_csv('../data/CDI visits.csv', sep=",", dtype=str)
    if 'crm_CDI_Visit_Campagne_Code' in data.columns:
        data.drop('crm_CDI_Visit_Campagne_Code', axis=1, inplace=True)
    titelChange(data)
    data.replace({'CDI_Visit_Adobe_Reader': {'Ja': 1, 'Nee': 0}}, inplace=True)
    data.replace({'CDI_Visit_Bounce': {'Ja': 1, 'Nee': 0}}, inplace=True)
    data.replace({'CDI_Visit_containssocialprofile': {
                 'Ja': 1, 'Nee': 0}}, inplace=True)
    numeric = data.select_dtypes(include='number').columns
    non_numeric = data.select_dtypes(exclude='number').columns
    data[numeric] = data[numeric].fillna(-1)
    data[non_numeric] = data[non_numeric].fillna('unknown')
    data.fillna(-1, inplace=True)
    if os.path.exists('../data_clean/CDI_visits_fixed.csv'):
        os.remove('../data_clean/CDI_visits_fixed.csv')
    data.to_csv('../data_clean/CDI_visits_fixed.csv', index=False)
    # Add your code to process 'CDI visits' here


def web_content():
    print('currently working on Web content')
    data = pd.read_csv('../data/CDI web content.csv', sep=",")
    titelChange(data)
    numeric = data.select_dtypes(include='number').columns
    non_numeric = data.select_dtypes(exclude='number').columns
    data[numeric] = data[numeric].fillna(-1)
    data[non_numeric] = data[non_numeric].fillna('unknown')
    data.fillna(-1, inplace=True)
    if os.path.exists('../data_clean/CDI_web_content_fixed.csv'):
        os.remove('../data_clean/CDI_web_content_fixed.csv')
    data.to_csv('../data_clean/CDI_web_content_fixed.csv', index=False)


def contact_functie():
    print('currently working on Contact functie')
    data = pd.read_csv('../data/Contact functie.csv', sep=",")
    titelChange(data)
    data = data.dropna()
    data.reset_index(inplace=True, drop=True)
    # data['index'] = data['index'] + 1
    # data.rename(columns={'index': 'ContactFunctie_ID'}, inplace=True)
    numeric = data.select_dtypes(include='number').columns
    non_numeric = data.select_dtypes(exclude='number').columns
    data[numeric] = data[numeric].fillna(-1)
    data[non_numeric] = data[non_numeric].fillna('unknown')
    data.fillna(-1, inplace=True)
    if os.path.exists('../data_clean/Contact_functie_fixed.csv'):
        os.remove('../data_clean/Contact_functie_fixed.csv')
    data.to_csv('../data_clean/Contact_functie_fixed.csv', index=False)


def contact():
    print('currently working on Contact')
    data = pd.read_csv('../data/Contact.csv', sep=",")
    titelChange(data)

    numeric = data.select_dtypes(include='number').columns
    non_numeric = data.select_dtypes(exclude='number').columns
    data[numeric] = data[numeric].fillna(-1)
    data[non_numeric] = data[non_numeric].fillna('unknown')
    data.fillna(-1, inplace=True)
    if os.path.exists('../data_clean/Contact_fixed.csv'):
        os.remove('../data_clean/Contact_fixed.csv')
    data.to_csv('../data_clean/Contact_fixed.csv', index=False)


def functie():
    print('currently working on Functie')
    data = pd.read_csv('../data/Functie.csv', sep=",")
    titelChange(data)
    numeric = data.select_dtypes(include='number').columns
    non_numeric = data.select_dtypes(exclude='number').columns
    data[numeric] = data[numeric].fillna(-1)
    data[non_numeric] = data[non_numeric].fillna('unknown')
    data.fillna(-1, inplace=True)
    if os.path.exists('../data_clean/Functie_fixed.csv'):
        os.remove('../data_clean/Functie_fixed.csv')
    data.to_csv('../data_clean/Functie_fixed.csv', index=False)


def gebruikers():
    print('currently working on Gebruikers')
    data = pd.read_csv('../data/Gebruikers.csv', sep=",")
    titelChange(data)
    numeric = data.select_dtypes(include='number').columns
    non_numeric = data.select_dtypes(exclude='number').columns
    data[numeric] = data[numeric].fillna(-1)
    data[non_numeric] = data[non_numeric].fillna('unknown')
    data.fillna(-1, inplace=True)
    if os.path.exists('../data_clean/Gebruikers_fixed.csv'):
        os.remove('../data_clean/Gebruikers_fixed.csv')
    data.to_csv('../data_clean/Gebruikers_fixed.csv', index=False)


def info_en_klachten():
    print('currently working on Info en klachten')
    data = pd.read_csv('../data/Info en klachten.csv', sep=",")
    titelChange(data)
    numeric = data.select_dtypes(include='number').columns
    non_numeric = data.select_dtypes(exclude='number').columns
    data[numeric] = data[numeric].fillna(-1)
    data[non_numeric] = data[non_numeric].fillna('unknown')
    data.fillna(-1, inplace=True)
    if os.path.exists('../data_clean/Info_en_klachten_fixed.csv'):
        os.remove('../data_clean/Info_en_klachten_fixed.csv')
    data.to_csv('../data_clean/Info_en_klachten_fixed.csv', index=False)


def inschrijving():
    print('currently working on Inschrijving')
    data = pd.read_csv('../data/Inschrijving.csv', sep=",")
    titelChange(data)
    numeric = data.select_dtypes(include='number').columns
    non_numeric = data.select_dtypes(exclude='number').columns
    data[numeric] = data[numeric].fillna(-1)
    data[non_numeric] = data[non_numeric].fillna('unknown')
    data.fillna(-1, inplace=True)
    if os.path.exists('../data_clean/Inschrijving_fixed.csv'):
        os.remove('../data_clean/Inschrijving_fixed.csv')
    data.to_csv('../data_clean/Inschrijving_fixed.csv', index=False)


def Lidmaatschap():
    print('currently working on Lidmaatschap')
    data = pd.read_csv('../data/Lidmaatschap.csv', sep=",")
    titelChange(data)
    numeric = data.select_dtypes(include='number').columns
    non_numeric = data.select_dtypes(exclude='number').columns
    data[numeric] = data[numeric].fillna(-1)
    data[non_numeric] = data[non_numeric].fillna('unknown')
    data.fillna(-1, inplace=True)
    if os.path.exists('../data_clean/Lidmaatschap_fixed.csv'):
        os.remove('../data_clean/Lidmaatschap_fixed.csv')
    data.to_csv('../data_clean/Lidmaatschap_fixed.csv', index=False)


def persoon():
    print('currently working on Persoon')
    data = pd.read_csv('../data/Persoon.csv', sep=",")
    data.replace('Nee', 0, inplace=True)
    data.replace('Ja', 1, inplace=True)
    titelChange(data)
    numeric = data.select_dtypes(include='number').columns
    non_numeric = data.select_dtypes(exclude='number').columns
    data[numeric] = data[numeric].fillna(-1)
    data[non_numeric] = data[non_numeric].fillna('unknown')
    data.fillna(-1, inplace=True)
    if os.path.exists('../data_clean/Persoon_fixed.csv'):
        os.remove('../data_clean/Persoon_fixed.csv')
    data.to_csv('../data_clean/Persoon_fixed.csv', index=False)


def sessie_inschrijving():
    print('currently working on Sessie inschrijving')
    data = pd.read_csv('../data/Sessie inschrijving.csv', sep=",")
    data.dropna(inplace=True)
    titelChange(data)
    numeric = data.select_dtypes(include='number').columns
    non_numeric = data.select_dtypes(exclude='number').columns
    data[numeric] = data[numeric].fillna(-1)
    data[non_numeric] = data[non_numeric].fillna('unknown')
    data.fillna(-1, inplace=True)
    if os.path.exists('../data_clean/Sessie_inschrijving_fixed.csv'):
        os.remove('../data_clean/Sessie_inschrijving_fixed.csv')
    data.to_csv('../data_clean/Sessie_inschrijving_fixed.csv', index=False)


def sessie():
    print('currently working on Sessie')
    data = pd.read_csv('../data/Sessie.csv', sep=",")
    titelChange(data)
    numeric = data.select_dtypes(include='number').columns
    non_numeric = data.select_dtypes(exclude='number').columns
    data[numeric] = data[numeric].fillna(-1)
    data[non_numeric] = data[non_numeric].fillna('unknown')
    data.fillna(-1, inplace=True)
    if os.path.exists('../data_clean/Sessie_fixed.csv'):
        os.remove('../data_clean/Sessie_fixed.csv')
    data.to_csv('../data_clean/Sessie_fixed.csv', index=False)


def teams():
    print('currently working on Teams')
    data = pd.read_csv('../data/Teams.csv', sep=",")
    # titelChange(data)
    # data.reset_index(inplace=True)
    # data['index'] = data['index'] + 1
    data.rename(columns={'index': 'XLS_Teams_ID'}, inplace=True)
    numeric = data.select_dtypes(include='number').columns
    non_numeric = data.select_dtypes(exclude='number').columns
    data[numeric] = data[numeric].fillna(-1)
    data[non_numeric] = data[non_numeric].fillna('unknown')
    data.fillna(-1, inplace=True)
    if os.path.exists('../data_clean/Teams_fixed.csv'):
        os.remove('../data_clean/Teams_fixed.csv')
    data.to_csv('../data_clean/Teams_fixed.csv', index=False)


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


