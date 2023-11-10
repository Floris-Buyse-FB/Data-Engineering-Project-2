USE Voka_DWH2;

INSERT INTO FactContact (
    contID,
    insID,
    visID,
    afsID,
    inschrijvingsDatumID,
    contactID
)
SELECT
    DC.contID AS contID,
    DI.insID AS insID,
    DV.visID AS visID,
    DA.afsID AS afsID,
    DD.dateID AS inschrijvingsDatumID,
    C.contactID AS contactID
FROM Voka.dbo.Contact C
INNER JOIN Voka_DWH2.dbo.DimContact DC ON C.contact_contact_id = DC.contactID
INNER JOIN Voka_DWH2.dbo.DimInschrijving DI ON C.contact_contact_id = DI.contactID
INNER JOIN Voka_DWH2.dbo.DimVisit DV ON C.contact_contact_id = DV.contactID
INNER JOIN Voka_DWH2.dbo.DimAfspraak DA ON C.contact_contactpersoon_id  = DA.contactID
INNER JOIN Voka_DWH2.dbo.DimDate DD ON DI.inschrijvingsDatum = DD.fullDate
