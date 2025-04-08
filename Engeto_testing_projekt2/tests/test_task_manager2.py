import pytest
import mysql.connector as mc
from src.Task_manager2 import Ukoly, Pomocnik, Databaze

# Nastavení testovací databáze
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

# spojení databáze se zdrojovým kodem
@pytest.fixture()
def ukoly(db_connection):
    db_instance = Databaze(database="testovaci")
    db_instance.conn = db_connection
    db_instance.cursor = db_connection.cursor()
    pomocnik_instance = Pomocnik(db_instance, table_name="test_TM2")
    return Ukoly(db_instance, pomocnik_instance, table_name="test_TM2")

# Pozitivní testy:


def test_pridat_ukol(ukoly):
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

# Negativní testy:

@pytest.mark.parametrize("nazev, popis, ukol_cislo, volba_stav, ocekavana_hodnota", [
    # Testy pro pridat_ukol
    ('A' * 51, 'B' * 101, None, None, mc.errors.DataError),  # Překročení délky sloupce
    ("", "", None, None, ValueError),  # Prázdné hodnoty pro nazev a popis

    # Testy pro aktualizovat_ukoly
    (None, None, 9999, None, ValueError),  # Neexistující ID
    (None, None, "abc", None, ValueError),  # Neplatná hodnota ID (není číslo)
    (None, None, 1, 3, ValueError),  # Neplatná volba stavu (mimo rozsah možností)

    # Testy pro odstranit_ukol
    (None, None, 9999, None, ValueError),  # Neexistující ID
    (None, None, "xyz", None, ValueError),  # Neplatná hodnota ID (není číslo)
])
def test_neplatna_data(ukoly, nazev, popis, ukol_cislo, volba_stav, ocekavana_hodnota):
    with pytest.raises(ocekavana_hodnota):
        # Testování pridat_ukol
        if nazev is not None and popis is not None:
            ukoly.pridat_ukol(nazev, popis, testovaci_rezim=True)

        # Testování aktualizovat_ukoly
        if ukol_cislo is not None and volba_stav is not None:
            ukoly.aktualizovat_ukoly(volba_stav=volba_stav, ukol_cislo=ukol_cislo, testovaci_rezim=True)

        # Testování odstranit_ukol
        if ukol_cislo is not None:
            ukoly.odstranit_ukol(ukol_cislo, testovaci_rezim=True)



