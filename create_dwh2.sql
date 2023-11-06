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
    );
    -- Add a unique constraint on the fullDate column
    ALTER TABLE DimDate
    ADD CONSTRAINT UC_DimDate_FullDate UNIQUE (fullDate);
END


-- = DimAfspraak
CREATE TABLE DimAfspraak (
    afspraakID VARCHAR(255) PRIMARY KEY, 
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
    lidmaatschapID VARCHAR(255) PRIMARY KEY NOT NULL,
    redenAangroei VARCHAR(255),
    redenVerloop VARCHAR(255),
    startDatum DATE,
    opzegDatum DATE,
    accountID VARCHAR(255),
)

--DimInfoEnKlachten
CREATE TABLE DimInfoEnKlachten (
    aanvraagID VARCHAR(255) PRIMARY KEY NOT NULL ,
    aanvraagDatum DATE,
    datumAfsluiting DATE,
    aanvraagStatus VARCHAR(255),
    accountID VARCHAR(255),
)


--EERSTE FACT TABLE => ACCOUNT
CREATE TABLE FactAccount (
    accountID VARCHAR(255),
    land VARCHAR(255),
    provincie VARCHAR(255),
    plaats VARCHAR(255),
    industriezone VARCHAR(255),
    postcode INT,
    isVokaEntiteit INT, 
    ondernemingstype VARCHAR(255),
    ondernemingsaard VARCHAR(255),
    accountStatus INT, 
    vokaNummer INT,
    financialDataID INT,
    oprichtingsdatum DATE,
    aanvraagID VARCHAR(255),
    lidmaatschapID VARCHAR(255),
    afspraakID VARCHAR(255),
    activiteitID VARCHAR(255),
    activiteitNaam VARCHAR(255),
    PRIMARY KEY (accountID),
    FOREIGN KEY (financialDataID) REFERENCES DimFinanciëleDataAccount(financialDataID),
    FOREIGN KEY (aanvraagID) REFERENCES DimInfoEnKlachten(aanvraagID),
    FOREIGN KEY (lidmaatschapID) REFERENCES DimLidmaatschap(lidmaatschapID),
    FOREIGN KEY (afspraakID) REFERENCES DimAfspraak(afspraakID),
    FOREIGN KEY (oprichtingsdatum) REFERENCES DimDate(fullDate),
);


--Dimtables rond tweede facttable => CONTACT

--DimInschrijving
CREATE TABLE DimInschrijving (
    inschrijvingID VARCHAR(255) NOT NULL PRIMARY KEY,
    aanwezigAfwezig VARCHAR(255),
    bron VARCHAR(255),
    facturatieBedrag VARCHAR(255),
    inschrijvingsDatum DATE,
    contactID VARCHAR(255), 
    campagneID VARCHAR(255),

)


-- DimCampagne
CREATE TABLE DimCampagne (
    campagneID VARCHAR(255) NOT NULL PRIMARY KEY, 
    campagneNummer VARCHAR(255), 
    campagneNaam VARCHAR(255),
    campagneNaamInEmail VARCHAR(255),
    campagneType VARCHAR(255),
    campagneSoort VARCHAR(255), 
    campagneStartdatumID INT, 
    campagneEinddatumID int,
    campagneStatus INT, 
    campagneURLVoka VARCHAR(255),
    visitID VARCHAR(255), 
    inschrijvingID VARCHAR(255),
    FOREIGN KEY (inschrijvingID) REFERENCES DimInschrijving(inschrijvingID),
);


--DimVisit= merge van visit, mailings, clicks
CREATE TABLE DimVisit (
    visitID VARCHAR(255) NOT NULL PRIMARY KEY,
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
    -- mailSent VARCHAR(255),
    mailing_onderwerp VARCHAR(255),
    mailSent_clicks INT,
    contactID VARCHAR(255),
    campagneID VARCHAR(255),
    FOREIGN KEY (campagneID) REFERENCES DimCampagne(campagneID),
);

    
--pageviews laten vallen want kwn wat da is


-- TWEEDE FACT TABLE = Contact
CREATE TABLE FactContact
    (
        contactID VARCHAR(255) NOT NULL PRIMARY KEY,
        contactStatus VARCHAR(255),
        isVokaMedewerker INT,
        functietitel VARCHAR(255),
        teamCode VARCHAR(255),
        persoonWeblogin VARCHAR(255),
        mailRegio VARCHAR(255), -- uit persoon, how?
        mailThema VARCHAR(255), -- uit persoon, how?
        mailType VARCHAR(255), -- uit persoon, how?
        inschrijvingID VARCHAR(255),
        campagneID VARCHAR(255),
        visitID VARCHAR(255),
        afspraakID VARCHAR(255),
        inschrijvingsDatum DATE,
        FOREIGN KEY (inschrijvingID) REFERENCES DimInschrijving(inschrijvingID),
        FOREIGN KEY (visitID) REFERENCES DimVisit(visitID),
        FOREIGN KEY (afspraakID) REFERENCES DimAfspraak(afspraakID),
        FOREIGN KEY (inschrijvingsDatum) REFERENCES DimDate(fullDate),
        
    );
