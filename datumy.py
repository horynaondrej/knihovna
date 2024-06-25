# Třída pro objekt spisovatel
class Datum:

    def __init__(self, klic, datum_id):
        self.klic = klic
        self.datum_id = datum_id.strftime('%Y%m%d')

        # Datum
        self.datum = datum_id.strftime("%d.%m.%Y")

        # Rok
        self.rok = datum_id.strftime("%Y")

        # Měsíc číslo
        self.mesic_cislo = datum_id.month

        # Měsíc slovně
        self.mesic_oznaceni = {
            1: "Leden",
            2: "Únor",
            3: "Březen",
            4: "Duben",
            5: "Květen",
            6: "Červen",
            7: "Červenec",
            8: "Srpen",
            9: "Září",
            10: "Říjen",
            11: "Listopad",
            12: "Prosinec"
        }[datum_id.month]

        # Čtvrtletí číslem
        self.ctvrtleti_cislo = (datum_id.month - 1) // 3 + 1

        # Čtvrtletí slovně
        self.ctvrtleti_oznaceni = "Q" + str((datum_id.month - 1) // 3 + 1)

        # RokMěsíc
        self.rok_mesic = datum_id.strftime("%Y%m")

        # RokČtvrtletí
        self.rok_ctvrtleti = datum_id.strftime("%Y" + "Q" + str(self.ctvrtleti_cislo))

    def format_sql(self):
        return (
            '(' + str(self.klic) + ', ' \
            + str(self.datum_id) + ', ' \
            + '\'' + str(self.datum)+ '\', ' \
            + str(self.rok) + ', ' \
            + str(self.mesic_cislo) + ', ' \
            + '\'' + str(self.mesic_oznaceni) + '\', ' \
            + str(self.ctvrtleti_cislo) + ', ' \
            + '\'' + str(self.ctvrtleti_oznaceni) + '\', ' \
            + '\'' + str(self.rok_mesic) + '\', ' \
            + '\'' + str(self.rok_ctvrtleti) + '\'),' 
            )

    def format_csv(self):
        return (
            str(self.klic) + ';' \
            + str(self.datum_id) + ';' \
            + str(self.datum) + ';' \
            + str(self.rok) + ';' \
            + str(self.mesic_cislo) + ';' \
            + str(self.mesic_oznaceni) + ';' \
            + str(self.ctvrtleti_cislo) + ';' \
            + str(self.ctvrtleti_oznaceni) + ';' \
            + str(self.rok_mesic) + ';' \
            + str(self.rok_ctvrtleti) + '' 
            )