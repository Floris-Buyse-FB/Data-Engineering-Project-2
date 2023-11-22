-- USE Voka;
CREATE VIEW dbo.ViewAccount
AS
SELECT DISTINCT
    a.account_account_id AS accountID,
    a.account_adres_land AS land,
    a.account_adres_provincie AS provincie,
    a.account_adres_plaats AS plaats,
    a.account_adres_geografische_subregio AS subregio,
    a.account_industriezone_naam_ AS industriezone,
    a.account_adres_postcode AS postcode,
    a.account_is_voka_entiteit AS isVokaEntiteit,
    a.account_status AS accountStatus,
    a.account_voka_nr_ AS vokaNummer,
    a.account_ondernemingsaard AS ondernemingsaard,
    a.account_ondernemingstype AS ondernemingstype,
     (
        SELECT TOP 1 ac.account_activiteitscode_activiteitscode
        FROM Voka.dbo.Account_activiteitscode ac
        WHERE ac.accou= a.account_account_id
    ) AS activiteitsID,
    a.account_primaire_activiteit AS activiteitNaam
FROM
    Voka.dbo.Account a
WHERE
    a.account_adres_provincie = 'Oost-Vlaanderen';

-- Step 2: Extract data from the view
SELECT * FROM Voka.dbo.ViewAccount;

-- Step 3: Load data into data warehouse table
INSERT INTO Voka_DWH5_2.dbo.DimAccount(accountID, land, provincie, plaats, subregio, industriezone, postcode, isVokaEntiteit, accountStatus, vokaNummer, ondernemingsaard, ondernemingstype, activiteitID, activiteitNaam
)
SELECT accountID, land, provincie, plaats, subregio, industriezone, postcode, isVokaEntiteit, accountStatus, vokaNummer, ondernemingsaard, ondernemingstype, activiteitsID, activiteitNaam
 FROM Voka.dbo.ViewAccount;
