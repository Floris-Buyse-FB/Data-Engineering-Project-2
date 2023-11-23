-- USE Voka;
CREATE VIEW dbo.ViewAfspraak
AS
SELECT
    a.afspraak_alle_afspraak_id AS afspraakID,
	c.afspraak_betreft_contactfiche_thema AS thema,
	c.afspraak_betreft_contactfiche_subthema AS subthema,
	c.afspraak_betreft_contactfiche_onderwerp AS onderwerp,
	c.afspraak_betreft_contactfiche_eindtijd AS eindtijd,
	c.afspraak_betreft_contactfiche_keyphrases AS keyphrases,
	c.afspraak_betreft_contactfiche_betreft_id AS contactID,
	Null as accountID
	
FROM
    Voka.dbo.Afspraak_alle a
inner JOIN
	Voka.dbo.Afspraak_betreft_contact_cleaned c ON a.afspraak_alle_afspraak_id = c.afspraak_betreft_contactfiche_afspraak_id
UNION ALL
SELECT
    a.afspraak_alle_afspraak_id AS afspraakID,
	ac.afspraak_betreft_account_thema AS thema,
	ac.afspraak_betreft_account_subthema AS subthema,
	ac.afspraak_betreft_account_onderwerp AS onderwerp,
	ac.afspraak_betreft_account_eindtijd AS eindtijd,
	ac.afspraak_betreft_account_keyphrases AS keyphrases,
	Null as contactID,
	ac.afspraak_betreft_account_betreft_id AS accountID
	
FROM
    Voka.dbo.Afspraak_alle a
inner JOIN
	Voka.dbo.Afspraak_betreft_account_cleaned ac ON a.afspraak_alle_afspraak_id = ac.afspraak_betreft_account_afspraak_id


-- Step 2: Extract data from the view
SELECT * FROM Voka.dbo.ViewAfspraak;

-- Step 3: Load data into data warehouse table
INSERT INTO Voka_DWH5_2.dbo.DimAfspraak(afspraakID, thema, subthema, onderwerp, eindtijd, contactID, accountID, keyphrases)
SELECT afspraakID, thema, subthema, onderwerp, eindtijd, contactID, accountID, keyphrases
FROM Voka.dbo.ViewAfspraak;
