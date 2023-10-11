from sqlalchemy import Column, Integer, Float, String, ForeignKey
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = sqlalchemy.orm.declarative_base()

class Account_activiteitscode(Base):
    __tablename__ = 'Account_activiteitscode'
    account_activiteitscode_account = Column(String(255), ForeignKey('Account.account_account_id'))
    account_activiteitscode_activiteitscode = Column(String(255), ForeignKey('Activiteitscode.activiteitscode_activiteitscode_id'))
    account_activiteitscode_inf_account_inf_activiteitscodeid = Column(String(255))

class Account(Base):
    __tablename__ = 'Account'
    account_account_id = Column(String(255), primary_key=True)
    account_adres_geografische_regio = Column(String(255))
    account_adres_geografische_subregio = Column(String(255))
    account_adres_plaats = Column(String(255))
    account_adres_postcode = Column(String(255))
    account_adres_provincie = Column(String(255))
    account_industriezone_naam_ = Column(String(255))
    account_is_voka_entiteit = Column(Integer)
    account_ondernemingsaard = Column(String(255))
    account_ondernemingstype = Column(String(255))
    account_oprichtingsdatum = Column(String(255))
    account_primaire_activiteit = Column(String(255))
    account_reden_van_status = Column(String(255))
    account_status = Column(Integer)
    account_voka_nr_ = Column(Integer)
    account_adres_land = Column(String(255))

class Account_financiële_data(Base):
    __tablename__ = 'Account_financiële_data'
    financieledata_ondernemingid = Column(String(255), ForeignKey('Account.account_account_id'))
    financieledata_boekjaar = Column(Integer)
    financieledata_aantal_maanden = Column(Float)
    financieledata_toegevoegde_waarde = Column(String(255))
    financieledata_fte = Column(String(255))
    financieledata_gewijzigd_op = Column(String(255))

class Activiteit_vereist_contact(Base):
    __tablename__ = 'Activiteit_vereist_contact'
    activiteitvereistcontact_activityid_id = Column(String(255), ForeignKey('Afspraak_alle.afspraak_alle_afspraak_id'), primary_key=True)
    activiteitvereistcontact_reqattendee = Column(String(255), ForeignKey('Contact.contact_contactpersoon_id'))