--CREATE DATABASE Voka;

USE Voka;

IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Account')
BEGIN
    CREATE TABLE Account
    (
        account_account_id VARCHAR(255) NOT NULL PRIMARY KEY,
        account_adres_geografische_regio VARCHAR(255),
        account_adres_geografische_subregio VARCHAR(255),
        account_adres_plaats VARCHAR(255),
        account_adres_postcode VARCHAR(255),
        account_adres_provincie VARCHAR(255),
        account_industriezone_naam_ VARCHAR(255),
        account_is_voka_entiteit INT,
        account_ondernemingsaard VARCHAR(255),
        account_ondernemingstype VARCHAR(255),
        account_oprichtingsdatum VARCHAR(255),
        account_primaire_activiteit VARCHAR(255),
        account_reden_van_status VARCHAR(255),
        account_status INT,
        account_voka_nr_ INT,
        account_adres_land VARCHAR(255)
    );
END

IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Account_financiële_data')
BEGIN
    CREATE TABLE Account_financiële_data
    (
        financieledata_id INT PRIMARY KEY IDENTITY(1,1),
        financieledata_ondernemingid VARCHAR(255),
        financieledata_boekjaar INT,
        financieledata_aantal_maanden FLOAT,
        financieledata_toegevoegde_waarde VARCHAR(255),
        financieledata_fte VARCHAR(255),
        financieledata_gewijzigd_op VARCHAR(255),
        FOREIGN KEY (financieledata_ondernemingid) REFERENCES Account(account_account_id)
    );
END

IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Afspraak_alle')
BEGIN
    CREATE TABLE Afspraak_alle
    (
        afspraak_alle_afspraak_id VARCHAR(255) NOT NULL PRIMARY KEY
    );
END

IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Persoon')
BEGIN
    CREATE TABLE Persoon
    (
        persoon_persoon_id VARCHAR(255) NOT NULL PRIMARY KEY,
        persoon_persoonsnr_ INT,
        persoon_reden_van_status VARCHAR(255),
        persoon_web_login VARCHAR(255),
        persoon_mail_regio_antwerpen_waasland INT,
        persoon_mail_regio_brussel_hoofdstedelijk_gewest INT,
        persoon_mail_regio_limburg INT,
        persoon_mail_regio_mechelen_kempen INT,
        persoon_mail_regio_oost_vlaanderen INT,
        persoon_mail_regio_vlaams_brabant INT,
        persoon_mail_regio_voka_nationaal INT,
        persoon_mail_regio_west_vlaanderen INT,
        persoon_mail_thema_duurzaamheid INT,
        persoon_mail_thema_financieel_fiscaal INT,
        persoon_mail_thema_innovatie INT,
        persoon_mail_thema_internationaal_ondernemen INT,
        persoon_mail_thema_mobiliteit INT,
        persoon_mail_thema_omgeving INT,
        persoon_mail_thema_sales_marketing_communicatie INT,
        persoon_mail_thema_strategie_en_algemeen_management INT,
        persoon_mail_thema_talent INT,
        persoon_mail_thema_welzijn INT,
        persoon_mail_type_bevraging INT,
        persoon_mail_type_communities_en_projecten INT,
        persoon_mail_type_netwerkevenementen INT,
        persoon_mail_type_nieuwsbrieven INT,
        persoon_mail_type_opleidingen INT,
        persoon_mail_type_persberichten_belangrijke_meldingen INT,
        persoon_marketingcommunicatie VARCHAR(255)
    );
END

IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Contact')
BEGIN
    CREATE TABLE Contact
    (
        contact_contactpersoon_id VARCHAR(255) NOT NULL PRIMARY KEY,
        contact_account VARCHAR(255),
        contact_functietitel VARCHAR(255),
        contact_persoon_id VARCHAR(255),
        contact_status VARCHAR(255),
        contact_voka_medewerker INT,
        FOREIGN KEY (contact_account) REFERENCES Account(account_account_id)
    );
END

IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Activiteit_vereist_contact')
BEGIN
    CREATE TABLE Activiteit_vereist_contact
    (
        activiteitvereistcontact_id INT PRIMARY KEY IDENTITY(1,1),
        activiteitvereistcontact_activityid_id VARCHAR(255),
        activiteitvereistcontact_reqattendee VARCHAR(255),
        FOREIGN KEY (activiteitvereistcontact_activityid_id) REFERENCES Afspraak_alle(afspraak_alle_afspraak_id),
        FOREIGN KEY (activiteitvereistcontact_reqattendee) REFERENCES Contact(contact_contactpersoon_id)
    );
END

IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Activiteitscode')
BEGIN
    CREATE TABLE Activiteitscode
    (
        activiteitscode_naam VARCHAR(255),
        activiteitscode_activiteitscode_id VARCHAR(255) NOT NULL PRIMARY KEY,
        activiteitscode_status VARCHAR(255)
    );
END

IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Account_activiteitscode')
BEGIN
    CREATE TABLE Account_activiteitscode
    (
        account_activiteitscode_id INT PRIMARY KEY IDENTITY(1,1),
        account_activiteitscode_account VARCHAR(255),
        account_activiteitscode_activiteitscode VARCHAR(255),
        account_activiteitscode_inf_account_inf_activiteitscodeid VARCHAR(255),
        FOREIGN KEY (account_activiteitscode_account) REFERENCES Account(account_account_id),
        FOREIGN KEY (account_activiteitscode_activiteitscode) REFERENCES Activiteitscode(activiteitscode_activiteitscode_id)
    );
END

IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Afspraak_betreft_account_cleaned')
BEGIN
    CREATE TABLE Afspraak_betreft_account_cleaned
    (
        afspraak_betreft_account_afspraak_id VARCHAR(255) NOT NULL PRIMARY KEY,
        afspraak_betreft_account_thema VARCHAR(255),
        afspraak_betreft_account_subthema VARCHAR(255),
        afspraak_betreft_account_onderwerp VARCHAR(255),
        afspraak_betreft_account_betreft_id VARCHAR(255),
        afspraak_betreft_account_eindtijd VARCHAR(255),
        afspraak_betreft_account_keyphrases VARCHAR(2000),
        FOREIGN KEY (afspraak_betreft_account_afspraak_id) REFERENCES Afspraak_alle(afspraak_alle_afspraak_id),
        FOREIGN KEY (afspraak_betreft_account_betreft_id) REFERENCES Account(account_account_id)
    );
END

IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Afspraak_betreft_contact_cleaned')
BEGIN
    CREATE TABLE Afspraak_betreft_contact_cleaned
    (
        afspraak_betreft_contactfiche_afspraak_id VARCHAR(255) NOT NULL PRIMARY KEY,
        afspraak_betreft_contactfiche_thema VARCHAR(255),
        afspraak_betreft_contactfiche_subthema VARCHAR(255),
        afspraak_betreft_contactfiche_onderwerp VARCHAR(255),
        afspraak_betreft_contactfiche_betreft_id VARCHAR(255),
        afspraak_betreft_contactfiche_eindtijd VARCHAR(255),
        afspraak_betreft_contactfiche_keyphrases VARCHAR(2000),
        FOREIGN KEY (afspraak_betreft_contactfiche_afspraak_id) REFERENCES Afspraak_alle(afspraak_alle_afspraak_id),
        FOREIGN KEY (afspraak_betreft_contactfiche_betreft_id) REFERENCES Contact(contact_contactpersoon_id)
    );
END

IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Afspraak_account_gelinkt_cleaned')
BEGIN
    CREATE TABLE Afspraak_account_gelinkt_cleaned
    (
        afspraak_account_gelinkt_afspraak_id VARCHAR(255) NOT NULL PRIMARY KEY,
        afspraak_account_gelinkt_thema VARCHAR(255),
        afspraak_account_gelinkt_subthema VARCHAR(255),
        afspraak_account_gelinkt_onderwerp VARCHAR(255),
        afspraak_account_gelinkt_eindtijd VARCHAR(255),
        afspraak_account_gelinkt_account VARCHAR(255),
        afspraak_account_gelinkt_keyphrases VARCHAR(2000),
        FOREIGN KEY (afspraak_account_gelinkt_account) REFERENCES Account(account_account_id),
        FOREIGN KEY (afspraak_account_gelinkt_afspraak_id) REFERENCES Afspraak_alle(afspraak_alle_afspraak_id)
    );
END

IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Campagne')
BEGIN
    CREATE TABLE Campagne
    (
        campagne_campagne_id VARCHAR(255) NOT NULL PRIMARY KEY,
        campagne_campagne_nr VARCHAR(255),
        campagne_einddatum VARCHAR(255),
        campagne_naam VARCHAR(255),
        campagne_naam_in_email VARCHAR(255),
        campagne_reden_van_status VARCHAR(255),
        campagne_startdatum VARCHAR(255),
        campagne_status VARCHAR(255),
        campagne_type_campagne VARCHAR(255),
        campagne_url_voka_be VARCHAR(255),
        campagne_soort_campagne VARCHAR(255)
    );
END

IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Cdi_mailing')
BEGIN
    CREATE TABLE Cdi_mailing
    (
        mailing_mailing_id VARCHAR(255) NOT NULL PRIMARY KEY,
        mailing_name VARCHAR(255),
        mailing_sent_on VARCHAR(255),
        mailing_onderwerp VARCHAR(255)
    );
END

IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Cdi_sent_email_clicks')
BEGIN
    CREATE TABLE Cdi_sent_email_clicks
    (
        sentemail_kliks_clicks INT,
        sentemail_kliks_contact VARCHAR(255),
        sentemail_kliks_e_mail_versturen VARCHAR(255),
        sentemail_kliks_sent_email_id VARCHAR(255) NOT NULL PRIMARY KEY,
        FOREIGN KEY (sentemail_kliks_contact) REFERENCES Contact(contact_contactpersoon_id),
        FOREIGN KEY (sentemail_kliks_e_mail_versturen) REFERENCES Cdi_mailing(mailing_mailing_id)
    );
END

IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Cdi_visits')
BEGIN
    CREATE TABLE Cdi_visits
    (
        visit_adobe_reader VARCHAR(255),
        visit_bounce VARCHAR(255),
        visit_browser VARCHAR(255),
        visit_campaign VARCHAR(255),
        visit_ip_stad VARCHAR(255),
        visit_ip_company VARCHAR(255),
        visit_contact VARCHAR(255),
        visit_contact_naam_ VARCHAR(255),
        visit_containssocialprofile VARCHAR(255),
        visit_ip_land VARCHAR(255),
        visit_duration FLOAT,
        visit_email_send VARCHAR(255),
        visit_ended_on VARCHAR(255),
        visit_entry_page VARCHAR(2000),
        visit_exit_page VARCHAR(2000),
        visit_first_visit VARCHAR(255),
        visit_ip_address VARCHAR(255),
        visit_ip_organization VARCHAR(255),
        visit_keywords VARCHAR(255),
        visit_ip_latitude FLOAT,
        visit_ip_longitude FLOAT,
        visit_operating_system VARCHAR(255),
        visit_ip_postcode VARCHAR(255),
        visit_referrer VARCHAR(2000),
        visit_referring_host VARCHAR(255),
        visit_score FLOAT,
        visit_referrer_type VARCHAR(255),
        visit_started_on VARCHAR(255),
        visit_ip_status VARCHAR(255),
        visit_time VARCHAR(255),
        visit_total_pages FLOAT,
        visit_visit_id VARCHAR(255) NOT NULL PRIMARY KEY,
        visit_aangemaakt_op VARCHAR(255),
        visit_gewijzigd_op VARCHAR(255),
        FOREIGN KEY (visit_contact) REFERENCES Contact(contact_contactpersoon_id),
        FOREIGN KEY (visit_campaign) REFERENCES Campagne(campagne_campagne_id),
        FOREIGN KEY (visit_email_send) REFERENCES Cdi_mailing(mailing_mailing_id)
    );
END


IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Cdi_pageviews')
BEGIN
    CREATE TABLE Cdi_pageviews
    (
        browser VARCHAR(255),
        campaign VARCHAR(255),
        contact VARCHAR(255),
        duration FLOAT,
        operatingsystem VARCHAR(255),
        pageview_id VARCHAR(255) NOT NULL PRIMARY KEY,
        referrertype VARCHAR(255),
        time VARCHAR(255),
        pagetitle VARCHAR(255),
        type VARCHAR(255),
        url VARCHAR(2000),
        viewedon VARCHAR(255),
        visit VARCHAR(255),
        visitorkey VARCHAR(255),
        webcontent VARCHAR(255),
        aangemaaktop VARCHAR(255),
        gewijzigddoor VARCHAR(255),
        gewijzigdop VARCHAR(255),
        status VARCHAR(255),
        redenvanstatus VARCHAR(255),
        FOREIGN KEY (campaign) REFERENCES Campagne(campagne_campagne_id),
        FOREIGN KEY (contact) REFERENCES Contact(contact_contactpersoon_id),
        -- FOREIGN KEY (webcontent) REFERENCES Cdi_web_content(webcontent_web_content_id),
        FOREIGN KEY (visit) REFERENCES Cdi_visits(visit_visit_id)
    );
END

IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Functie')
BEGIN
    CREATE TABLE Functie
    (
        functie_functie_id VARCHAR(255) NOT NULL PRIMARY KEY,
        functie_naam VARCHAR(255)
    );
END

IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Contact_functie')
BEGIN
    CREATE TABLE Contact_functie
    (
        contactfunctie_id INT PRIMARY KEY IDENTITY(1,1),
        contactfunctie_contactpersoon VARCHAR(255),
        contactfunctie_functie VARCHAR(255),
        FOREIGN KEY (contactfunctie_contactpersoon) REFERENCES Contact(contact_contactpersoon_id),
        FOREIGN KEY (contactfunctie_functie) REFERENCES Functie(functie_functie_id)
    );
END

IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Gebruikers')
BEGIN
    CREATE TABLE Gebruikers
    (
        gebruikers_crm_user_id_id VARCHAR(255) NOT NULL PRIMARY KEY,
        gebruikers_business_unit_naam_ VARCHAR(255)
    );
END

IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Info_en_klachten')
BEGIN
    CREATE TABLE Info_en_klachten
    (
        info_en_klachten_aanvraag_id VARCHAR(255) NOT NULL PRIMARY KEY,
        info_en_klachten_account VARCHAR(255),
        info_en_klachten_datum VARCHAR(255),
        info_en_klachten_datum_afsluiting VARCHAR(255),
        info_en_klachten_status VARCHAR(255),
        info_en_klachten_eigenaar VARCHAR(255),
        FOREIGN KEY (info_en_klachten_account) REFERENCES Account(account_account_id),
        FOREIGN KEY (info_en_klachten_eigenaar) REFERENCES Gebruikers(gebruikers_crm_user_id_id)
    );
END

IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Inschrijving')
BEGIN
    CREATE TABLE Inschrijving
    (
        inschrijving_aanwezig_afwezig VARCHAR(255),
        inschrijving_bron VARCHAR(255),
        inschrijving_contactfiche VARCHAR(255),
        inschrijving_datum_inschrijving VARCHAR(255),
        inschrijving_inschrijving_id VARCHAR(255) NOT NULL PRIMARY KEY,
        inschrijving_facturatie_bedrag VARCHAR(255),
        inschrijving_campagne VARCHAR(255),
        inschrijving_campagne_naam_ VARCHAR(255),
        FOREIGN KEY (inschrijving_contactfiche) REFERENCES Contact(contact_contactpersoon_id),
        FOREIGN KEY (inschrijving_campagne) REFERENCES Campagne(campagne_campagne_id)
    );
END

-- LET OP: CSV File heet Lidmaatschap maar in het ERD heet deze table Account helpdeskvragen
IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Lidmaatschap')
BEGIN
    CREATE TABLE Lidmaatschap
    (
        lidmaatschap_datum_opzeg VARCHAR(255),
        lidmaatschap_lidmaatschap_id VARCHAR(255) NOT NULL PRIMARY KEY,
        lidmaatschap_onderneming VARCHAR(255),
        lidmaatschap_reden_aangroei VARCHAR(255),
        lidmaatschap_reden_verloop VARCHAR(255),
        lidmaatschap_startdatum VARCHAR(255),
        FOREIGN KEY (lidmaatschap_onderneming) REFERENCES Account(account_account_id)
    );
END

IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Sessie')
BEGIN
    CREATE TABLE Sessie
    (
        sessie_activiteitstype VARCHAR(255),
        sessie_campagne VARCHAR(255),
        sessie_eind_datum_tijd VARCHAR(255),
        sessie_product VARCHAR(255),
        sessie_sessie_id VARCHAR(255) NOT NULL PRIMARY KEY,
        sessie_sessie_nr_ VARCHAR(255),
        sessie_start_datum_tijd VARCHAR(255),
        sessie_thema_naam_ VARCHAR(255),
        FOREIGN KEY (sessie_campagne) REFERENCES Campagne(campagne_campagne_id)
    );
END

IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Sessie_inschrijving')
BEGIN
    CREATE TABLE Sessie_inschrijving
    (
        sessieinschrijving_sessieinschrijving_id VARCHAR(255) NOT NULL PRIMARY KEY,
        sessieinschrijving_sessie VARCHAR(255),
        sessieinschrijving_inschrijving VARCHAR(255),
        FOREIGN KEY (sessieinschrijving_inschrijving) REFERENCES Inschrijving(inschrijving_inschrijving_id),
        FOREIGN KEY (sessieinschrijving_sessie) REFERENCES Sessie(sessie_sessie_id)
    );
END

IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Teams')
BEGIN
    CREATE TABLE Teams
    (
        xls_teams_id INT PRIMARY KEY IDENTITY(1,1),
        xls_teams_team_code_selecteer_uit_lijst_ VARCHAR(255),
        xls_teams_activiteit_boeking_naam_ter_info_ VARCHAR(255)
    );
END