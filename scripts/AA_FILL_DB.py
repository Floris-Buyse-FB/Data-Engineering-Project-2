from sqlalchemy import Column, DateTime, Integer, Numeric, String, Date, Boolean, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Time
import csv

Base = declarative_base()

class Accounts(Base):
    __tablename__ = 'Accounts'
    Account = Column(Integer, primary_key=True)
    Adres_Geografische_regio = Column(String(255))
    Adres_Geografische_subregio = Column(String(255))
    Adres_Plaats = Column(String(255))
    Adres_Postcode = Column(Integer)
    Adres_Provincie = Column(String(255))
    Industriezone_Naam = Column(String(255))
    Is_Voka_entiteit = Column(Boolean)
    Ondernemingsaard = Column(String(255))
    Ondernemingstype = Column(String(255))
    Oprichtingsdatum = Column(Date)
    Primaire_activiteit = Column(String(255))
    Reden_van_status = Column(String(255))
    Status = Column(String(255))
    Voka_Nr = Column(Integer)
    # Hoofd_NaCe_Code = Column(String(255))  # Uncomment if needed
    Adres_Land = Column(String(255))

class InfoEnKlachten(Base):
    __tablename__ = 'Info_en_klachten'
    Aanvraag = Column(Integer, primary_key=True)
    Account = Column(Integer, ForeignKey('Accounts.Account'), nullable=False)
    Datum = Column(Date)
    Afsluiting = Column(Date)
    Status = Column(String(255))
    Eigenaar = Column(String(255))
    # relation to Accounts table
    account = relationship('Accounts', backref='info_en_klachten')

class Gebruiker(Base):
    __tablename__ = 'Gebruiker'
    Account = Column(Integer, primary_key=True)
    Business_Unit_Naam = Column(String(255))
    # Define a relationship to the Accounts table
    account = relationship('Accounts', backref='gebruiker')

class AccountHelpdeskvragen(Base):
    __tablename__ = 'Account_helpdeskvragen'
    Lidmaatschap = Column(Integer, primary_key=True)
    Account = Column(Integer, ForeignKey('Accounts.Account'), nullable=False)

class AccountFinanciëleData(Base):
    __tablename__ = 'Account_financiële_data'
    OndernemingID = Column(Integer, ForeignKey('Accounts.Account'), primary_key=True)
    Boekjaar = Column(Integer, primary_key=True)
    Aantal_maanden = Column(Integer)
    Toegevoegde_waarde = Column(Integer)
    FTE = Column(Integer)
    Gewijzigd_op = Column(Date)

class AccountActiviteitscode(Base):
    __tablename__ = 'Account_Activiteitscode'
    Account = Column(Integer, ForeignKey('Accounts.Account'), primary_key=True)
    Activiteitdscode = Column(Integer, ForeignKey('ActiviteitsCode.Activiteitdscode'), primary_key=True)

class ActiviteitsCode(Base):
    __tablename__ = 'ActiviteitsCode'
    Activiteitdscode = Column(Integer, primary_key=True)

class Contactfiches(Base):
    __tablename__ = 'Contactfiches'
    Contactfiche = Column(Integer, primary_key=True)
    Account = Column(Integer, ForeignKey('Accounts.Account'), nullable=False)
    Persoon = Column(Integer, ForeignKey('Personen.Persoon'), nullable=False)
    Functietitel = Column(String(255))
    Persoon_ID = Column(Integer)
    Status = Column(String(50))
    Voka_medewerker = Column(String(100))

class Personen(Base):
    __tablename__ = 'Personen'
    Persoon = Column(Integer, primary_key=True)
    Contactfiche = Column(Integer, ForeignKey('Contactfiches.Contactfiche'), nullable=False)
    Persoonsnr_ = Column(Integer)
    Reden_van_status = Column(Boolean)
    Web_Login = Column(Boolean)
    Mail_regio_Antwerpen_Waasland = Column(Boolean)
    Mail_regio_Brussel_Hoofdstedelijk_Gewest = Column(Boolean)
    Mail_regio_Limburg = Column(Boolean)
    Mail_regio_Mechelen_Kempen = Column(Boolean)
    Mail_regio_Oost_Vlaanderen = Column(Boolean)
    Mail_regio_Vlaams_Brabant = Column(Boolean)
    Mail_regio_Voka_nationaal = Column(Boolean)
    Mail_regio_West_Vlaanderen = Column(Boolean)
    Mail_thema_duurzaamheid = Column(Boolean)
    Mail_thema_financieel_fiscaal = Column(Boolean)
    Mail_thema_innovatie = Column(Boolean)
    Mail_thema_internationaal_ondernemen = Column(Boolean)
    Mail_thema_mobiliteit = Column(Boolean)
    Mail_thema_omgeving = Column(Boolean)
    Mail_thema_sales_marketing_communicatie = Column(Boolean)
    Mail_thema_strategie_en_algemeen_management = Column(Boolean)
    Mail_thema_talent = Column(Boolean)
    Mail_thema_welzijn = Column(Boolean)
    Mail_type_Bevraging = Column(Boolean)
    Mail_type_communities_en_projecten = Column(Boolean)
    Mail_type_netwerkevenementen = Column(Boolean)
    Mail_type_nieuwsbrieven = Column(Boolean)
    Mail_type_opleidingen = Column(Boolean)
    Mail_type_persberichten_belangrijke_meldingen = Column(Boolean)
    Marketingcommunicatie = Column(String(255))

class Functie(Base):
    __tablename__ = 'Functie'
    Functie = Column(String(255), primary_key=True)
    Naam = Column(String(255))

class ContactficheFuncties(Base):
    __tablename__ = 'Contactfiche_functies'
    Contactfiche = Column(Integer, ForeignKey('Contactfiches.Contactfiche'), nullable=False)
    Functie = Column(String(255))
    # Define a relationship to the Contactfiches table
    contactfiche = relationship('Contactfiches', backref='contactfiche_functies')

class AfspraakBetreftContactfiche(Base):
    __tablename__ = 'Afspraak_betreft_Contactfiche'
    Afspraak = Column(Integer, nullable=False)
    BetreftID = Column(Integer, nullable=False)
    Thema = Column(String(255))
    Subthema = Column(String(255))
    Onderwerp = Column(String(255))
    Eindtijd = Column(DateTime)
    KeyPhrases = Column(String(255))
    # Define a relationship to the Contactfiches table
    contactfiche = relationship('Contactfiches', backref='afspraak_betreft_contactfiche')

class AfspraakAccountGelinkt(Base):
    __tablename__ = 'Afspraak_account_gelinkt'
    Afspraak = Column(Integer, nullable=False)
    AccountID = Column(Integer, nullable=False)
    Thema = Column(String(255))
    Subthema = Column(String(255))
    Onderwerp = Column(String(255))
    Eindtijd = Column(DateTime)
    KeyPhrases = Column(String(255))
    # Define a relationship to the Accounts table
    account = relationship('Accounts', backref='afspraak_account_gelinkt')

class AfspraakBetreftAccount(Base):
    __tablename__ = 'Afspraak_betreft_Account'
    Afspraak = Column(Integer, nullable=False)
    BetreftID = Column(String(255), nullable=False)
    Thema = Column(String(255))
    Subthema = Column(String(255))
    Onderwerp = Column(String(255))
    Eindtijd = Column(DateTime)
    KeyPhrases = Column(String(255))
    # Define a relationship to the Accounts table
    account = relationship('Accounts', backref='afspraak_betreft_account')

class Afspraak(Base):
    __tablename__ = 'Afspraak'
    Afspraak = Column(Integer, primary_key=True)

class AfspraakVereistContact(Base):
    __tablename__ = 'Afspraak_vereist_contact'
    Afspraak = Column(Integer, nullable=False)
    Contact = Column(Integer, nullable=False)
    # Define a relationship to the Contactfiches table
    contactfiche = relationship('Contactfiches', backref='afspraak_vereist_contact')

class Inschrijving(Base):
    __tablename__ = 'Inschrijving'
    Inschrijving = Column(String(255), primary_key=True)
    Contactfiche = Column(String(255), ForeignKey('Contactfiches.Contactfiche'), nullable=False)
    Campagne = Column(String(255), ForeignKey('Campagne.Campagne'), nullable=False)
    Aanwezig_Afwezig = Column(String(255))
    Bron = Column(String(255))
    Datum_inschrijving = Column(Date)
    Facturatie_Bedrag = Column(Numeric(precision=10, scale=2))

class SessieInschrijving(Base):
    __tablename__ = 'Sessie_inschrijving'
    Sessieinschrijving = Column(String(255), primary_key=True)
    Inschrijving = Column(String(255), ForeignKey('Inschrijving.Inschrijving'), nullable=False)
    Sessie = Column(String(255), ForeignKey('Sessie.Sessie'), nullable=False)
    # Define a relationship to the Sessie table
    sessie = relationship('Sessie', backref='sessie_inschrijving')

class Sessie(Base):
    __tablename__ = 'Sessie'
    Sessie = Column(String(255), primary_key=True)
    Campagne = Column(String(255), ForeignKey('Campagne.Campagne'), nullable=False)
    Activiteitstype = Column(String(255))
    Eind_Datum_Tijd = Column(DateTime)  # Adjust to your desired date/time format
    Product = Column(String(255))
    Sessie_nr_ = Column(Integer)
    Start_Datum_Tijd = Column(DateTime)  # Adjust to your desired date/time format
    Thema_Naam = Column(String(255))
    # Define a relationship to the Campagne table
    campagne = relationship('Campagne', backref='sessie')

class Campagne(Base):
    __tablename__ = 'Campagne'
    Campagne = Column(String(255), primary_key=True)
    Campagne_Nr = Column(Integer)
    Einddatum = Column(Date)
    Naam = Column(String(255))
    Naam_in_email = Column(String(255))
    Reden_van_status = Column(String(255))
    Startdatum = Column(Date)
    Status = Column(String(255))
    Type_campagne = Column(String(255))
    URL_voka_be = Column(String(255))
    Soort_Campagne = Column(String(255))

class CDI_Pageview(Base):
    __tablename__ = 'CDI_Pageview'
    CDI_pageview = Column(String(255), primary_key=True)
    Campaign = Column(Integer, ForeignKey('Campaign.Campaign'), nullable=False)
    Contact = Column(Integer)
    Web_Content = Column(String(255))
    # Anonymous_Visitor = Column(String(255))
    Browser = Column(String(255))
    Duration = Column(Integer)
    Operating_System = Column(String(255))
    Referrer_Type = Column(String(255))
    Time = Column(Time)
    Page_Title = Column(String(255))
    Type = Column(String(255))
    Url = Column(String(255))
    Viewed_On = Column(Date)
    Visit = Column(Integer)
    Visitor_Key = Column(String(255))
    Aangemaakt_op = Column(DateTime)
    Gewijzigd_door = Column(String(255))
    Gewijzigd_op = Column(DateTime)
    Status = Column(String(255))
    Reden_van_status = Column(String(255))
    # Define a relationship to the Campaign table
    campaign = relationship('Campaign', backref='cdi_pageview')

class CDI_Visit(Base):
    __tablename__ = 'CDI_Visit'
    CDI_visit = Column(Integer, primary_key=True)
    Adobe_Reader = Column(String(255))
    Bounce = Column(String(255))
    Browser = Column(String(255))
    Campaign = Column(String(255), ForeignKey('Campaign.Campaign'))
    IP_Stad = Column(String(255))
    IP_Company = Column(String(255))
    Contact = Column(String(255))
    Contact_Naam = Column(String(255))
    containssocialprofile = Column(String(255))
    IP_Land = Column(String(255))
    Duration = Column(Integer)
    Email_Send = Column(String(255))
    Ended_On = Column(DateTime)
    Entry_Page = Column(String(255))
    Exit_Page = Column(String(255))
    First_Visit = Column(String(255))
    IP_Address = Column(String(255))
    IP_Organization = Column(String(255))
    Keywords = Column(String(255))
    IP_Latitude = Column(String(255))
    IP_Longitude = Column(String(255))
    Operating_System = Column(String(255))
    IP_Postcode = Column(String(255))
    Referrer = Column(String(255))
    Referring_Host = Column(String(255))
    Score = Column(String(255))
    Referrer_Type = Column(String(255))
    Started_On = Column(DateTime)
    IP_Status = Column(String(255))
    Time = Column(Time)
    Total_Pages = Column(Integer)
    Aangemaakt_op = Column(DateTime)
    Gewijzigd_op = Column(DateTime)
    # Define a relationship to the Campaign table
    campaign = relationship('Campaign', backref='cdi_visit')
    # Define a relationship to the Email_Send table
    email_send = relationship('Email_Send', backref='cdi_visit')

class CDI_Mailing(Base):
    __tablename__ = 'CDI_Mailing'
    
    Mailing = Column(Integer, primary_key=True)
    Name = Column(String(255))
    Sent_On = Column(DateTime)
    Onderwerp = Column(String(255))

class CDI_sentemail_click(Base):
    __tablename__ = 'CDI_sentemail_click'
    
    Sent_Email = Column(Integer, primary_key=True)
    Contact = Column(Integer, ForeignKey('Contactfiches.Contactfiche'))
    Email_versturen = Column(Integer, ForeignKey('CDI_Mailing.Mailing'))
    Clicks = Column(Integer)

# Create the engine
DB_URL = 'sqlite:///voka.db'  # Adjust based on your database type and connection details
engine = create_engine(DB_URL)

# Create the tables
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Define a dictionary mapping table names to their corresponding classes
table_classes = {
    'Accounts': Accounts,
    'Info_en_klachten': InfoEnKlachten,
    'Gebruiker': Gebruiker,
    'Account_helpdeskvragen': AccountHelpdeskvragen,
    'Account_financiële_data': AccountFinanciëleData,
    'Account_Activiteitscode': AccountActiviteitscode,
    'ActiviteitsCode': ActiviteitsCode,
    'Contactfiches': Contactfiches,
    'Personen': Personen,
    'Functie': Functie,
    'Contactfiche_functies': ContactficheFuncties,
    'Afspraak_betreft_Contactfiche': AfspraakBetreftContactfiche,
    'Afspraak_account_gelinkt': AfspraakAccountGelinkt,
    'Afspraak_betreft_Account': AfspraakBetreftAccount,
    'Afspraak': Afspraak,
    'Afspraak_vereist_contact': AfspraakVereistContact,
    'Inschrijving': Inschrijving,
    'Sessie_inschrijving': SessieInschrijving,
    'Sessie': Sessie,
    'Campagne': Campagne,
    'CDI_Pageview': CDI_Pageview,
    'CDI_Visit': CDI_Visit,
    'CDI_Mailing': CDI_Mailing,
    'CDI_sentemail_click': CDI_sentemail_click,
    
}

# CSV files to read and import
csv_files = {
    'Accounts': 'Account_fixed.csv',
    'Info_en_klachten': 'Info en klachten_fixed.csv',
    'Gebruiker': 'Gebruikers_fixed.csv',
    'Account_helpdeskvragen': 'account_helpdeskvragen.csv',
    'Account_financiële_data': 'Account financiële data_fixed.csv',
    'Account_Activiteitscode': 'Account activiteitscode_fixed.csv',
    'ActiviteitsCode': 'Activiteitscode_fixed.csv',
    'Contactfiches': 'Contact_fixed.csv',
    'Personen': 'Persoon_fixed.csv',
    'Functie': 'Functie_fixed.csv',
    'Contactfiche_functies': 'Contact functie_fixed.csv',
    'Afspraak_betreft_Contactfiche': 'Afspraak betreft contact_cleaned_fixed.csv',
    'Afspraak_account_gelinkt': 'Afspraak_account_gelinkt_cleaned_fixed.csv',
    'Afspraak_betreft_Account': 'Afspraak betreft account_cleaned_fixed.csv',
    'Afspraak': 'Afspraak alle_fixed.csv',
    'Afspraak_vereist_contact': 'Activiteit vereist contact_fixed.csv',
    'Inschrijving': 'Inschrijving_fixed.csv',
    'Sessie_inschrijving': 'Sessie inschrijving_fixed.csv',
    'Sessie': 'Sessie_fixed.csv',
    'Campagne': 'Campagne_fixed.csv',
    'CDI_Pageview': 'cdi pageviews_fixed.csv',
    'CDI_Visit': 'CDI visits_fixed.csv',
    'CDI_Mailing': 'CDI mailing_fixed.csv',
    'CDI_sentemail_click': 'CDI sent email clicks_fixed.csv',
}

def populate_table(table_name, csv_file):
    # Get the column names for the specified table
    table_columns = [col.name for col in table_classes[table_name].__table__.columns]
    
    with open(csv_file, 'r', encoding='utf-8-sig') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            new_row = table_classes[table_name]()
            for col_index, col_value in enumerate(row):
                setattr(new_row, table_columns[col_index], col_value)
            session.add(new_row)

# Create the tables
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Populate each table
for table_name, csv_file in csv_files.items():
    populate_table(table_name, csv_file)

# Commit the changes
session.commit()