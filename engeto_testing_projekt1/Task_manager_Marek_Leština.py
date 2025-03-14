ukoly = []

class Menu:
    def zobrazit(self):
        print("Správce úkolů - Hlavní menu")
        print("1. Přidat nový úkol")
        print("2. Zobrazit úkoly")
        print("3. Odstranit úkol")
        print("4. Konec Programu")

class Ukoly:
    def pridat_ukol(self):
        ukol_nazev = input("Zadejte název úkolu: ")
        ukol_popis = input("Zadejte popis úkolu:")
        if ukol_nazev and ukol_popis != "":
            ukoly.append((ukol_nazev, ukol_popis))
            print(f"Úkol '{ukol_nazev}' byl přidán.")
        else:
            print('název a popis nesmí být prázdný text. Opakuj volbu!')

    def zobrazit_ukoly(self):
        if not ukoly:
            print("Seznam úkolů je prázdný.")
        else:
            print("Seznam úkolů:")
            for index, ukol in enumerate(ukoly, start=1):
                print(f"{index}. {ukol[0]} - {ukol[1]}")

    def odstranit_ukol(self):
        if not ukoly:
            print("Seznam úkolů je prázdný, není co odstranit.")
            return

        self.zobrazit_ukoly()
        try:
            ukol_cislo = int(input("Zadejte číslo úkolu, který chcete odstranit: "))
            if 1 <= ukol_cislo <= len(ukoly):
                odstranovany_ukol = ukoly.pop(ukol_cislo - 1)
                print(f"Úkol '{odstranovany_ukol}' byl odstraněn.")
            else:
                print("Neplatné číslo úkolu.")
        except ValueError:
            print("Neplatný vstup. Zadejte číslo.")

# Vytvoření instancí mimo smyčku
menu = Menu()
ukoly_instance = Ukoly()

# Hlavní smyčka programu
while True:
    menu.zobrazit()
    volba = int(input("Vyberte možnost (1-4): "))

    if volba == 1:
        ukoly_instance.pridat_ukol()
    elif volba == 2:
        ukoly_instance.zobrazit_ukoly()
    elif volba == 3:
        ukoly_instance.odstranit_ukol()
    elif volba == 4:
        print("Program byl ukončen.")
        break
    else:
        print("Neplatná volba. Zkuste to znovu.")

