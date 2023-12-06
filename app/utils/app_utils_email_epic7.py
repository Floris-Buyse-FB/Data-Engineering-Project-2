import random
import streamlit as st
from sqlalchemy import create_engine
import pandas as pd

from utils.app_utils_rec_epic_3 import *

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


def get_data(contactids):
    st.write('Setting up database connection and preloading data, please wait a moment')
    conn = connect_db()
    merged_total, df_inschrijving = get_all_data(contactids, conn)
    return merged_total, df_inschrijving,conn

def generate_personalized_email(naam, campaigns, doelen, strategien, handtekening,lengte):
  email_template = """Beste {klant_naam}

{begroeting}

{reden_voor_contact}

{campagnes_section}
{afspraak}

Bedankt voor je tijd en ik kijk ernaar uit om samen te werken aan het verder laten groeien van jouw bedrijf.

Met vriendelijke groet,

{handtekening}"""

  begroeting_library = [
        'Ik hoop dat deze e-mail je in goede gezondheid bereikt. Graag wil ik je bedanken voor je voortdurende vertrouwen in onze diensten. Wij bij Voka, zijn altijd op zoek naar manieren om onze samenwerking te versterken en jouw bedrijfsdoelstellingen te ondersteunen.',
        'Ik vertrouw erop dat deze boodschap je welzijn weerspiegelt. Dank je wel voor het voortdurende vertrouwen in onze diensten. Als toegewijde medewerkers bij Voka, streven we voortdurend naar manieren om onze samenwerking te optimaliseren en jouw bedrijfsdoelen te ondersteunen.',
        'Hopelijk ontvang je deze e-mail in goede gezondheid. Wij waarderen je voortdurende vertrouwen in onze diensten. Als team van Voka zijn we constant bezig met het vinden van manieren om onze samenwerking te versterken en jouw bedrijfsdoelen te realiseren.',
        'Deze boodschap bereikt je hopelijk in uitstekende conditie. Hartelijk dank voor het aanhoudende vertrouwen in onze diensten. Als professionals bij Voka, zoeken we voortdurend naar manieren om onze samenwerking te verbeteren en jouw bedrijfsdoelstellingen te ondersteunen.',
        'Moge deze e-mail je bereiken terwijl het goed met je gaat. Ik ben dankbaar voor het voortdurende vertrouwen in onze diensten. Als betrokken team van Voka, zetten we ons voortdurend in om onze samenwerking te versterken en jouw bedrijfsdoelstellingen te faciliteren.',
        'Ik hoop dat deze woorden je in goede gezondheid bereiken. Bedankt voor het blijvende vertrouwen in onze diensten. Als medewerkers van Voka, blijven we actief werken aan het versterken van onze samenwerking en het ondersteunen van jouw bedrijfsdoelstellingen.'
    ]

  reden_voor_contact_library = [
        'Ons team heeft nauwlettend uw bedrijf geanalyseerd en wij zijn ervan overtuigd dat de volgende campagnes perfect bij uw doelstellingen zullen passen.',
        'Na grondig onderzoek van uw bedrijf, zijn wij ervan overtuigd dat de voorgestelde campagnes naadloos aansluiten bij uw doelen.',
        'Op basis van onze analyse denken wij dat de voorgestelde campagnes een waardevolle aanvulling zullen zijn op uw huidige strategieën.',
        'Wij hebben uw bedrijf zorgvuldig geëvalueerd en zijn ervan overtuigd dat de onderstaande campagnes de juiste richting uitgaan voor uw groei en succes.',
        'Door een diepgaande analyse van uw onderneming zijn wij ervan overtuigd dat de geselecteerde campagnes uw bedrijfsdoelen effectief zullen ondersteunen.',
    ]


  afspraak_library = [
      'Ik geloof sterk dat de voorgestelde campagnes een aanzienlijke invloed kunnen hebben op de resultaten van uw bedrijf en de betrokkenheid van uw klanten kunnen verhogen. Laten we bijeenkomen om deze ideeën nader te bespreken en af te stemmen op de specifieke behoeften van uw onderneming.',
      'De potentiële impact van deze campagnes op uw bedrijfsresultaten en klantenbetrokkenheid is aanzienlijk. Laten we samen zitten om deze concepten in detail te bespreken en aan te passen aan de specifieke behoeften van uw onderneming.',
      'Mijn overtuiging is sterk dat deze campagnes een substantiële invloed kunnen hebben op uw bedrijfsprestaties en de betrokkenheid van uw klanten. Kunnen we in de komende week een afspraak maken om deze ideeën grondig te bespreken en op maat te maken voor uw onderneming?',
      'De impact die deze campagnes kunnen hebben op uw bedrijfsresultaten en klantenbetrokkenheid is aanzienlijk. Zullen we samenkomen om deze ideeën verder uit te werken en af te stemmen op de unieke behoeften van uw onderneming? Laat me weten wanneer u beschikbaar bent voor een overleg in de komende week.',
      'Ik ben overtuigd van de potentie van deze campagnes om aanzienlijke verbeteringen te brengen in uw bedrijfsresultaten en klantenbetrokkenheid. Laten we binnenkort samenkomen om deze ideeën te bespreken en aan te passen aan uw specifieke bedrijfsbehoeften.',
    ]


  campagnes_section = ""
  for i in range(lengte):
    print(i)
    campagnes_section += f"  {i + 1}. **{campaigns[i]}:**\n"
    campagnes_section += f"       - Soort: {doelen[i]}.\n"
    campagnes_section += f"       - Type: {strategien[i]}.\n\n"




  begroeting = begroeting_library[random.randint(0, len(begroeting_library)-1)]
  reden_voor_contact= reden_voor_contact_library[random.randint(0, len(reden_voor_contact_library)-1)]
  afspraak = afspraak_library[random.randint(0, len(afspraak_library)-1)]
    
  email_template = email_template.format(
          klant_naam=naam,
          begroeting=begroeting,
          reden_voor_contact=reden_voor_contact,
          campagnes_section=campagnes_section,
          afspraak=afspraak,
          handtekening=handtekening
    )

  return email_template