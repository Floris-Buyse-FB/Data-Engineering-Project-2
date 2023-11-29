-- USE Voka;
CREATE VIEW dbo.ViewAccount
AS
SELECT Distinct
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
    ac.activiteitscode_naam AS activiteitNaam
FROM
    Voka.dbo.Account a
LEFT JOIN Account_activiteitscode aac on aac.account_activiteitscode_account = a.account_account_id
LEFT JOIN Activiteitscode ac on ac.activiteitscode_activiteitscode_id = aac.account_activiteitscode_activiteitscode


-- Step 2: Extract data from the view
SELECT * FROM Voka.dbo.ViewAccount 


-- Step 3: Load data into data warehouse table
INSERT INTO Voka_DWH.dbo.DimAccount (accountID, land, provincie, plaats, subregio, industriezone, postcode, isVokaEntiteit, accountStatus, vokaNummer, ondernemingsaard, ondernemingstype, activiteitNaam)
SELECT
    accountID,
    MAX(land) AS land,
    MAX(provincie) AS provincie,
    MAX(plaats) AS plaats,
    MAX(subregio) AS subregio,
    MAX(industriezone) AS industriezone,
    MAX(postcode) AS postcode,
    MAX(isVokaEntiteit) AS isVokaEntiteit,
    MAX(accountStatus) AS accountStatus,
    MAX(vokaNummer) AS vokaNummer,
    MAX(ondernemingsaard) AS ondernemingsaard,
    MAX(ondernemingstype) AS ondernemingstype,
    STRING_AGG(activiteitNaam, ',') AS activiteitNaamCombined
FROM Voka.dbo.ViewAccount
GROUP BY accountID;