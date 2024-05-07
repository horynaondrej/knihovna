# Třída pro objekt zaměstnanec knihovny
class Zamestnanec:

    def __init__(self, klic, zamestnanec_id, prijmeni, jmeno):
        self.klic = klic
        self.zamestnanec_id = zamestnanec_id
        self.prijmeni = prijmeni
        self.jmeno = jmeno

    def format_sql(self):
        return (
            '(' + str(self.klic) + ', ' \
            + '\'' + str(self.zamestnanec_id) + '\', '
            + '\'' + self.prijmeni + '\', '
            + '\'' + self.jmeno + '\'),'
            )

    def format_csv(self):
        return (
            str(self.klic) + ';' \
            + str(self.zamestnanec_id) + ';'
            + self.prijmeni + ';'
            + self.jmeno + ''
            )