import argparse
import re
import pandas as pd


def account_activiteit():
    data = pd.read_csv('../data/Account activiteitscode.csv', sep=",")
    data.dropna(inplace=True)
    # Add your code to process 'Account Activiteit' here


def account_financiele_data():
    data = pd.read_csv('../data/Account.csv', sep=",")
    data.head()
    if 'crm_Account_Hoofd_NaCe_Code' in data.columns:
        data.drop('crm_Account_Hoofd_NaCe_Code', axis=1, inplace=True)
    # Add your code to process 'Account financiele data' here


def afspraak_betreft_account_cleaned():
    data = pd.read_csv('../data/Afspraak betreft account_cleaned.csv', sep=",")
    data['crm_Afspraak_BETREFT_ACCOUNT_KeyPhrases'] = data['crm_Afspraak_BETREFT_ACCOUNT_KeyPhrases'].replace(
        '\[NAME\] ,*', '', regex=True)
    # Add your code to process 'Afspraak betreft account cleaned' here


def afspraak_betreft_contact_cleaned():
    data = pd.read_csv('../data/Afspraak betreft contact_cleaned.csv', sep=",")
    data['crm_Afspraak_BETREFT_CONTACTFICHE_KeyPhrases'] = data['crm_Afspraak_BETREFT_CONTACTFICHE_KeyPhrases'].replace(
        '\[NAME\] ,*', '', regex=True)
    # Add your code to process 'Afspraak betreft contact cleaned' here


def afspraak_account_gelinkt_cleaned():
    data = pd.read_csv('../data/Afspraak_account_gelinkt_cleaned.csv', sep=",")
    data['crm_Afspraak_ACCOUNT_GELINKT_KeyPhrases'] = data['crm_Afspraak_ACCOUNT_GELINKT_KeyPhrases'].replace(
        '\[NAME\] ,*', '', regex=True)
    # Add your code to process 'Afspraak betreft gelinkt cleaned' here


def cdi_pageviews():
    data = pd.read_csv('../data/cdi pageviews.csv',
                       encoding="latin-1", sep=";")
    data.columns = data.columns.map(lambda x: re.sub(
        r'^crm CDI_PageView\[(.*)\]$', r'\1', x))
    if 'Anonymous Visitor' in data.columns:
        data.drop(['Anonymous Visitor'], axis=1, inplace=True)
    # Add your code to process 'CDI pageviews' here


def visits():
    data = pd.read_csv('../data/CDI visits.csv', sep=",")
    if 'crm_CDI_Visit_Campagne_Code' in data.columns:
        data.drop('crm_CDI_Visit_Campagne_Code', axis=1, inplace=True)
    # Add your code to process 'CDI visits' here


def contact():
    data = pd.read_csv('../data/Contact functie.csv', sep=",")
    data = data.dropna()


def persoon():
    data = pd.read_csv('../data/persoon.csv', sep=",")
    data.replace('Nee', 0, inplace=True)
    data.replace('Ja', 1, inplace=True)


def sessie_inschrijving():
    data = pd.read_csv('../data/Sessie inschrijving.csv', sep=",")
    data.dropna(inplace=True)


# Define a dictionary mapping subcommands to functions
subcommands = {
    'account_activiteit': account_activiteit,
    'account_financiele_data': account_financiele_data,
    'afspraak_betreft_account_cleaned': afspraak_betreft_account_cleaned,
    'afspraak_betreft_contact_cleaned': afspraak_betreft_contact_cleaned,
    'afspraak_account_gelinkt_cleaned': afspraak_account_gelinkt_cleaned,
    'cdi_pageviews': cdi_pageviews,
    'visits': visits,
    'contact': contact,
    'persoon': persoon,
    'sessie_inschrijving': sessie_inschrijving,
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
    args.func()
else:
    print("Please specify a valid subcommand.")
