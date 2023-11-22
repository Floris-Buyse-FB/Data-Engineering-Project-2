-- USE Voka;
CREATE VIEW dbo.ViewAfspraak
AS
SELECT
    a.afspraak_alle_afspraak_id AS afspraakID,
	ac.afspraak_betreft_account_thema AS account_thema,
	ac.afspraak_betreft_account_subthema AS account_subthema,
	ac.afspraak_betreft_account_onderwerp AS account_onderwerp,
	ac.afspraak_betreft_account_eindtijd AS account_eindtijd,
	LEFT(ac.afspraak_betreft_account_keyphrases, 255) AS account_keyphrases,
	c.afspraak_betreft_contactfiche_thema AS contact_thema,
	c.afspraak_betreft_contactfiche_subthema AS contact_subthema,
	c.afspraak_betreft_contactfiche_onderwerp AS contact_onderwerp,
	c.afspraak_betreft_contactfiche_eindtijd AS contact_eindtijd,
	LEFT(c.afspraak_betreft_contactfiche_keyphrases, 255) AS conact_keyphrases,
	ac.afspraak_betreft_account_betreft_id AS accountID,
	c.afspraak_betreft_contactfiche_betreft_id AS contactID
FROM
    Voka.dbo.Afspraak_alle a
LEFT JOIN
    Voka.dbo.Afspraak_betreft_account_cleaned ac ON a.afspraak_alle_afspraak_id = ac.afspraak_betreft_account_afspraak_id
LEFT JOIN
	Voka.dbo.Afspraak_betreft_contact_cleaned c ON a.afspraak_alle_afspraak_id = c.afspraak_betreft_contactfiche_afspraak_id

-- Step 2: Extract data from the view
SELECT * FROM Voka.dbo.ViewAfspraak;

-- Step 3: Load data into data warehouse table
INSERT INTO Voka_DWH5_2.dbo.DimAfspraak(afspraakID, account_thema, account_subthema, account_onderwerp, account_eindtijd, account_keyphrases, contact_thema, contact_subthema, contact_onderwerp, contact_eindtijd, conact_keyphrases
)
SELECT afspraakID, account_thema, account_subthema, account_onderwerp, account_eindtijd, account_keyphrases, contact_thema, contact_subthema, contact_onderwerp, contact_eindtijd, conact_keyphrases
FROM Voka.dbo.ViewAfspraak;
