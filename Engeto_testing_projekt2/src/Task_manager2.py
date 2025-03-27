import mysql.connector as mc
import mysql.connector.errors as err
import datetime as dt


###
# Hlavní část kódu ⬇️🚧💭
# 1. vložení kodu z TM1 ✅
# 2. úprava kodu z TM1 - ošetření chyb zjištěných v testu ✅
# 3. implementace připojení databáze k programu ✅ - ošetření tvorbou class Databaze
# 4. implementace nové metody pro aktualizaci ukolů ✅ - def aktualizovat_ukoly()
# 5. refaktoring pro zajištění metody DRY -- opakuje se: ✅
#       - ověření id
#       - ošetření chyb
#       - ověření dat v db
#       Návrh -> vytvoření nové class Pomocník
# ###


class Databaze:
    def __init__(self, host="localhost", user="root", password="alatriste", database="sys"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None

    def pripojeni_db(self):

        # nastavení připojení k databázi ⚠️
        try:
            self.conn = mc.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            # If conn Ok, vytvoří se kurzor pro provádění SQL příkazů ️
            self.cursor = self.conn.cursor()
            print('připojení k databázi se zdařilo')
        except err:
            Pomocnik.chybova_hlaska()


    def vytvoreni_tabulky(self):
        # Tvorba tabulky v databazi, pokud neexistuje
        try:
            self.cursor.execute('''
            create table IF NOT EXISTS ukoly(
        	id int primary key auto_increment,
        	nazev varchar(50),
            popis varchar(100),
            stav varchar(25),
            datum_vytvoreni DATE
        );  
            '''
                           )
        except err:
            Pomocnik.chybova_hlaska()


class Menu:
    def zobrazit(self):
        print("Správce úkolů - Hlavní menu \n 1. Přidat nový úkol \n 2. Zobrazit úkoly \n 3. Aktualizovat úkol \n 4. Odstranit úkol \n 5. Konec Programu ")


class Pomocnik:
    def __init__(self, db_instance, table_name="ukoly"):
        self.db = db_instance
        self.table_name = table_name

    def chybova_hlaska(self):
        """Zobrazí chybovou hlášku"""
        print(f"Nastala neočekávaná chyba: \n {err}")


    def overeni_id(self, ukol_cislo=None):
        """Ověří, zda existuje zadané ID v databázi."""
        if ukol_cislo is None:
            ukol_cislo = int(input("\n Vyberte id úkolu, který chcete aktualizovat/odstranit: "))
        try:
            self.db.cursor.execute(f"SELECT id from {self.table_name} where id = %s", (ukol_cislo,))
            id_check = self.db.cursor.fetchone()
            return ukol_cislo, id_check
        except err:
            self.chybova_hlaska()

    def overeni_dat(self, query):
        """Ověří, zda existují úkoly v db."""
        try:
            self.db.cursor.execute(query)
            prvni_zaznam = self.db.cursor.fetchone()[0]
            if prvni_zaznam is None:
                print("Seznam úkolů je prázdný.")
            else:
                print("Seznam úkolů:")
                vsechny_zaznamy = self.db.cursor.fetchall()
                for row in vsechny_zaznamy:
                    print(row)
        except err:
            self.chybova_hlaska()


class Ukoly:
    def __init__(self, db_instance, pomocnik_instance, table_name="ukoly"):
        self.db = db_instance
        self.table_name = table_name
        self.pomocnik = pomocnik_instance
    def pridat_ukol(self, ukol_nazev=None, ukol_popis= None):
        if ukol_nazev is None:
            ukol_nazev = input("Zadejte název úkolu: ").strip()
        if ukol_popis is None:
            ukol_popis = input("Zadejte popis úkolu:").strip()
        datum = dt.datetime.now()
        if ukol_nazev != "" and ukol_popis != "":
           try:
                query=f"INSERT INTO {self.table_name} (nazev, popis, stav, datum_vytvoreni) VALUES (%s, %s, %s, %s)"
                self.db.cursor.execute(query, (ukol_nazev, ukol_popis,"Nezahájeno",datum))
                self.db.conn.commit()
                print(f"Úkol '{ukol_nazev}' byl přidán.")
           except err:
               self.pomocnik.chybova_hlaska()

        else:
            print('název a popis nesmí být prázdný text. Opakuj volbu!')

    def zobrazit_ukoly(self):
        query = f"SELECT id, nazev, popis, stav FROM {self.table_name} WHERE stav IN ('Probíhá', 'nezahájeno')"
        self.pomocnik.overeni_dat(query)

    def aktualizovat_ukoly(self, volba_stav = None, ukol_cislo = None):
        ###
        # Změna stavu úkolu
        # - Uživatel vidí seznam úkolů (ID, název, stav).
        # - Vybere úkol podle ID.
        # - Dostane na výběr nový stav: "Probíhá" nebo "Hotovo"
        # - Po potvrzení se aktualizuje DB.
        # - Pokud zadá neexistující ID, program ho upozorní a nechá ho vybrat znovu.
        #
        # ###

        query = f"SELECT ID, nazev, stav FROM {self.table_name}"
        self.pomocnik.overeni_dat(query)
        try:
            ukol_cislo, id_check = self.pomocnik.overeni_id(ukol_cislo)
            if not id_check:
                print('Zadejte platné ID!')
            else:
                if volba_stav is None:
                    try:
                        volba_stav = int(input('zadejte číslo stavu úkolu: \n č.1 - Probíhá \n č.2 - Hotovo '))
                        if volba_stav not in [1,2]:
                            print("Neplatná volba, opakujte zadání!")
                    except ValueError:
                        print('Zadejte číselnou hodnotu!')

                novy_stav = "Probíhá" if volba_stav == 1 else "Hotovo"

        except err:
            self.pomocnik.chybova_hlaska()

        self.db.cursor.execute(f"UPDATE {self.table_name} set stav = %s where id = %s", (novy_stav, ukol_cislo))
        self.db.conn.commit()
        print("Stav úkolu byl úspěšně změněn")


    def odstranit_ukol(self, ukol_cislo=None):
        query = f"SELECT * FROM {self.table_name}"
        self.pomocnik.overeni_dat(query)

        ukol_cislo, id_check = self.pomocnik.overeni_id(ukol_cislo)
        if not id_check:
            print('Zadejte platné ID')
        else:
            self.db.cursor.execute(f"DELETE FROM {self.table_name} WHERE id = %s", (ukol_cislo,))
            self.db.conn.commit()
            print(f"Záznam s ID {ukol_cislo} byl úspěšně odstraněn.")


if __name__ == "__main__":
    # připojení k databázi
    db_instance = Databaze()
    db_instance.pripojeni_db()

    # Vytvoření instancí mimo smyčku

    pomocnik_instance = Pomocnik(db_instance)
    ukoly_instance = Ukoly(db_instance, pomocnik_instance)
    menu = Menu()

    # Hlavní smyčka programu
    while True:

        menu.zobrazit()
        try:
            volba = int(input("Vyberte možnost (1-5): "))

            if volba == 1:
                ukoly_instance.pridat_ukol()
            elif volba == 2:
                ukoly_instance.zobrazit_ukoly()
            elif volba == 3:
                ukoly_instance.aktualizovat_ukoly()
            elif volba == 4:
                ukoly_instance.odstranit_ukol()
            elif volba == 5:
                print("Program byl ukončen.")
                break
            else:
                print("Neplatná volba. Zkuste to znovu.")
        except ValueError:
            print('Neplatná volba, zkuste zadat znovu!')


    # uzavření kurzoru a ukončení připojení k databází ⛔
    db_instance.cursor.close()
    db_instance.conn.close()
