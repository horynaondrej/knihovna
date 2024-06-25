#!/usr/bin/env python3
import logging 
import datetime
import random
import os
import cProfile
import pstats
from exemplar import Exemplar
from nakup import Nakup
from prodej import Prodej
from kniha import Kniha
from spisovatel import Spisovatel
from nakladatel import Nakladatel
from zamestnanec import Zamestnanec
from zakaznik import Zakaznik
from kategorie import Kategorie
from datumy import Datum
from databaze import Databaze


""" Globální proměnné a konstanty
"""
MARZE: float = 1.15

ROK = 2024
MESIC = 6

VAHA_ZACATEK = 500
VAHA_KONEC = 1000


class Generovani:
    ''' Hlavní třída pro generování záznamů
    '''

    def __init__(self):

        self.cesta = os.path.dirname(__file__)

        self.exemplare: list[Exemplar] = []
        self.exemplare_k_prodeji: list[Exemplar] = []
        self.prodej_klic = 1
        self.nakup_klic = 1
        self.exemplar_klic = 1
        self.prodeje = []
        self.nakupy = []
        self.knihy = []
        self.zamestnanci = []
        self.spisovatele = []
        self.zakaznici = []
        self.nakladatele = []
        self.kategorie = []
        self.datumy = []

        # Datum začátku provozu sklad knih
        self.datum = datetime.date(ROK, MESIC, 1)

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
    """
    def najdi_exemplar(self) -> Exemplar:
        ''' Funkce pro nalezení exempláře knihy

        Return:
            Exemplar: obj
        '''
        for exemplar in self.exemplare:
            if exemplar.prodani is None:
                return exemplar
        return None
    """

    def najdi_exemplar(self) -> Exemplar:
        ''' Funkce pro nalezení exempláře knihy

        Return:
            Exemplar: obj
        '''
        # print(self.exemplare_k_prodeji)
        if len(self.exemplare_k_prodeji) == 0:
            return None
        return self.exemplare_k_prodeji.pop(0)

    def nalezni_cenu_nakupu(self, kniha_id: int) -> int:
        """ Funkce nalezne cenu z ceníku
        """
        return self.knihy[kniha_id - 1].cena
    
    def najdi_cenu_prodeje(self, exemplar: Exemplar) -> int:
        """ Funkce nalezne cenu nakoupené knihy a vrátí 
        její cenu

        Args:
            exemplar: objekt exemplar

        Return:
            nákupní cena zadaného exempláře
        """

        # print(f'Exemplář dohledávám: {exemplar}')
        # print(f'Pole exemplářů: {self.exemplare}')
    
        return self.knihy[exemplar.kniha_id - 1].cena
    
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

        prodejni_cena = round(self.najdi_cenu_prodeje(exemplar) * MARZE, 2)
        # datum_prodeje = self.datum + datetime.timedelta(days=1)
        datum_prodeje = self.datum

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
    
    def stav_procesu(self, pocet: int) -> None:
        """ Funkce vypíše do konzole stav iterace
        """
        krok = 1000
        if (pocet % krok == 0):
            print(f'Index: {pocet}, Dělení: {round(pocet / 1000, 4)}, Modulo: {pocet % 1000}')

    def generovani(self) -> None:
        ''' Metoda pro generování nákupů a prodejů
        '''
        pocet_nakupu: int = 0
        pocet_prodeju: int = 0

        print(f'Počáteční datum: {self.datum}')

        # Generování počátečního počtu exemplářů na sklad
        for d in range(1, 10):
            exemplar, nakup = self.generuj_nakup()
            self.exemplare.append(exemplar)
            self.exemplare_k_prodeji.append(exemplar)
            self.nakupy.append(nakup)

            # print(f'Exemplář: {exemplar}')
            # print(f"Nákup: {nakup}")

        # print(self.exemplare_k_prodeji)

        c = 0
        while True:

            self.datumy.append(Datum(c + 1, self.datum))
        
            # Provádí n počet prodejů
            i = 0
            nahodny_pocet_prodeju = random.randint(VAHA_ZACATEK, VAHA_KONEC)
            pocet_prodeju += nahodny_pocet_prodeju
            
            while i < nahodny_pocet_prodeju:

                # Nalezení exempláře knihy na skladě
                exemplar = self.najdi_exemplar()

                # Pokud je exemplář na skladě, proveď prodej
                if exemplar:
                    prodej = self.generuj_prodej(exemplar)
                    self.prodeje.append(prodej)

                    # print(f"Prodej: {prodej}")

                i += 1

            print(f'Počet prodejů: {pocet_prodeju : <10}')

            # Pokud exemplář není na skladě, proveď nákup
            a = 0

            # Proveď n počet nákupů, do zásoby
            nahodny_pocet_nakupu = random.randint(VAHA_ZACATEK, VAHA_KONEC)
            pocet_nakupu += nahodny_pocet_nakupu
            
            while a < nahodny_pocet_nakupu:

                exemplar, nakup = self.generuj_nakup()
                self.exemplare.append(exemplar)
                self.exemplare_k_prodeji.append(exemplar)
                self.nakupy.append(nakup)

                # print(f'Exemplář: {exemplar}')
                # print(f"Nákup: {nakup}")
                
                a += 1

            print(f'Počet nákupů: {pocet_nakupu : <10}')

            self.datum = self.datum + datetime.timedelta(days=1)
            c += 1

            print(f'Koncové datum: {self.datum}')
            # Když je datum dnes, ukonči veškerou činnost
            if self.datum == datetime.date.today():
                break

# Hlavní metoda skriptu
def main():

    logging.basicConfig(level=logging.INFO)

    logging.info('Spuštění skriptu')

    # V prodejích se neresetuje klic

    g = Generovani()

    g.spisovatele.append(Spisovatel(1, 1, 'Novák', 'Jan'))
    g.spisovatele.append(Spisovatel(2, 2, 'Svoboda', 'Petr'))
    g.spisovatele.append(Spisovatel(3, 3, 'Malý', 'Jiří'))
    g.spisovatele.append(Spisovatel(4, 4, 'Zelený', 'Karel'))

    g.nakladatele.append(Nakladatel(1, 1, 'Computer Press'))
    g.nakladatele.append(Nakladatel(2, 2, 'CZ.NIC'))

    g.kategorie.append(Kategorie(1, 1, 'Programování'))
    g.kategorie.append(Kategorie(2, 2, 'Data a databáze'))
    g.kategorie.append(Kategorie(3, 3, 'Informační systémy'))
    g.kategorie.append(Kategorie(4, 4, 'Internet a web'))
    g.kategorie.append(Kategorie(5, 5, 'Kancelářské aplikace'))
    g.kategorie.append(Kategorie(6, 6, 'Ostatní'))

    g.knihy.append(Kniha(1, 1, 1, 2, 3, 'Linux příkazy', 2004, 850))
    g.knihy.append(Kniha(2, 2, 2, 1, 3, 'Windows 10 průvodce', 2010, 350))
    g.knihy.append(Kniha(3, 3, 2, 1, 2, 'MSSQL mistrovství', 2012, 720))
    g.knihy.append(Kniha(4, 4, 3, 2, 1, 'Python 3.11', 2020, 745))
    g.knihy.append(Kniha(5, 5, 4, 1, 5, 'Excel 2013', 2013, 900))
    g.knihy.append(Kniha(6, 6, 1, 1, 1, 'C#', 2008, 1200))
    g.knihy.append(Kniha(7, 7, 1, 1, 1, 'Powershell', 2022, 280))
    g.knihy.append(Kniha(8, 8, 4, 1, 4, 'HTML 5 a CSS 3', 2022, 460))
    g.knihy.append(Kniha(9, 9, 5, 1, 4, 'XHTML', 1996, 349))
    g.knihy.append(Kniha(10, 10, 5, 1, 4, 'CSS 5', 1999, 349))
    g.knihy.append(Kniha(11, 11, 5, 1, 2, 'DAX optimalization', 2001, 399))
    g.knihy.append(Kniha(12, 12, 6, 2, 2, 'Deep learning', 1813, 249))
    g.knihy.append(Kniha(13, 13, 6, 1, 5, 'Excel 2021', 2009, 349))
    g.knihy.append(Kniha(14, 14, 7, 1, 1, 'Java 21', 1965, 199))
    g.knihy.append(Kniha(15, 15, 7, 1, 3, 'Windows 11', 1967, 199))
    g.knihy.append(Kniha(16, 16, 7, 1, 5, 'Office 365', 1972, 249))
    g.knihy.append(Kniha(17, 17, 8, 1, 2, 'Big data', 1967, 399))
    g.knihy.append(Kniha(18, 18, 8, 1, 2, 'SQL', 1987, 349))
    g.knihy.append(Kniha(19, 19, 9, 1, 2, '1000 příkladů SQL', 1967, 449))
    g.knihy.append(Kniha(20, 20, 9, 1, 4, 'Wordpress', 1985, 349))
    g.knihy.append(Kniha(21, 21, 10, 1, 3, 'Tvorba informačních systémů', 1980, 299))
    g.knihy.append(Kniha(22, 22, 10, 1, 1, 'Jazyk R', 1985, 399))
    g.knihy.append(Kniha(23, 23, 10, 1, 1, 'Java 8', 1989, 399))
    g.knihy.append(Kniha(24, 24, 11, 1, 6, 'Adobe Photoshop CS6', 1965, 549))
    g.knihy.append(Kniha(25, 25, 11, 2, 2, 'NoSQL databáze', 1977, 499))
    g.knihy.append(Kniha(26, 26, 11, 1, 2, 'Postgres', 1987, 499))
    g.knihy.append(Kniha(27, 27, 12, 1, 6, 'CAD', 1979, 299))
    g.knihy.append(Kniha(28, 28, 12, 1, 1, 'Testování softwaru', 1986, 349))
    g.knihy.append(Kniha(29, 29, 12, 2, 1, 'Python evoluce', 1992, 349))
    g.knihy.append(Kniha(30, 30, 13, 1, 3, 'Android', 1982, 399))

    g.zamestnanci.append(Zamestnanec(1, 1, 'Kouba', 'František'))
    g.zamestnanci.append(Zamestnanec(2, 2, 'Pokorná', 'Simona'))

    g.zakaznici.append(Zakaznik(1, 1, 'Svobodová', 'Marie', 'Valašské Meziříčí', 545058, 'K Hrušovu', 73, 83407))
    g.zakaznici.append(Zakaznik(2, 2, 'Kučera', 'Jakub', 'Teplice', 567442, 'Do Vršku', 47, 72981))
    g.zakaznici.append(Zakaznik(3, 3, 'Němcová', 'Hana', 'Městec Králové', 537489, 'Severní Viii', 168, 23608))
    g.zakaznici.append(Zakaznik(4, 4, 'Němcová', 'Petra', 'Jablonec nad Nisou', 563510, 'Statková', 2, 36734))
    g.zakaznici.append(Zakaznik(5, 5, 'Procházková', 'Zdeňka', 'Havířov', 555088, 'K samotě', 56, 68125))
    g.zakaznici.append(Zakaznik(6, 6, 'Pospíšilová', 'Jana', 'Pyšely', 538680, 'Mírová', 598, 50965))
    g.zakaznici.append(Zakaznik(7, 7, 'Marková', 'Jana', 'Kroměříž', 588296, 'Pavlišovská', 4, 76701))
    g.zakaznici.append(Zakaznik(8, 8, 'Veselá', 'Stanislava', 'Židlochovice', 584282, 'Augustova', 66, 43409))
    g.zakaznici.append(Zakaznik(9, 9, 'Slavík', 'Otakar', 'Neveklov', 530310, 'Kukelská', 8, 21748))
    g.zakaznici.append(Zakaznik(10, 10, 'Strnad', 'Blahoslav', 'Slatiňany', 572268, 'V Závitu', 8, 51833))
    g.zakaznici.append(Zakaznik(11, 11, 'Tůmová', 'Květoslava', 'Stod', 558389, 'Javornická', 6, 12827))
    g.zakaznici.append(Zakaznik(12, 12, 'Krejčová', 'Vanda', 'Vysoké Veselí', 573809, 'Rýmařovská', 411, 23476))
    g.zakaznici.append(Zakaznik(13, 13, 'Strnadová', 'Johana', 'Zliv', 545341, 'K Vodě', 1, 49762))
    g.zakaznici.append(Zakaznik(14, 14, 'Dvořáková', 'Anna', 'Vizovice', 585939, 'Nad Rokytkou', 45, 37396))
    g.zakaznici.append(Zakaznik(15, 15, 'Benešová', 'Dominika', 'Odolena Voda', 538574, 'Na Laurové', 287, 28912))
    g.zakaznici.append(Zakaznik(16, 16, 'Růžička', 'Ctirad', 'Hlinsko', 569267, 'Horní Chaloupky', 1, 51448))
    g.zakaznici.append(Zakaznik(17, 17, 'Moravec', 'Ján', 'Ledeč nad Sázavou', 568988, 'Kadaňská', 942, 79936))
    g.zakaznici.append(Zakaznik(18, 18, 'Svoboda', 'Boleslav', 'Hoštka', 564877, 'Tovární', 92, 59512))
    g.zakaznici.append(Zakaznik(19, 19, 'Dostálová', 'Marie', 'Klobouky u Brna', 584550, 'Čestmírova', 7, 69484))
    g.zakaznici.append(Zakaznik(20, 20, 'Novák', 'Miloš', 'Loštice', 540196, 'Průškova', 980, 60169))
    g.zakaznici.append(Zakaznik(21, 21, 'Černá', 'Monika', 'Vratimov', 598879, 'Na Kozinci', 9, 74608))
    g.zakaznici.append(Zakaznik(22, 22, 'Mašková', 'Evelína', 'Smržovka', 563811, 'Nad Rohatci', 28, 40272))
    g.zakaznici.append(Zakaznik(23, 23, 'Bláhová', 'Martina', 'Lovosice', 565229, 'Mádrova', 45, 12827))
    g.zakaznici.append(Zakaznik(24, 24, 'Doležal', 'Rostislav', 'Dubá', 561533, 'Mezi Lysinami', 56, 47771))
    g.zakaznici.append(Zakaznik(25, 25, 'Kopecký', 'Robin', 'Krásná Hora nad Vltavou', 540552, 'Doubravická', 9, 27860))
    g.zakaznici.append(Zakaznik(26, 26, 'Dušek', 'Matyáš', 'Bakov nad Jizerou', 535427, 'Hostýnská', 705, 78296))
    g.zakaznici.append(Zakaznik(27, 27, 'Pokorný', 'Tadeáš', 'Počátky', 548561, 'Šachovská', 2, 17500))
    g.zakaznici.append(Zakaznik(28, 28, 'Vávrová', 'Pavlína', 'Zákupy', 562262, 'U Smíchovského Hřbitova', 7, 17583))
    g.zakaznici.append(Zakaznik(29, 29, 'Müllerová', 'Marie', 'Lišov', 544779, 'Nouzov', 205, 45718))
    g.zakaznici.append(Zakaznik(30, 30, 'Poláková', 'Petra', 'Osek', 598828, 'Ambrožova', 3, 58734))
    g.zakaznici.append(Zakaznik(31, 31, 'Vaněk', 'Vratislav', 'Šluknov', 562858, 'Křížkovského', 448, 67314))
    g.zakaznici.append(Zakaznik(32, 32, 'Vávrová', 'Ivona', 'Dolní Kounice', 582956, 'Palackého', 57, 64858))
    g.zakaznici.append(Zakaznik(33, 33, 'Ševčíková', 'Apolena', 'Dobrovice', 535672, 'Nad Plynovodem', 4, 29290))
    g.zakaznici.append(Zakaznik(34, 34, 'Sedláková', 'Edita', 'Přebuz', 560596, 'K Matěji', 790, 65989))
    g.zakaznici.append(Zakaznik(35, 35, 'Valentová', 'Naděžda', 'Semily', 576964, 'Vajgarská', 116, 18416))
    g.zakaznici.append(Zakaznik(36, 36, 'Kadlec', 'Luboš', 'Libčice nad Vltavou', 539414, 'Všejanská', 4, 25949))
    g.zakaznici.append(Zakaznik(37, 37, 'Sedláková', 'Miroslava', 'Bělá pod Bezdězem', 535443, 'Sladovnická', 72, 44439))
    g.zakaznici.append(Zakaznik(38, 38, 'Janečková', 'Blanka', 'Rožďalovice', 537756, 'Kotrčová', 17, 13874))
    g.zakaznici.append(Zakaznik(39, 39, 'Procházka', 'Mikuláš', 'Potštát', 517101, 'Machovická', 410, 39923))
    g.zakaznici.append(Zakaznik(40, 40, 'Kubíček', 'Zdeněk', 'Plánice', 556955, 'U Staré Pošty', 505, 39112))
    g.zakaznici.append(Zakaznik(41, 41, 'Soukup', 'Adam', 'Hlinsko', 569267, 'Jasná I', 356, 16060))
    g.zakaznici.append(Zakaznik(42, 42, 'Navrátilová', 'Lýdie', 'Klimkovice', 599549, 'Josefa Šimůnka', 9, 17312))
    g.zakaznici.append(Zakaznik(43, 43, 'Bláhová', 'Miroslava', 'Tanvald', 563820, 'Tachovské Náměstí', 116, 23135))
    g.zakaznici.append(Zakaznik(44, 44, 'Fialová', 'Květoslava', 'Štětí', 565709, 'Mlékárenská', 5, 27197))
    g.zakaznici.append(Zakaznik(45, 45, 'Burešová', 'Anna', 'Janské Lázně', 579351, 'Mukařovského', 6, 29773))
    g.zakaznici.append(Zakaznik(46, 46, 'Strnadová', 'Naděžda', 'Loštice', 540196, 'Šermířská', 4, 56764))
    g.zakaznici.append(Zakaznik(47, 47, 'Svobodová', 'Jindřiška', 'Veltrusy', 535273, 'Severovýchodní Vi', 76, 73514))
    g.zakaznici.append(Zakaznik(48, 48, 'Malá', 'Irena', 'Trmice', 553697, 'Na Staré Vinici', 532, 60733))
    g.zakaznici.append(Zakaznik(49, 49, 'Ježková', 'Emilie', 'Králův Dvůr', 533203, 'Černá', 1, 51228))
    g.zakaznici.append(Zakaznik(50, 50, 'Zeman', 'Lukáš', 'Kopidlno', 573060, 'Kostnické Náměstí', 5, 14655))
    g.zakaznici.append(Zakaznik(51, 51, 'Dostálová', 'Klaudie', 'Bučovice', 592943, 'Otradovická', 46, 60766))
    g.zakaznici.append(Zakaznik(52, 52, 'Kučera', 'Štefan', 'Nýřany', 559300, 'Záblatská', 627, 51283))
    g.zakaznici.append(Zakaznik(53, 53, 'Šmídová', 'Sabina', 'Chrastava', 564117, 'Lovčenská', 2, 71390))
    g.zakaznici.append(Zakaznik(54, 54, 'Pokorná', 'Apolena', 'Kouřim', 533424, 'Mezi Sklady', 157, 74311))
    g.zakaznici.append(Zakaznik(55, 55, 'Hruška', 'Dušan', 'Moravský Beroun', 597678, 'Adélčina', 46, 20429))
    g.zakaznici.append(Zakaznik(56, 56, 'Malý', 'René', 'Borovany', 544281, 'Rokytnická', 84, 42789))
    g.zakaznici.append(Zakaznik(57, 57, 'Horváthová', 'Milada', 'Horní Jelení', 574996, 'Za Stadionem', 73, 65171))
    g.zakaznici.append(Zakaznik(58, 58, 'Ševčíková', 'Vladimíra', 'Chropyně', 588512, 'Doubravínova', 67, 38759))
    g.zakaznici.append(Zakaznik(59, 59, 'Černá', 'Anežka', 'Brtnice', 586943, 'Na Bojišti', 293, 13537))
    g.zakaznici.append(Zakaznik(60, 60, 'Čech', 'Erik', 'Kamenický Šenov', 561681, 'Prusíkova', 61, 59203))
    g.zakaznici.append(Zakaznik(61, 61, 'Valentová', 'Gabriela', 'Vyšší Brod', 545848, 'K Lučinám', 57, 58241))
    g.zakaznici.append(Zakaznik(62, 62, 'Horáček', 'Luboš', 'Týn nad Vltavou', 545201, 'Rudoltická', 81, 60743))
    g.zakaznici.append(Zakaznik(63, 63, 'Musilová', 'Vilma', 'Duchcov', 567515, 'Libichovská', 3, 14664))
    g.zakaznici.append(Zakaznik(64, 64, 'Havlíčková', 'Františka', 'Meziměstí', 574252, 'Dobrošovská', 67, 55002))
    g.zakaznici.append(Zakaznik(65, 65, 'Čermák', 'Ivan', 'Strážov', 557137, 'Vlčická', 27, 36116))
    g.zakaznici.append(Zakaznik(66, 66, 'Mašková', 'Veronika', 'Jablunkov', 598259, 'Šárovo Kolo', 677, 10338))
    g.zakaznici.append(Zakaznik(67, 67, 'Matoušková', 'Iva', 'Velká Bystřice', 505609, 'Lovčenská', 49, 59392))
    g.zakaznici.append(Zakaznik(68, 68, 'Zeman', 'Alexander', 'Šluknov', 562858, 'Vinohradská', 8, 52217))
    g.zakaznici.append(Zakaznik(69, 69, 'Machová', 'Otýlie', 'Kryry', 566314, 'U Nových Domů I', 8, 68004))
    g.zakaznici.append(Zakaznik(70, 70, 'Havlíček', 'Ignác', 'Kelč', 542989, 'Suchdolská', 5, 18873))
    g.zakaznici.append(Zakaznik(71, 71, 'Blažek', 'Marek', 'Skuteč', 572241, 'Vizovická', 512, 44922))
    g.zakaznici.append(Zakaznik(72, 72, 'Brožová', 'Edita', 'Dolní Poustevna', 562441, 'Hostivařské Nám.', 806, 26067))
    g.zakaznici.append(Zakaznik(73, 73, 'Stejskalová', 'Natálie', 'Jablonec nad Nisou', 563510, 'Rýmařovská', 593, 37769))
    g.zakaznici.append(Zakaznik(74, 74, 'Kadlecová', 'Linda', 'Trhový Štěpánov', 530816, 'Náměstí I. P. Pavlova', 586, 31774))
    g.zakaznici.append(Zakaznik(75, 75, 'Jarošová', 'Linda', 'Kladruby', 560405, 'Dělostřelecká', 14, 27760))
    g.zakaznici.append(Zakaznik(76, 76, 'Kopecký', 'Karel', 'Švihov', 557200, 'Jasná I', 40, 48849))
    g.zakaznici.append(Zakaznik(77, 77, 'Bláhová', 'Danuše', 'Dubňany', 586161, 'Mezilesní', 5, 55669))
    g.zakaznici.append(Zakaznik(78, 78, 'Soukup', 'Dominik', 'Ústí nad Labem', 0, 'Nad Zavážkou', 556, 44877))
    g.zakaznici.append(Zakaznik(79, 79, 'René', 'pan', 'Neveklov', 530310, 'Neužilova', 5, 78741))
    g.zakaznici.append(Zakaznik(80, 80, 'Kříž', 'Alois', 'Hostouň', 553689, 'Na Fišerce', 42, 60604))
    g.zakaznici.append(Zakaznik(81, 81, 'Němcová', 'Alexandra', 'Janov', 576328, 'V Zátiší', 6, 15203))
    g.zakaznici.append(Zakaznik(82, 82, 'Urbanová', 'Alžběta', 'Zruč nad Sázavou', 534633, 'Maňákova', 61, 49274))
    g.zakaznici.append(Zakaznik(83, 83, 'Slavík', 'Miloš', 'Pec pod Sněžkou', 579581, 'U Podjezdu', 2, 22582))
    g.zakaznici.append(Zakaznik(84, 84, 'Kučera', 'Artur', 'Smržovka', 563811, 'K Brusce', 774, 69951))
    g.zakaznici.append(Zakaznik(85, 85, 'Vítek', 'Svatoslav', 'Hostinné', 579297, 'Benákova', 369, 39642))
    g.zakaznici.append(Zakaznik(86, 86, 'Machová', 'Nela', 'Mirovice', 549592, 'Hněvkovského', 18, 51445))
    g.zakaznici.append(Zakaznik(87, 87, 'Janda', 'Ctirad', 'Lom', 536822, 'Jablonecká', 278, 75786))
    g.zakaznici.append(Zakaznik(88, 88, 'Růžička', 'Milan', 'Klimkovice', 599549, 'Plynární', 74, 63875))
    g.zakaznici.append(Zakaznik(89, 89, 'Burešová', 'Patricie', 'Hoštka', 564877, 'Trytova', 647, 14361))
    g.zakaznici.append(Zakaznik(90, 90, 'Novotný', 'Oto', 'Verneřice', 562921, 'K Lučinám', 34, 42645))
    g.zakaznici.append(Zakaznik(91, 91, 'Macháčková', 'Alena', 'Nejdek', 555380, 'Havlíčkova', 9, 59418))
    g.zakaznici.append(Zakaznik(92, 92, 'Čermáková', 'Petra', 'Česká Skalice', 573990, 'Paťanka', 15, 59452))
    g.zakaznici.append(Zakaznik(93, 93, 'Fišerová', 'Helena', 'Rosice', 583782, 'Jarešova', 784, 50674))
    g.zakaznici.append(Zakaznik(94, 94, 'Mach', 'Ján', 'Ústí nad Labem', 0, 'Na Kuthence', 18, 59287))
    g.zakaznici.append(Zakaznik(95, 95, 'Jelínek', 'Emil', 'Smiřice', 570877, 'Petřínská', 944, 75437))
    g.zakaznici.append(Zakaznik(96, 96, 'Stejskal', 'Ivo', 'Blovice', 557587, 'Trytova', 338, 30539))
    g.zakaznici.append(Zakaznik(97, 97, 'Hájková', 'Michaela', 'Slavkov u Brna', 593583, 'Hvězdonická', 86, 73065))
    g.zakaznici.append(Zakaznik(98, 98, 'Kadlec', 'Jakub', 'Velké Pavlovice', 585017, 'Horní Stromky', 85, 32798))
    g.zakaznici.append(Zakaznik(99, 99, 'Růžičková', 'Pavla', 'Deštná', 546151, 'Kotrčová', 6, 60138))
    g.zakaznici.append(Zakaznik(100, 100, 'Holubová', 'Šárka', 'Vodňany', 551953, 'Vstupní', 89, 32213))
    g.zakaznici.append(Zakaznik(101, 101, 'Brožová', 'Stanislava', 'Lanžhot', 584622, 'Rašínská', 750, 18299))
    g.zakaznici.append(Zakaznik(102, 102, 'Janečková', 'Michaela', 'Vyšší Brod', 545848, 'Mádrova', 9, 50926))
    g.zakaznici.append(Zakaznik(103, 103, 'Poláková', 'Lada', 'Lučany nad Nisou', 563692, 'Dejvická', 3, 20754))
    g.zakaznici.append(Zakaznik(104, 104, 'Kadlecová', 'Anežka', 'Bezdružice', 560740, 'Plánická', 9, 78385))
    g.zakaznici.append(Zakaznik(105, 105, 'Novotný', 'Petr', 'Bílovec', 599247, 'Pod Velkým Hájem', 2, 35533))
    g.zakaznici.append(Zakaznik(106, 106, 'Král', 'Samuel', 'Stochov', 532860, 'Tachovské Náměstí', 748, 44882))
    g.zakaznici.append(Zakaznik(107, 107, 'Vávra', 'Svatopluk', 'Husinec', 550230, 'Na Příčné Mezi', 9, 41786))
    g.zakaznici.append(Zakaznik(108, 108, 'Sedláková', 'Šárka', 'Vysoké Veselí', 573809, 'Náměstí Hrdinů', 568, 35184))

    profiler = cProfile.Profile()
    profiler.enable()

    g.generovani()

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('tottime')
    stats.print_stats()

    logging.info(f'Počet nákupů: {len(g.nakupy)}')
    logging.info(f'Počet prodejů: {len(g.prodeje)}')

    g.zapis_do_csv_souboru('klic;zakaznik_id;prijmeni;jmeno;mesto;mesto_kod;ulice;cislo;psc', g.zakaznici, 'zakaznici.txt')
    g.zapis_do_csv_souboru('klic;zamestnanec_id;prijmeni;jmeno', g.zamestnanci, 'zamestnanci.txt')
    g.zapis_do_csv_souboru('klic;spisovatel_id;prijmeni;jmeno', g.spisovatele, 'spisovatele.txt')
    g.zapis_do_csv_souboru('klic;nakladatel_id;nazev', g.nakladatele, 'nakladatele.txt')
    g.zapis_do_csv_souboru('klic;kategorie_id;oznaceni', g.kategorie, 'kategorie.txt')
    g.zapis_do_csv_souboru('klic;kniha_id;spisovatel_id;nakladatel_id;kategorie_id;nazev;rok_vydani;cena', g.knihy, 'knihy.txt')
    g.zapis_do_csv_souboru('klic;kod;kniha_id;nakoupeni;prodani', g.exemplare, 'exemplare.txt')
    g.zapis_do_csv_souboru('klic;datum_naskladneni_klic;exemplar_id;zamestnanec_id;cena', g.nakupy, 'nakupy.txt')
    g.zapis_do_csv_souboru('klic;datum_prodeje_klic;exemplar_id;zakaznik_id;zamestnanec_id;cena', g.prodeje, 'prodeje.txt')
    g.zapis_do_csv_souboru('klic;datum_id;datum;rok;mesic_cislo;mesic_oznaceni;ctvrtleti_cislo;ctvrtleti_oznaceni;rok_mesic;rok_ctvrtleti', g.datumy, 'datumy.txt')

    d = Databaze()
    d.smazani_prikazu()
    d.import_dat(
        g.prodeje,
        g.nakupy,
        g.knihy,
        g.zamestnanci,
        g.spisovatele,
        g.zakaznici,
        g.nakladatele,
        g.kategorie,
        g.datumy,
        g.exemplare
        )
            
    d1 = 'drop table if exists zakaznici;'
    d2 = 'drop table if exists zamestnanci;'
    d3 = 'drop table if exists spisovatele;'
    d4 = 'drop table if exists knihy;'
    d5 = 'drop table if exists nakupy;'
    d6 = 'drop table if exists prodeje;'
    d7 = 'drop table if exists datumy;'
    d8 = 'drop table if exists exemplare;'
    d9 = 'drop table if exists nakladatele;'
    d10 = 'drop table if exists kategorie;'
    
    d.ulozeni_prikazu(d1)
    d.ulozeni_prikazu(d2)
    d.ulozeni_prikazu(d3)
    d.ulozeni_prikazu(d4)
    d.ulozeni_prikazu(d5)
    d.ulozeni_prikazu(d6)
    d.ulozeni_prikazu(d7)
    d.ulozeni_prikazu(d8)
    d.ulozeni_prikazu(d9)
    d.ulozeni_prikazu(d10)
    

    logging.info('Zapsány příkazy DROP')

    c1 = 'create table zakaznici (\n' \
        + 'klic int not null,\n' \
        + 'zakaznik_id int not null,\n' \
        + 'prijmeni text not null,\n' \
        + 'jmeno text,\n' \
        + 'mesto text,\n' \
        + 'mesto_kod int,\n' \
        + 'ulice text,\n' \
        + 'cislo int,\n' \
        + 'psc int,\n' \
        + 'foreign key (zakaznik_id) references prodeje (zakaznik_id) \n' \
        + ');\n'

    c2 = 'create table zamestnanci (\n' \
        + 'klic int not null,\n' \
        + 'zamestnanec_id int not null,\n' \
        + 'prijmeni text not null,\n' \
        + 'jmeno text,\n' \
        + 'foreign key (zamestnanec_id) references nakupy (zamestnanec_id), \n' \
        + 'foreign key (zamestnanec_id) references prodeje (zamestnanec_id) \n' \
        + ');\n'

    c3 = 'create table spisovatele (\n' \
        + 'klic int not null,\n' \
        + 'spisovatel_id int not null,\n' \
        + 'prijmeni text not null,\n' \
        + 'jmeno text,\n' \
        + 'foreign key (spisovatel_id) references knihy (spisovatel_id) \n' \
        + ');\n'
    
    c4 = 'create table knihy (\n' \
        + 'klic int not null,\n' \
        + 'kniha_id int not null,\n' \
        + 'spisovatel_id int not null,\n' \
        + 'nakladatel_id int not null,\n' \
        + 'kategorie_id int not null,\n' \
        + 'nazev text not null,\n' \
        + 'rok_vydani int not null,\n' \
        + 'cena int not null,\n' \
        + 'foreign key (kniha_id) references exemplare (kniha_id), \n' \
        + 'foreign key (spisovatel_id) references spisovatele (spisovatel_id) \n' \
        + 'foreign key (nakladatel_id) references nakladatele (nakladatel_id) \n' \
        + 'foreign key (kategorie_id) references kategorie (kategorie_id) \n' \
        + ');\n'

    c5 = 'create table nakupy (\n' \
        + 'klic int not null,\n' \
        + 'datum_klic int not null,\n' \
        + 'exemplar_id int not null,\n' \
        + 'zamestnanec_id int not null,\n' \
        + 'cena real not null,\n' \
        + 'foreign key (datum_klic) references datumy (datum_klic), \n' \
        + 'foreign key (exemplar_id) references exemplare (exemplar_id), \n' \
        + 'foreign key (zamestnanec_id) references zamestnanci (zamestnanec_id) \n' \
        + ');\n' 

    c6 = 'create table prodeje (\n' \
        + 'klic int not null,\n' \
        + 'datum_klic int not null, \n' \
        + 'exemplar_id int not null, \n' \
        + 'zakaznik_id int not null,\n' \
        + 'zamestnanec_id int not null, \n' \
        + 'cena real not null,\n' \
        + 'foreign key (datum_klic) references datumy (datum_klic), \n' \
        + 'foreign key (exemplar_id) references exemplare (exemplar_id), \n' \
        + 'foreign key (zakaznik_id) references zakaznici (zakaznik_id), \n' \
        + 'foreign key (zamestnanec_id) references zamestnanci (zamestnanec_id) \n' \
        + ');\n'
    
    c7 = 'create table datumy (\n' \
        + 'klic int not null,\n' \
        + 'datum_klic int not null,\n' \
        + 'datum text not null,\n' \
        + 'rok int not null,\n' \
        + 'mesic_cislo int not null,\n' \
        + 'mesic_oznaceni text not null,\n' \
        + 'ctvrtleti_cislo int not null,\n' \
        + 'ctvrtleti_oznaceni text not null,\n' \
        + 'rok_mesic text not null,\n' \
        + 'rok_ctvrtleti text not null,\n' \
        + 'foreign key (datum_klic) references prodeje (datum_klic), \n' \
        + 'foreign key (datum_klic) references nakupy (datum_klic) \n' \
        + ');\n'

    c8 = 'create table zamestnanci (\n' \
        + 'klic int not null,\n' \
        + 'kategorie_id int not null,\n' \
        + 'oznaceni text not null,\n' \
        + 'foreign key (kategorie_id) references knihy (kategorie_id) \n' \
        + ');\n'
    
    c9 = 'create table nakladatele (\n' \
        + 'klic int not null,\n' \
        + 'nakladatel_id int not null,\n' \
        + 'oznaceni text not null,\n' \
        + 'foreign key (nakladatel_id) references knihy (nakladatel_id) \n' \
        + ');\n'
    
    c10 = 'create table exemplare (\n' \
        + 'klic int not null,\n' \
        + 'kod text not null,\n' \
        + 'kniha_id int not null,\n' \
        + 'nakoupeni int not null,\n' \
        + 'prodani int,\n' \
        + 'foreign key (kniha_id) references knihy (kniha_id) \n' \
        + 'foreign key (klic) references prodeje (exemplar_id), \n' \
        + 'foreign key (klic) references nakupy (exemplar_id) \n' \
        + ');\n'
    
    d.ulozeni_prikazu(c1)
    d.ulozeni_prikazu(c2)
    d.ulozeni_prikazu(c3)
    d.ulozeni_prikazu(c4)
    d.ulozeni_prikazu(c5)
    d.ulozeni_prikazu(c6)
    d.ulozeni_prikazu(c7)
    d.ulozeni_prikazu(c8)
    d.ulozeni_prikazu(c9)
    d.ulozeni_prikazu(c10)
    
    logging.info('Zapsány příkazy CREATE')

    i1 = 'insert into zakaznici (klic, zakaznik_id, prijmeni, jmeno, mesto, mesto_kod, ulice, cislo, psc) values '
    d.ulozeni_prikazu(i1)
    d.ulozeni_tabulky(d.zakaznici)

    i2 = 'insert into zamestnanci (klic, zamestnanec_id, prijmeni, jmeno) values '
    d.ulozeni_prikazu(i2)
    d.ulozeni_tabulky(d.zamestnanci)

    i3 = 'insert into spisovatele (klic, spisovatel_id, prijmeni, jmeno) values '
    d.ulozeni_prikazu(i3)
    d.ulozeni_tabulky(d.spisovatele)

    i4 = 'insert into knihy (klic, kniha_id, spisovatel_id, nakladatel_id, kategorie_id, nazev, rok_vydani, cena) values '
    d.ulozeni_prikazu(i4)
    d.ulozeni_tabulky(d.knihy)

    i5 = 'insert into nakupy (klic, datum_klic, exemplar_id, zamestnanec_id, cena) values '
    d.ulozeni_rozsahle_tabulky(d.nakupy, i5)

    i6 = 'insert into prodeje (klic, datum_klic, exemplar_id, zakaznik_id, zamestnanec_id, cena) values '
    d.ulozeni_rozsahle_tabulky(d.prodeje, i6)

    i10 = 'insert into exemplare (klic, kod, kniha_id, nakoupeni, prodani) values '
    d.ulozeni_rozsahle_tabulky(d.exemplare, i10)

    i7 = 'insert into datumy (klic, datum_klic, datum, rok, mesic_cislo, mesic_oznaceni, ctvrtleti_cislo, ctvrtleti_oznaceni, rok_mesic, rok_ctvrtleti) values '
    d.ulozeni_rozsahle_tabulky(d.datumy, i7)

    i8 = 'insert into kategorie (klic, kategorie_id, oznaceni) values '
    d.ulozeni_prikazu(i8)
    d.ulozeni_tabulky(d.kategorie)

    i9 = 'insert into nakladatele (klic, nakladatel_id, oznaceni) values '
    d.ulozeni_prikazu(i9)
    d.ulozeni_tabulky(d.nakladatele)
    
    logging.info('Zapsány příkazy INSERT')

    logging.info('Ukončení skriptu')

# Hlavní vlákno skriptu
if __name__ == "__main__":
    main()