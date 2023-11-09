from sqlalchemy import Column, Integer, Float, String, ForeignKey, Date
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = sqlalchemy.orm.declarative_base()

class Account_activiteitscode(Base):
    __tablename__ = 'Account_activiteitscode'
    account_activiteitscode_id = Column(Integer, primary_key=True, autoincrement=True)
    account_activiteitscode_account = Column(String(255), ForeignKey('Account.account_account_id'))
    account_activiteitscode_activiteitscode = Column(String(255), ForeignKey('Activiteitscode.activiteitscode_activiteitscode_id'))
    account_activiteitscode_inf_account_inf_activiteitscodeid = Column(String(255))

class Account(Base):
    __tablename__ = 'Account'
    account_account_id = Column(String(255), primary_key=True)
    account_adres_geografische_regio = Column(String(255))
    account_adres_geografische_subregio = Column(String(255))
    account_adres_plaats = Column(String(255))
    account_adres_postcode = Column(String(255))
    account_adres_provincie = Column(String(255))
    account_industriezone_naam_ = Column(String(255))
    account_is_voka_entiteit = Column(Integer)
    account_ondernemingsaard = Column(String(255))
    account_ondernemingstype = Column(String(255))
    account_oprichtingsdatum = Column(Date)
    account_primaire_activiteit = Column(String(255))
    account_reden_van_status = Column(String(255))
    account_status = Column(Integer)
    account_voka_nr_ = Column(Integer)
    account_adres_land = Column(String(255))

class Account_financiële_data(Base):
    __tablename__ = 'Account_financiële_data'
    financieledata_id = Column(Integer, primary_key=True, autoincrement=True)
    financieledata_ondernemingid = Column(String(255), ForeignKey('Account.account_account_id'))
    financieledata_boekjaar = Column(Integer)
    financieledata_aantal_maanden = Column(Float)
    financieledata_toegevoegde_waarde = Column(String(255))
    financieledata_fte = Column(String(255))
    financieledata_gewijzigd_op = Column(String(255))

class Afspraak_alle(Base):
    __tablename__ = 'Afspraak_alle'
    afspraak_alle_afspraak_id = Column(String(255), primary_key=True)

class Persoon(Base):
    __tablename__ = 'Persoon'
    persoon_persoon_id = Column(String(255), primary_key=True)
    persoon_persoonsnr_ = Column(Integer)
    persoon_reden_van_status = Column(String(255))
    persoon_web_login = Column(String(255))
    persoon_mail_regio_antwerpen_waasland = Column(Integer)
    persoon_mail_regio_brussel_hoofdstedelijk_gewest = Column(Integer)
    persoon_mail_regio_limburg = Column(Integer)
    persoon_mail_regio_mechelen_kempen = Column(Integer)
    persoon_mail_regio_oost_vlaanderen = Column(Integer)
    persoon_mail_regio_vlaams_brabant = Column(Integer)
    persoon_mail_regio_voka_nationaal = Column(Integer)
    persoon_mail_regio_west_vlaanderen = Column(Integer)
    persoon_mail_thema_duurzaamheid = Column(Integer)
    persoon_mail_thema_financieel_fiscaal = Column(Integer)
    persoon_mail_thema_innovatie = Column(Integer)
    persoon_mail_thema_internationaal_ondernemen = Column(Integer)
    persoon_mail_thema_mobiliteit = Column(Integer)
    persoon_mail_thema_omgeving = Column(Integer)
    persoon_mail_thema_sales_marketing_communicatie = Column(Integer)
    persoon_mail_thema_strategie_en_algemeen_management = Column(Integer)
    persoon_mail_thema_talent = Column(Integer)
    persoon_mail_thema_welzijn = Column(Integer)
    persoon_mail_type_bevraging = Column(Integer)
    persoon_mail_type_communities_en_projecten = Column(Integer)
    persoon_mail_type_netwerkevenementen = Column(Integer)
    persoon_mail_type_nieuwsbrieven = Column(Integer)
    persoon_mail_type_opleidingen = Column(Integer)
    persoon_mail_type_persberichten_belangrijke_meldingen = Column(Integer)
    persoon_marketingcommunicatie = Column(String(255))

class Contact(Base):
    __tablename__ = 'Contact'
    contact_contactpersoon_id = Column(String(255), primary_key=True)
    contact_account = Column(String(255), ForeignKey('Account.account_account_id'))
    contact_functietitel = Column(String(255))
    contact_persoon_id = Column(String(255), ForeignKey('Persoon.persoon_persoon_id'))
    contact_status = Column(String(255))
    contact_voka_medewerker = Column(Integer)

class Activiteit_vereist_contact(Base):
    __tablename__ = 'Activiteit_vereist_contact'
    activiteitvereistcontact_id = Column(Integer, primary_key=True, autoincrement=True)
    activiteitvereistcontact_activityid_id = Column(String(255), ForeignKey('Afspraak_alle.afspraak_alle_afspraak_id'))
    activiteitvereistcontact_reqattendee = Column(String(255), ForeignKey('Contact.contact_contactpersoon_id'))

class Activiteitscode(Base):
    __tablename__ = 'Activiteitscode'
    activiteitscode_naam = Column(String(255))
    activiteitscode_activiteitscode_id = Column(String(255), primary_key=True)
    activiteitscode_status = Column(String(255))

class Afspraak_betreft_account_cleaned(Base):
    __tablename__ = 'Afspraak_betreft_account_cleaned'
    afspraak_betreft_account_afspraak_id = Column(String(255), ForeignKey('Afspraak_alle.afspraak_alle_afspraak_id'), primary_key=True)
    afspraak_betreft_account_thema = Column(String(255))
    afspraak_betreft_account_subthema = Column(String(255))
    afspraak_betreft_account_onderwerp = Column(String(255))
    afspraak_betreft_account_betreft_id = Column(String(255), ForeignKey('Account.account_account_id'))
    afspraak_betreft_account_eindtijd = Column(Date)
    afspraak_betreft_account_keyphrases = Column(String(2000))

class Afspraak_betreft_contact_cleaned(Base):
    __tablename__ = 'Afspraak_betreft_contact_cleaned'
    afspraak_betreft_contactfiche_afspraak_id = Column(String(255), ForeignKey('Afspraak_alle.afspraak_alle_afspraak_id'), primary_key=True)
    afspraak_betreft_contactfiche_thema = Column(String(255))
    afspraak_betreft_contactfiche_subthema = Column(String(255))
    afspraak_betreft_contactfiche_onderwerp = Column(String(255))
    afspraak_betreft_contactfiche_betreft_id = Column(String(255), ForeignKey('Contact.contact_contactpersoon_id'))
    afspraak_betreft_contactfiche_eindtijd = Column(Date)
    afspraak_betreft_contactfiche_keyphrases = Column(String(2000))

class Afspraak_account_gelinkt_cleaned(Base):
    __tablename__ = 'Afspraak_account_gelinkt_cleaned'
    afspraak_account_gelinkt_afspraak_id = Column(String(255), ForeignKey('Afspraak_alle.afspraak_alle_afspraak_id'), primary_key=True)
    afspraak_account_gelinkt_thema = Column(String(255))
    afspraak_account_gelinkt_subthema = Column(String(255))
    afspraak_account_gelinkt_onderwerp = Column(String(255))
    afspraak_account_gelinkt_eindtijd = Column(Date)
    afspraak_account_gelinkt_account = Column(String(255), ForeignKey('Account.account_account_id'))
    afspraak_account_gelinkt_keyphrases = Column(String(2000))

class Campagne(Base):
    __tablename__ = 'Campagne'
    campagne_campagne_id = Column(String(255), primary_key=True)
    campagne_campagne_nr = Column(String(255))
    campagne_einddatum = Column(Date)
    campagne_naam = Column(String(255))
    campagne_naam_in_email = Column(String(255))
    campagne_reden_van_status = Column(String(255))
    campagne_startdatum = Column(Date)
    campagne_status = Column(String(255))
    campagne_type_campagne = Column(String(255))
    campagne_url_voka_be = Column(String(255))
    campagne_soort_campagne = Column(String(255))

class Cdi_mailing(Base):
    __tablename__ = 'Cdi_mailing'
    mailing_mailing_id = Column(String(255), primary_key=True)
    mailing_name = Column(String(255))
    mailing_sent_on = Column(String(255))
    mailing_onderwerp = Column(String(255))

class Cdi_pageviews(Base):
    __tablename__ = 'Cdi_pageviews'
    page_view_id = Column(String(255), primary_key=True)
    browser = Column(String(255))
    campaign = Column(String(255), ForeignKey('Campagne.campagne_campagne_id'))
    contact = Column(String(255), ForeignKey('Contact.contact_contactpersoon_id'))
    duration = Column(Float)
    operating_system = Column(String(255))
    referrer_type = Column(String(255))
    time = Column(Date)
    page_title = Column(String(255))
    type = Column(String(255))
    url = Column(String(2000))
    viewed_on = Column(Date)
    visit = Column(String(255), ForeignKey('Cdi_visits.visit_visit_id'))
    web_content = Column(String(255)) # , ForeignKey('Cdi_web_content.webcontent_web_content_id')
    aangemaakt_op = Column(Date)
    gewijzigd_door = Column(String(255))
    gewijzigd_op = Column(Date)
    status = Column(String(255))
    redenvanstatus = Column(String(255))

class Cdi_sent_email_clicks(Base):
    __tablename__ = 'Cdi_sent_email_clicks'
    sentemail_kliks_clicks = Column(Integer)
    sentemail_kliks_contact = Column(String(255), ForeignKey('Contact.contact_contactpersoon_id'))
    sentemail_kliks_e_mail_versturen = Column(String(255), ForeignKey('Cdi_mailing.mailing_mailing_id'))
    sentemail_kliks_sent_email_id = Column(String(255), primary_key=True)

class Cdi_visits(Base):
    __tablename__ = 'Cdi_visits'
    visit_adobe_reader = Column(String(255))
    visit_bounce = Column(String(255))
    visit_browser = Column(String(255))
    visit_campaign = Column(String(255), ForeignKey('Campagne.campagne_campagne_id'))
    visit_ip_stad = Column(String(255))
    visit_ip_company = Column(String(255))
    visit_contact = Column(String(255), ForeignKey('Contact.contact_contactpersoon_id'))
    visit_containssocialprofile = Column(String(255))
    visit_ip_land = Column(String(255))
    visit_duration = Column(Float)
    visit_email_send = Column(String(255), ForeignKey('Cdi_mailing.mailing_mailing_id'))
    visit_ended_on = Column(String(255))
    visit_entry_page = Column(String(2000))
    visit_exit_page = Column(String(2000))
    visit_first_visit = Column(String(255))
    visit_ip_address = Column(String(255))
    visit_ip_organization = Column(String(255))
    visit_keywords = Column(String(255))
    visit_ip_latitude = Column(Float)
    visit_ip_longitude = Column(Float)
    visit_operating_system = Column(String(255))
    visit_ip_postcode = Column(String(255))
    visit_referrer = Column(String(2000))
    visit_referring_host = Column(String(255))
    visit_score = Column(Float)
    visit_referrer_type = Column(String(255))
    visit_started_on = Column(String(255))
    visit_ip_status = Column(String(255))
    visit_total_pages = Column(Float)
    visit_visit_id = Column(String(255), primary_key=True)
    visit_aangemaakt_op = Column(String(255))
    visit_gewijzigd_op = Column(String(255))

# class Cdi_web_content(Base):
#     __tablename__ = 'Cdi_web_content'
#     webcontent_campaign = Column(String(255), ForeignKey('Campagne.campagne_campagne_id'))
#     webcontent_name = Column(String(255))
#     webcontent_web_content_id = Column(String(255), primary_key=True)
#     webcontent_gemaakt_door_naam_ = Column(String(255))
#     webcontent_created_on = Column(String(255))
#     webcontent_gewijzigd_door_naam_ = Column(String(255))
#     webcontent_modified_on = Column(String(255))
#     webcontent_owner = Column(String(255))
#     webcontent_owner_name = Column(String(255))
#     webcontent_het_bezitten_van_business_unit = Column(String(255))

class Functie(Base):
    __tablename__ = 'Functie'
    functie_functie_id = Column(String(255), primary_key=True)
    functie_naam = Column(String(255))

class Contact_functie(Base):
    __tablename__ = 'Contact_functie'
    contactfunctie_id = Column(Integer, primary_key=True, autoincrement=True)
    contactfunctie_contactpersoon = Column(String(255), ForeignKey('Contact.contact_contactpersoon_id'))
    contactfunctie_functie = Column(String(255), ForeignKey('Functie.functie_functie_id'))

class Gebruikers(Base):
    __tablename__ = 'Gebruikers'
    gebruikers_crm_user_id_id = Column(String(255), primary_key=True)
    gebruikers_business_unit_naam_ = Column(String(255))

class Info_en_klachten(Base):
    __tablename__ = 'Info_en_klachten'
    info_en_klachten_aanvraag_id = Column(String(255), primary_key=True)
    info_en_klachten_account = Column(String(255), ForeignKey('Account.account_account_id'))
    info_en_klachten_datum = Column(Date)
    info_en_klachten_datum_afsluiting = Column(Date)
    info_en_klachten_status = Column(String(255))
    info_en_klachten_eigenaar = Column(String(255), ForeignKey('Gebruikers.gebruikers_crm_user_id_id'))

class Inschrijving(Base):
    __tablename__ = 'Inschrijving'
    inschrijving_aanwezig_afwezig = Column(String(255))
    inschrijving_bron = Column(String(255))
    inschrijving_contactfiche = Column(String(255), ForeignKey('Contact.contact_contactpersoon_id'))
    inschrijving_datum_inschrijving = Column(Date)
    inschrijving_inschrijving_id = Column(String(255), primary_key=True)
    inschrijving_facturatie_bedrag = Column(String(255))
    inschrijving_campagne = Column(String(255), ForeignKey('Campagne.campagne_campagne_id'))
    inschrijving_campagne_naam_ = Column(String(255))

class Lidmaatschap(Base):
    __tablename__ = 'Lidmaatschap'
    lidmaatschap_datum_opzeg = Column(Date)
    lidmaatschap_lidmaatschap_id = Column(String(255), primary_key=True)
    lidmaatschap_onderneming = Column(String(255), ForeignKey('Account.account_account_id'))
    lidmaatschap_reden_aangroei = Column(String(255))
    lidmaatschap_reden_verloop = Column(String(255))
    lidmaatschap_startdatum = Column(Date)

class Sessie(Base):
    __tablename__ = 'Sessie'
    sessie_activiteitstype = Column(String(255))
    sessie_campagne = Column(String(255), ForeignKey('Campagne.campagne_campagne_id'))
    sessie_eind_datum_tijd = Column(Date)
    sessie_product = Column(String(255))
    sessie_sessie_id = Column(String(255), primary_key=True)
    sessie_sessie_nr_ = Column(String(255))
    sessie_start_datum_tijd = Column(Date)
    sessie_thema_naam_ = Column(String(255))

class Sessie_inschrijving(Base):
    __tablename__ = 'Sessie_inschrijving'
    sessieinschrijving_sessieinschrijving_id = Column(String(255), primary_key=True)
    sessieinschrijving_sessie = Column(String(255), ForeignKey('Sessie.sessie_sessie_id'))
    sessieinschrijving_inschrijving = Column(String(255), ForeignKey('Inschrijving.inschrijving_inschrijving_id'))

class Teams(Base):
    __tablename__ = 'Teams'
    xls_teams_id = Column(Integer, primary_key=True, autoincrement=True)
    xls_teams_team_code_selecteer_uit_lijst_ = Column(String(255))
    xls_teams_activiteit_boeking_naam_ter_info_ = Column(String(255))