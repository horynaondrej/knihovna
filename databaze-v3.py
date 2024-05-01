#!/usr/bin/env python3
import logging 
import datetime
import random
from exemplar import Exemplar
from nakup import Nakup
from prodej import Prodej


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
        datum_nakupu = datetime.date.today()
        kod = f'KOD{self.exemplar_klic + 1:03d}'
        exemplar = Exemplar(
                self.exemplar_klic, 
                kod, 
                1, 
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
    
        i = 0
        while True:

            # Nalezení exempláře knihy na skladě
            exemplar = self.najdi_exemplar()

            # Pokud je exemplář na skladě, proveď prodej
            if exemplar:
                prodej = self.generuj_prodej(exemplar)
                self.prodeje.append(prodej)
                print(f"Prodej: {prodej}")
                if i == 10:
                    break
                i += 1

            # Pokud exemplář není na skladě, proveď nákup
            else:
                a = 0
                while a < 10:
                    nakup = self.generuj_nakup()
                    self.nakupy.append(nakup)
                    print(f"Nákup: {nakup}")
                    a += 1

# Hlavní metoda skriptu
def main():

    logging.basicConfig(level=logging.INFO)

    logging.info('Spuštění skriptu')

    """
    Když je datum 1.4.2024 tak se začne generovat nákup
    
    Tento den se například objedná n počet knih.
    V tento den se pak začne i generovat i prodej,
    náhodný počet prodaných knih

    V další den se bude dělat nákup, pouze, když
    je hodnota neprodaných knih > n

    """

    d = Databaze()
    d.generovani()
    
    print(f'Celkový výpis databáze')
    for i in d.exemplare:
        print(i)

    logging.info('Ukončení skriptu')

# Hlavní vlákno skriptu
if __name__ == "__main__":
    main()