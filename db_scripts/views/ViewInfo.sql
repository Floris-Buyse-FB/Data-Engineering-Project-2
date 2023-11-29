-- USE Voka;
CREATE VIEW dbo.ViewInfo
AS
SELECT
	i.info_en_klachten_aanvraag_id AS aanvraagID,
	i.info_en_klachten_datum AS aanvraagDatum,
	i.info_en_klachten_datum_afsluiting AS datumAfsluiting,
	i.info_en_klachten_status AS aanvraagStatus,
	i.info_en_klachten_account AS accountID
	
FROM
    Voka.dbo.Info_en_klachten i

-- Step 2: Extract data from the view
SELECT * FROM Voka.dbo.ViewInfo;

-- Step 3: Load data into data warehouse table
INSERT INTO Voka_DWH.dbo.DimInfoEnKlachten(aanvraagID, aanvraagDatum, datumAfsluiting, aanvraagStatus, accountID

)
SELECT aanvraagID, aanvraagDatum, datumAfsluiting, aanvraagStatus, accountID

 FROM Voka.dbo.ViewInfo;
