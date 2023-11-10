-- CREATE DATABASE Voka_DWH3;
USE Voka_DWH3;


IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'DimDate')
BEGIN
    CREATE TABLE DimDate (
        dateID INT IDENTITY(1,1) PRIMARY KEY,
        fullDate DATE,
        dayOfMonth INT,
        dayOfYear INT,
        dayOfWeek INT,
        dayName VARCHAR(10),
        monthNumber INT,
        monthName VARCHAR(10),
        year INT
    )
END


CREATE TABLE DimVisit (
    visID INT IDENTITY(1,1) PRIMARY KEY,
    visitID VARCHAR(255),
    visit_bounce VARCHAR(255),
    visit_browser VARCHAR(255),
    visit_ip_address VARCHAR(255),
    visit_ip_company VARCHAR(255),
    visit_ip_land VARCHAR(255),
    visit_ip_postcode VARCHAR(255),
    visit_ip_stad VARCHAR(255),
    visit_duration FLOAT,
    visit_first_visit VARCHAR(255),
    visit_entry_page VARCHAR(2000),
    visit_exit_page VARCHAR(2000),
    visit_referrer_type VARCHAR(255),
    visit_started_on VARCHAR(255),
    visit_total_pages FLOAT,
    mailSent VARCHAR(255),
    mailing_onderwerp VARCHAR(255),
    mailSent_clicks INT,
    campaignID VARCHAR(255),
);


CREATE TABLE DimInschrijving (
    inschrijvingID VARCHAR(255) PRIMARY KEY,
    aanwezigAfwezig VARCHAR(255),
    bron VARCHAR(255),
    facturatieBedrag VARCHAR(255),
    inschrijvingsDatum DATE
)



--TODO
--zie vb Afspraak 
-- in pipeling mergen met SessieInschriving
CREATE TABLE DimSessie (
    sesID INT IDENTITY(1,1) PRIMARY KEY,
    sessieID VARCHAR(255),
    sessieNummer VARCHAR(255),
    activiteitstype VARCHAR(255),
    campaignID VARCHAR(255),
    startDatumTijd DATE,    
    eindDatumTijd DATE,
    product VARCHAR(255),
    themaNaam VARCHAR(255), 
    inschrijvingID VARCHAR(255),
    FOREIGN KEY (inschrijvingID) REFERENCES DimInschrijving(inschrijvingID),
)



-- pageviews vallen voorlopig

CREATE TABLE FactCampagne (
    factCampagneID INT IDENTITY(1,1) PRIMARY KEY,
    campagneID VARCHAR(255),
    campagneNummer VARCHAR(255), 
    campagneNaam VARCHAR(255),
    campagneNaamInEmail VARCHAR(255),
    campagneType VARCHAR(255),
    campagneSoort VARCHAR(255), 
    campagneStartdatumID INT, 
    campagneEinddatumID INT,
    campagneStatus INT, 
    campagneURLVoka VARCHAR(255),
    visID INT,
    sesID INT,
    FOREIGN KEY (campagneStartdatumID) REFERENCES DimDate(dateID),
    FOREIGN KEY (campagneEinddatumID) REFERENCES DimDate(dateID),
    FOREIGN KEY (visID) REFERENCES DimVisit(visID),
    FOREIGN KEY (sesID) REFERENCES DimSessie(sesID),
)



CREATE TABLE DimContact (
    contID INT IDENTITY(1,1) PRIMARY KEY,
    contactID VARCHAR(255),
    contactStatus VARCHAR(255),
    isVokaMedewerker INT,
    functietitel VARCHAR(255),
    teamCode VARCHAR(255),
    persoonWeblogin VARCHAR(255),
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
    

CREATE TABLE DimAccount (
    accountID VARCHAR(255) PRIMARY KEY,
    land VARCHAR(255),
    provincie VARCHAR(255),
    plaats VARCHAR(255),
    industriezone VARCHAR(255),
    postcode VARCHAR(255),
    isVokaEntiteit INT, 
    accountStatus INT,
    vokaNummer INT,
    ondernemingsaard VARCHAR(255),
    ondernemingstype VARCHAR(255),
    activiteitID VARCHAR(255),
    activiteitNaam VARCHAR(255),
)



CREATE TABLE DimLidmaatschap (
    lidID INT IDENTITY(1,1) PRIMARY KEY,
    lidmaatschapID VARCHAR(255) NOT NULL,
    redenAangroei VARCHAR(255),
    redenVerloop VARCHAR(255),
    startDatum DATE,
    opzegDatum DATE,
    accountID VARCHAR(255),
    FOREIGN KEY (accountID) REFERENCES DimAccount(accountID),
)


CREATE TABLE DimInfoEnKlachten (
    infoID INT IDENTITY(1,1) PRIMARY KEY,
    aanvraagID VARCHAR(255) NOT NULL ,
    aanvraagDatum DATE,
    datumAfsluiting DATE,
    aanvraagStatus VARCHAR(255),
    accountID VARCHAR(255),
    FOREIGN KEY (accountID) REFERENCES DimAccount(accountID),
)



CREATE TABLE DimFinanciëleDataAccount (
    financialDataID INT PRIMARY KEY,
    boekjaar INT,
    aantalMaanden FLOAT,
    toegevoegdeWaarde VARCHAR(255),
    FTE VARCHAR(255),
    gewijzigdOp DATE,
    accountID VARCHAR(255),
    FOREIGN KEY (accountID) REFERENCES DimAccount(accountID),
    
);






CREATE TABLE FactAfspraak (
    factAfspraakID INT IDENTITY(1,1) PRIMARY KEY,
    afspraakID VARCHAR(255), 
    thema VARCHAR(255),
    subthema VARCHAR(255),
    onderwerp VARCHAR(255),
    keyphrases VARCHAR(255),
    contactID VARCHAR(255),
    accountID VARCHAR(255),
    eindtijdID INT,
    contID INT,
    FOREIGN KEY (eindtijdID) REFERENCES DimDate(dateID),
    FOREIGN KEY (contID) REFERENCES DimContact(contID),
    FOREIGN KEY (accountID) REFERENCES DimAccount(accountID),
)

