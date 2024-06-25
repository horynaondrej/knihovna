#!/usr/bin/env python3


class Nakup:
    ''' Tabulka pro objekt nákupu
    '''

    def __init__(
        self, 
        klic, 
        datum_klic, 
        exemplar_id, 
        zamestnanec_id,
        cena
    ):
        self.klic = klic
        self.datum_klic = datum_klic
        self.exemplar_id = exemplar_id
        self.zamestnanec_id = zamestnanec_id
        self.cena = cena

    def __str__(self):
        return f'Klíč: {self.klic}, ' \
            f'Datum: {self.datum_klic}, ' \
            f'Exemplář ID: {self.exemplar_id}, ' \
            f'Zaměstnanec ID: {self.zamestnanec_id}, ' \
            f'Cena: {self.cena}'
    
    def format_sql(self):
        return (
            f"({str(self.klic)}, " \
            f"{str(self.datum_klic)}, " \
            f"{str(self.exemplar_id)}, " \
            f"{str(self.zamestnanec_id)}, " \
            f"{str(self.cena)}), " \
            )
    
    def format_csv(self):
        return (
            str(self.klic) + ';'
            + str(self.datum_klic) + ';'
            + str(self.exemplar_id) + ';'
            + str(self.zamestnanec_id) + ';'
            + str(self.cena)
            )

