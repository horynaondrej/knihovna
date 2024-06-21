# Třída pro objekt spisovatel
class Kategorie:

    def __init__(self, klic, kategorie_id, oznaceni):
        self.klic = klic
        self.kategorie_id = kategorie_id
        self.oznaceni = oznaceni

    def format_sql(self):
        return (
            '(' + str(self.klic) + ', ' \
            + '\'' + str(self.kategorie_id)+ '\', ' \
            + '\'' + self.oznaceni + '\'),' 
            )

    def format_csv(self):
        return (
            str(self.klic) + ';' \
            + str(self.kategorie_id) + ';' \
            + self.oznaceni + '' 
            )