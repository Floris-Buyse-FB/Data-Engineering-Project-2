-- USE Voka;
CREATE VIEW dbo.ViewLidmaatschap
AS
SELECT
	l.lidmaatschap_lidmaatschap_id AS lidmaatschapID,
	l.lidmaatschap_reden_aangroei AS redenAangroei,
	l.lidmaatschap_reden_verloop AS redenVerloop,
	l.lidmaatschap_startdatum AS startDatum,
	l.lidmaatschap_datum_opzeg AS opzegDatum,
	l.lidmaatschap_onderneming AS accountID
	
FROM
    Voka.dbo.Lidmaatschap l

-- Step 2: Extract data from the view
SELECT * FROM Voka.dbo.ViewLidmaatschap;

-- Step 3: Load data into data warehouse table
INSERT INTO Voka_DWH5_2.dbo.DimLidmaatschap(lidmaatschapID, redenAangroei, redenVerloop, startDatum, opzegDatum, accountID
)
SELECT lidmaatschapID, redenAangroei, redenVerloop, startDatum, opzegDatum, accountID
 FROM Voka.dbo.ViewLidmaatschap;
