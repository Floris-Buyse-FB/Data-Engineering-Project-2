-- USE Voka;
CREATE VIEW dbo.ViewVisit
AS
SELECT
    v.visit_visit_id AS visitID,
	v.visit_bounce AS visit_bounce,
	v.visit_browser AS visit_browser,
	v.visit_ip_address AS visit_ip_address,
	v.visit_ip_company AS visit_ip_company,
	v.visit_ip_land AS visit_ip_land,
	v.visit_ip_postcode AS visit_ip_postcode,
	v.visit_ip_stad AS visit_ip_stad,
	v.visit_duration AS visit_duration,
	v.visit_first_visit AS visit_first_visit,
	v.visit_entry_page AS visit_entry_page,
	v.visit_exit_page AS visit_exit_page,
	v.visit_referrer_type AS visit_referrer_type,
	v.visit_started_on AS visit_started_on,
	v.visit_total_pages AS visit_total_pages,
	-- m.mailing_onderwerp AS mailing_onderwerp,
	v.visit_email_send AS mailSent,
	-- v. AS mailing_name,
	cl.sentemail_kliks_clicks AS mailSent_clicks,
	v.visit_campaign AS campaignID,
	v.visit_contact AS contactID
FROM
    Voka.dbo.Cdi_visits v
INNER JOIN
    Voka.dbo.Cdi_sent_email_clicks cl ON v.visit_contact = cl.sentemail_kliks_contact
-- INNER JOIN
	-- Voka.dbo.Cdi_mailing m ON cl.sentemail_kliks_sent_email_id = m.mailing_mailing_id

-- Step 2: Extract data from the view
SELECT * FROM Voka.dbo.ViewVisit;

-- Step 3: Load data into data warehouse table
INSERT INTO Voka_DWH5_2.dbo.DimVisit(visitID, visit_bounce, visit_browser, visit_ip_address, visit_ip_company, visit_ip_land, visit_ip_postcode, visit_ip_stad, visit_duration, visit_first_visit, visit_entry_page, visit_exit_page, visit_referrer_type, visit_started_on, visit_total_pages, mailSent, mailSent_clicks, campaignID, contactID
)
SELECT visitID, visit_bounce, visit_browser, visit_ip_address, visit_ip_company, visit_ip_land, visit_ip_postcode, visit_ip_stad, visit_duration, visit_first_visit, visit_entry_page, visit_exit_page, visit_referrer_type, visit_started_on, visit_total_pages, mailSent, mailSent_clicks, campaignID, contactID
 FROM Voka.dbo.ViewVisit;
