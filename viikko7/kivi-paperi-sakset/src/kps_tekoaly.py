from tekoaly import Tekoaly
from kivi_paperi_sakset import KiviPaperiSakset


class KPSTekoaly(KiviPaperiSakset):  
    def __init__(self):
        self._tekoaly = Tekoaly()

    def _toisen_siirto(self, ensimmaisen_siirto):
        toka_siirto = self._tekoaly.anna_siirto()
        print(f"Tietokone valitsi: {toka_siirto}")
        self._tekoaly.aseta_siirto(ensimmaisen_siirto)
        return toka_siirto