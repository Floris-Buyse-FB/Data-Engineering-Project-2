from sqlalchemy import Column, Integer, Float, String, ForeignKey
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = sqlalchemy.orm.declarative_base()

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