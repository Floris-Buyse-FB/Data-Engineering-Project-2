-- USE Voka;
CREATE VIEW dbo.ViewSessie
AS
SELECT
    s.sessie_sessie_id AS sessieID,
	s.sessie_sessie_nr_ AS sessieNummer,
	s.sessie_activiteitstype AS activiteitstype,
	s.sessie_campagne AS campaignID,
	si.sessieinschrijving_inschrijving AS inschrijvingsID,
	s.sessie_start_datum_tijd AS startDatumTijd,
	s.sessie_eind_datum_tijd AS eindDatumTijd,
	s.sessie_product AS product,
	s.sessie_thema_naam_ AS themaNaam
FROM
    Voka.dbo.Sessie s
INNER JOIN
    Voka.dbo.Sessie_inschrijving si ON s.sessie_sessie_id = si.sessieinschrijving_sessie

-- Step 2: Extract data from the view
SELECT * FROM Voka.dbo.ViewSessie;

-- Step 3: Load data into data warehouse table
INSERT INTO Voka_DWH5_2.dbo.DimSessie (sessieID, sessieNummer, activiteitstype, campaignID, inschrijvingsID, startDatumTijd, eindDatumTijd, product, themaNaam)
SELECT sessieID, sessieNummer, activiteitstype, campaignID, inschrijvingsID, startDatumTijd, eindDatumTijd, product, themaNaam FROM Voka.dbo.ViewSessie;
