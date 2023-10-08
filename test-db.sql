CREATE DATABASE Voka;

use Voka;

--Account activiteitscode_fixed.csv
IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Account_activiteitscode')
BEGIN
    CREATE TABLE Account_activiteitscode
    (
        Account_ActiviteitsCode_Account VARCHAR(255),
        Account_ActiviteitsCode_Activiteitscode VARCHAR(255),
        Account_ActiviteitsCode_inf_account_inf_activiteitscodeId VARCHAR(255)
    );
END

--Account_fixed.csv
IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Account')
BEGIN
    CREATE TABLE Account
    (
        Account_Account VARCHAR(255) PRIMARY KEY,
        Account_Adres_Geografische_regio VARCHAR(255),
        Account_Adres_Geografische_subregio VARCHAR(255),
        Account_Adres_Plaats VARCHAR(255),
        Account_Adres_Postcode VARCHAR(255),
        Account_Adres_Provincie VARCHAR(255),
        Account_Industriezone_Naam_ VARCHAR(255),
        Account_Is_Voka_entiteit INT,
        Account_Ondernemingsaard VARCHAR(255),
        Account_Ondernemingstype VARCHAR(255),
        Account_Oprichtingsdatum VARCHAR(255),
        Account_Primaire_activiteit VARCHAR(255),
        Account_Reden_van_status VARCHAR(255),
        Account_Status INT,
        Account_Voka_Nr_ INT,
        Account_Adres_Land VARCHAR(255)
    );
END

--Account financiële data_fixed.csv
IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Account_financiële_data')
BEGIN
    CREATE TABLE Account_financiële_data
    (
        FinancieleData_OndernemingID VARCHAR(255),
        FinancieleData_Boekjaar INT,
        FinancieleData_Aantal_maanden FLOAT,
        FinancieleData_Toegevoegde_waarde VARCHAR(255),
        FinancieleData_FTE VARCHAR(255),
        FinancieleData_Gewijzigd_op VARCHAR(255)
        FOREIGN KEY (FinancieleData_OndernemingID) REFERENCES Account(Account_Account)
    );
END

--Afspraak alle_fixed.csv
IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Afspraak_alle')
BEGIN
    CREATE TABLE Afspraak_alle
    (
        Afspraak_ALLE_Afspraak VARCHAR(255) PRIMARY KEY,
    );
END

--Persoon_fixed.csv
IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Persoon')
BEGIN
    CREATE TABLE Persoon
    (
        Persoon_persoon VARCHAR(255) PRIMARY KEY,
        Persoon_Persoonsnr_ INT,
        Persoon_Reden_van_status VARCHAR(255),
        Persoon_Web_Login VARCHAR(255),
        Persoon_Mail_regio_Antwerpen_Waasland INT,
        Persoon_Mail_regio_Brussel_Hoofdstedelijk_Gewest INT,
        Persoon_Mail_regio_Limburg INT,
        Persoon_Mail_regio_Mechelen_Kempen INT,
        Persoon_Mail_regio_Oost_Vlaanderen INT,
        Persoon_Mail_regio_Vlaams_Brabant INT,
        Persoon_Mail_regio_Voka_nationaal INT,
        Persoon_Mail_regio_West_Vlaanderen INT,
        Persoon_Mail_thema_duurzaamheid INT,
        Persoon_Mail_thema_financieel_fiscaal INT,
        Persoon_Mail_thema_innovatie INT,
        Persoon_Mail_thema_internationaal_ondernemen INT,
        Persoon_Mail_thema_mobiliteit INT,
        Persoon_Mail_thema_omgeving INT,
        Persoon_Mail_thema_sales_marketing_communicatie INT,
        Persoon_Mail_thema_strategie_en_algemeen_management INT,
        Persoon_Mail_thema_talent INT,
        Persoon_Mail_thema_welzijn INT,
        Persoon_Mail_type_Bevraging INT,
        Persoon_Mail_type_communities_en_projecten INT,
        Persoon_Mail_type_netwerkevenementen INT,
        Persoon_Mail_type_nieuwsbrieven INT,
        Persoon_Mail_type_opleidingen INT,
        Persoon_Mail_type_persberichten_belangrijke_meldingen INT,
        Persoon_Marketingcommunicatie VARCHAR(255)
    );
END

--Contact_fixed.csv
IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Contact')
BEGIN
    CREATE TABLE Contact
    (
        Contact_Contactpersoon VARCHAR(255) PRIMARY KEY,
        Contact_Account VARCHAR(255),
        Contact_Functietitel VARCHAR(255),
        Contact_Persoon_ID VARCHAR(255),
        Contact_Status VARCHAR(255),
        Contact_Voka_medewerker INT
        FOREIGN KEY (Contact_Account) REFERENCES Account(Account_Account),
        FOREIGN KEY (Contact_Persoon_ID) REFERENCES Persoon(Persoon_persoon)
    );
END


--Activiteit vereist contact_fixed.csv
IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Activiteit_vereist_contact')
BEGIN
    CREATE TABLE Activiteit_vereist_contact
    (
        ActiviteitVereistContact_ActivityId VARCHAR(255),
        ActiviteitVereistContact_ReqAttendee VARCHAR(255)
        FOREIGN KEY (ActiviteitVereistContact_ActivityId) REFERENCES Afspraak_alle(Afspraak_ALLE_Afspraak),
        FOREIGN KEY (ActiviteitVereistContact_ReqAttendee) REFERENCES Contact(Contact_Contactpersoon)
    );
END

--Activiteitscode_fixed.csv
IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Activiteitscode')
BEGIN
    CREATE TABLE Activiteitscode
    (
        ActiviteitsCode_Naam VARCHAR(255),
        ActiviteitsCode_Activiteitscode VARCHAR(255) PRIMARY KEY,
        ActiviteitsCode_Status VARCHAR(255)
    );
END

--Afspraak betreft account_cleaned_fixed.csv
IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Afspraak_betreft_account_cleaned')
BEGIN
    CREATE TABLE Afspraak_betreft_account_cleaned
    (
        Afspraak_BETREFT_ACCOUNT_Afspraak VARCHAR(255),
        Afspraak_BETREFT_ACCOUNT_Thema VARCHAR(255),
        Afspraak_BETREFT_ACCOUNT_Subthema VARCHAR(255),
        Afspraak_BETREFT_ACCOUNT_Onderwerp VARCHAR(255),
        Afspraak_BETREFT_ACCOUNT_Betreft_id VARCHAR(255),
        Afspraak_BETREFT_ACCOUNT_Eindtijd VARCHAR(255),
        Afspraak_BETREFT_ACCOUNT_KeyPhrases VARCHAR(255)
        FOREIGN KEY (Afspraak_BETREFT_ACCOUNT_Afspraak) REFERENCES Afspraak_alle(Afspraak_ALLE_Afspraak),
        FOREIGN KEY (Afspraak_BETREFT_ACCOUNT_Betreft_id) REFERENCES Account(Account_Account)
    );
END

--Afspraak betreft contact_cleaned_fixed.csv
IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Afspraak_betreft_contact_cleaned')
BEGIN
    CREATE TABLE Afspraak_betreft_contact_cleaned
    (
        Afspraak_BETREFT_CONTACTFICHE_Afspraak VARCHAR(255),
        Afspraak_BETREFT_CONTACTFICHE_Thema VARCHAR(255),
        Afspraak_BETREFT_CONTACTFICHE_Subthema VARCHAR(255),
        Afspraak_BETREFT_CONTACTFICHE_Onderwerp VARCHAR(255),
        Afspraak_BETREFT_CONTACTFICHE_Betreft_id VARCHAR(255),
        Afspraak_BETREFT_CONTACTFICHE_Eindtijd VARCHAR(255),
        Afspraak_BETREFT_CONTACTFICHE_KeyPhrases VARCHAR(255)
        FOREIGN KEY (Afspraak_BETREFT_CONTACTFICHE_Afspraak) REFERENCES Afspraak_alle(Afspraak_ALLE_Afspraak),
        FOREIGN KEY (Afspraak_BETREFT_CONTACTFICHE_Betreft_id) REFERENCES Contact(Contact_Contactpersoon)
    );
END

--Afspraak_account_gelinkt_cleaned_fixed.csv
IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Afspraak_account_gelinkt_cleaned')
BEGIN
    CREATE TABLE Afspraak_account_gelinkt_cleaned
    (
        Afspraak_ACCOUNT_GELINKT_Afspraak VARCHAR(255),
        Afspraak_ACCOUNT_GELINKT_Thema VARCHAR(255),
        Afspraak_ACCOUNT_GELINKT_Subthema VARCHAR(255),
        Afspraak_ACCOUNT_GELINKT_Onderwerp VARCHAR(255),
        Afspraak_ACCOUNT_GELINKT_Eindtijd VARCHAR(255),
        Afspraak_ACCOUNT_GELINKT_Account VARCHAR(255),
        Afspraak_ACCOUNT_GELINKT_KeyPhrases VARCHAR(255)
        FOREIGN KEY (Afspraak_ACCOUNT_GELINKT_Afspraak) REFERENCES Afspraak_alle(Afspraak_ALLE_Afspraak),
        FOREIGN KEY (Afspraak_ACCOUNT_GELINKT_Account) REFERENCES Account(Account_Account)
    );
END

--Campagne_fixed.csv
IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Campagne')
BEGIN
    CREATE TABLE Campagne
    (
        Campagne_Campagne VARCHAR(255) PRIMARY KEY,
        Campagne_Campagne_Nr VARCHAR(255),
        Campagne_Einddatum VARCHAR(255),
        Campagne_Naam VARCHAR(255),
        Campagne_Naam_in_email VARCHAR(255),
        Campagne_Reden_van_status VARCHAR(255),
        Campagne_Startdatum VARCHAR(255),
        Campagne_Status VARCHAR(255),
        Campagne_Type_campagne VARCHAR(255),
        Campagne_URL_voka_be VARCHAR(255),
        Campagne_Soort_Campagne VARCHAR(255)
    );
END

--CDI mailing_fixed.csv
IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'CDI_mailing')
BEGIN
    CREATE TABLE CDI_mailing
    (
        CDI_Mailing_Mailing VARCHAR(255) PRIMARY KEY,
        CDI_Mailing_Name VARCHAR(255),
        CDI_Mailing_Sent_On VARCHAR(255),
        CDI_Mailing_Onderwerp VARCHAR(255)
    );
END

--CDI visits_fixed.csv
IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'CDI_visits')
BEGIN
    CREATE TABLE CDI_visits
    (
        CDI_Visit_Adobe_Reader INT,
        CDI_Visit_Bounce INT,
        CDI_Visit_Browser VARCHAR(255),
        CDI_Visit_Campaign VARCHAR(255),
        CDI_Visit_IP_Stad VARCHAR(255),
        CDI_Visit_IP_Company VARCHAR(255),
        CDI_Visit_Contact VARCHAR(255),
        CDI_Visit_Contact_Naam_ VARCHAR(255),
        CDI_Visit_containssocialprofile INT,
        CDI_Visit_IP_Land VARCHAR(255),
        CDI_Visit_Duration FLOAT,
        CDI_Visit_Email_Send VARCHAR(255),
        CDI_Visit_Ended_On VARCHAR(255),
        CDI_Visit_Entry_Page VARCHAR(255),
        CDI_Visit_Exit_Page VARCHAR(255),
        CDI_Visit_First_Visit VARCHAR(255),
        CDI_Visit_IP_Address VARCHAR(255),
        CDI_Visit_IP_Organization VARCHAR(255),
        CDI_Visit_Keywords VARCHAR(255),
        CDI_Visit_IP_Latitude FLOAT,
        CDI_Visit_IP_Longitude FLOAT,
        CDI_Visit_Operating_System VARCHAR(255),
        CDI_Visit_IP_Postcode VARCHAR(255),
        CDI_Visit_Referrer VARCHAR(255),
        CDI_Visit_Referring_Host VARCHAR(255),
        CDI_Visit_Score FLOAT,
        CDI_Visit_Referrer_Type VARCHAR(255),
        CDI_Visit_Started_On VARCHAR(255),
        CDI_Visit_IP_Status VARCHAR(255),
        CDI_Visit_Time VARCHAR(255),
        CDI_Visit_Total_Pages FLOAT,
        CDI_Visit_Visit VARCHAR(255) PRIMARY KEY,
        CDI_Visit_Aangemaakt_op VARCHAR(255),
        CDI_Visit_Gewijzigd_op VARCHAR(255)
        FOREIGN KEY (CDI_Visit_Campaign) REFERENCES Campagne(Campagne_Campagne),
        FOREIGN KEY (CDI_Visit_Contact) REFERENCES Contact(Contact_Contactpersoon),
        FOREIGN KEY (CDI_Visit_Email_Send) REFERENCES CDI_mailing(CDI_Mailing_Mailing)
        --FOREIGN KEY (CDI_Visit_Entry_Page) REFERENCES CDI_web_content(CDI_WebContent_Web_Content)
        --FOREIGN KEY (CDI_Visit_Exit_Page) REFERENCES CDI_web_content(CDI_WebContent_Web_Content)
    );
END

--CDI web content_fixed.csv
IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'CDI_web_content')
BEGIN
    CREATE TABLE CDI_web_content
    (
        CDI_WebContent_Campaign VARCHAR(255),
        CDI_WebContent_Campaign_Name VARCHAR(255),
        CDI_WebContent_Name VARCHAR(255),
        CDI_WebContent_Web_Content VARCHAR(255) PRIMARY KEY,
        CDI_WebContent_Gemaakt_door_Naam_ VARCHAR(255),
        CDI_WebContent_Created_On VARCHAR(255),
        CDI_WebContent_Gewijzigd_door_Naam_ VARCHAR(255),
        CDI_WebContent_Modified_On VARCHAR(255),
        CDI_WebContent_Owner VARCHAR(255),
        CDI_WebContent_Owner_Name VARCHAR(255),
        CDI_WebContent_Het_bezitten_van_Business_Unit VARCHAR(255)
    );
END

--cdi pageviews_fixed.csv
IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'cdi_pageviews')
BEGIN
    CREATE TABLE cdi_pageviews
    (
        Browser VARCHAR(255),
        Campaign VARCHAR(255),
        Contact VARCHAR(255),
        Duration FLOAT,
        Operating_System VARCHAR(255),
        Page_View VARCHAR(255) PRIMARY KEY,
        Referrer_Type VARCHAR(255),
        [Time] VARCHAR(255),
        Page_Title VARCHAR(255),
        [Type] VARCHAR(255),
        [Url] VARCHAR(255),
        Viewed_On VARCHAR(255),
        Visit VARCHAR(255),
        Visitor_Key VARCHAR(255),
        Web_Content VARCHAR(255),
        Aangemaakt_op VARCHAR(255),
        Gewijzigd_door VARCHAR(255),
        Gewijzigd_op VARCHAR(255),
        [Status] VARCHAR(255),
        Reden_van_status VARCHAR(255)
        FOREIGN KEY (Campaign) REFERENCES Campagne(Campagne_Campagne),
        FOREIGN KEY (Contact) REFERENCES Contact(Contact_Contactpersoon),
        FOREIGN KEY (Web_Content) REFERENCES CDI_web_content(CDI_WebContent_Web_Content),
        FOREIGN KEY (Visit) REFERENCES CDI_visits(CDI_Visit_Visit)
    );
END

--CDI sent email clicks_fixed.csv
IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'CDI_sent_email_clicks')
BEGIN
    CREATE TABLE CDI_sent_email_clicks
    (
        CDI_SentEmail_kliks_Clicks INT PRIMARY KEY,
        CDI_SentEmail_kliks_Contact VARCHAR(255),
        CDI_SentEmail_kliks_E_mail_versturen VARCHAR(255),
        CDI_SentEmail_kliks_Sent_Email VARCHAR(255)
        FOREIGN KEY (CDI_SentEmail_kliks_Contact) REFERENCES Contact(Contact_Contactpersoon),
        FOREIGN KEY (CDI_SentEmail_kliks_Sent_Email) REFERENCES CDI_mailing(CDI_Mailing_Mailing)
    );
END

--Functie_fixed.csv
IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Functie')
BEGIN
    CREATE TABLE Functie
    (
        Functie_Functie VARCHAR(255) PRIMARY KEY,
        Functie_Naam VARCHAR(255)
    );
END

--Contact functie_fixed.csv
IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Contact_functie')
BEGIN
    CREATE TABLE Contact_functie
    (
        ContactFunctie_Contactpersoon VARCHAR(255),
        ContactFunctie_Functie VARCHAR(255)
        FOREIGN KEY (ContactFunctie_Contactpersoon) REFERENCES Contact(Contact_Contactpersoon),
        FOREIGN KEY (ContactFunctie_Functie) REFERENCES Functie(Functie_Functie)
    );
END

--Gebruikers_fixed.csv
IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Gebruikers')
BEGIN
    CREATE TABLE Gebruikers
    (
        Gebruikers_CRM_User_ID VARCHAR(255) PRIMARY KEY,
        Gebruikers_Business_Unit_Naam_ VARCHAR(255)
    );
END

--Info en klachten_fixed.csv
IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Info_en_klachten')
BEGIN
    CREATE TABLE Info_en_klachten
    (
        Info_en_Klachten_Aanvraag VARCHAR(255) PRIMARY KEY,
        Info_en_Klachten_Account VARCHAR(255),
        Info_en_Klachten_Datum VARCHAR(255),
        Info_en_Klachten_Datum_afsluiting VARCHAR(255),
        Info_en_Klachten_Status VARCHAR(255),
        Info_en_Klachten_Eigenaar VARCHAR(255)
        FOREIGN KEY (Info_en_Klachten_Account) REFERENCES Account(Account_Account),
        FOREIGN KEY (Info_en_Klachten_Eigenaar) REFERENCES Gebruikers(Gebruikers_CRM_User_ID)
    );
END

--Inschrijving_fixed.csv
IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Inschrijving')
BEGIN
    CREATE TABLE Inschrijving
    (
        Inschrijving_Aanwezig_Afwezig VARCHAR(255),
        Inschrijving_Bron VARCHAR(255),
        Inschrijving_Contactfiche VARCHAR(255),
        Inschrijving_Datum_inschrijving VARCHAR(255),
        Inschrijving_Inschrijving VARCHAR(255) PRIMARY KEY,
        Inschrijving_Facturatie_Bedrag VARCHAR(255)
        FOREIGN KEY (Inschrijving_Contactfiche) REFERENCES Contact(Contact_Contactpersoon)
        -- FOREIGN KEY naar campagne maar heeft geen column campagne
    );
END

--Lidmaatschap_fixed.csv in ERD heet het Account helpdeskvragen
IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Lidmaatschap')
BEGIN
    CREATE TABLE Lidmaatschap
    (
        Lidmaatschap_Datum_Opzeg VARCHAR(255),
        Lidmaatschap_Lidmaatschap VARCHAR(255) PRIMARY KEY,
        Lidmaatschap_Onderneming VARCHAR(255),
        Lidmaatschap_Reden_Aangroei VARCHAR(255),
        Lidmaatschap_Reden_Verloop VARCHAR(255),
        Lidmaatschap_Startdatum VARCHAR(255)
        FOREIGN KEY (Lidmaatschap_Onderneming) REFERENCES Account(Account_Account)
    );
END

--Sessie_fixed.csv
IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Sessie')
BEGIN
    CREATE TABLE Sessie
    (
        Sessie_Activiteitstype VARCHAR(255),
        Sessie_Campagne VARCHAR(255),
        Sessie_Eind_Datum_Tijd VARCHAR(255),
        Sessie_Product VARCHAR(255),
        Sessie_Sessie VARCHAR(255) PRIMARY KEY,
        Sessie_Sessie_nr_ VARCHAR(255),
        Sessie_Start_Datum_Tijd VARCHAR(255),
        Sessie_Thema_Naam_ VARCHAR(255)
        FOREIGN KEY (Sessie_Campagne) REFERENCES Campagne(Campagne_Campagne)
    );
END

--Sessie inschrijving_fixed.csv
IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Sessie_inschrijving')
BEGIN
    CREATE TABLE Sessie_inschrijving
    (
        SessieInschrijving_SessieInschrijving VARCHAR(255) PRIMARY KEY,
        SessieInschrijving_Sessie VARCHAR(255),
        SessieInschrijving_Inschrijving VARCHAR(255)
        FOREIGN KEY (SessieInschrijving_Inschrijving) REFERENCES Inschrijving(Inschrijving_Inschrijving),
        FOREIGN KEY (SessieInschrijving_Sessie) REFERENCES Sessie(Sessie_Sessie)
    );
END

--Teams_fixed.csv
IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Teams')
BEGIN
    CREATE TABLE Teams
    (
        XLS_Teams_Team_code_selecteer_uit_lijst_ VARCHAR(255),
        XLS_Teams_Activiteit_boeking_naam_ter_info_ VARCHAR(255)
    );
END
