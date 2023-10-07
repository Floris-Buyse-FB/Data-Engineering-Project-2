CREATE DATABASE Voka;

-- Accounts
IF NOT EXISTS (SELECT * FROM Voka.TABLES WHERE TABLE_NAME = 'Accounts')
BEGIN
    CREATE TABLE Accounts (
        Account INT PRIMARY KEY,
        Adres_Geografische_regio VARCHAR(255),
        Adres_Geografische_subregio VARCHAR(255),
        Adres_Plaats VARCHAR(255),
        Adres_Postcode INT,
        Adres_Provincie VARCHAR(255),
        Industriezone_Naam VARCHAR(255),
        Is_Voka_entiteit BIT,
        Ondernemingsaard VARCHAR(255),
        Ondernemingstype VARCHAR(255),
        Oprichtingsdatum DATE,
        Primaire_activiteit VARCHAR(255),
        Reden_van_status VARCHAR(255),
        [Status] VARCHAR(255),
        Voka_Nr INT,
        --Hoofd_NaCe_Code VARCHAR(255),
        Adres_Land VARCHAR(255)
    );
END

-- Info en klachten
IF NOT EXISTS (SELECT * FROM Voka.TABLES WHERE TABLE_NAME = 'Info_en_klachten')
BEGIN
  CREATE TABLE Info_en_klachten(
    Aanvraag INT PRIMARY KEY,
    Account INT NOT NULL,
    Datum DATE,
    Afsluiting DATE,
    Status VARCHAR(255),
    Eigenaar VARCHAR(255),
    FOREIGN KEY (Account) REFERENCES Accounts(Account)
  );
END

-- Gebruiker
IF NOT EXISTS (SELECT * FROM Voka.TABLES WHERE TABLE_NAME = 'Gebruiker')
BEGIN
  CREATE TABLE Gebruiker(
    Account INT PRIMARY KEY,
    Business_Unit_Naam VARCHAR(255),
    FOREIGN KEY (Account) REFERENCES Accounts(Account)
  );
END

-- Account helpdeskvragen
IF NOT EXISTS (SELECT * FROM Voka.TABLES WHERE TABLE_NAME = 'Account_helpdeskvragen')
BEGIN
  CREATE TABLE Account_helpdeskvragen(
    Lidmaatschap INT PRIMARY KEY,
    Account INT NOT NULL,
    FOREIGN KEY (Account) REFERENCES Accounts(Account)
  );
END

-- Account financiële data
IF NOT EXISTS (SELECT * FROM Voka.TABLES WHERE TABLE_NAME = 'Account_financiële_data')
BEGIN
  CREATE TABLE Account_financiële_data(
    OndernemingID INT,
    Boekjaar INT,
    Aantal_maanden INT,
    Toegevoegde_waarde INT,
    FTE INT,
    Gewijzigd_op DATE,
    FOREIGN KEY (OndernemingID) REFERENCES Accounts(Account)
  );
END

-- Account Activiteitscode
IF NOT EXISTS (SELECT * FROM Voka.TABLES WHERE TABLE_NAME = 'Account_Activiteitscode')
BEGIN
  CREATE TABLE Account_Activiteitscode(
    Account INT NOT NULL,
    Activiteitdscode INT NOT NULL,
    FOREIGN KEY (Account) REFERENCES Accounts(Account),
    FOREIGN KEY (Activiteitdscode) REFERENCES ActiviteitsCode(Activiteitdscode)
  );
END

-- ActiviteitsCode
IF NOT EXISTS (SELECT * FROM Voka.TABLES WHERE TABLE_NAME = 'ActiviteitsCode')
BEGIN
  CREATE TABLE ActiviteitsCode(
    Activiteitdscode INT PRIMARY KEY
  );
END

-- Contactfiches
IF NOT EXISTS (SELECT * FROM Voka.TABLES WHERE TABLE_NAME = '')
BEGIN
  CREATE TABLE Contactfiches(
    Contactfiche INT PRIMARY KEY,
    Account INT NOT NULL,
    Persoon INT NOT NULL,
    Functietitel VARCHAR(255),
    Persoon_ID INT,
    [Status] VARCHAR(50),
    Voka_medewerker VARCHAR(100)
    FOREIGN KEY (Persoon) REFERENCES Personen(Persoon),
    FOREIGN KEY (Account) REFERENCES Accounts(Account)
  );
END

-- Personen
IF NOT EXISTS (SELECT * FROM Voka.TABLES WHERE TABLE_NAME = 'Personen')
BEGIN
  CREATE TABLE Personen(
    Persoon INT PRIMARY KEY,
    Contactfiche INT NOT NULL,
    Persoonsnr_ INT,
    Reden_van_status BOOLEAN,
    Web_Login BOOLEAN,
    Mail_regio_Antwerpen_Waasland BOOLEAN,
    Mail_regio_Brussel_Hoofdstedelijk_Gewest BOOLEAN,
    Mail_regio_Limburg BOOLEAN,
    Mail_regio_Mechelen_Kempen BOOLEAN,
    Mail_regio_Oost_Vlaanderen BOOLEAN,
    Mail_regio_Vlaams_Brabant BOOLEAN,
    Mail_regio_Voka_nationaal BOOLEAN,
    Mail_regio_West_Vlaanderen BOOLEAN,
    Mail_thema_duurzaamheid BOOLEAN,
    Mail_thema_financieel_fiscaal BOOLEAN,
    Mail_thema_innovatie BOOLEAN,
    Mail_thema_internationaal_ondernemen BOOLEAN,
    Mail_thema_mobiliteit BOOLEAN,
    Mail_thema_omgeving BOOLEAN,
    Mail_thema_sales_marketing_communicatie BOOLEAN,
    Mail_thema_strategie_en_algemeen_management BOOLEAN,
    Mail_thema_talent BOOLEAN,
    Mail_thema_welzijn BOOLEAN,
    Mail_type_Bevraging BOOLEAN,
    Mail_type_communities_en_projecten BOOLEAN,
    Mail_type_netwerkevenementen BOOLEAN,
    Mail_type_nieuwsbrieven BOOLEAN,
    Mail_type_opleidingen BOOLEAN,
    Mail_type_persberichten_belangrijke_meldingen BOOLEAN,
    Marketingcommunicatie VARCHAR(255),
    FOREIGN KEY (Contactfiche) REFERENCES Contactfiches(Contactfiche)
  );
END

-- Functie
IF NOT EXISTS (SELECT * FROM Voka.TABLES WHERE TABLE_NAME = 'Functie')
BEGIN
  CREATE TABLE Functie(
    Functie VARCHAR(255) PRIMARY KEY,
    Naam VARCHAR(255)
  );
END

-- Contactfiche functies
IF NOT EXISTS (SELECT * FROM Voka.TABLES WHERE TABLE_NAME = 'Contactfiche_functies')
BEGIN
  CREATE TABLE Contactfiche_functies(
    Contactfiche INT NOT NULL,
    Functie VARCHAR(255),
    FOREIGN KEY (Contactfiche) REFERENCES Contactfiches(Contactfiche),
    FOREIGN KEY (Functie) REFERENCES Functie(Functie)
  );
END

-- Afspraak betreft Contactfiche
IF NOT EXISTS (SELECT * FROM Voka.TABLES WHERE TABLE_NAME = 'Afspraak_betreft_Contactfiche')
BEGIN
  CREATE TABLE Afspraak_betreft_Contactfiche(
    Afspraak INT NOT NULL,
    BetreftID INT NOT NULL,
    Thema VARCHAR(255),
    Subthema VARCHAR(255),
    Onderwerp VARCHAR(255),
    Eindtijd DATETIME,
    KeyPhrases VARCHAR(255),
    FOREIGN KEY (BetreftID) REFERENCES Contactfiches(Contactfiche)
  );
END

-- Afspraak account gelinkt
IF NOT EXISTS (SELECT * FROM Voka.TABLES WHERE TABLE_NAME = 'Afspraak_account_gelinkt')
BEGIN
  CREATE TABLE Afspraak_account_gelinkt(
    Afspraak INT NOT NULL,
    AccountID INT NOT NULL,
    Thema VARCHAR(255),
    Subthema VARCHAR(255),
    Onderwerp VARCHAR(255),
    Eindtijd DATETIME,
    KeyPhrases VARCHAR(255),
    FOREIGN KEY (AccountID) REFERENCES Accounts(Account)
  );
END

-- Afspraak betreft Account
IF NOT EXISTS (SELECT * FROM Voka.TABLES WHERE TABLE_NAME = 'Afspraak_betreft_Account')
BEGIN
  CREATE TABLE Afspraak_betreft_Account(
    Afspraak INT NOT NULL,
    BetreftID VARCHAR(255) NOT NULL,
    Thema VARCHAR(255),
    Subthema VARCHAR(255),
    Onderwerp VARCHAR(255),
    Eindtijd DATETIME,
    KeyPhrases VARCHAR(255)
    FOREIGN KEY (BetreftID) REFERENCES Accounts(Account)
  );
END

-- Afspraak Alle
IF NOT EXISTS (SELECT * FROM Voka.TABLES WHERE TABLE_NAME = 'Afspraak')
BEGIN
  CREATE TABLE Afspraak(
    Afspraak INT PRIMARY KEY,
  );
END

-- Afsrpaak vereist contact
IF NOT EXISTS (SELECT * FROM Voka.TABLES WHERE TABLE_NAME = 'Afspraak_vereist_contact')
BEGIN
  CREATE TABLE Afspraak_vereist_contact(
    Afspraak INT NOT NULL,
    Contact INT NOT NULL,
    FOREIGN KEY (Contact) REFERENCES Contactfiches(Contactfiche)
  );
END

-- Inschrijving
IF NOT EXISTS (SELECT * FROM Voka.TABLES WHERE TABLE_NAME = 'Inschrijving')
BEGIN
  CREATE TABLE Inschrijving(
    Inschrijving VARCHAR(255) PRIMARY KEY,
    Contactfiche VARCHAR(255) NOT NULL,
    Campagne VARCHAR(255) NOT NULL,
    Aanwezig_Afwezig VARCHAR(255),
    Bron VARCHAR(255),
    Datum_inschrijving DATE,
    Facturatie_Bedrag DECIMAL(10, 2)
    FOREIGN KEY (Contactfiche) REFERENCES Contactfiches(Contactfiche)
    FOREIGN KEY (Campagne) REFERENCES Campagne(Campagne)
  );
END

-- Sessie inschrijving
IF NOT EXISTS (SELECT * FROM Voka.TABLES WHERE TABLE_NAME = 'Sessie_inschrijving')
BEGIN
  CREATE TABLE Sessie_inschrijving(
    Sessieinschrijving VARCHAR(255) PRIMARY KEY,
    Inschrijving VARCHAR(255),
    Sessie VARCHAR(255),
    FOREIGN KEY (Sessie) REFERENCES Sessie(Sessie),
    FOREIGN KEY (Inschrijving) REFERENCES Inschrijving(Inschrijving)
  );
END

-- Sessie
IF NOT EXISTS (SELECT * FROM Voka.TABLES WHERE TABLE_NAME = 'Sessie')
BEGIN
  CREATE TABLE Sessie(
    Sessie VARCHAR(255) PRIMARY KEY,
    Campagne VARCHAR(255) NOT NULL,
    Activiteitstype VARCHAR(255),
    Eind_Datum_Tijd DATETIME, -- Adjust to your desired date/time format
    Product VARCHAR(255),
    Sessie_nr_ INT,
    Start_Datum_Tijd DATETIME, -- Adjust to your desired date/time format
    Thema_Naam VARCHAR(255)
    FOREIGN KEY (Campagne) REFERENCES Campagne(Campagne)
  );
END

-- Campagne
IF NOT EXISTS (SELECT * FROM Voka.TABLES WHERE TABLE_NAME = 'Campagne')
BEGIN
  CREATE TABLE Campagne(
    Campagne VARCHAR(255) PRIMARY KEY,
    Campagne_Nr INT,
    Einddatum DATE,
    Naam VARCHAR(255),
    Naam_in_email VARCHAR(255),
    Reden_van_status VARCHAR(255),
    Startdatum DATE,
    [Status] VARCHAR(255),
    Type_campagne VARCHAR(255),
    URL_voka_be VARCHAR(255),
    Soort_Campagne VARCHAR(255)
  );
END

-- CDI Pageview
IF NOT EXISTS (SELECT * FROM Voka.TABLES WHERE TABLE_NAME = 'CDI_Pageview')
BEGIN
  CREATE TABLE CDI_Pageview(
    CDI_pageview VARCHAR(255) PRIMARY KEY,
    Campaign INT NOT NULL,
    Contact INT,
    Web_Content VARCHAR(255),
    --Anonymous_Visitor VARCHAR(255),
    Browser VARCHAR(255),
    Duration INT,
    Operating_System VARCHAR(255),
    Referrer_Type VARCHAR(255),
    [Time] TIME,
    Page_Title VARCHAR(255),
    [Type] VARCHAR(255),
    [Url] VARCHAR(255),
    Viewed_On DATE,
    Visit INT,
    Visitor_Key VARCHAR(255),
    Aangemaakt_op DATETIME,
    Gewijzigd_door VARCHAR(255),
    Gewijzigd_op DATETIME,
    [Status] VARCHAR(255),
    Reden_van_status VARCHAR(255)
    FOREIGN KEY (Campaign) REFERENCES Campaign(Campaign)
  );
END

-- CDI Visit
IF NOT EXISTS (SELECT * FROM Voka.TABLES WHERE TABLE_NAME = 'CDI_Visit')
BEGIN
  CREATE TABLE CDI_Visit(
    CDI_visit INT PRIMARY KEY,
    Adobe_Reader VARCHAR(255),
    Bounce VARCHAR(255),
    Browser VARCHAR(255),
    --Campagne_Code VARCHAR(255),
    Campaign VARCHAR(255),
    IP_Stad VARCHAR(255),
    IP_Company VARCHAR(255),
    Contact VARCHAR(255),
    Contact_Naam VARCHAR(255),
    containssocialprofile VARCHAR(255),
    IP_Land VARCHAR(255),
    Duration INT,
    Email_Send VARCHAR(255),
    Ended_On DATETIME,  -- Adjust to your desired date/time format
    Entry_Page VARCHAR(255),
    Exit_Page VARCHAR(255),
    First_Visit VARCHAR(255),
    IP_Address VARCHAR(255),
    IP_Organization VARCHAR(255),
    Keywords VARCHAR(255),
    IP_Latitude VARCHAR(255),
    IP_Longitude VARCHAR(255),
    Operating_System VARCHAR(255),
    IP_Postcode VARCHAR(255),
    Referrer VARCHAR(255),
    Referring_Host VARCHAR(255),
    Score VARCHAR(255),
    Referrer_Type VARCHAR(255),
    Started_On DATETIME,  -- Adjust to your desired date/time format
    IP_Status VARCHAR(255),
    [Time] TIME,  -- Adjust to your desired time format
    Total_Pages INT,
    Aangemaakt_op DATETIME,  -- Adjust to your desired date/time format
    Gewijzigd_op DATETIME
    FOREIGN KEY (Campaign) REFERENCES Campaign(Campaign)
    FOREIGN KEY (Email_Send) REFERENCES Email_Send(Email_Send)
  );
END

-- CDI Mailing
IF NOT EXISTS (SELECT * FROM Voka.TABLES WHERE TABLE_NAME = 'CDI_Mailing')
BEGIN
  CREATE TABLE CDI_Mailing(
    Mailing INT PRIMARY KEY,
    [Name] VARCHAR(255),
    Sent_On DATETIME,
    Onderwerp VARCHAR(255)
  );
END

-- CDI sentemail click
IF NOT EXISTS (SELECT * FROM Voka.TABLES WHERE TABLE_NAME = 'CDI_sentemail_click')
BEGIN
  CREATE TABLE CDI_sentemail_click(
    Sent_Email INT PRIMARY KEY,
    Contact INT,
    Email_versturen INT,
    Clicks INT,
    FOREIGN KEY (Contact) REFERENCES Contactfiches(Contactfiche),
    FOREIGN KEY (Email_versturen) REFERENCES CDI_Mailing(Mailing)
  );
END
