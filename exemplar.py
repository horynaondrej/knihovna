#!/usr/bin/env python3


class Exemplar:
    ''' Představuje instanci exempláře knihy
    '''

    def __init__(
        self, 
        klic, 
        kod, 
        kniha_id, 
        nakoupeni, 
        prodani
    ):
        self.klic = klic
        self.kod = kod
        self.kniha_id = kniha_id
        self.nakoupeni = nakoupeni
        self.prodani = prodani
    
    def __str__(self):
        return f'Klíč: {self.klic}, ' \
        f'Kód: {self.kod}, ' \
        f'Kniha: {self.kniha_id}, ' \
        f'Nakoupeni: {self.nakoupeni}, ' \
        f'Prodání: {self.prodani}'

    def format_csv(self):
        return (
            str(self.klic) + ';'
            + str(self.kod) + ';'
            + str(self.kniha_id) + ';'
            + str(self.nakoupeni) + ';'
            + str(self.prodani if self.prodani is not None else '')
            )