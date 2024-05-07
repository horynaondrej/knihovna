#!/usr/bin/env python3
import logging 
import datetime
import random
from exemplar import Exemplar
from nakup import Nakup
from prodej import Prodej
from kniha import Kniha
from spisovatel import Spisovatel
from zamestnanec import Zamestnanec


class Databaze:
    ''' Hlavní třída pro generování záznamů
    '''

    def __init__(self):
        self.exemplare = []
        self.prodej_klic = 1
        self.nakup_klic = 1
        self.exemplar_klic = 1
        self.prodeje = []
        self.nakupy = []
        self.knihy = []
        self.zamestnanci = []

        # Datum začátku provozu sklad knih
        self.datum = datetime.date(2024, 4, 1)

    def najdi_exemplar(self):
        ''' Funkce pro nalezení exempláře knihy

        Return:
            Exemplar: obj
        '''

        for exemplar in self.exemplare:
            if exemplar.prodani is None:
                return exemplar
        return None
    
    def generuj_prodej(self, exemplar):
        ''' Funkce pro generování záznamu o prodeji

        Arg:
            exemplar: obj

        Return:
            prodej: obj
            Upravuje datum prodeje exempláře
        '''

        prodejni_cena = 12
        datum_prodeje = self.datum + datetime.timedelta(days=1)
        prodej = Prodej(
            self.prodej_klic, 
            datum_prodeje.strftime('%Y%m%d'), 
            exemplar.klic,
            random.choices(self.zamestnanci)[0].zamestnanec_id, 
            prodejni_cena
        )
        exemplar.prodani = datum_prodeje.strftime('%Y%m%d')
        print(f'Exemplář: {exemplar}')
        
        self.prodej_klic += 1
        return prodej
    
    def generuj_nakup(self):
        ''' Funkce pro generování záznamu o nákupu
        '''

        nakupni_cena = 10
        datum_nakupu = self.datum
        kod = f'KOD{self.exemplar_klic + 1:03d}'
        exemplar = Exemplar(
                self.exemplar_klic, 
                kod, 
                random.choices(self.knihy)[0].kniha_id,
                datum_nakupu.strftime('%Y%m%d'), 
                None
            )
        self.exemplare.append(exemplar)
        print(f'Exemplář: {exemplar}')
        nakup = Nakup(
                self.nakup_klic, 
                datum_nakupu.strftime('%Y%m%d'), 
                exemplar.klic, 
                nakupni_cena
            )
        self.exemplar_klic += 1
        return nakup

    def generovani(self):
        ''' Metoda pro generování nákupů a prodejů
        '''

        for i in range(1, 10):
            nakup = self.generuj_nakup()
            self.nakupy.append(nakup)

        c = 0
        while c < 10:
        
            i = 0
            while i < 10:

                # Nalezení exempláře knihy na skladě
                exemplar = self.najdi_exemplar()

                # Pokud je exemplář na skladě, proveď prodej
                if exemplar:
                    prodej = self.generuj_prodej(exemplar)
                    self.prodeje.append(prodej)
                    print(f"Prodej: {prodej}")
                i += 1

            # Pokud exemplář není na skladě, proveď nákup
            a = 0
            while a < 10:
                nakup = self.generuj_nakup()
                self.nakupy.append(nakup)
                print(f"Nákup: {nakup}")
                a += 1

            self.datum = self.datum + datetime.timedelta(days=1)
            c += 1

# Hlavní metoda skriptu
def main():

    logging.basicConfig(level=logging.INFO)

    logging.info('Spuštění skriptu')

    d = Databaze()

    d.spisovatele.append(Spisovatel(1, 1, 'Novák', 'Jan'))
    d.spisovatele.append(Spisovatel(2, 2, 'Svoboda', 'Petr'))
    d.spisovatele.append(Spisovatel(3, 3, 'Malý', 'Jiří'))
    d.spisovatele.append(Spisovatel(4, 4, 'Zelený', 'Karel'))

    d.knihy.append(Kniha(1, 1, 1, 'Linux příkazy', 900, 2004))
    d.knihy.append(Kniha(2, 2, 2, 'Windows 10 průvodce', 750, 2010))
    d.knihy.append(Kniha(3, 3, 2, 'MSSQL mistrovství', 600, 2012))
    d.knihy.append(Kniha(4, 4, 3, 'Python 3.11', 720, 2020))
    d.knihy.append(Kniha(5, 5, 4, 'Excel 2013', 1000, 2013))
    d.knihy.append(Kniha(6, 6, 1, 'C#', 297, 2008))
    d.knihy.append(Kniha(7, 7, 1, 'Powershell', 502, 2022))
    d.knihy.append(Kniha(8, 8, 4, 'HTML 5 a CSS 3', 502, 2022))

    d.zamestnanci.append(Zamestnanec(1, 1, 'Kouba', 'František'))
    d.zamestnanci.append(Zamestnanec(2, 2, 'Pokorná', 'Simona'))
    
    d.generovani()
    
    print(f'Celkový výpis databáze')
    for i in d.exemplare:
        print(i)

    logging.info('Ukončení skriptu')

# Hlavní vlákno skriptu
if __name__ == "__main__":
    main()