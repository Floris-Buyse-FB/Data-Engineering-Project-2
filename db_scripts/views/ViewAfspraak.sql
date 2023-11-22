-- USE Voka;
CREATE VIEW dbo.ViewAfspraak
AS
SELECT
    a.afspraak_alle_afspraak_id AS afspraakID,
	
FROM
    Voka.dbo.Afspraak_alle a
INNER JOIN
    Voka.dbo.Afspraak_betreft_account_cleaned ac ON a.afspraak_alle_afspraak_id = ac.afspraak_betreft_account_afspraak_id
INNER JOIN
	Voka.dbo.Afspraak_betreft_contact_cleaned c ON a.afspraak_alle_afspraak_id = c.afspraak_betreft_contactfiche_afspraak_id

-- Step 2: Extract data from the view
SELECT * FROM Voka.dbo.ViewAfspraak;

-- Step 3: Load data into data warehouse table
INSERT INTO Voka_DWH5_2.dbo.DimAfspraak()
SELECT FROM Voka.dbo.ViewAfspraak;
