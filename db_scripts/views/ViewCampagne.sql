-- USE Voka;
CREATE VIEW dbo.ViewCampagne
AS
SELECT
    c.campagne_campagne_id AS campagneID,
	c.campagne_campagne_nr AS campagneNummer,
	c.campagne_naam AS campagneNaam,
	c.campagne_naam_in_email AS campagenNaamInEmail,
	c.campagne_type_campagne AS campagneType,
	c.campagne_soort_campagne AS campagneSoort,
	c.campagne_startdatum AS campagneStartdatum,
	c.campagne_einddatum AS campagneEinddatum,
	c.campagne_status AS campagneStatus,
	c.campagne_url_voka_be AS campagneURLVoka

FROM
    Voka.dbo.Campagne c

-- Step 2: Extract data from the view
SELECT * FROM Voka.dbo.ViewCampagne;

-- Step 3: Load data into data warehouse table
INSERT INTO Voka_DWH.dbo.DimCampagne (campagneID, campagneNummer, campagneNaam, campagneNaamInEmail, campagneType, campagneSoort, campagneStartdatum, campagneEinddatum, campagneStatus, campagneURLVoka)
SELECT campagneID, campagneNummer, campagneNaam, campagenNaamInEmail, campagneType, campagneSoort, campagneStartdatum, campagneEinddatum, campagneStatus, campagneURLVoka FROM Voka.dbo.ViewCampagne;
