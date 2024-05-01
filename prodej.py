#!/usr/bin/env python3


class Prodej:
    ''' Třída představující instanci prodeje
    '''

    def __init__(
        self, 
        klic, 
        datum_klic, 
        exemplar_id, 
        cena
    ):
        self.klic = klic
        self.datum_klic = datum_klic
        self.exemplar_id = exemplar_id
        self.cena = cena
    
    def __str__(self):
        return f'Klíč: {self.klic}, ' \
        f'Datum: {self.datum_klic}, ' \
        f'Exemplář ID: {self.exemplar_id}, ' \
        f'Cena: {self.cena}'
