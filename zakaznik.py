# Třída pro objekt zaměstnanec knihovny
class Zakaznik:

    def __init__(self, klic, zakaznik_id, prijmeni, jmeno, mesto, mesto_kod, ulice, cislo, psc):
        self.klic = klic
        self.zakaznik_id = zakaznik_id
        self.prijmeni = prijmeni
        self.jmeno = jmeno
        self.mesto = mesto
        self.mesto_kod = mesto_kod
        self.ulice = ulice
        self.cislo = cislo
        self.psc = psc

    def format_sql(self):
        return (
            '(' + str(self.klic) + ', ' \
            + '\'' + str(self.zakaznik_id) + '\', '
            + '\'' + self.prijmeni + '\', '
            + '\'' + self.jmeno + '\','
            + '\'' + self.mesto + '\','
            + '' + str(self.mesto_kod) + ','
            + '\'' + self.ulice + '\','
            + '' + str(self.cislo) + ','
            + '' + str(self.psc) + '),'
            )

    def format_csv(self):
        return (
            str(self.klic) + ';'
            + str(self.zakaznik_id) + ';'
            + self.prijmeni + ';'
            + self.jmeno + ';'
            + self.mesto + ';'
            + str(self.mesto_kod) + ';'
            + self.ulice + ';'
            + str(self.cislo) + ';'
            + str(self.psc) + ''
            )