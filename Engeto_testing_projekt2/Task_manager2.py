import mysql.connector as mc
import mysql.connector.errors as err

#nastavení připojení k databázi ⚠️
try:
    conn = mc.connect(
        host="localhost",
        user="root",
        password="alatriste",
        database="sys"
    )
    print('připojení k databázi se zdařilo')
except err:
    print(f'chyba v připojení{err}')

# Vytvoření kurzoru pro provádění SQL příkazů
cursor = conn.cursor()

# Tvorba tabulky v databazi, pokud neexistuje
try:
    cursor.execute('''
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
        print(f'nastala chyba při vytváření tabulky {err}')

###
# Hlavní část kódu ⬇️🚧💭
# 1. vložení kodu z TM1
# 2. úprava kodu z TM1 - ošetření chyb zjištěných v testu
# 3. implementace připojení databáze k programu
#
# ###







# uzavření kurzoru a ukončení připojení k databází ⛔
cursor.close()
conn.close()