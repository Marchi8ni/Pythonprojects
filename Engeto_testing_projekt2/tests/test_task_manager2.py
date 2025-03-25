import pytest
import mysql.connector as mc
from Engeto_testing_projekt2.src.Task_manager2 import Ukoly, Menu, Pomocnik, Databaze

@pytest.fixture(scope="module")
def db_connection():
    spojeni = mc.connect(
        host="localhost",
        user="root",
        password="alatriste",
        database="testovaci"
    )
    kurzor = spojeni.cursor()

    kurzor.execute('''
                create table IF NOT EXISTS test_TM2(
            	id int primary key auto_increment,
            	nazev varchar(50),
                popis varchar(100),
                stav varchar(25),
                datum_vytvoreni DATE
            );  
                ''')
    spojeni.commit()

    # předání spojení a kurzoru testům !
    yield spojeni

    # cleaning
    kurzor.execute("DROP TABLE IF EXISTS test_TM2")
    spojeni.commit()

    kurzor.close()
    spojeni.close()

@pytest.fixture()
def ukoly(db_connection):
    db_instance = Databaze(database="testovaci")
    db_instance.conn = db_connection
    db_instance.cursor = db_connection.cursor()
    return Ukoly(db_instance, table_name="test_TM2")


def test_pridat_ukol(ukoly):
    # pozitivní test
    ukoly.pridat_ukol()



