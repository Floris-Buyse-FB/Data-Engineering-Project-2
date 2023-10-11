from sqlalchemy import Column, Integer, Float, String, ForeignKey
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = sqlalchemy.orm.declarative_base()

class Account_activiteitscode(Base):
    __tablename__ = 'Account_activiteitscode'
    Account_ActiviteitsCode_Account = Column(String(255))
    Account_ActiviteitsCode_Activiteitscode = Column(String(255))
    Account_ActiviteitsCode_inf_account_inf_activiteitscodeId = Column(String(255), primary_key=True)

class Account(Base):
    __tablename__ = 'Account'
    Account_Account = Column(String(255), primary_key=True)
    Account_Adres_Geografische_regio = Column(String(255))
    Account_Adres_Geografische_subregio = Column(String(255))
    Account_Adres_Plaats = Column(String(255))
    Account_Adres_Postcode = Column(String(255))
    Account_Adres_Provincie = Column(String(255))
    Account_Industriezone_Naam_ = Column(String(255))
    Account_Is_Voka_entiteit = Column(Integer)
    Account_Ondernemingsaard = Column(String(255))
    Account_Ondernemingstype = Column(String(255))
    Account_Oprichtingsdatum = Column(String(255))
    Account_Primaire_activiteit = Column(String(255))
    Account_Reden_van_status = Column(String(255))
    Account_Status = Column(Integer)
    Account_Voka_Nr_ = Column(Integer)
    Account_Adres_Land = Column(String(255))

    Account_financiële_data = relationship("Account_financiële_data", backref="account_from_financiële_data")
    Afspraak_betreft_account_cleaned = relationship("Afspraak_betreft_account_cleaned", backref="account_from_betreft_account_cleaned")
    Afspraak_account_gelinkt_cleaned = relationship("Afspraak_account_gelinkt_cleaned", backref="account_from_account_gelinkt_cleaned")
    Info_en_klachten = relationship("Info_en_klachten", backref="account_from_info_en_klachten")
    Lidmaatschap = relationship("Lidmaatschap", backref="account_from_lidmaatschap")

class Account_financiële_data(Base):
    __tablename__ = 'Account_financiële_data'
    FinancieleData_ID = Column(Integer, primary_key=True)
    Account_Account = Column(String(255), ForeignKey('Account.Account_Account'))
    FinancieleData_Boekjaar = Column(Integer)
    FinancieleData_Aantal_maanden = Column(Float)
    FinancieleData_Toegevoegde_waarde = Column(String(255))
    FinancieleData_FTE = Column(String(255))
    FinancieleData_Gewijzigd_op = Column(String(255))

    Account = relationship("Account", backref="account_from_financiële_data")

class Afspraak_alle(Base):
    __tablename__ = 'Afspraak_alle'
    Afspraak_ALLE_Afspraak = Column(String(255), primary_key=True)

    Activiteit_vereist_contact = relationship("Activiteit_vereist_contact", backref="afspraak_van_alle_vereist_contact")
    Afspraak_betreft_account_cleaned = relationship("Afspraak_betreft_account_cleaned", backref="afspraak_van_alle_betreft_account")
    Afspraak_betreft_contact_cleaned = relationship("Afspraak_betreft_contact_cleaned", backref="afspraak_van_alle_betreft_contact")
    Afspraak_account_gelinkt_cleaned = relationship("Afspraak_account_gelinkt_cleaned", backref="Afspraak_alle_from_account_gelinkt_cleaned")

class Persoon(Base):
    __tablename__ = 'Persoon'
    Persoon_persoon = Column(String(255), primary_key=True)
    Persoon_Persoonsnr_ = Column(Integer)
    Persoon_Reden_van_status = Column(String(255))
    Persoon_Web_Login = Column(String(255))
    Persoon_Mail_regio_Antwerpen_Waasland = Column(Integer)
    Persoon_Mail_regio_Brussel_Hoofdstedelijk_Gewest = Column(Integer)
    Persoon_Mail_regio_Limburg = Column(Integer)
    Persoon_Mail_regio_Mechelen_Kempen = Column(Integer)
    Persoon_Mail_regio_Oost_Vlaanderen = Column(Integer)
    Persoon_Mail_regio_Vlaams_Brabant = Column(Integer)
    Persoon_Mail_regio_Voka_nationaal = Column(Integer)
    Persoon_Mail_regio_West_Vlaanderen = Column(Integer)
    Persoon_Mail_thema_duurzaamheid = Column(Integer)
    Persoon_Mail_thema_financieel_fiscaal = Column(Integer)
    Persoon_Mail_thema_innovatie = Column(Integer)
    Persoon_Mail_thema_internationaal_ondernemen = Column(Integer)
    Persoon_Mail_thema_mobiliteit = Column(Integer)
    Persoon_Mail_thema_omgeving = Column(Integer)
    Persoon_Mail_thema_sales_marketing_communicatie = Column(Integer)
    Persoon_Mail_thema_strategie_en_algemeen_management = Column(Integer)
    Persoon_Mail_thema_talent = Column(Integer)
    Persoon_Mail_thema_welzijn = Column(Integer)
    Persoon_Mail_type_Bevraging = Column(Integer)
    Persoon_Mail_type_communities_en_projecten = Column(Integer)
    Persoon_Mail_type_netwerkevenementen = Column(Integer)
    Persoon_Mail_type_nieuwsbrieven = Column(Integer)
    Persoon_Mail_type_opleidingen = Column(Integer)
    Persoon_Mail_type_persberichten_belangrijke_meldingen = Column(Integer)
    Persoon_Marketingcommunicatie = Column(String(255))

class Contact(Base):
    __tablename__ = 'Contact'
    Contact_Contactpersoon = Column(String(255), primary_key=True)
    Account_Account = Column(String(255), ForeignKey('Account.Account_Account'))
    Contact_Functietitel = Column(String(255))
    Persoon_Persoon = Column(String(255), ForeignKey('Persoon.Persoon_persoon'))
    Contact_Status = Column(String(255))
    Contact_Voka_medewerker = Column(Integer)

    Activiteit_vereist_contact = relationship("Activiteit_vereist_contact", backref="contact_van_vereist_contact")
    Afspraak_betreft_contact_cleaned = relationship("Afspraak_betreft_contact_cleaned", backref="contact_van_betreft_contact")
    CDI_visits = relationship("CDI_visits", backref="contact_van_visits")
    cdi_pageviews = relationship("cdi_pageviews", primaryjoin="Contact.Contact_Contactpersoon == cdi_pageviews.Contact")
    CDI_sent_email_clicks = relationship("CDI_sent_email_clicks", backref="contact_van_sent_email_clicks")
    Contact_functie = relationship("Contact_functie", backref="contact_van_functie")
    Inschrijving = relationship("Inschrijving", backref="contact_van_inschrijving")

class Activiteit_vereist_contact(Base):
    __tablename__ = 'Activiteit_vereist_contact'
    Activiteit_vereist_contact_ID = Column(Integer, primary_key=True)
    Afspraak_ALLE_Afspraak = Column(String(255), ForeignKey('Afspraak_alle.Afspraak_ALLE_Afspraak'))
    Contact_Contactpersoon = Column(String(255), ForeignKey('Contact.Contact_Contactpersoon'))

    Afspraak_alle = relationship("Afspraak_alle", backref="afspraak_van_alle_vereist_contact")
    Contact = relationship("Contact", backref="contact_van_vereist_contact")

class Activiteitscode(Base):
    __tablename__ = 'Activiteitscode'
    ActiviteitsCode_Naam = Column(String(255))
    ActiviteitsCode_Activiteitscode = Column(String(255), primary_key=True)
    ActiviteitsCode_Status = Column(String(255))

class Afspraak_betreft_account_cleaned(Base):
    __tablename__ = 'Afspraak_betreft_account_cleaned'
    Afspraak_ALLE_Afspraak = Column(String(255), ForeignKey('Afspraak_alle.Afspraak_ALLE_Afspraak'))
    Afspraak_BETREFT_ACCOUNT_Thema = Column(String(255))
    Afspraak_BETREFT_ACCOUNT_Subthema = Column(String(255))
    Afspraak_BETREFT_ACCOUNT_Onderwerp = Column(String(255))
    Account_Account = Column(String(255), ForeignKey('Account.Account_Account'))
    Afspraak_BETREFT_ACCOUNT_Eindtijd = Column(String(255))
    Afspraak_BETREFT_ACCOUNT_KeyPhrases = Column(String(255))
    Afspraak_BETREFT_ACCOUNT_ID = Column(Integer, primary_key=True)

    Afspraak_alle = relationship("Afspraak_alle", backref="afspraak_van_alle_betreft_account")
    Account = relationship("Account", backref="account_from_betreft_account_cleaned")

class Afspraak_betreft_contact_cleaned(Base):
    __tablename__ = 'Afspraak_betreft_contact_cleaned'
    Afspraak_ALLE_Afspraak = Column(String(255), ForeignKey('Afspraak_alle.Afspraak_ALLE_Afspraak'))
    Afspraak_BETREFT_CONTACTFICHE_Thema = Column(String(255))
    Afspraak_BETREFT_CONTACTFICHE_Subthema = Column(String(255))
    Afspraak_BETREFT_CONTACTFICHE_Onderwerp = Column(String(255))
    Contact_Contactpersoon = Column(String(255), ForeignKey('Contact.Contact_Contactpersoon'))
    Afspraak_BETREFT_CONTACTFICHE_Eindtijd = Column(String(255))
    Afspraak_BETREFT_CONTACTFICHE_KeyPhrases = Column(String(255))
    Afspraak_BETREFT_CONTACTFICHE_ID = Column(Integer, primary_key=True)

    Afspraak_alle = relationship("Afspraak_alle", backref="afspraak_van_alle_betreft_contact")
    Contact = relationship("Contact", backref="contact_van_betreft_contact")

class Afspraak_account_gelinkt_cleaned(Base):
    __tablename__ = 'Afspraak_account_gelinkt_cleaned'
    Afspraak_ALLE_Afspraak = Column(String(255), ForeignKey('Afspraak_alle.Afspraak_ALLE_Afspraak'))
    Afspraak_ACCOUNT_GELINKT_Thema = Column(String(255))
    Afspraak_ACCOUNT_GELINKT_Subthema = Column(String(255))
    Afspraak_ACCOUNT_GELINKT_Onderwerp = Column(String(255))
    Afspraak_ACCOUNT_GELINKT_Eindtijd = Column(String(255))
    Account_Account = Column(String(255), ForeignKey('Account.Account_Account'))
    Afspraak_ACCOUNT_GELINKT_KeyPhrases = Column(String(255))
    Afspraak_ACCOUNT_GELINKT_ID = Column(Integer, primary_key=True)

    Afspraak_alle = relationship("Afspraak_alle", backref="afspraak_alle_from_account_gelinkt_cleaned")
    Account = relationship("Account", backref="account_from_account_gelinkt_cleaned")

class Campagne(Base):
    __tablename__ = 'Campagne'
    Campagne_Campagne = Column(String(255), primary_key=True)
    Campagne_Campagne_Nr = Column(String(255))
    Campagne_Einddatum = Column(String(255))
    Campagne_Naam = Column(String(255))
    Campagne_Naam_in_email = Column(String(255))
    Campagne_Reden_van_status = Column(String(255))
    Campagne_Startdatum = Column(String(255))
    Campagne_Status = Column(String(255))
    Campagne_Type_campagne = Column(String(255))
    Campagne_URL_voka_be = Column(String(255))
    Campagne_Soort_Campagne = Column(String(255))

    CDI_visits = relationship("CDI_visits", backref="campagne_from_visits")
    cdi_pageviews = relationship("cdi_pageviews", backref="campagne_from_pageviews")
    Sessie = relationship("Sessie", backref="campagne_from_sessie")

class CDI_mailing(Base):
    __tablename__ = 'CDI_mailing'
    Mailing_Mailing = Column(String(255), primary_key=True)
    Mailing_Name = Column(String(255))
    Mailing_Sent_On = Column(String(255))
    Mailing_Onderwerp = Column(String(255))

    CDI_visits = relationship("CDI_visits", backref="cdi_mailing_from_visits")
    CDI_sent_email_clicks = relationship("CDI_sent_email_clicks", backref="cdi_mailing_from_sent_email_clicks")

class CDI_visits(Base):
    __tablename__ = 'CDI_visits'
    Visit_Adobe_Reader = Column(Integer)
    Visit_Bounce = Column(Integer)
    Visit_Browser = Column(String(255))
    Campagne_Campagne = Column(String(255), ForeignKey('Campagne.Campagne_Campagne'))
    Visit_IP_Stad = Column(String(255))
    Visit_IP_Company = Column(String(255))
    Contact_Contactpersoon = Column(String(255), ForeignKey('Contact.Contact_Contactpersoon'))
    Visit_Contact_Naam_ = Column(String(255))
    Visit_containssocialprofile = Column(Integer)
    Visit_IP_Land = Column(String(255))
    Visit_Duration = Column(Float)
    Mailing_Mailing = Column(String(255), ForeignKey('CDI_mailing.Mailing_Mailing'))
    Visit_Ended_On = Column(String(255))
    Visit_Entry_Page = Column(String(255))
    Visit_Exit_Page = Column(String(255))
    Visit_First_Visit = Column(String(255))
    Visit_IP_Address = Column(String(255))
    Visit_IP_Organization = Column(String(255))
    Visit_Keywords = Column(String(255))
    Visit_IP_Latitude = Column(Float)
    Visit_IP_Longitude = Column(Float)
    Visit_Operating_System = Column(String(255))
    Visit_IP_Postcode = Column(String(255))
    Visit_Referrer = Column(String(255))
    Visit_Referring_Host = Column(String(255))
    Visit_Score = Column(Float)
    Visit_Referrer_Type = Column(String(255))
    Visit_Started_On = Column(String(255))
    Visit_IP_Status = Column(String(255))
    Visit_Time = Column(String(255))
    Visit_Total_Pages = Column(Float)
    Visit_Visit = Column(String(255), primary_key=True)
    Visit_Aangemaakt_op = Column(String(255))
    Visit_Gewijzigd_op = Column(String(255))

    Campagne = relationship("Campagne", backref="campagne_from_visits")
    Contact = relationship("Contact", backref="contact_van_visits")
    CDI_mailing = relationship("CDI_mailing", backref="cdi_mailing_from_visits")
    cdi_pageviews = relationship("cdi_pageviews", backref="cdi_visits_from_pageviews")

class CDI_web_content(Base):
    __tablename__ = 'CDI_web_content'
    WebContent_Campaign = Column(String(255))
    WebContent_Campaign_Name = Column(String(255))
    WebContent_Name = Column(String(255))
    WebContent_Web_Content = Column(String(255), primary_key=True)
    WebContent_Gemaakt_door_Naam_ = Column(String(255))
    WebContent_Created_On = Column(String(255))
    WebContent_Gewijzigd_door_Naam_ = Column(String(255))
    WebContent_Modified_On = Column(String(255))
    WebContent_Owner = Column(String(255))
    WebContent_Owner_Name = Column(String(255))
    WebContent_Het_bezitten_van_Business_Unit = Column(String(255))

    cdi_pageviews = relationship("cdi_pageviews", backref="cdi_web_content_from_pageviews")

class cdi_pageviews(Base):
    __tablename__ = 'cdi_pageviews'
    Browser = Column(String(255))
    Campagne_Campagne = Column(String(255), ForeignKey('Campagne.Campagne_Campagne'))
    Contact_Contactpersoon = Column(String(255), ForeignKey('Contact.Contact_Contactpersoon'))
    Duration = Column(Float)
    Operating_System = Column(String(255))
    Page_View = Column(String(255), primary_key=True)
    Referrer_Type = Column(String(255))
    Time = Column(String(255))
    Page_Title = Column(String(255))
    Type = Column(String(255))
    Url = Column(String(255))
    Viewed_On = Column(String(255))
    Visit_Visit = Column(String(255), ForeignKey('CDI_visits.Visit_Visit'))
    Visitor_Key = Column(String(255))
    WebContent_Web_Content = Column(String(255), ForeignKey('CDI_web_content.WebContent_Web_Content'))
    Aangemaakt_op = Column(String(255))
    Gewijzigd_door = Column(String(255))
    Gewijzigd_op = Column(String(255))
    Status = Column(String(255))
    Reden_van_status = Column(String(255))

    Campagne = relationship("Campagne", backref="campagne_from_pageviews")
    CDI_visits = relationship("CDI_visits", backref="cdi_visits_from_pageviews")
    CDI_web_content = relationship("CDI_web_content", backref="cdi_web_content_from_pageviews")

class CDI_sent_email_clicks(Base):
    __tablename__ = 'CDI_sent_email_clicks'
    SentEmail_kliks_Clicks = Column(Integer, primary_key=True)
    Contact_Contactpersoon = Column(String(255), ForeignKey('Contact.Contact_Contactpersoon'))
    SentEmail_kliks_E_mail_versturen = Column(String(255))
    Mailing_Mailing = Column(String(255), ForeignKey('CDI_mailing.Mailing_Mailing'))

    Contact = relationship("Contact", backref="contact_van_sent_email_clicks")
    CDI_mailing = relationship("CDI_mailing", backref="cdi_mailing_from_sent_email_clicks")

class Functie(Base):
    __tablename__ = 'Functie'
    Functie_Functie = Column(String(255), primary_key=True)
    Functie_Naam = Column(String(255))

    Contact_functie = relationship("Contact_functie", backref="contact_functie_from_functie")

class Contact_functie(Base):
    __tablename__ = 'Contact_functie'
    Contact_Contactpersoon = Column(String(255), ForeignKey('Contact.Contact_Contactpersoon'))
    Functie_Functie = Column(String(255), ForeignKey('Functie.Functie_Functie'))
    ContactFunctie_ID = Column(Integer, primary_key=True)

    Contact = relationship("Contact", backref="contact_van_functie")
    Functie = relationship("Functie", backref="contact_functie_from_functie")

class Gebruikers(Base):
    __tablename__ = 'Gebruikers'
    Gebruikers_CRM_User_ID = Column(String(255), primary_key=True)
    Gebruikers_Business_Unit_Naam_ = Column(String(255))

    Info_en_klachten = relationship("Info_en_klachten", backref="info_en_klachten_from_gebruikers")

class Info_en_klachten(Base):
    __tablename__ = 'Info_en_klachten'
    Info_en_Klachten_Aanvraag = Column(String(255), primary_key=True)
    Account_Account = Column(String(255), ForeignKey('Account.Account_Account'))
    Info_en_Klachten_Datum = Column(String(255))
    Info_en_Klachten_Datum_afsluiting = Column(String(255))
    Info_en_Klachten_Status = Column(String(255))
    Gebruikers_CRM_User_ID = Column(String(255), ForeignKey('Gebruikers.Gebruikers_CRM_User_ID'))

    Account = relationship("Account", backref="account_from_info_en_klachten")
    Gebruikers = relationship("Gebruikers", backref="info_en_klachten_from_gebruikers")

class Inschrijving(Base):
    __tablename__ = 'Inschrijving'
    Inschrijving_Aanwezig_Afwezig = Column(String(255))
    Inschrijving_Bron = Column(String(255))
    Contact_Contactpersoon = Column(String(255), ForeignKey('Contact.Contact_Contactpersoon'))
    Inschrijving_Datum_inschrijving = Column(String(255))
    Inschrijving_Inschrijving = Column(String(255), primary_key=True)
    Inschrijving_Facturatie_Bedrag = Column(String(255))

    Contact = relationship("Contact", backref="contact_van_inschrijving")
    Sessie_inschrijving = relationship("Sessie_inschrijving", backref="sessie_inschrijving_from_inschrijving")

class Lidmaatschap(Base):
    __tablename__ = 'Lidmaatschap'
    Lidmaatschap_Datum_Opzeg = Column(String(255))
    Lidmaatschap_Lidmaatschap = Column(String(255), primary_key=True)
    Account_Account = Column(String(255), ForeignKey('Account.Account_Account'))
    Lidmaatschap_Reden_Aangroei = Column(String(255))
    Lidmaatschap_Reden_Verloop = Column(String(255))
    Lidmaatschap_Startdatum = Column(String(255))

    Account = relationship("Account", backref="account_from_lidmaatschap")

class Sessie(Base):
    __tablename__ = 'Sessie'
    Sessie_Activiteitstype = Column(String(255))
    Campagne_Campagne = Column(String(255), ForeignKey('Campagne.Campagne_Campagne'))
    Sessie_Eind_Datum_Tijd = Column(String(255))
    Sessie_Product = Column(String(255))
    Sessie_Sessie = Column(String(255), primary_key=True)
    Sessie_Sessie_nr_ = Column(String(255))
    Sessie_Start_Datum_Tijd = Column(String(255))
    Sessie_Thema_Naam_ = Column(String(255))

    Campagne = relationship("Campagne", backref="campagne_from_sessie")
    Sessie_inschrijving = relationship("Sessie_inschrijving", backref="sessie_from_sessie_inschrijving")

class Sessie_inschrijving(Base):
    __tablename__ = 'Sessie_inschrijving'
    SessieInschrijving_SessieInschrijving = Column(String(255), primary_key=True)
    Sessie_Sessie = Column(String(255), ForeignKey('Sessie.Sessie_Sessie'))
    Inschrijving_Inschrijving = Column(String(255), ForeignKey('Inschrijving.Inschrijving_Inschrijving'))

    Inschrijving = relationship("Inschrijving", backref="sessie_inschrijving_from_inschrijving")
    Sessie = relationship("Sessie", backref="sessie_from_sessie_inschrijving")

class Teams(Base):
    __tablename__ = 'Teams'
    XLS_Teams_Team_code_selecteer_uit_lijst_ = Column(String(255))
    XLS_Teams_Activiteit_boeking_naam_ter_info_ = Column(String(255))
    XLS_Teams_ID = Column(Integer, primary_key=True)
