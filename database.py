from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

engine = create_engine('sqlite:///smartkey.db')
Base = declarative_base()

# Dobivanje apsolutne putanje do mape "smartkey",
#tu sam bio žestoko zapeo
SMARTKEY_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SMARTKEY_DIR, "smartkey.db")

# Ostatak vašeg koda za definiranje baze podataka
engine = create_engine(f'sqlite:///{DB_PATH}')


class Osoba(Base):
    __tablename__ = 'osobe'

    id = Column(Integer, primary_key=True, index=True)
    ime = Column(String, index=True)
    prezime = Column(String, index=True)
    pin = Column(String, index=True) 
    aktivna = Column(Boolean, default=True)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def add_user(first_name, last_name, pin, admin=False):
    session = Session()
    user = Osoba(ime=first_name, prezime=last_name, pin=pin, aktivna=True)
    session.add(user)
    session.commit()
    session.close()

def edit_user(user_id, first_name, last_name, pin, active=True, admin=False):
    session = Session()
    user = session.query(Osoba).filter_by(id=user_id).first()
    if user:
        user.ime = first_name
        user.prezime = last_name
        user.pin = pin
        user.aktivna = active
        session.commit()
    session.close()

def delete_user(user_id):
    session = Session()
    user = session.query(Osoba).filter_by(id=user_id).first()
    if user:
        session.delete(user)
        session.commit()
    session.close()


