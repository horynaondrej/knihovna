# Třída pro objekt spisovatel
class Spisovatel:

    def __init__(self, klic, spisovatel_id, prijmeni, jmeno):
        self.klic = klic
        self.spisovatel_id = spisovatel_id
        self.prijmeni = prijmeni
        self.jmeno = jmeno

    def format_sql(self):
        return (
            '(' + str(self.klic) + ', ' \
            + '\'' + str(self.spisovatel_id)+ '\', ' \
            + '\'' + self.prijmeni + '\', ' \
            + '\'' + self.jmeno + '\'),' 
            )

    def format_csv(self):
        return (
            str(self.klic) + ';' \
            + str(self.spisovatel_id) + ';' \
            + self.prijmeni + ';' \
            + self.jmeno + '' 
            )