import pytest
import mysql.connector as mc
from src.Task_manager2 import Ukoly, Menu, Pomocnik, Databaze

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
    pomocnik_instance = Pomocnik(db_instance, table_name="test_TM2")
    return Ukoly(db_instance, pomocnik_instance, table_name="test_TM2")


def test_pridat_ukol_pozitivni(ukoly):
    # pozitivní test
    ukoly.pridat_ukol(ukol_nazev="Testovací Úkol", ukol_popis="Testovací Popis")
    # ověření předání dat do tabulky testovací databáze
    ukoly.db.cursor.execute(f"SELECT nazev, popis FROM {ukoly.table_name} WHERE nazev = %s", ("Testovací Úkol",))
    result = ukoly.db.cursor.fetchone()
    assert result is not None, "Úkol nebyl přidán do databáze."
    assert result[0] == "Testovací Úkol", "Název nesouhlasí."
    assert result[1] == "Testovací Popis", "Popis nesouhlasí."

def test_aktualizovat_ukol(ukoly):
    #pozitivní test
    # spuštění metody pro aktualizaci ukolu
    ukoly.aktualizovat_ukoly(ukol_cislo = 1, volba_stav = 2 )

    # Ověření, že stav byl aktualizován
    ukoly.db.cursor.execute(f"SELECT stav FROM {ukoly.table_name} WHERE nazev = %s", ("Testovací Úkol",))
    result = ukoly.db.cursor.fetchone()
    assert result is not None, "Úkol nebyl nalezen."
    assert result[0] == "Hotovo", "Stav úkolu nebyl správně aktualizován."

def test_odstranit_ukol(ukoly):
    #pozitivní test
    # spuštění metody pro aktualizaci ukolu
    ukoly.odstranit_ukol(ukol_cislo = 1)

    # ověření, že byl úkol odstraněn
    ukoly.db.cursor.execute(f"SELECT * FROM {ukoly.table_name} WHERE id = %s", (1,))
    result = ukoly.db.cursor.fetchone()
    assert result is None, "Úkol nebyl úspěšně odstraněn z databáze."

