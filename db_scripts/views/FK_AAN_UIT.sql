--UITZETTEN FK's
-- USE Voka_DWH5_2;
EXEC sp_msforeachtable 'ALTER TABLE ? NOCHECK CONSTRAINT ALL';


--AANZETTEN FK's
-- USE Voka_DWH5_2;
EXEC sp_msforeachtable 'ALTER TABLE ? CHECK CONSTRAINT ALL';
