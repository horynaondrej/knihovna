#!/usr/bin/env python3

# Třída pro objekt produkt
class Kniha:

    def __init__(
            self, 
            klic, 
            kniha_id, 
            spisovatel_id, 
            nazev, 
            rok_vydani,
            cena
        ):
        self.klic = klic
        self.kniha_id = kniha_id
        self.spisovatel_id = spisovatel_id
        self.nazev = nazev
        self.rok_vydani = rok_vydani
        self.cena = cena

    def format_sql(self):
        return (
            '(' + str(self.klic) + ', ' \
            + str(self.kniha_id) + ', ' \
            + str(self.spisovatel_id) + ', ' \
            +  '\'' + self.nazev + '\', ' \
            + str(self.rok_vydani) + '\', ' \
            + str(self.cena) + ')'
            )

    def format_csv(self):
        return (
            str(self.klic) + ';' \
            + str(self.kniha_id) + ';' \
            + str(self.spisovatel_id) + ';' \
            + self.nazev + ';' \
            + str(self.rok_vydani) + ';' \
            + str(self.cena)
            )