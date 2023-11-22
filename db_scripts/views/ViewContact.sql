-- USE Voka;
CREATE VIEW dbo.ViewContact
AS
SELECT
	c.contact_contactpersoon_id AS contactID,
	c.contact_status AS contactStatus,
	c.contact_voka_medewerker AS isVokaMedewerker,
	c.contact_functietitel AS functietitel,
	p.persoon_web_login AS persoonWeblogin,
	p.persoon_mail_regio_antwerpen_waasland AS persoon_mail_regio_antwerpen_waasland,
	p.persoon_mail_regio_brussel_hoofdstedelijk_gewest AS persoon_mail_regio_brussel_hoofdstedelijk_gewes,
	p.persoon_mail_regio_limburg AS persoon_mail_regio_limburg,
	p.persoon_mail_regio_mechelen_kempen AS persoon_mail_regio_mechelen_kempen,
	p.persoon_mail_regio_oost_vlaanderen AS persoon_mail_regio_oost_vlaanderen,
	p.persoon_mail_regio_vlaams_brabant AS persoon_mail_regio_vlaams_brabant,
	p.persoon_mail_regio_voka_nationaal AS persoon_mail_regio_voka_nationaal,
	p.persoon_mail_regio_west_vlaanderen AS persoon_mail_regio_west_vlaanderen,
	p.persoon_mail_thema_duurzaamheid AS persoon_mail_thema_duurzaamheid,
	p.persoon_mail_thema_financieel_fiscaal AS persoon_mail_thema_financieel_fiscaal,
	p.persoon_mail_thema_innovatie AS persoon_mail_thema_innovatie,
	p.persoon_mail_thema_internationaal_ondernemen AS persoon_mail_thema_internationaal_ondernemen,
	p.persoon_mail_thema_mobiliteit AS persoon_mail_thema_mobiliteit,
	p.persoon_mail_thema_omgeving AS persoon_mail_thema_omgeving,
	p.persoon_mail_thema_sales_marketing_communicatie AS persoon_mail_thema_sales_marketing_communicatie,
	p.persoon_mail_thema_strategie_en_algemeen_management AS persoon_mail_thema_strategie_en_algemeen_management,
	p.persoon_mail_thema_talent AS persoon_mail_thema_talent,
	p.persoon_mail_thema_welzijn AS persoon_mail_thema_welzijn,
	p.persoon_mail_type_bevraging AS persoon_mail_type_bevraging,
	p.persoon_mail_type_communities_en_projecten AS persoon_mail_type_communities_en_projecten,
	p.persoon_mail_type_netwerkevenementen AS persoon_mail_type_netwerkevenementen,
	p.persoon_mail_type_nieuwsbrieven AS persoon_mail_type_nieuwsbrieven,
	p.persoon_mail_type_opleidingen AS persoon_mail_type_opleidingen,
	p.persoon_mail_type_persberichten_belangrijke_meldingen AS persoon_mail_type_persberichten_belangrijke_meldingen,
	p.persoon_marketingcommunicatie AS persoon_marketingcommunicatie,
	STRING_AGG(f.functie_naam, ', ') AS functieNaam,
	c.contact_account AS accountID
    
FROM
    Voka.dbo.Contact c
LEFT OUTER JOIN
    Voka.dbo.Persoon p ON c.contact_persoon_id = p.persoon_persoon_id
LEFT OUTER JOIN
	Voka.dbo.Contact_functie cf ON c.contact_contactpersoon_id = cf.contactfunctie_contactpersoon
LEFT OUTER JOIN
	Voka.dbo.Functie f ON cf.contactfunctie_functie = f.functie_functie_id
group by
	c.contact_contactpersoon_id,
    c.contact_status,
    c.contact_voka_medewerker,
    c.contact_functietitel,
    p.persoon_web_login,
    p.persoon_mail_regio_antwerpen_waasland,
    p.persoon_mail_regio_brussel_hoofdstedelijk_gewest,
    p.persoon_mail_regio_limburg,
    p.persoon_mail_regio_mechelen_kempen,
    p.persoon_mail_regio_oost_vlaanderen,
    p.persoon_mail_regio_vlaams_brabant,
    p.persoon_mail_regio_voka_nationaal,
    p.persoon_mail_regio_west_vlaanderen,
    p.persoon_mail_thema_duurzaamheid,
    p.persoon_mail_thema_financieel_fiscaal,
    p.persoon_mail_thema_innovatie,
    p.persoon_mail_thema_internationaal_ondernemen,
    p.persoon_mail_thema_mobiliteit,
    p.persoon_mail_thema_omgeving,
    p.persoon_mail_thema_sales_marketing_communicatie,
    p.persoon_mail_thema_strategie_en_algemeen_management,
    p.persoon_mail_thema_talent,
    p.persoon_mail_thema_welzijn,
    p.persoon_mail_type_bevraging,
    p.persoon_mail_type_communities_en_projecten,
    p.persoon_mail_type_netwerkevenementen,
    p.persoon_mail_type_nieuwsbrieven,
    p.persoon_mail_type_opleidingen,
    p.persoon_mail_type_persberichten_belangrijke_meldingen,
    p.persoon_marketingcommunicatie,
    c.contact_account;

-- Step 2: Extract data from the view
SELECT * FROM Voka.dbo.ViewContact;

-- Step 3: Load data into data warehouse table
INSERT INTO Voka_DWH5_2.dbo.DimContact(contactID, contactStatus, isVokaMedewerker, functietitel, persoonWeblogin, persoon_mail_regio_antwerpen_waasland, persoon_mail_regio_brussel_hoofdstedelijk_gewest, persoon_mail_regio_limburg, persoon_mail_regio_mechelen_kempen, persoon_mail_regio_oost_vlaanderen, persoon_mail_regio_vlaams_brabant, persoon_mail_regio_voka_nationaal, persoon_mail_regio_west_vlaanderen, persoon_mail_thema_duurzaamheid, persoon_mail_thema_financieel_fiscaal, persoon_mail_thema_innovatie, persoon_mail_thema_internationaal_ondernemen, persoon_mail_thema_mobiliteit, persoon_mail_thema_omgeving, persoon_mail_thema_sales_marketing_communicatie, persoon_mail_thema_strategie_en_algemeen_management, persoon_mail_thema_talent, persoon_mail_thema_welzijn, persoon_mail_type_bevraging, persoon_mail_type_communities_en_projecten, persoon_mail_type_netwerkevenementen, persoon_mail_type_nieuwsbrieven, persoon_mail_type_opleidingen, persoon_mail_type_persberichten_belangrijke_meldingen, persoon_marketingcommunicatie, functieNaam, accountID
)
SELECT contactID, contactStatus, isVokaMedewerker, functietitel, persoonWeblogin, persoon_mail_regio_antwerpen_waasland, persoon_mail_regio_brussel_hoofdstedelijk_gewes, persoon_mail_regio_limburg, persoon_mail_regio_mechelen_kempen, persoon_mail_regio_oost_vlaanderen, persoon_mail_regio_vlaams_brabant, persoon_mail_regio_voka_nationaal, persoon_mail_regio_west_vlaanderen, persoon_mail_thema_duurzaamheid, persoon_mail_thema_financieel_fiscaal, persoon_mail_thema_innovatie, persoon_mail_thema_internationaal_ondernemen, persoon_mail_thema_mobiliteit, persoon_mail_thema_omgeving, persoon_mail_thema_sales_marketing_communicatie, persoon_mail_thema_strategie_en_algemeen_management, persoon_mail_thema_talent, persoon_mail_thema_welzijn, persoon_mail_type_bevraging, persoon_mail_type_communities_en_projecten, persoon_mail_type_netwerkevenementen, persoon_mail_type_nieuwsbrieven, persoon_mail_type_opleidingen, persoon_mail_type_persberichten_belangrijke_meldingen, persoon_marketingcommunicatie, functieNaam, accountID
  FROM Voka.dbo.ViewContact;
