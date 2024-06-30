import logging
import os


class Databaze:

    def __init__(self) -> None:
        self.cesta = os.path.dirname(__file__)
        self.nazev = os.path.join(self.cesta, 'prikaz.sql')

        self.prodeje = []
        self.nakupy = []
        self.knihy = []
        self.zamestnanci = []
        self.spisovatele = []
        self.zakaznici = []
        self.nakladatele = []
        self.kategorie = []
        self.datumy = []
        self.exemplare = []

    def import_dat(self, 
        prodeje,
        nakupy,
        knihy,
        zamestnanci,
        spisovatele,
        zakaznici,
        nakladatele,
        kategorie,
        datumy,
        exemplare
    ) -> None:
        """ Funkce pro import dat z generování
        """
        self.prodeje = prodeje
        self.nakupy = nakupy
        self.knihy = knihy
        self.zamestnanci = zamestnanci
        self.spisovatele = spisovatele
        self.zakaznici = zakaznici
        self.nakladatele = nakladatele
        self.kategorie = kategorie
        self.datumy = datumy
        self.exemplare = exemplare
 
    def smazani_prikazu(self) -> None:
        """ Smaže původní záznamy ze souboru s SQL příkazem
        """
        with open(self.nazev, 'w', encoding='utf8') as s:
            pass
            s.close()
        logging.info('Soubor se podařilo před zápisem smazat.')

    def ulozeni_prikazu(self, prikaz):
        """ Metoda pro uložení SQL příkazu. Připojení na
        konec souboru
        """
        try:
            with open(self.nazev, 'a', encoding='utf8') as s:
                s.write(prikaz)
                s.write('\n')
        except FileNotFoundError:
            logging.info('Soubor se nepodařilo uložit')

    # Metoda pro uložení tabulky
    def ulozeni_tabulky(self, tabulka):
        try:
            with open(self.nazev, 'a', encoding='utf8') as s:
                temp = ''
                res = ''
                for i in tabulka:

                    # Do výsledné proměnné se vloží celý postupně
                    # složený text, odebere se poslední čárka 
                    # a na konec vloží se středník
                    temp += str(i.format_sql()).replace('\'null\'', 'null') + '\n'
                    res = temp[:-2] + ';' 
                s.write(res)
                s.write('\nGO\n')
        except FileNotFoundError:
            logging.info('Soubor se nepodařilo uložit')

    # Metoda pro uložení velké tabulky
    def ulozeni_rozsahle_tabulky(self, tabulka, hlavicka):
        try:
            with open(self.nazev, 'a', encoding='utf8') as s:
                for i in range(0, len(tabulka), 1000):
                    s.write(hlavicka)
                    s.write('\n')
                    temp = ''
                    res = ''
                    for j in tabulka[i: i + 1000]:
                        temp += str(j.format_sql()) + '\n'
                    res = temp[:-2] + ';' 
                    s.write(res)
                    s.write('\nGO\n')
        except FileNotFoundError:
            logging.info('Soubor se nepodařilo uložit')
