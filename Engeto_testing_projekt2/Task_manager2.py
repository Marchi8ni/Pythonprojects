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
                host="localhost",
                user="root",
                password="alatriste",
                database="sys"
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
    @staticmethod
    def chybova_hlaska():
        """Zobrazí chybovou hlášku"""
        print(f"Nastala neočekávaná chyba: \n {err}")

    @staticmethod
    def overeni_id(db):
        """Ověří, zda existuje zadané ID v databázi."""
        try:
            ukol_cislo = int(input("\n Vyberte id úkolu, který chcete aktualizovat/odstranit: "))
            db.cursor.execute("SELECT id from ukoly where id = %s", (ukol_cislo,))
            id_check = db.cursor.fetchone()
            return ukol_cislo, id_check
        except err:
            Pomocnik.chybova_hlaska()

    @staticmethod
    def overeni_dat(db, query):
        """Ověří, zda existují úkoly v db."""
        try:
            db.cursor.execute(query)
            prvni_zaznam = db.cursor.fetchone()[0]
            if prvni_zaznam is None:
                print("Seznam úkolů je prázdný.")
            else:
                print("Seznam úkolů:")
                vsechny_zaznamy = db.cursor.fetchall()
                for row in vsechny_zaznamy:
                    print(row)
        except err:
            Pomocnik.chybova_hlaska()


class Ukoly:
    def pridat_ukol(self):
        ukol_nazev = input("Zadejte název úkolu: ")
        ukol_popis = input("Zadejte popis úkolu:")
        datum = dt.datetime.now()
        if ukol_nazev and ukol_popis != "":
           try:
                db.cursor.execute("Insert into ukoly (nazev, popis, stav, datum_vytvoreni) VALUES(%s, %s, %s, %s)", (ukol_nazev, ukol_popis,"Nezahájeno",datum))
                db.conn.commit()
                print(f"Úkol '{ukol_nazev}' byl přidán.")
           except err:
               Pomocnik.chybova_hlaska()

        else:
            print('název a popis nesmí být prázdný text. Opakuj volbu!')

    def zobrazit_ukoly(self):
        query = "SELECT id, nazev, popis, stav FROM ukoly WHERE stav IN ('Probíhá', 'nezahájeno')"
        Pomocnik.overeni_dat(db, query)

    def aktualizovat_ukoly(self):
        ###
        # Změna stavu úkolu
        # - Uživatel vidí seznam úkolů (ID, název, stav).
        # - Vybere úkol podle ID.
        # - Dostane na výběr nový stav: "Probíhá" nebo "Hotovo"
        # - Po potvrzení se aktualizuje DB.
        # - Pokud zadá neexistující ID, program ho upozorní a nechá ho vybrat znovu.
        #
        # ###

        query = "SELECT ID, nazev, stav FROM ukoly"
        Pomocnik.overeni_dat(db, query)
        try:
            ukol_cislo, id_check = Pomocnik.overeni_id(db)
            if not id_check:
                print('Zadejte platné ID!')
            else:
                volba_stav = int(input('zadejte číslo stavu úkolu: \n č.1 - Probíhá \n č.2 - Hotovo '))
                if volba_stav == 1:
                    novy_stav = "Probíhá"
                elif volba_stav == 2:
                    novy_stav = "Hotovo"
                else:
                    print("Neplatná volba, opakujte zadání!")
        except ValueError:
            print('Zadejte číselnou hodnotu!')
        except err:
            Pomocnik.chybova_hlaska()

        db.cursor.execute("UPDATE ukoly set stav = %s where id = %s", (novy_stav, ukol_cislo))
        db.conn.commit()
        print("Stav úkolu byl úspěšně změněn")


    def odstranit_ukol(self):
        query = "SELECT * FROM ukoly"
        Pomocnik.overeni_dat(db, query)

        ukol_cislo, id_check = Pomocnik.overeni_id(db)
        if not id_check:
            print('Zadejte platné ID')
        else:
            db.cursor.execute("DELETE FROM ukoly WHERE id = %s", (ukol_cislo,))
            db.conn.commit()
            print(f"Záznam s ID {ukol_cislo} byl úspěšně odstraněn.")

# Vytvoření instancí mimo smyčku

menu = Menu()
ukoly_instance = Ukoly()

# připojení k databázi
db = Databaze()
db.pripojeni_db()

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
db.cursor.close()
db.conn.close()
