--CREATE DATABASE Voka;

--USE Voka;

IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Account_activiteitscode')
BEGIN
    CREATE TABLE Account_activiteitscode
    (
        account_activiteitscode_account VARCHAR(255),
        account_activiteitscode_activiteitscode VARCHAR(255),
        account_activiteitscode_inf_account_inf_activiteitscodeid VARCHAR(255),
        FOREIGN KEY (account_activiteitscode_account) REFERENCES Account(account_account_id),
        FOREIGN KEY (account_activiteitscode_activiteitscode) REFERENCES Activiteitscode(activiteitscode_activiteitscode_id)
    );
END

IF NOT EXISTS (SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Account')
BEGIN
    CREATE TABLE Account
    (
        account_account_id INT NOT NULL PRIMARY KEY IDENTITY(1,1),
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
        financieledata_id INT,
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
WHERE TABLE_NAME = 'Activiteit_vereist_contact')
BEGIN
    CREATE TABLE Activiteit_vereist_contact
    (
        activiteitvereistcontact_activityid_id INT NOT NULL PRIMARY KEY IDENTITY(1,1),
        activiteitvereistcontact_reqattendee VARCHAR(255),
        FOREIGN KEY (activiteitvereistcontact_activityid_id) REFERENCES Afspraak_alle(afspraak_alle_afspraak_id),
        FOREIGN KEY (activiteitvereistcontact_reqattendee) REFERENCES Contact(contact_contactpersoon_id)
    );
END