--CREATE DATABASE Voka;

--USE Voka;

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