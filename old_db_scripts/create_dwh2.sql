-- CREATE DATABASE Voka_DWH2;
USE Voka_DWH2;

-- VERBINDENDE DIMENSION TABLES
--  = DimDate
-- Modify the DimDate table to include a primary key constraint
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


-- = DimAfspraak
CREATE TABLE DimAfspraak (
    afsID INT IDENTITY(1,1) PRIMARY KEY,
    afspraakID VARCHAR(255), 
    thema VARCHAR(255),
    subthema VARCHAR(255),
    onderwerp VARCHAR(255),
    eindtijd DATETIME,
    keyphrases VARCHAR(255),
    contactID VARCHAR(255),
    accountID VARCHAR(255),
    
);



--Dimtables rond eerste facttable => ACCOUNT

--DimFinanciëleDataAccount
CREATE TABLE DimFinanciëleDataAccount (
    financialDataID INT PRIMARY KEY,
    boekjaar INT,
    aantalMaanden FLOAT,
    toegevoegdeWaarde VARCHAR(255),
    FTE VARCHAR(255),
    gewijzigdOp DATE,
    accountID VARCHAR(255),
    
);

--DimLidmaatschap
CREATE TABLE DimLidmaatschap (
    lidID INT IDENTITY(1,1) PRIMARY KEY,
    lidmaatschapID VARCHAR(255) NOT NULL,
    redenAangroei VARCHAR(255),
    redenVerloop VARCHAR(255),
    startDatum DATE,
    opzegDatum DATE,
    accountID VARCHAR(255),
)

--DimInfoEnKlachten
CREATE TABLE DimInfoEnKlachten (
    infoID INT IDENTITY(1,1) PRIMARY KEY,
    aanvraagID VARCHAR(255) NOT NULL ,
    aanvraagDatum DATE,
    datumAfsluiting DATE,
    aanvraagStatus VARCHAR(255),
    accountID VARCHAR(255),
)

CREATE TABLE DimAccount (
    ondernemingID INT IDENTITY(1,1) PRIMARY KEY, 
    accountID VARCHAR(255),
    land VARCHAR(255),
    provincie VARCHAR(255),
    plaats VARCHAR(255),
    industriezone VARCHAR(255),
    postcode VARCHAR(255),
    isVokaEntiteit INT, 
    accountStatus INT,
)


--EERSTE FACT TABLE => ACCOUNT
CREATE TABLE FactAccount (
    factAccountID INT IDENTITY(1,1) PRIMARY KEY,
    financialDataID INT,
    infoID INT,
    lidID INT,
    afsID INT,
    oprichtingsDateID INT,
    ondernemingID INT,
    accountID VARCHAR(255),
    
    FOREIGN KEY (financialDataID) REFERENCES DimFinanciëleDataAccount(financialDataID),
    FOREIGN KEY (infoID) REFERENCES DimInfoEnKlachten(infoID),
    FOREIGN KEY (LidID) REFERENCES DimLidmaatschap(LidID),
    FOREIGN KEY (afsID) REFERENCES DimAfspraak(afsID), -- Corrected reference here
    FOREIGN KEY (oprichtingsDateID) REFERENCES DimDate(dateID),
    FOREIGN KEY (ondernemingID) REFERENCES DimAccount(ondernemingID),
);



--Dimtables rond tweede facttable => CONTACT

--DimInschrijving
CREATE TABLE DimInschrijving (
    insID INT IDENTITY(1,1) PRIMARY KEY,
    inschrijvingID VARCHAR(255),
    aanwezigAfwezig VARCHAR(255),
    bron VARCHAR(255),
    facturatieBedrag VARCHAR(255),
    inschrijvingsDatum DATE,
    contactID VARCHAR(255), 
    campagneID VARCHAR(255),

)


-- DimCampagne
CREATE TABLE DimCampagne (
    campagneID VARCHAR(255) PRIMARY KEY,
    campagneNummer VARCHAR(255), 
    campagneNaam VARCHAR(255),
    campagneNaamInEmail VARCHAR(255),
    campagneType VARCHAR(255),
    campagneSoort VARCHAR(255), 
    campagneStartdatum DATE, 
    campagneEinddatum DATE,
    campagneStatus INT, 
    campagneURLVoka VARCHAR(255),
    
);


--DimVisit= merge van visit, mailings, clicks, pageviews
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
    pageview_browser VARCHAR(255),
    pageview_operating_system VARCHAR(255),
    pageview_web_content VARCHAR(255),
    pageview_duration FLOAT,
    contactID VARCHAR(255),
    campaignID VARCHAR(255),
    FOREIGN KEY (campaignID) REFERENCES DimCampagne(campagneID),
);

    


CREATE TABLE DimContact (
    contID INT IDENTITY(1,1) PRIMARY KEY,
    contactID VARCHAR(255),
    contactStatus VARCHAR(255),
    isVokaMedewerker INT,
    functietitel VARCHAR(255),
    teamCode VARCHAR(255),
    persoonWeblogin VARCHAR(255),
    --mailRegio VARCHAR(255), -- uit persoon, how?
    --mailThema VARCHAR(255), -- uit persoon, how?
    --mailType VARCHAR(255), -- uit persoon, how?

)



-- TWEEDE FACT TABLE = Contact
CREATE TABLE FactContact
    (
        factContactID INT IDENTITY(1,1) PRIMARY KEY,
        contID INT,
        insID INT,
        visID INT,
        afsID INT,
        inschrijvingsDatumID INT,
        contactID VARCHAR(255),
        FOREIGN KEY (contID) REFERENCES DimContact(contID),
        FOREIGN KEY (insID) REFERENCES DimInschrijving(insID),
        FOREIGN KEY (visID) REFERENCES DimVisit(visID),
        FOREIGN KEY (afsID) REFERENCES DimAfspraak(afsID),
        FOREIGN KEY (inschrijvingsDatumID) REFERENCES DimDate(dateID),
        
    );


