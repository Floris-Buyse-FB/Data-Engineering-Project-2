-- CREATE DATABASE Voka_DWH;
USE Voka_DWH;

-- VERBINDENDE DIMENSION TABLE = DimDate
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
END


-- DIMTABLES ROND EERSTE FACTTABLE => ACCOUNT
CREATE TABLE DimFinanciëleDataAccount (
    financialDataID INT PRIMARY KEY,
    boekjaar INT,
    aantalMaanden FLOAT,
    toegevoegdeWaarde VARCHAR(255),
    FTE VARCHAR(255),
    gewijzigdOp DATE,
    
);


-- ?
CREATE TABLE DimGebruikers (
    gebruikersID VARCHAR(255) PRIMARY KEY NOT NULL, 
    gebruikersNaam VARCHAR(255),
);


CREATE TABLE DimInfoEnKlachten (
    aanvraagID VARCHAR(255) PRIMARY KEY NOT NULL ,
    aanvraagDatum DATE,
    datumAfsluiting DATE,
    aanvraagStatus VARCHAR(255),
    eigenaar VARCHAR(255),
    FOREIGN KEY (eigenaar) REFERENCES DimGebruikers(gebruikersID),
)



CREATE TABLE DimLidmaatschap (
    lidmaatschapID VARCHAR(255) PRIMARY KEY NOT NULL,
    redenAangroei VARCHAR(255),
    redenVerloop VARCHAR(255),
    startDatum DATE,
    opzegDatum DATE,

)

CREATE TABLE DimPersoon (
        persoonID VARCHAR(255) PRIMARY KEY NOT NULL ,
        persoonNummer INT,
        persoonStatus VARCHAR(255),
        persoonWeblogin VARCHAR(255),
        persoonMarketingCommunicatie VARCHAR(255),
        mailRegio VARCHAR(255),
        mailThema VARCHAR(255),
        mailType VARCHAR(255),
       
);


CREATE TABLE DimFunctie (
    functieID VARCHAR(255) PRIMARY KEY NOT NULL, 
    functieNaam VARCHAR(255),
);


CREATE TABLE DimTeams (
    teamsID INT PRIMARY KEY NOT NULL ,
    teamCode VARCHAR(255),
    teamBoeking VARCHAR(255),
)



CREATE TABLE DimContactfiche (
    contactID VARCHAR(255) PRIMARY KEY,
    contactStatus INT, 
    isVokaMedewerker INT, 
    persoonID VARCHAR(255), 
    functieID VARCHAR(255),
    teamsID INT,
    FOREIGN KEY (persoonID) REFERENCES DimPersoon(persoonID),
    FOREIGN KEY (functieID) REFERENCES DimFunctie(functieID),
    FOREIGN KEY (teamsID) REFERENCES DimTeams(teamsID),
  
);


CREATE TABLE DimAfspraak (
    afspraakID VARCHAR(255) PRIMARY KEY, 
    thema VARCHAR(255),
    subthema VARCHAR(255),
    onderwerp VARCHAR(255),
    eindtijd DATETIME,
    keyphrases VARCHAR(255),
    contactID VARCHAR(255),
    FOREIGN KEY (contactID) REFERENCES DimContactfiche(contactID), -- if applicable
);


CREATE TABLE DimActiviteit (
    activiteitID VARCHAR(255) PRIMARY KEY NOT NULL, 
    activiteitNaam VARCHAR(255),
    activiteitStatus INT, 
    contactID VARCHAR(255), 
    FOREIGN KEY (contactID) REFERENCES DimContactfiche(contactID), -- if applicable

)








--EERSTE FACTTABLE = ACCOUNT

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
    oprichtingsdatumID INT, 
    primaireActiviteit VARCHAR(255), -- laten vallen? (heel veel unknowns),
    accountStatus INT, 
    vokaNummer INT,
    financialDataID INT,
    aanvraagID VARCHAR(255),
    lidmaatschapID VARCHAR(255),
    contactID VARCHAR(255),
    afspraakID VARCHAR(255),
    activiteitID VARCHAR(255), 
    PRIMARY KEY (accountID),
    FOREIGN KEY (financialDataID) REFERENCES DimFinanciëleDataAccount(financialDataID),
    FOREIGN KEY (aanvraagID) REFERENCES DimInfoEnKlachten(aanvraagID),
    FOREIGN KEY (lidmaatschapID) REFERENCES DimLidmaatschap(lidmaatschapID),
    FOREIGN KEY (contactID) REFERENCES DimContactfiche(contactID),
    FOREIGN KEY (afspraakID) REFERENCES DimAfspraak(afspraakID),
    FOREIGN KEY (activiteitID) REFERENCES DimActiviteit(activiteitID),
    FOREIGN KEY (oprichtingsdatumID) REFERENCES DimDate(dateID),
    -- kolommen die ik hier heb laten vallen (voorlopig): geografische regio, subregio (zou er eig nog laten vallen ma bon)
);












-- DIMTABLES ROND TWEEDE FACTTABLE => CAMPAGNE

CREATE TABLE DimCDIClicks (
    clickID INT PRIMARY KEY NOT NULL IDENTITY(1,1),
    aantalClicks INT,
)


CREATE TABLE DimCDIMails (
    mailID VARCHAR(255) PRIMARY KEY NOT NULL ,
    mailNaam VARCHAR(255),
    mailOnderwerp VARCHAR(255),
    mailZendDatum DATE,
    clickID INT, 
    FOREIGN KEY (clickID) REFERENCES DimCDIClicks(clickID),
)

CREATE TABLE DimCDIPageviews
    (
        pageviewID VARCHAR(255) NOT NULL PRIMARY KEY,
        pageTitle VARCHAR(255),
        browser VARCHAR(255),
        operatingSystem VARCHAR(255),
        referrerType VARCHAR(255),
        pageviewDuration FLOAT,
        pageviewTime DATETIME,
        viewedOn DATE,
        pageviewType VARCHAR(255),
        pageviewURL VARCHAR(2000),
        visitorKey VARCHAR(255),
        aangemaaktOp DATE,
        gewijzigdOp DATE,
        gewijzigdDoor VARCHAR(255),
        pageviewStatus VARCHAR(255),
        campagneID VARCHAR(255), -- foreign key naar DimCampagne
        visitID VARCHAR(255), -- foreign key naar DimCDIVisits

    );

CREATE TABLE DimCDIVisits (
    visitID VARCHAR(255) PRIMARY KEY NOT NULL,
    visitAdobeReader VARCHAR(255),  -- (JA/NEE)
    visitBounce VARCHAR(255), -- (JA/NEE)
    browser VARCHAR(255),
    IPStad VARCHAR(255),
    IPCompany VARCHAR(255),
    IPLand VARCHAR(255),
    visitDuration FLOAT,
    visitStarttijd DATE,
    visitEindtijd DATE,
    visitTime DATETIME,
    entrypage VARCHAR(255),
    exitpage VARCHAR(255),
    firstVisit VARCHAR(255), -- (JA/NEE)
    IPAdress VARCHAR(255),
    IPOrganization VARCHAR(255),
    keywords VARCHAR(255), 
    IPLongitude FLOAT, 
    IPLatitude FLOAT,
    operatingSystem VARCHAR(255),
    IPPostcode VARCHAR(255),
    referrer VARCHAR(255),
    referringHost VARCHAR(255),
    referrerType VARCHAR(255),
    visitScore FLOAT,
    visit_ip_status VARCHAR(255),
    aangemaaktOp DATE,
    gewijzigdOp DATE,
    mailID VARCHAR(255), 
    pageviewID VARCHAR(255),
    FOREIGN KEY (mailID) REFERENCES DimCDIMails(mailID),
    FOREIGN KEY (pageviewID) REFERENCES DimCDIPageviews(pageviewID),
    -- contactnaam en containssocialprofile heb ik laten vallen want leeg

)




CREATE TABLE DimSessie(
    sessieID VARCHAR(255) NOT NULL PRIMARY KEY,
    sessieNummer VARCHAR(255),
    activiteitsType VARCHAR(255),
    sessieThema VARCHAR(255),
    sessieProduct VARCHAR(255),
    sessieStartTijd DATETIME,
    sessieEindTijd DATETIME,
    
)

-- wou niet inladen bij mij dus kwn of 100% juist
CREATE TABLE DimInschrijving (
    inschrijvingID VARCHAR(255) NOT NULL PRIMARY KEY,
    aanwezigAfwezig VARCHAR(255),
    bron VARCHAR(255),
    facturatieBedrag VARCHAR(255),
    inschrijvingsDatum DATE,
    contactID VARCHAR(255), 
    sessieID VARCHAR(255), 
    FOREIGN KEY (contactID) REFERENCES DimContactfiche(contactID),
    FOREIGN KEY (sessieID) REFERENCES DimSessie(sessieID),

)




-- TWEEDE FACT TABLE = Campagne

CREATE TABLE FactCampagne (
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
    pageviewID VARCHAR(255),
    sessieID VARCHAR(255),
    inschrijvingID VARCHAR(255),
    FOREIGN KEY (visitID) REFERENCES DimCDIVisits(visitID),
    FOREIGN KEY (pageviewID) REFERENCES DimCDIPageviews(pageviewID),
    FOREIGN KEY (sessieID) REFERENCES DimSessie(sessieID),
    FOREIGN KEY (inschrijvingID) REFERENCES DimInschrijving(inschrijvingID),
    FOREIGN KEY (campagneStartdatumID) REFERENCES DimDate(dateID),
    FOREIGN KEY (campagneEinddatumID) REFERENCES DimDate(dateID),
);


















