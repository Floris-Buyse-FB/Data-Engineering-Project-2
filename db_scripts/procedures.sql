CREATE OR ALTER PROCEDURE InsertAccountData (
    @account_account_id VARCHAR(255),
    @account_adres_geografische_regio VARCHAR(255),
    @account_adres_geografische_subregio VARCHAR(255),
    @account_adres_plaats VARCHAR(255),
    @account_adres_postcode VARCHAR(255),
    @account_adres_provincie VARCHAR(255),
    @account_industriezone_naam_ VARCHAR(255),
    @account_is_voka_entiteit INT,
    @account_ondernemingsaard VARCHAR(255),
    @account_ondernemingstype VARCHAR(255),
    @account_oprichtingsdatum DATE,
    @account_primaire_activiteit VARCHAR(255),
    @account_reden_van_status VARCHAR(255),
    @account_status INT,
    @account_voka_nr_ INT,
    @account_adres_land VARCHAR(255)
)
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Account WHERE account_account_id = @account_account_id)
    BEGIN
        INSERT INTO Account (
            account_account_id,
            account_adres_geografische_regio,
            account_adres_geografische_subregio,
            account_adres_plaats,
            account_adres_postcode,
            account_adres_provincie,
            account_industriezone_naam_,
            account_is_voka_entiteit,
            account_ondernemingsaard,
            account_ondernemingstype,
            account_oprichtingsdatum,
            account_primaire_activiteit,
            account_reden_van_status,
            account_status,
            account_voka_nr_,
            account_adres_land
        )
        VALUES (
            @account_account_id,
            @account_adres_geografische_regio,
            @account_adres_geografische_subregio,
            @account_adres_plaats,
            @account_adres_postcode,
            @account_adres_provincie,
            @account_industriezone_naam_,
            @account_is_voka_entiteit,
            @account_ondernemingsaard,
            @account_ondernemingstype,
            @account_oprichtingsdatum,
            @account_primaire_activiteit,
            @account_reden_van_status,
            @account_status,
            @account_voka_nr_,
            @account_adres_land
        );
    END
END;

CREATE OR ALTER PROCEDURE InsertFinancialData (
    @financieledata_ondernemingid VARCHAR(255),
    @financieledata_boekjaar INT,
    @financieledata_aantal_maanden FLOAT,
    @financieledata_toegevoegde_waarde VARCHAR(255),
    @financieledata_fte VARCHAR(255),
    @financieledata_gewijzigd_op DATE
)
AS
BEGIN
    IF NOT EXISTS (
        SELECT 1 
        FROM Account_financiële_data 
        WHERE financieledata_ondernemingid = @financieledata_ondernemingid
        AND financieledata_boekjaar = @financieledata_boekjaar
    )
    BEGIN
        INSERT INTO Account_financiële_data (
            financieledata_ondernemingid,
            financieledata_boekjaar,
            financieledata_aantal_maanden,
            financieledata_toegevoegde_waarde,
            financieledata_fte,
            financieledata_gewijzigd_op
        )
        VALUES (
            @financieledata_ondernemingid,
            @financieledata_boekjaar,
            @financieledata_aantal_maanden,
            @financieledata_toegevoegde_waarde,
            @financieledata_fte,
            @financieledata_gewijzigd_op
        );
    END
END;

CREATE OR ALTER PROCEDURE InsertAfspraak (
    @afspraak_alle_afspraak_id VARCHAR(255)
)
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Afspraak_alle WHERE afspraak_alle_afspraak_id = @afspraak_alle_afspraak_id)
    BEGIN
        INSERT INTO Afspraak_alle (afspraak_alle_afspraak_id)
        VALUES (@afspraak_alle_afspraak_id);
    END
END;

CREATE PROCEDURE InsertPersoon (
    @persoon_persoon_id VARCHAR(255),
    @persoon_persoonsnr_ INT, 
    @persoon_reden_van_status VARCHAR(255),
    @persoon_web_login VARCHAR(255),
    @persoon_mail_regio_antwerpen_waasland INT,
    @persoon_mail_regio_brussel_hoofdstedelijk_gewest INT,
    @persoon_mail_regio_limburg INT,
    @persoon_mail_regio_mechelen_kempen INT,
    @persoon_mail_regio_oost_vlaanderen INT,
    @persoon_mail_regio_vlaams_brabant INT,
    @persoon_mail_regio_voka_nationaal INT,
    @persoon_mail_regio_west_vlaanderen INT,
    @persoon_mail_thema_duurzaamheid INT,
    @persoon_mail_thema_financieel_fiscaal INT,
    @persoon_mail_thema_innovatie INT,
    @persoon_mail_thema_internationaal_ondernemen INT,
    @persoon_mail_thema_mobiliteit INT,
    @persoon_mail_thema_omgeving INT,
    @persoon_mail_thema_sales_marketing_communicatie INT,
    @persoon_mail_thema_strategie_en_algemeen_management INT,
    @persoon_mail_thema_talent INT,
    @persoon_mail_thema_welzijn INT,
    @persoon_mail_type_bevraging INT,
    @persoon_mail_type_communities_en_projecten INT,
    @persoon_mail_type_netwerkevenementen INT,
    @persoon_mail_type_nieuwsbrieven INT,
    @persoon_mail_type_opleidingen INT,
    @persoon_mail_type_persberichten_belangrijke_meldingen INT,
    @persoon_marketingcommunicatie VARCHAR(255)
)
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Persoon WHERE persoon_persoon_id = @persoon_persoon_id)
    BEGIN
        INSERT INTO Persoon (
            persoon_persoon_id,
            persoon_persoonsnr_,
            persoon_reden_van_status,
            persoon_web_login,
            persoon_mail_regio_antwerpen_waasland,
            persoon_mail_regio_brussel_hoofdstedelijk_gewest,
            persoon_mail_regio_limburg,
            persoon_mail_regio_mechelen_kempen,
            persoon_mail_regio_oost_vlaanderen,
            persoon_mail_regio_vlaams_brabant,
            persoon_mail_regio_voka_nationaal,
            persoon_mail_regio_west_vlaanderen,
            persoon_mail_thema_duurzaamheid,
            persoon_mail_thema_financieel_fiscaal,
            persoon_mail_thema_innovatie,
            persoon_mail_thema_internationaal_ondernemen,
            persoon_mail_thema_mobiliteit,
            persoon_mail_thema_omgeving,
            persoon_mail_thema_sales_marketing_communicatie,
            persoon_mail_thema_strategie_en_algemeen_management,
            persoon_mail_thema_talent,
            persoon_mail_thema_welzijn,
            persoon_mail_type_bevraging,
            persoon_mail_type_communities_en_projecten,
            persoon_mail_type_netwerkevenementen,
            persoon_mail_type_nieuwsbrieven,
            persoon_mail_type_opleidingen,
            persoon_mail_type_persberichten_belangrijke_meldingen,
            persoon_marketingcommunicatie
        )
        VALUES (
            @persoon_persoon_id,
            @persoon_persoonsnr_,
            @persoon_reden_van_status,
            @persoon_web_login,
            @persoon_mail_regio_antwerpen_waasland,
            @persoon_mail_regio_brussel_hoofdstedelijk_gewest,
            @persoon_mail_regio_limburg,
            @persoon_mail_regio_mechelen_kempen,
            @persoon_mail_regio_oost_vlaanderen,
            @persoon_mail_regio_vlaams_brabant,
            @persoon_mail_regio_voka_nationaal,
            @persoon_mail_regio_west_vlaanderen,
            @persoon_mail_thema_duurzaamheid,
            @persoon_mail_thema_financieel_fiscaal,
            @persoon_mail_thema_innovatie,
            @persoon_mail_thema_internationaal_ondernemen,
            @persoon_mail_thema_mobiliteit,
            @persoon_mail_thema_omgeving,
            @persoon_mail_thema_sales_marketing_communicatie,
            @persoon_mail_thema_strategie_en_algemeen_management,
            @persoon_mail_thema_talent,
            @persoon_mail_thema_welzijn,
            @persoon_mail_type_bevraging,
            @persoon_mail_type_communities_en_projecten,
            @persoon_mail_type_netwerkevenementen,
            @persoon_mail_type_nieuwsbrieven,
            @persoon_mail_type_opleidingen,
            @persoon_mail_type_persberichten_belangrijke_meldingen,
            @persoon_marketingcommunicatie
        );
    END
END;

CREATE OR ALTER PROCEDURE InsertContact (
    @contact_contactpersoon_id VARCHAR(255),
    @contact_account VARCHAR(255),
    @contact_functietitel VARCHAR(255),
    @contact_persoon_id VARCHAR(255),
    @contact_status VARCHAR(255),
    @contact_voka_medewerker INT
)
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Contact WHERE contact_contactpersoon_id = @contact_contactpersoon_id)
    BEGIN
        INSERT INTO Contact (
            contact_contactpersoon_id,
            contact_account,
            contact_functietitel,
            contact_persoon_id,
            contact_status,
            contact_voka_medewerker
        )
        VALUES (
            @contact_contactpersoon_id,
            @contact_account,
            @contact_functietitel,
            @contact_persoon_id,
            @contact_status,
            @contact_voka_medewerker
        );
    END
END;

CREATE OR ALTER PROCEDURE InsertActiviteitVereistContact (
    @activiteitvereistcontact_activityid_id VARCHAR(255),
    @activiteitvereistcontact_reqattendee VARCHAR(255)
)
AS
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM Activiteit_vereist_contact
        WHERE activiteitvereistcontact_activityid_id = @activiteitvereistcontact_activityid_id
        AND activiteitvereistcontact_reqattendee = @activiteitvereistcontact_reqattendee
    )
    BEGIN
        INSERT INTO Activiteit_vereist_contact (
            activiteitvereistcontact_activityid_id,
            activiteitvereistcontact_reqattendee
        )
        VALUES (
            @activiteitvereistcontact_activityid_id,
            @activiteitvereistcontact_reqattendee
        );
    END
END;

CREATE OR ALTER PROCEDURE InsertActiviteitscode (
    @activiteitscode_naam VARCHAR(255),
    @activiteitscode_activiteitscode_id VARCHAR(255),
    @activiteitscode_status VARCHAR(255)
)
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Activiteitscode WHERE activiteitscode_activiteitscode_id = @activiteitscode_activiteitscode_id)
    BEGIN
        INSERT INTO Activiteitscode (
            activiteitscode_naam,
            activiteitscode_activiteitscode_id,
            activiteitscode_status
        )
        VALUES (
            @activiteitscode_naam,
            @activiteitscode_activiteitscode_id,
            @activiteitscode_status
        );
    END
END;

CREATE OR ALTER PROCEDURE InsertAccountActiviteitscode (
    @account_activiteitscode_account VARCHAR(255),
    @account_activiteitscode_activiteitscode VARCHAR(255),
    @account_activiteitscode_inf_account_inf_activiteitscodeid VARCHAR(255)
)
AS
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM Account_activiteitscode
        WHERE account_activiteitscode_account = @account_activiteitscode_account
        AND account_activiteitscode_activiteitscode = @account_activiteitscode_activiteitscode
    )
    BEGIN
        INSERT INTO Account_activiteitscode (
            account_activiteitscode_account,
            account_activiteitscode_activiteitscode,
            account_activiteitscode_inf_account_inf_activiteitscodeid
        )
        VALUES (
            @account_activiteitscode_account,
            @account_activiteitscode_activiteitscode,
            @account_activiteitscode_inf_account_inf_activiteitscodeid
        );
    END
END;

CREATE OR ALTER PROCEDURE InsertAfspraakBetreftAccount (
    @afspraak_betreft_account_afspraak_id VARCHAR(255),
    @afspraak_betreft_account_thema VARCHAR(255),
    @afspraak_betreft_account_subthema VARCHAR(255),
    @afspraak_betreft_account_onderwerp VARCHAR(255),
    @afspraak_betreft_account_betreft_id VARCHAR(255),
    @afspraak_betreft_account_eindtijd DATE,
    @afspraak_betreft_account_keyphrases VARCHAR(2000)
)
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Afspraak_betreft_account_cleaned WHERE afspraak_betreft_account_afspraak_id = @afspraak_betreft_account_afspraak_id)
    BEGIN
        INSERT INTO Afspraak_betreft_account_cleaned (
            afspraak_betreft_account_afspraak_id,
            afspraak_betreft_account_thema,
            afspraak_betreft_account_subthema,
            afspraak_betreft_account_onderwerp,
            afspraak_betreft_account_betreft_id,
            afspraak_betreft_account_eindtijd,
            afspraak_betreft_account_keyphrases
        )
        VALUES (
            @afspraak_betreft_account_afspraak_id,
            @afspraak_betreft_account_thema,
            @afspraak_betreft_account_subthema,
            @afspraak_betreft_account_onderwerp,
            @afspraak_betreft_account_betreft_id,
            @afspraak_betreft_account_eindtijd,
            @afspraak_betreft_account_keyphrases
        );
    END
END;

CREATE OR ALTER PROCEDURE InsertAfspraakBetreftContact (
    @afspraak_betreft_contactfiche_afspraak_id VARCHAR(255),
    @afspraak_betreft_contactfiche_thema VARCHAR(255),
    @afspraak_betreft_contactfiche_subthema VARCHAR(255),
    @afspraak_betreft_contactfiche_onderwerp VARCHAR(255),
    @afspraak_betreft_contactfiche_betreft_id VARCHAR(255),
    @afspraak_betreft_contactfiche_eindtijd DATE,
    @afspraak_betreft_contactfiche_keyphrases VARCHAR(2000)
)
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Afspraak_betreft_contact_cleaned WHERE afspraak_betreft_contactfiche_afspraak_id = @afspraak_betreft_contactfiche_afspraak_id)
    BEGIN
        INSERT INTO Afspraak_betreft_contact_cleaned (
            afspraak_betreft_contactfiche_afspraak_id,
            afspraak_betreft_contactfiche_thema,
            afspraak_betreft_contactfiche_subthema,
            afspraak_betreft_contactfiche_onderwerp,
            afspraak_betreft_contactfiche_betreft_id,
            afspraak_betreft_contactfiche_eindtijd,
            afspraak_betreft_contactfiche_keyphrases
        )
        VALUES (
            @afspraak_betreft_contactfiche_afspraak_id,
            @afspraak_betreft_contactfiche_thema,
            @afspraak_betreft_contactfiche_subthema,
            @afspraak_betreft_contactfiche_onderwerp,
            @afspraak_betreft_contactfiche_betreft_id,
            @afspraak_betreft_contactfiche_eindtijd,
            @afspraak_betreft_contactfiche_keyphrases
        );
    END
END;

CREATE OR ALTER PROCEDURE InsertAfspraakAccountGelinkt (
    @afspraak_account_gelinkt_afspraak_id VARCHAR(255),
    @afspraak_account_gelinkt_thema VARCHAR(255),
    @afspraak_account_gelinkt_subthema VARCHAR(255),
    @afspraak_account_gelinkt_onderwerp VARCHAR(255),
    @afspraak_account_gelinkt_eindtijd DATE,
    @afspraak_account_gelinkt_account VARCHAR(255),
    @afspraak_account_gelinkt_keyphrases VARCHAR(2000)
)
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Afspraak_account_gelinkt_cleaned WHERE afspraak_account_gelinkt_afspraak_id = @afspraak_account_gelinkt_afspraak_id)
    BEGIN
        INSERT INTO Afspraak_account_gelinkt_cleaned (
            afspraak_account_gelinkt_afspraak_id,
            afspraak_account_gelinkt_thema,
            afspraak_account_gelinkt_subthema,
            afspraak_account_gelinkt_onderwerp,
            afspraak_account_gelinkt_eindtijd,
            afspraak_account_gelinkt_account,
            afspraak_account_gelinkt_keyphrases
        )
        VALUES (
            @afspraak_account_gelinkt_afspraak_id,
            @afspraak_account_gelinkt_thema,
            @afspraak_account_gelinkt_subthema,
            @afspraak_account_gelinkt_onderwerp,
            @afspraak_account_gelinkt_eindtijd,
            @afspraak_account_gelinkt_account,
            @afspraak_account_gelinkt_keyphrases
        );
    END
END;

CREATE OR ALTER PROCEDURE InsertCampagne (
    @campagne_campagne_id VARCHAR(255),
    @campagne_campagne_nr VARCHAR(255),
    @campagne_einddatum DATE,
    @campagne_naam VARCHAR(255),
    @campagne_naam_in_email VARCHAR(255),
    @campagne_reden_van_status VARCHAR(255),
    @campagne_startdatum DATE,
    @campagne_status VARCHAR(255),
    @campagne_type_campagne VARCHAR(255),
    @campagne_url_voka_be VARCHAR(255),
    @campagne_soort_campagne VARCHAR(255)
)
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Campagne WHERE campagne_campagne_id = @campagne_campagne_id)
    BEGIN
        INSERT INTO Campagne (
            campagne_campagne_id,
            campagne_campagne_nr,
            campagne_einddatum,
            campagne_naam,
            campagne_naam_in_email,
            campagne_reden_van_status,
            campagne_startdatum,
            campagne_status,
            campagne_type_campagne,
            campagne_url_voka_be,
            campagne_soort_campagne
        )
        VALUES (
            @campagne_campagne_id,
            @campagne_campagne_nr,
            @campagne_einddatum,
            @campagne_naam,
            @campagne_naam_in_email,
            @campagne_reden_van_status,
            @campagne_startdatum,
            @campagne_status,
            @campagne_type_campagne,
            @campagne_url_voka_be,
            @campagne_soort_campagne
        );
    END
END;

CREATE OR ALTER PROCEDURE InsertCdiMailing (
    @mailing_mailing_id VARCHAR(255),
    @mailing_name VARCHAR(255),
    @mailing_sent_on VARCHAR(255),
    @mailing_onderwerp VARCHAR(255)
)
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Cdi_mailing WHERE mailing_mailing_id = @mailing_mailing_id)
    BEGIN
        INSERT INTO Cdi_mailing (
            mailing_mailing_id,
            mailing_name,
            mailing_sent_on,
            mailing_onderwerp
        )
        VALUES (
            @mailing_mailing_id,
            @mailing_name,
            @mailing_sent_on,
            @mailing_onderwerp
        );
    END
END;

CREATE OR ALTER PROCEDURE InsertCdiSentEmailClicks (
    @sentemail_kliks_clicks INT,
    @sentemail_kliks_contact VARCHAR(255),
    @sentemail_kliks_e_mail_versturen VARCHAR(255),
    @sentemail_kliks_sent_email_id VARCHAR(255)
)
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Cdi_sent_email_clicks WHERE sentemail_kliks_sent_email_id = @sentemail_kliks_sent_email_id)
    BEGIN
        INSERT INTO Cdi_sent_email_clicks (
            sentemail_kliks_clicks,
            sentemail_kliks_contact,
            sentemail_kliks_e_mail_versturen,
            sentemail_kliks_sent_email_id
        )
        VALUES (
            @sentemail_kliks_clicks,
            @sentemail_kliks_contact,
            @sentemail_kliks_e_mail_versturen,
            @sentemail_kliks_sent_email_id
        );
    END
END;

CREATE OR ALTER PROCEDURE InsertCdiVisit (
    @visit_adobe_reader VARCHAR(255),
    @visit_bounce VARCHAR(255),
    @visit_browser VARCHAR(255),
    @visit_campaign VARCHAR(255),
    @visit_ip_stad VARCHAR(255),
    @visit_ip_company VARCHAR(255),
    @visit_contact VARCHAR(255),
    @visit_contact_naam_ VARCHAR(255),
    @visit_containssocialprofile VARCHAR(255),
    @visit_ip_land VARCHAR(255),
    @visit_duration FLOAT,
    @visit_email_send VARCHAR(255),
    @visit_ended_on VARCHAR(255),
    @visit_entry_page VARCHAR(2000),
    @visit_exit_page VARCHAR(2000),
    @visit_first_visit VARCHAR(255),
    @visit_ip_address VARCHAR(255),
    @visit_ip_organization VARCHAR(255),
    @visit_keywords VARCHAR(255),
    @visit_ip_latitude FLOAT,
    @visit_ip_longitude FLOAT,
    @visit_operating_system VARCHAR(255),
    @visit_ip_postcode VARCHAR(255),
    @visit_referrer VARCHAR(2000),
    @visit_referring_host VARCHAR(255),
    @visit_score FLOAT,
    @visit_referrer_type VARCHAR(255),
    @visit_started_on VARCHAR(255),
    @visit_ip_status VARCHAR(255),
    @visit_time VARCHAR(255),
    @visit_total_pages FLOAT,
    @visit_visit_id VARCHAR(255),
    @visit_aangemaakt_op VARCHAR(255),
    @visit_gewijzigd_op VARCHAR(255)
)
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Cdi_visits WHERE visit_visit_id = @visit_visit_id)
    BEGIN
        INSERT INTO Cdi_visits (
            visit_adobe_reader,
            visit_bounce,
            visit_browser,
            visit_campaign,
            visit_ip_stad,
            visit_ip_company,
            visit_contact,
            visit_contact_naam_,
            visit_containssocialprofile,
            visit_ip_land,
            visit_duration,
            visit_email_send,
            visit_ended_on,
            visit_entry_page,
            visit_exit_page,
            visit_first_visit,
            visit_ip_address,
            visit_ip_organization,
            visit_keywords,
            visit_ip_latitude,
            visit_ip_longitude,
            visit_operating_system,
            visit_ip_postcode,
            visit_referrer,
            visit_referring_host,
            visit_score,
            visit_referrer_type,
            visit_started_on,
            visit_ip_status,
            visit_time,
            visit_total_pages,
            visit_visit_id,
            visit_aangemaakt_op,
            visit_gewijzigd_op
        )
        VALUES (
            @visit_adobe_reader,
            @visit_bounce,
            @visit_browser,
            @visit_campaign,
            @visit_ip_stad,
            @visit_ip_company,
            @visit_contact,
            @visit_contact_naam_,
            @visit_containssocialprofile,
            @visit_ip_land,
            @visit_duration,
            @visit_email_send,
            @visit_ended_on,
            @visit_entry_page,
            @visit_exit_page,
            @visit_first_visit,
            @visit_ip_address,
            @visit_ip_organization,
            @visit_keywords,
            @visit_ip_latitude,
            @visit_ip_longitude,
            @visit_operating_system,
            @visit_ip_postcode,
            @visit_referrer,
            @visit_referring_host,
            @visit_score,
            @visit_referrer_type,
            @visit_started_on,
            @visit_ip_status,
            @visit_time,
            @visit_total_pages,
            @visit_visit_id,
            @visit_aangemaakt_op,
            @visit_gewijzigd_op
        );
    END
END;

CREATE OR ALTER PROCEDURE InsertCdiPageview (
    @browser VARCHAR(255),
    @campaign VARCHAR(255),
    @contact VARCHAR(255),
    @duration FLOAT,
    @operatingsystem VARCHAR(255),
    @pageview_id VARCHAR(255),
    @referrertype VARCHAR(255),
    @time VARCHAR(255),
    @pagetitle VARCHAR(255),
    @type VARCHAR(255),
    @url VARCHAR(2000),
    @viewedon VARCHAR(255),
    @visit VARCHAR(255),
    @visitorkey VARCHAR(255),
    @webcontent VARCHAR(255),
    @aangemaaktop VARCHAR(255),
    @gewijzigddoor VARCHAR(255),
    @gewijzigdop VARCHAR(255),
    @status VARCHAR(255),
    @redenvanstatus VARCHAR(255)
)
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Cdi_pageviews WHERE pageview_id = @pageview_id)
    BEGIN
        INSERT INTO Cdi_pageviews (
            browser,
            campaign,
            contact,
            duration,
            operatingsystem,
            pageview_id,
            referrertype,
            time,
            pagetitle,
            type,
            url,
            viewedon,
            visit,
            visitorkey,
            webcontent,
            aangemaaktop,
            gewijzigddoor,
            gewijzigdop,
            status,
            redenvanstatus
        )
        VALUES (
            @browser,
            @campaign,
            @contact,
            @duration,
            @operatingsystem,
            @pageview_id,
            @referrertype,
            @time,
            @pagetitle,
            @type,
            @url,
            @viewedon,
            @visit,
            @visitorkey,
            @webcontent,
            @aangemaaktop,
            @gewijzigddoor,
            @gewijzigdop,
            @status,
            @redenvanstatus
        );
    END
END;

CREATE OR ALTER PROCEDURE InsertFunctie (
    @functie_functie_id VARCHAR(255),
    @functie_naam VARCHAR(255)
)
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Functie WHERE functie_functie_id = @functie_functie_id)
    BEGIN
        INSERT INTO Functie (
            functie_functie_id,
            functie_naam
        )
        VALUES (
            @functie_functie_id,
            @functie_naam
        );
    END
END;

CREATE OR ALTER PROCEDURE InsertContactFunctie (
    @contactfunctie_contactpersoon VARCHAR(255),
    @contactfunctie_functie VARCHAR(255)
)
AS
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM Contact_functie
        WHERE contactfunctie_contactpersoon = @contactfunctie_contactpersoon
        AND contactfunctie_functie = @contactfunctie_functie
    )
    BEGIN
        INSERT INTO Contact_functie (
            contactfunctie_contactpersoon,
            contactfunctie_functie
        )
        VALUES (
            @contactfunctie_contactpersoon,
            @contactfunctie_functie
        );
    END
END;

CREATE OR ALTER PROCEDURE InsertGebruiker (
    @gebruikers_crm_user_id_id VARCHAR(255),
    @gebruikers_business_unit_naam_ VARCHAR(255)
)
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Gebruikers WHERE gebruikers_crm_user_id_id = @gebruikers_crm_user_id_id)
    BEGIN
        INSERT INTO Gebruikers (
            gebruikers_crm_user_id_id,
            gebruikers_business_unit_naam_
        )
        VALUES (
            @gebruikers_crm_user_id_id,
            @gebruikers_business_unit_naam_
        );
    END
END;

CREATE OR ALTER PROCEDURE InsertInfoEnKlacht (
    @info_en_klachten_aanvraag_id VARCHAR(255),
    @info_en_klachten_account VARCHAR(255),
    @info_en_klachten_datum DATE,
    @info_en_klachten_datum_afsluiting DATE,
    @info_en_klachten_status VARCHAR(255),
    @info_en_klachten_eigenaar VARCHAR(255)
)
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Info_en_klachten WHERE info_en_klachten_aanvraag_id = @info_en_klachten_aanvraag_id)
    BEGIN
        INSERT INTO Info_en_klachten (
            info_en_klachten_aanvraag_id,
            info_en_klachten_account,
            info_en_klachten_datum,
            info_en_klachten_datum_afsluiting,
            info_en_klachten_status,
            info_en_klachten_eigenaar
        )
        VALUES (
            @info_en_klachten_aanvraag_id,
            @info_en_klachten_account,
            @info_en_klachten_datum,
            @info_en_klachten_datum_afsluiting,
            @info_en_klachten_status,
            @info_en_klachten_eigenaar
        );
    END
END;

CREATE OR ALTER PROCEDURE InsertInschrijving (
    @inschrijving_aanwezig_afwezig VARCHAR(255),
    @inschrijving_bron VARCHAR(255),
    @inschrijving_contactfiche VARCHAR(255),
    @inschrijving_datum_inschrijving DATE,
    @inschrijving_inschrijving_id VARCHAR(255),
    @inschrijving_facturatie_bedrag VARCHAR(255),
    @inschrijving_campagne VARCHAR(255),
    @inschrijving_campagne_naam_ VARCHAR(255)
)
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Inschrijving WHERE inschrijving_inschrijving_id = @inschrijving_inschrijving_id)
    BEGIN
        INSERT INTO Inschrijving (
            inschrijving_aanwezig_afwezig,
            inschrijving_bron,
            inschrijving_contactfiche,
            inschrijving_datum_inschrijving,
            inschrijving_inschrijving_id,
            inschrijving_facturatie_bedrag,
            inschrijving_campagne,
            inschrijving_campagne_naam_
        )
        VALUES (
            @inschrijving_aanwezig_afwezig,
            @inschrijving_bron,
            @inschrijving_contactfiche,
            @inschrijving_datum_inschrijving,
            @inschrijving_inschrijving_id,
            @inschrijving_facturatie_bedrag,
            @inschrijving_campagne,
            @inschrijving_campagne_naam_
        );
    END
END;

CREATE OR ALTER PROCEDURE InsertLidmaatschap (
    @lidmaatschap_datum_opzeg DATE,
    @lidmaatschap_lidmaatschap_id VARCHAR(255),
    @lidmaatschap_onderneming VARCHAR(255),
    @lidmaatschap_reden_aangroei VARCHAR(255),
    @lidmaatschap_reden_verloop VARCHAR(255),
    @lidmaatschap_startdatum DATE
)
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Lidmaatschap WHERE lidmaatschap_lidmaatschap_id = @lidmaatschap_lidmaatschap_id)
    BEGIN
        INSERT INTO Lidmaatschap (
            lidmaatschap_datum_opzeg,
            lidmaatschap_lidmaatschap_id,
            lidmaatschap_onderneming,
            lidmaatschap_reden_aangroei,
            lidmaatschap_reden_verloop,
            lidmaatschap_startdatum
        )
        VALUES (
            @lidmaatschap_datum_opzeg,
            @lidmaatschap_lidmaatschap_id,
            @lidmaatschap_onderneming,
            @lidmaatschap_reden_aangroei,
            @lidmaatschap_reden_verloop,
            @lidmaatschap_startdatum
        );
    END
END;

CREATE OR ALTER PROCEDURE InsertSessie (
    @sessie_activiteitstype VARCHAR(255),
    @sessie_campagne VARCHAR(255),
    @sessie_eind_datum_tijd DATE,
    @sessie_product VARCHAR(255),
    @sessie_sessie_id VARCHAR(255),
    @sessie_sessie_nr_ VARCHAR(255),
    @sessie_start_datum_tijd DATE,
    @sessie_thema_naam_ VARCHAR(255)
)
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Sessie WHERE sessie_sessie_id = @sessie_sessie_id)
    BEGIN
        INSERT INTO Sessie (
            sessie_activiteitstype,
            sessie_campagne,
            sessie_eind_datum_tijd,
            sessie_product,
            sessie_sessie_id,
            sessie_sessie_nr_,
            sessie_start_datum_tijd,
            sessie_thema_naam_
        )
        VALUES (
            @sessie_activiteitstype,
            @sessie_campagne,
            @sessie_eind_datum_tijd,
            @sessie_product,
            @sessie_sessie_id,
            @sessie_sessie_nr_,
            @sessie_start_datum_tijd,
            @sessie_thema_naam_
        );
    END
END;

CREATE OR ALTER PROCEDURE InsertSessieInschrijving (
    @sessieinschrijving_sessieinschrijving_id VARCHAR(255),
    @sessieinschrijving_sessie VARCHAR(255),
    @sessieinschrijving_inschrijving VARCHAR(255)
)
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Sessie_inschrijving WHERE sessieinschrijving_sessieinschrijving_id = @sessieinschrijving_sessieinschrijving_id)
    BEGIN
        INSERT INTO Sessie_inschrijving (
            sessieinschrijving_sessieinschrijving_id,
            sessieinschrijving_sessie,
            sessieinschrijving_inschrijving
        )
        VALUES (
            @sessieinschrijving_sessieinschrijving_id,
            @sessieinschrijving_sessie,
            @sessieinschrijving_inschrijving
        );
    END
END;

CREATE OR ALTER PROCEDURE InsertTeam (
    @team_code_selecteer_uit_lijst_ VARCHAR(255),
    @activiteit_boeking_naam_ter_info_ VARCHAR(255)
)
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Teams WHERE xls_teams_team_code_selecteer_uit_lijst_ = @team_code_selecteer_uit_lijst_)
    BEGIN
        INSERT INTO Teams (
            xls_teams_team_code_selecteer_uit_lijst_,
            xls_teams_activiteit_boeking_naam_ter_info_
        )
        VALUES (
            @team_code_selecteer_uit_lijst_,
            @activiteit_boeking_naam_ter_info_
        );
    END
END;