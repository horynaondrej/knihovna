#!/usr/bin/env python3
import logging 
import datetime
import random
import os
from exemplar import Exemplar
from nakup import Nakup
from prodej import Prodej
from kniha import Kniha
from spisovatel import Spisovatel
from zamestnanec import Zamestnanec
from zakaznik import Zakaznik


class Databaze:
    ''' Hlavní třída pro generování záznamů
    '''

    def __init__(self):

        self.cesta = os.path.dirname(__file__)

        self.exemplare = []
        self.prodej_klic = 1
        self.nakup_klic = 1
        self.exemplar_klic = 1
        self.prodeje = []
        self.nakupy = []
        self.knihy = []
        self.zamestnanci = []
        self.spisovatele = []
        self.zakaznici = []

        # Datum začátku provozu sklad knih
        self.datum = datetime.date(2024, 4, 1)

    def zapis_do_csv_souboru(self, hla, tab, n) -> None:
        """ Metoda zapíše data do souboru jako CSV.
        Pouze pro jenoduchý formáté
        """
        nazev = os.path.join(self.cesta, n)

        # Uložení do souboru
        with open(nazev, 'w', encoding='utf8') as s:
            s.write(hla + '\n')
            for nty in tab:
                s.write(str(nty.format_csv()) + '\n')
        logging.info(f'Zápis souboru {n} proběhl v pořádku')

    def najdi_exemplar(self):
        ''' Funkce pro nalezení exempláře knihy

        Return:
            Exemplar: obj
        '''

        for exemplar in self.exemplare:
            if exemplar.prodani is None:
                return exemplar
        return None
      
    def nalezni_cenu_nakupu(self, kniha_id: int) -> int:
        """ Funkce nalezne cenu z ceníku
        """

        return self.knihy[kniha_id - 1].cena
    
    def najdi_cenu_prodeje(self, exemplar: int) -> int:
        """ Funkce nalezne cenu nakoupené knihy a vrátí 
        její cenu

        Args:
            exemplar: objekt exemplar

        Return:
            nákupní cena zadaného exempláře
        """

        # print(f'Exemplář dohledávám: {exemplar}')
        # print(f'Pole exemplářů: {self.exemplare}')

        for nty in self.exemplare:
            if exemplar.klic == nty.klic:
                return self.knihy[nty.kniha_id - 1].cena
        return 0
    
    def nahodne_vahy(self, delka):
        """ Funkce vrací indexy pro výběr jen části pole
        """

        start = random.randint(0, delka)
        konec = random.randint(0, delka)

        # Když se čísla rovnají, vygeneruje se jiné
        # Když je rozdíl menší než 20, vygeneruje se jiné
        while start == konec or abs(start - konec) < 4:
            konec = random.randint(0, delka)

        # Když je start větší než konec, vrací se 
        # indexy v obráceném pořadí
        if start > konec:
            return konec, start
        else:
            return start, konec
    
    def generuj_prodej(self, exemplar):
        ''' Funkce pro generování záznamu o prodeji

        Arg:
            exemplar: obj

        Return:
            prodej: obj
            Upravuje datum prodeje exempláře
        '''

        # Upravení váhy výběru zákazníka
        vahy_zakaznici = [0] * len(self.zakaznici)
        zacatek, konec = self.nahodne_vahy(len(self.zakaznici))
        vahy_zakaznici[zacatek:konec] = [50] * (konec - zacatek)

        prodejni_cena = self.najdi_cenu_prodeje(exemplar)
        datum_prodeje = self.datum + datetime.timedelta(days=1)

        prodej = Prodej(
            self.prodej_klic, 
            datum_prodeje.strftime('%Y%m%d'),
            exemplar.klic,
            random.choices(self.zakaznici, weights=vahy_zakaznici, k=1)[0].zakaznik_id, 
            random.choices(self.zamestnanci)[0].zamestnanec_id, 
            prodejni_cena
        )
        exemplar.prodani = datum_prodeje.strftime('%Y%m%d')
        # print(f'Exemplář: {exemplar}')
        
        self.prodej_klic += 1

        return prodej
    
    def generuj_nakup(self):
        ''' Funkce pro generování záznamu o nákupu
        '''

        # Vlož počáteční datum do dočasné proměnné
        datum_nakupu = self.datum

        # Deklaruje počáteční hodnotu kódu exempláře
        kod = f'ID{self.exemplar_klic + 1:020d}'

        # Cena se musí určit ještě před tím, než se vytvoří nový záznam
        # o nákupu nové knihy
        kniha_id_temp = self.knihy[random.randint(0, len(self.knihy) - 1)].kniha_id

        nakupni_cena = self.nalezni_cenu_nakupu(kniha_id_temp)

        # Nový exemplář
        exemplar = Exemplar(
                self.exemplar_klic, 
                kod, 
                kniha_id_temp,
                datum_nakupu.strftime('%Y%m%d'), 
                None
            )
        
        nakup = Nakup(
                self.nakup_klic, 
                datum_nakupu.strftime('%Y%m%d'), 
                exemplar.klic, 
                random.choices(self.zamestnanci)[0].zamestnanec_id,
                nakupni_cena
            )
        
        self.nakup_klic += 1
        self.exemplar_klic += 1

        return exemplar, nakup

    def generovani(self) -> None:
        ''' Metoda pro generování nákupů a prodejů
        '''

        # Generování počátečního počtu exemplářů na sklad
        for i in range(1, 10):
            exemplar, nakup = self.generuj_nakup()
            self.exemplare.append(exemplar)
            self.nakupy.append(nakup)

            # print(f'Exemplář: {exemplar}')
            # print(f"Nákup: {nakup}")

        c = 0
        krok = 1000
        while c < 500000:
        
            if (c % krok == 0):
                print(f'Index: {c}, Dělení: {round(c / 1000, 4)}, Modulo: {c % 1000}')

            # Provádí n počet prodejů
            while i < random.randint(50000, 100000):

                # Nalezení exempláře knihy na skladě
                exemplar = self.najdi_exemplar()

                # Pokud je exemplář na skladě, proveď prodej
                if exemplar:
                    prodej = self.generuj_prodej(exemplar)
                    self.prodeje.append(prodej)

                    # print(f"Prodej: {prodej}")

                i += 1

            # Pokud exemplář není na skladě, proveď nákup
            a = 0

            # Proveď n počet nákupů, do zásoby
            while a < random.randint(20, 30):
                exemplar, nakup = self.generuj_nakup()
                self.exemplare.append(exemplar)
                self.nakupy.append(nakup)

                # print(f'Exemplář: {exemplar}')
                # print(f"Nákup: {nakup}")
                
                a += 1

            self.datum = self.datum + datetime.timedelta(days=1)
            c += 1

            # Když je datum dnes, ukonči veškerou činnost
            if self.datum == datetime.date.today():
                return

# Hlavní metoda skriptu
def main():

    logging.basicConfig(level=logging.INFO)

    logging.info('Spuštění skriptu')

    # V prodejích se neresetuje klic

    d = Databaze()

    d.spisovatele.append(Spisovatel(1, 1, 'Novák', 'Jan'))
    d.spisovatele.append(Spisovatel(2, 2, 'Svoboda', 'Petr'))
    d.spisovatele.append(Spisovatel(3, 3, 'Malý', 'Jiří'))
    d.spisovatele.append(Spisovatel(4, 4, 'Zelený', 'Karel'))

    d.knihy.append(Kniha(1, 1, 1, 'Linux příkazy', 2004, 850))
    d.knihy.append(Kniha(2, 2, 2, 'Windows 10 průvodce', 2010, 350))
    d.knihy.append(Kniha(3, 3, 2, 'MSSQL mistrovství', 2012, 720))
    d.knihy.append(Kniha(4, 4, 3, 'Python 3.11', 2020, 745))
    d.knihy.append(Kniha(5, 5, 4, 'Excel 2013', 2013, 900))
    d.knihy.append(Kniha(6, 6, 1, 'C#', 2008, 1200))
    d.knihy.append(Kniha(7, 7, 1, 'Powershell', 2022, 280))
    d.knihy.append(Kniha(8, 8, 4, 'HTML 5 a CSS 3', 2022, 460))

    d.zamestnanci.append(Zamestnanec(1, 1, 'Kouba', 'František'))
    d.zamestnanci.append(Zamestnanec(2, 2, 'Pokorná', 'Simona'))

    d.zakaznici.append(Zakaznik(1, 1, 'Svobodová', 'Marie', 'Valašské Meziříčí', 545058, 'K Hrušovu', 73, 83407))
    d.zakaznici.append(Zakaznik(2, 2, 'Kučera', 'Jakub', 'Teplice', 567442, 'Do Vršku', 47, 72981))
    d.zakaznici.append(Zakaznik(3, 3, 'Němcová', 'Hana', '', '', '', '', ''))
    d.zakaznici.append(Zakaznik(4, 4, 'Němcová', 'Petra', 'Jablonec nad Nisou', 563510, 'Statková', 2, 36734))
    d.zakaznici.append(Zakaznik(5, 5, 'Procházková', 'Zdeňka', 'Havířov', 555088, 'K samotě', 56, 68125))
    d.zakaznici.append(Zakaznik(6, 6, 'Pospíšilová', 'Jana', '', '', '', '', ''))
    d.zakaznici.append(Zakaznik(7, 7, 'Marková', 'Jana', 'Kroměříž', 588296, 'Pavlišovská', 4, 76701))
    d.zakaznici.append(Zakaznik(8, 8, 'Veselá', 'Stanislava', '', '', '', '', ''))
    
    d.generovani()

    logging.info(f'Počet nákupů: {len(d.nakupy)}')
    logging.info(f'Počet prodejů: {len(d.prodeje)}')

    d.zapis_do_csv_souboru('klic;zakaznik_id;prijmeni;jmeno;mesto;mesto_kod;ulice;cislo;psc',d.zakaznici, 'zakaznici.txt')
    d.zapis_do_csv_souboru('klic;zamestnanec_id;prijmeni;jmeno', d.zamestnanci, 'zamestnanci.txt')
    d.zapis_do_csv_souboru('klic;spisovatel_id;prijmeni;jmeno', d.spisovatele, 'spisovatele.txt')
    d.zapis_do_csv_souboru('klic;kniha_id;spisovatel_id;nazev;rok_vydani', d.knihy, 'knihy.txt')
    d.zapis_do_csv_souboru('klic;kod;kniha_id;nakoupeni;prodani', d.exemplare, 'exemplare.txt')
    d.zapis_do_csv_souboru('klic;datum_naskladneni_klic;exemplar_id;zamestnanec_id;cena', d.nakupy, 'nakupy.txt')
    d.zapis_do_csv_souboru('klic;datum_prodeje_klic;exemplar_id;zakaznik_id;zamestnanec_id;cena', d.prodeje, 'prodeje.txt')

    logging.info('Ukončení skriptu')

# Hlavní vlákno skriptu
if __name__ == "__main__":
    main()