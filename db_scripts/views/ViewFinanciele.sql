-- USE Voka;
CREATE VIEW dbo.ViewFinanciele
AS
SELECT
	f.financieledata_id AS financialDataID,
	f.financieledata_boekjaar AS boekjaar,
	f.financieledata_aantal_maanden AS aantalMaanden,
	f.financieledata_toegevoegde_waarde AS toegevoegdeWaarde,
	f.financieledata_fte AS FTE,
	f.financieledata_gewijzigd_op AS gewijzigdOp,
	f.financieledata_ondernemingid AS accountID
	
	
FROM
    Voka.dbo.Account_financiële_data f

-- Step 2: Extract data from the view
SELECT * FROM Voka.dbo.ViewFinanciele;

-- Step 3: Load data into data warehouse table
INSERT INTO Voka_DWH.dbo.DimFinanciëleDataAccount(financialDataID, boekjaar, aantalMaanden, toegevoegdeWaarde, FTE, gewijzigdOp, accountID


)
SELECT financialDataID, boekjaar, aantalMaanden, toegevoegdeWaarde, FTE, gewijzigdOp, accountID


 FROM Voka.dbo.ViewFinanciele;
