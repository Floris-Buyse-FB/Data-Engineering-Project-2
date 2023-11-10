USE Voka_DWH2;

INSERT INTO FactAccount (
    oprichtingsDateID,
    financialDataID,
    infoID,
    lidID,
    afsID,
    ondernemingID,
    accountID,
    vokaNummer,
    ondernemingsaard,
    ondernemingstype
    -- activiteitID,
    -- activiteitNaam
)
SELECT
    D.dateID AS oprichtingsDateID,
    F.financialDataID AS financialDataID,
    I.infoID AS infoID,
    L.lidID AS lidID,
    Af.afsID AS afsID,
    DimA.ondernemingID AS ondernemingID,
    A.account_account_id AS accountID,
    A.account_voka_nr_ AS vokaNummer,
    A.account_ondernemingsaard AS ondernemingsaard,
    A.account_ondernemingstype  AS ondernemingstype
    -- Ac.account_activiteitscode_activiteitscode AS activiteitID,
    -- Act.activiteitscode_naam AS activiteitNaam
FROM Voka.dbo.Account A
INNER JOIN Voka_DWH2.dbo.DimDate D ON A.account_oprichtingsdatum = D.fullDate
INNER JOIN Voka_DWH2.dbo.DimFinanciëleDataAccount F ON A.account_account_id = F.accountID 
INNER JOIN Voka_DWH2.dbo.DimInfoEnKlachten I ON A.account_account_id = I.accountID
INNER JOIN Voka_DWH2.dbo.DimLidmaatschap L ON A.account_account_id = L.accountID
INNER JOIN Voka_DWH2.dbo.DimAfspraak Af ON A.account_account_id = Af.accountID
INNER JOIN Voka_DWH2.dbo.DimAccount DimA ON A.account_account_id = DimA.accountID
INNER JOIN Voka.dbo.Account_activiteitscode Ac ON A.account_account_id = Ac.account_activiteitscode_account
-- INNER JOIN Voka.dbo.Activiteitscode Act ON Ac.account_activiteitscode_activiteitscode = Act.activiteitscode_activiteitscode_id 

