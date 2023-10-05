import re
import pandas as pd

# Account Activiteit

data = pd.read_csv('../data/Account activiteitscode.csv', sep=",")
data.dropna(inplace=True)

# Account financiele data

# Account
data = pd.read_csv('../data/Account.csv', sep=",")
data.head()
if 'crm_Account_Hoofd_NaCe_Code' in data.columns:
    data.drop('crm_Account_Hoofd_NaCe_Code', axis=1, inplace=True)


# Activiteit vereist contact

# Activiteitscode

# Afspraak alle

# Afspraak betreft account cleaned
data = pd.read_csv('../data/Afspraak betreft account_cleaned.csv', sep=",")
data['crm_Afspraak_BETREFT_ACCOUNT_KeyPhrases'] = data['crm_Afspraak_BETREFT_ACCOUNT_KeyPhrases'].replace(
    '\[NAME\] ,*', '', regex=True)

# Afspraak betreft contact cleaned
data = pd.read_csv('../data/Afspraak betreft contact_cleaned.csv', sep=",")
data['crm_Afspraak_BETREFT_CONTACTFICHE_KeyPhrases'] = data['crm_Afspraak_BETREFT_CONTACTFICHE_KeyPhrases'].replace(
    '\[NAME\] ,*', '', regex=True)


# Afspraak betreft gelinkt cleaned
data = pd.read_csv('../data/Afspraak_account_gelinkt_cleaned.csv', sep=",")
data['crm_Afspraak_ACCOUNT_GELINKT_KeyPhrases'] = data['crm_Afspraak_ACCOUNT_GELINKT_KeyPhrases'].replace(
    '\[NAME\] ,*', '', regex=True)


# Campagne


# CDI sent emails clicks

# cdi pageviews
data = pd.read_csv('../data/cdi pageviews.csv', encoding="latin-1", sep=";")
data.columns = data.columns.map(lambda x: re.sub(
    r'^crm CDI_PageView\[(.*)\]$', r'\1', x))
if 'Anonymous Visitor' in data.columns:
    data.drop(['Anonymous Visitor'], axis=1, inplace=True)

data.head()


# CDI visits
data = pd.read_csv('../data/CDI visits.csv', sep=",")
if 'crm_CDI_Visit_Campagne_Code' in data.columns:
    data.drop('crm_CDI_Visit_Campagne_Code', axis=1, inplace=True)

# CDI Web content

# Contact functies
data = pd.read_csv('../data/Contact functie.csv', sep=",")
data = data.dropna()

# Contact

# Gebruikers

# info en klachten

# inschrijving

# lidmaatschap

# Persoon
data = pd.read_csv('../data/persoon.csv', sep=",")
data.replace('Nee', 0, inplace=True)
data.replace('Ja', 1, inplace=True)

# Sessie inschrijving
data = pd.read_csv('../data/Sessie inschrijving.csv', sep=",")
data.dropna(inplace=True)

# Sessie

# teams
