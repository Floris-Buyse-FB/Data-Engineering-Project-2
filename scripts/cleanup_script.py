import argparse
import re
import pandas as pd
import os


def titelChange(data):
    for col in data.columns:
        if col.startswith('crm_'):
            data.columns = data.columns.str.replace('crm_', '')


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
    data = pd.read_csv('../data/Account activiteitscode.csv', sep=",")
    titelChange(data)
    data.dropna(inplace=True)
    if os.path.exists('../data_clean/Account activiteitscode_fixed.csv'):
        os.remove('../data_clean/Account activiteitscode_fixed.csv')
    data.to_csv(
        '../data_clean/Account activiteitscode_fixed.csv', index=False)

    # Add your code to process 'Account Activiteit' here


def account_financiele_data():
    data = pd.read_csv('../data/Account financiele data.csv', sep=",")
    titelChange(data)
    if os.path.exists('../data_clean/Account financiele data_fixed.csv'):
        os.remove('../data_clean/Account financiele data_fixed.csv')
    data.to_csv(
        '../data_clean/Account financiele data_fixed.csv', index=False)
    # Add your code to process 'Account financiele data' here


def account():
    data = pd.read_csv('../data/Account.csv', sep=",")
    titelChange(data)
    data.reset_index(inplace=True)
    data['index'] = data['index'] + 1
    if 'crm_Account_Hoofd_NaCe_Code' in data.columns:
        data.drop('crm_Account_Hoofd_NaCe_Code', axis=1, inplace=True)
    if os.path.exists('../data_clean/Account_fixed.csv'):
        os.remove('../data_clean/Account_fixed.csv')
    data.to_csv('../data_clean/Account_fixed.csv', index=False)

    # Add your code to process 'Account financiele data' here


def activiteit_vereist_contact():
    data = pd.read_csv('../data/Activiteit vereist contact.csv', sep=",")
    titelChange(data)
    if os.path.exists('../data_clean/Activiteit vereist contact_fixed.csv'):
        os.remove('../data_clean/Activiteit vereist contact_fixed.csv')
    data.to_csv(
        '../data_clean/Activiteit vereist contact_fixed.csv', index=False)


def activiteitscode():
    data = pd.read_csv('../data/Activiteitscode.csv', sep=",")
    titelChange(data)
    if os.path.exists('../data_clean/Activiteitscode_fixed.csv'):
        os.remove('../data_clean/Activiteitscode_fixed.csv')
    data.to_csv('../data_clean/Activiteitscode_fixed.csv', index=False)


def afspraak_alle():
    data = pd.read_csv('../data/Afspraak alle.csv', sep=",")
    titelChange(data)
    if os.path.exists('../data_clean/Afspraak alle_fixed.csv'):
        os.remove('../data_clean/Afspraak alle_fixed.csv')
    data.to_csv('../data_clean/Afspraak alle_fixed.csv', index=False)


def afspraak_betreft_account_cleaned():
    data = pd.read_csv('../data/Afspraak betreft account_cleaned.csv', sep=",")
    data['crm_Afspraak_BETREFT_ACCOUNT_KeyPhrases'] = data['crm_Afspraak_BETREFT_ACCOUNT_KeyPhrases'].replace(
        '\[NAME\] ,*', '', regex=True)
    titelChange(data)
    if os.path.exists('../data_clean/Afspraak betreft account_cleaned_fixed.csv'):
        os.remove('../data_clean/Afspraak betreft account_cleaned_fixed.csv')
    data.to_csv(
        '../data_clean/Afspraak betreft account_cleaned_fixed.csv', index=False)

    # Add your code to process 'Afspraak betreft account cleaned' here


def afspraak_betreft_contact_cleaned():
    data = pd.read_csv('../data/Afspraak betreft contact_cleaned.csv', sep=",")
    data['crm_Afspraak_BETREFT_CONTACTFICHE_KeyPhrases'] = data['crm_Afspraak_BETREFT_CONTACTFICHE_KeyPhrases'].replace(
        '\[NAME\] ,*', '', regex=True)
    titelChange(data)
    if os.path.exists('../data_clean/Afspraak betreft contact_cleaned_fixed.csv'):
        os.remove('../data_clean/Afspraak betreft contact_cleaned_fixed.csv')
    data.to_csv(
        '../data_clean/Afspraak betreft contact_cleaned_fixed.csv', index=False)

    # Add your code to process 'Afspraak betreft contact cleaned' here


def afspraak_account_gelinkt_cleaned():
    data = pd.read_csv('../data/Afspraak_account_gelinkt_cleaned.csv', sep=",")
    data['crm_Afspraak_ACCOUNT_GELINKT_KeyPhrases'] = data['crm_Afspraak_ACCOUNT_GELINKT_KeyPhrases'].replace(
        '\[NAME\] ,*', '', regex=True)
    titelChange(data)
    if os.path.exists('../data_clean/Afspraak_account_gelinkt_cleaned_fixed.csv'):
        os.remove('../data_clean/Afspraak_account_gelinkt_cleaned_fixed.csv')
    data.to_csv(
        '../data_clean/Afspraak_account_gelinkt_cleaned_fixed.csv', index=False)
    # Add your code to process 'Afspraak betreft gelinkt cleaned' here


def campagne():
    data = pd.read_csv('../data/Campagne.csv', sep=",")
    titelChange(data)
    if os.path.exists('../data_clean/Campagne_fixed.csv'):
        os.remove('../data_clean/Campagne_fixed.csv')
    data.to_csv('../data_clean/Campagne_fixed.csv', index=False)


def mailings():
    data = pd.read_csv('../data/CDI mailings.csv', sep=",")
    titelChange(data)
    if os.path.exists('../data_clean/CDI mailings_fixed.csv'):
        os.remove('../data_clean/CDI mailings_fixed.csv')
    data.to_csv('../data_clean/CDI mailings_fixed.csv', index=False)


def sent_email_clicks():
    data = pd.read_csv('../data/CDI sent email clicks.csv', sep=",")
    titelChange(data)
    if os.path.exists('../data_clean/CDI sent email clicks_fixed.csv'):
        os.remove('../data_clean/CDI sent email clicks_fixed.csv')
    data.to_csv('../data_clean/CDI sent email clicks_fixed.csv', index=False)


def pageviews():
    data = pd.read_csv('../data/cdi pageviews.csv',
                       encoding="latin-1", sep=";")
    data.columns = data.columns.map(lambda x: re.sub(
        r'^crm CDI_PageView\[(.*)\]$', r'\1', x))
    if 'Anonymous Visitor' in data.columns:
        data.drop(['Anonymous Visitor'], axis=1, inplace=True)
    if 'crm_CDI_PageView_Campagne_Code' in data.columns:
        data.drop('crm_CDI_PageView_Campagne_Code', axis=1, inplace=True)
    data.to_csv('../data_clean/cdi pageviews_fixed.csv', index=False)
    # Add your code to process 'CDI pageviews' here


def visits():
    data = pd.read_csv('../data/CDI visits.csv', sep=",")
    if 'crm_CDI_Visit_Campagne_Code' in data.columns:
        data.drop('crm_CDI_Visit_Campagne_Code', axis=1, inplace=True)
    titelChange(data)
    if os.path.exists('../data_clean/CDI visits_fixed.csv'):
        os.remove('../data_clean/CDI visits_fixed.csv')
    data.to_csv('../data_clean/CDI visits_fixed.csv', index=False)
    # Add your code to process 'CDI visits' here


def web_content():
    data = pd.read_csv('../data/CDI web content.csv', sep=",")
    titelChange(data)
    if os.path.exists('../data_clean/CDI web content_fixed.csv'):
        os.remove('../data_clean/CDI web content_fixed.csv')
    data.to_csv('../data_clean/CDI web content_fixed.csv', index=False)


def contact_functie():
    data = pd.read_csv('../data/Contact functie.csv', sep=",")
    titelChange(data)
    data = data.dropna()
    if os.path.exists('../data_clean/Contact functie_fixed.csv'):
        os.remove('../data_clean/Contact functie_fixed.csv')
    data.to_csv('../data_clean/Contact functie_fixed.csv', index=False)


def contact():
    data = pd.read_csv('../data/Contact.csv', sep=",")
    titelChange(data)
    if os.path.exists('../data_clean/Contact_fixed.csv'):
        os.remove('../data_clean/Contact_fixed.csv')
    data.to_csv('../data_clean/Contact_fixed.csv', index=False)


def functie():
    data = pd.read_csv('../data/Functie.csv', sep=",")
    titelChange(data)
    if os.path.exists('../data_clean/Functie_fixed.csv'):
        os.remove('../data_clean/Functie_fixed.csv')
    data.to_csv('../data_clean/Functie_fixed.csv', index=False)


def gebruikers():
    data = pd.read_csv('../data/Gebruikers.csv', sep=",")
    titelChange(data)
    if os.path.exists('../data_clean/Gebruikers_fixed.csv'):
        os.remove('../data_clean/Gebruikers_fixed.csv')
    data.to_csv('../data_clean/Gebruikers_fixed.csv', index=False)


def info_en_klachten():
    data = pd.read_csv('../data/Info en klachten.csv', sep=",")
    titelChange(data)
    if os.path.exists('../data_clean/Info en klachten_fixed.csv'):
        os.remove('../data_clean/Info en klachten_fixed.csv')
    data.to_csv('../data_clean/Info en klachten_fixed.csv', index=False)


def inschrijving():
    data = pd.read_csv('../data/Inschrijving.csv', sep=",")
    titelChange(data)
    if os.path.exists('../data_clean/Inschrijving_fixed.csv'):
        os.remove('../data_clean/Inschrijving_fixed.csv')
    data.to_csv('../data_clean/Inschrijving_fixed.csv', index=False)


def Lidmaatschap():
    data = pd.read_csv('../data/Lidmaatschap.csv', sep=",")
    titelChange(data)
    if os.path.exists('../data_clean/Lidmaatschap_fixed.csv'):
        os.remove('../data_clean/Lidmaatschap_fixed.csv')
    data.to_csv('../data_clean/Lidmaatschap_fixed.csv', index=False)


def persoon():
    data = pd.read_csv('../data/persoon.csv', sep=",")
    data.replace('Nee', 0, inplace=True)
    data.replace('Ja', 1, inplace=True)
    titelChange(data)
    if os.path.exists('../data_clean/persoon_fixed.csv'):
        os.remove('../data_clean/persoon_fixed.csv')
    data.to_csv('../data_clean/persoon_fixed.csv', index=False)


def sessie_inschrijving():
    data = pd.read_csv('../data/Sessie inschrijving.csv', sep=",")
    data.dropna(inplace=True)
    titelChange(data)
    if os.path.exists('../data_clean/Sessie inschrijving_fixed.csv'):
        os.remove('../data_clean/Sessie inschrijving_fixed.csv')
    data.to_csv('../data_clean/Sessie inschrijving_fixed.csv', index=False)


def sessie():
    data = pd.read_csv('../data/Sessie.csv', sep=",")
    titelChange(data)
    if os.path.exists('../data_clean/Sessie_fixed.csv'):
        os.remove('../data_clean/Sessie_fixed.csv')
    data.to_csv('../data_clean/Sessie_fixed.csv', index=False)


def teams():
    data = pd.read_csv('../data/Teams.csv', sep=",")
    titelChange(data)
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
