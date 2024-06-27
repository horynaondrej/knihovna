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
    
    def format_sql(self):
        return (
            '(' + str(self.klic) + ', ' \
            +  '\'' + str(self.kod) + '\', ' \
            + str(self.kniha_id) + ', ' \
            + str(self.nakoupeni) + ', ' \
            + str(self.prodani if self.prodani is not None else '22001231') + '),'
            )

    def format_csv(self):
        return (
            str(self.klic) + ';'
            + str(self.kod) + ';'
            + str(self.kniha_id) + ';'
            + str(self.nakoupeni) + ';'
            + str(self.prodani if self.prodani is not None else '22001231')
            )
    