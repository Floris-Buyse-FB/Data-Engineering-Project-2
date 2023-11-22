-- USE Voka;
drop view dbo.viewAccount
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
	(
        SELECT TOP 1 aac_inner.account_activiteitscode_activiteitscode
        FROM Voka.dbo.Account a_inner
        INNER JOIN Account_activiteitscode aac_inner ON aac_inner.account_activiteitscode_account = a_inner.account_account_id
        INNER JOIN Activiteitscode ac_inner ON ac_inner.activiteitscode_activiteitscode_id = aac_inner.account_activiteitscode_activiteitscode
        WHERE a_inner.account_account_id = a.account_account_id
        ORDER BY aac_inner.account_activiteitscode_activiteitscode
    ) AS activiteitsID,
	(
            SELECT TOP 1 ac_inner.activiteitscode_naam
            FROM Voka.dbo.Account a_inner
            INNER JOIN Account_activiteitscode aac_inner ON aac_inner.account_activiteitscode_account = a_inner.account_account_id
            INNER JOIN Activiteitscode ac_inner ON ac_inner.activiteitscode_activiteitscode_id = aac_inner.account_activiteitscode_activiteitscode
            WHERE a_inner.account_account_id = a.account_account_id
            ORDER BY aac_inner.account_activiteitscode_activiteitscode
        ) AS activiteitNaam
FROM
    Voka.dbo.Account a
Inner JOIN Account_activiteitscode aac on aac.account_activiteitscode_account = a.account_account_id
Inner JOIN Activiteitscode ac on ac.activiteitscode_activiteitscode_id = aac.account_activiteitscode_activiteitscode
WHERE
    a.account_adres_provincie = 'Oost-Vlaanderen'
group by
	a.account_account_id,
    a.account_adres_land,
    a.account_adres_provincie,
    a.account_adres_plaats,
    a.account_adres_geografische_subregio,
    a.account_industriezone_naam_,
    a.account_adres_postcode,
    a.account_is_voka_entiteit,
    a.account_status,
    a.account_voka_nr_,
    a.account_ondernemingsaard,
    a.account_ondernemingstype;

-- Step 2: Extract data from the view
SELECT * FROM Voka.dbo.ViewAccount;

-- Step 3: Load data into data warehouse table
INSERT INTO Voka_DWH5_2.dbo.DimAccount(accountID, land, provincie, plaats, subregio, industriezone, postcode, isVokaEntiteit, accountStatus, vokaNummer, ondernemingsaard, ondernemingstype, activiteitID, activiteitNaam
)
SELECT accountID, land, provincie, plaats, subregio, industriezone, postcode, isVokaEntiteit, accountStatus, vokaNummer, ondernemingsaard, ondernemingstype, activiteitsID, activiteitNaam
 FROM Voka.dbo.ViewAccount;
