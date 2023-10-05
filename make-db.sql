-- Accounts
CREATE TABLE IF NOT EXISTS Accounts(
  Account INT PRIMARY KEY,
  Adres_Geografische_regio VARCHAR(255),
  Adres_Geografische_subregio VARCHAR(255),
  Adres_Plaats VARCHAR(255),
  Adres_Postcode INT,
  Adres_Provincie VARCHAR(255),
  Industriezone_Naam VARCHAR(255),
  Is_Voka_entiteit BOOLEAN,
  Ondernemingsaard VARCHAR(255),
  Ondernemingstype VARCHAR(255),
  Oprichtingsdatum DATE,
  Primaire_activiteit VARCHAR(255),
  Reden_van_status VARCHAR(255),
  [Status] VARCHAR(255),
  Voka_Nr INT,
  Hoofd_NaCe_Code VARCHAR(255),
  Adres_Land VARCHAR(255),
)

-- Info en klachten
CREATE TABLE IF NOT EXISTS Info_en_klachten(
  Aanvraag INT PRIMARY KEY,
  Account INT NOT NULL,
  Datum DATE,
  Afsluiting DATE,
  Status VARCHAR(255),
  Eigenaar VARCHAR(255),
  FOREIGN KEY (Account) REFERENCES Accounts(Account)
)

-- Gebruiker
CREATE TABLE IF NOT EXISTS Gebruiker(
  Account INT PRIMARY KEY,
  Business_Unit_Naam VARCHAR(255),
  FOREIGN KEY (Account) REFERENCES Accounts(Account)
)

-- Account helpdeskvragen
CREATE TABLE IF NOT EXISTS Account_helpdeskvragen(
  Lidmaatschap INT PRIMARY KEY,
  Account INT NOT NULL,
  FOREIGN KEY (Account) REFERENCES Accounts(Account)
)

-- Account financiële data
CREATE TABLE IF NOT EXISTS Account_financiële_data(
  OndernemingID INT,
  Boekjaar INT,
  Aantal_maanden INT,
  Toegevoegde_waarde INT,
  FTE INT,
  Gewijzigd_op DATE,
  FOREIGN KEY (OndernemingID) REFERENCES Accounts(Account)
)

-- Account Activiteitscode
CREATE TABLE IF NOT EXISTS Account_Activiteitscode(
  Account INT NOT NULL,
  Activiteitdscode INT NOT NULL,
  FOREIGN KEY (Account) REFERENCES Accounts(Account),
  FOREIGN KEY (Activiteitdscode) REFERENCES ActiviteitsCode(Activiteitdscode)
)

-- ActiviteitsCode
CREATE TABLE IF NOT EXISTS ActiviteitsCode(
  Activiteitdscode INT PRIMARY KEY
)

-- Contactfiches
CREATE TABLE IF NOT EXISTS Contactfiches(
  Contactfiche INT PRIMARY KEY,
  Account INT NOT NULL,
  Persoon INT NOT NULL,
  Functietitel VARCHAR(255),
  Persoon_ID INT,
  [Status] VARCHAR(50),
  Voka_medewerker VARCHAR(100)
  FOREIGN KEY (Persoon) REFERENCES Personen(Persoon),
  FOREIGN KEY (Account) REFERENCES Accounts(Account)
)

-- Personen
CREATE TABLE IF NOT EXISTS Personen(
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
)

-- Functie
CREATE TABLE IF NOT EXISTS Functie(
  Functie VARCHAR(255) PRIMARY KEY,
  Naam VARCHAR(255)
)

-- Contactfiche functies
CREATE TABLE IF NOT EXISTS Contactfiche_functies(
  Contactfiche INT NOT NULL,
  Functie VARCHAR(255),
  FOREIGN KEY (Contactfiche) REFERENCES Contactfiches(Contactfiche),
  FOREIGN KEY (Functie) REFERENCES Functie(Functie)
)

-- Afspraak betreft Contactfiche
CREATE TABLE IF NOT EXISTS Afspraak_betreft_Contactfiche(
  Afspraak INT NOT NULL,
  BetreftID INT NOT NULL,
  Thema VARCHAR(255),
  Subthema VARCHAR(255),
  Onderwerp VARCHAR(255),
  Eindtijd DATETIME,
  KeyPhrases VARCHAR(255),
  FOREIGN KEY (BetreftID) REFERENCES Contactfiches(Contactfiche)
)

-- Afspraak account gelinkt
CREATE TABLE IF NOT EXISTS Afspraak_account_gelinkt(
  Afspraak INT NOT NULL,
  AccountID INT NOT NULL,
  Thema VARCHAR(255),
  Subthema VARCHAR(255),
  Onderwerp VARCHAR(255),
  Eindtijd DATETIME,
  KeyPhrases VARCHAR(255),
  FOREIGN KEY (AccountID) REFERENCES Accounts(Account)
)

-- Afspraak betreft Account
CREATE TABLE IF NOT EXISTS Afspraak_betreft_Account(
  Afspraak INT NOT NULL,
  BetreftID VARCHAR(255) NOT NULL,
  Thema VARCHAR(255),
  Subthema VARCHAR(255),
  Onderwerp VARCHAR(255),
  Eindtijd DATETIME,
  KeyPhrases VARCHAR(255)
  FOREIGN KEY (BetreftID) REFERENCES Accounts(Account)
)

-- Afspraak Alle
CREATE TABLE IF NOT EXISTS Afspraak(
  Afspraak INT PRIMARY KEY,
)

-- Afsrpaak vereist contact
CREATE TABLE IF NOT EXISTS Afspraak_vereist_contact(
  Afspraak INT NOT NULL,
  Contact INT NOT NULL,
  FOREIGN KEY (Contact) REFERENCES Contactfiches(Contactfiche)
)

-- Inschrijving
CREATE TABLE IF NOT EXISTS Inschrijving(
  Inschrijving VARCHAR(255) PRIMARY KEY,
  Contactfiche VARCHAR(255) NOT NULL,
  Campagne VARCHAR(255) NOT NULL,
  Aanwezig_Afwezig VARCHAR(255),
  Bron VARCHAR(255),
  Datum_inschrijving DATE,
  Facturatie_Bedrag DECIMAL(10, 2)
  FOREIGN KEY (Contactfiche) REFERENCES Contactfiches(Contactfiche)
  FOREIGN KEY (Campagne) REFERENCES Campagne(Campagne)
)

-- Sessie inschrijving
CREATE TABLE IF NOT EXISTS Sessie_inschrijving(
  Sessieinschrijving VARCHAR(255) PRIMARY KEY,
  Inschrijving VARCHAR(255),
  Sessie VARCHAR(255),
  FOREIGN KEY (Sessie) REFERENCES Sessie(Sessie),
  FOREIGN KEY (Inschrijving) REFERENCES Inschrijving(Inschrijving)
)

-- Sessie
CREATE TABLE IF NOT EXISTS Sessie(
  Sessie VARCHAR(255) PRIMARY KEY,
  Campagne VARCHAR(255) NOT NULL,
  Activiteitstype VARCHAR(255),
  Eind_Datum_Tijd DATETIME, -- Adjust to your desired date/time format
  Product VARCHAR(255),
  Sessie_nr_ INT,
  Start_Datum_Tijd DATETIME, -- Adjust to your desired date/time format
  Thema_Naam VARCHAR(255)
  FOREIGN KEY (Campagne) REFERENCES Campagne(Campagne)
)

-- Campagne
CREATE TABLE IF NOT EXISTS Campagne(
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
)

-- CDI Pageview
CREATE TABLE IF NOT EXISTS CDI_Pageview(
  CDI_pageview VARCHAR(255) PRIMARY KEY,
  Campaign INT NOT NULL,
  Contact INT,
  Web_Content VARCHAR(255),
  Anonymous_Visitor VARCHAR(255),
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
)

-- CDI Visit
CREATE TABLE IF NOT EXISTS CDI_Visit(
  CDI_visit INT PRIMARY KEY,
  Adobe_Reader VARCHAR(255),
  Bounce VARCHAR(255),
  Browser VARCHAR(255),
  Campagne_Code VARCHAR(255),
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
)

-- CDI Mailing
CREATE TABLE IF NOT EXISTS CDI_Mailing(
  Mailing INT PRIMARY KEY,
  Name VARCHAR(255),
  Sent_On DATETIME,
  Onderwerp VARCHAR(255)
)

-- CDI sentemail click
CREATE TABLE IF NOT EXISTS CDI_sentemail_click(
  Sent_Email INT PRIMARY KEY,
  Contact INT,
  Email_versturen INT,
  Clicks INT,
  FOREIGN KEY (Contact) REFERENCES Contactfiches(Contactfiche)
  FOREIGN KEY (Email_versturen) REFERENCES Email_versturen(Email_versturen)
)