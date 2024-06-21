# Třída pro objekt spisovatel
class Nakladatel:

    def __init__(self, klic, nakladatel_id, nazev):
        self.klic = klic
        self.nakladatel_id = nakladatel_id
        self.nazev = nazev

    def format_sql(self):
        return (
            '(' + str(self.klic) + ', ' \
            + '\'' + str(self.nakladatel_id)+ '\', ' \
            + '\'' + self.nazev + '\'),' 
            )

    def format_csv(self):
        return (
            str(self.klic) + ';' \
            + str(self.nakladatel_id) + ';' \
            + self.nazev + '' 
            )