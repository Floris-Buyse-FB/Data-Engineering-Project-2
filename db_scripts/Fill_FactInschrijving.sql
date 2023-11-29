USE Voka_DWH;

INSERT INTO FactInschrijving(
    inschrijvingID,
    aanwezigAfwezig,
    bron,
    facturatieBedrag,
    campagneID,
    inschrijvingsDatumID,
    sesID,
    contactID
)
SELECT
    I.inschrijving_inschrijving_id AS inschrijvingID,
    I.inschrijving_aanwezig_afwezig AS aanwezigAfwezig,
    I.inschrijving_bron AS bron,
    I.inschrijving_facturatie_bedrag AS facturatieBedrag,
    Camp.campagneID AS campagneID,
    D.dateID AS inschrijvingsDatumID,
    S.sesID AS sesID,
    C.contactID AS contactID

FROM Voka.dbo.Inschrijving I
INNER JOIN Voka_DWH.dbo.DimDate D ON I.inschrijving_datum_inschrijving = D.fullDate
INNER JOIN Voka_DWH.dbo.DimSessie S ON I.inschrijving_inschrijving_id = S.inschrijvingsID
INNER JOIN Voka_DWH.dbo.DimContact C ON I.inschrijving_contactfiche = C.contactID
INNER JOIN Voka_DWH.dbo.DimCampagne Camp ON I.inschrijving_campagne = Camp.campagneID

