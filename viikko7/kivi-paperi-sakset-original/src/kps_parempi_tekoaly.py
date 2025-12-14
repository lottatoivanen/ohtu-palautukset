from tekoaly_parannettu import TekoalyParannettu
from kivi_paperi_sakset import KiviPaperiSakset


class KPSParempiTekoaly(KiviPaperiSakset):
    def __init__(self, muistin_koko=20):
        self._tekoaly = TekoalyParannettu(muistin_koko)

    def _toisen_siirto(self, ensimmaisen_siirto):
        toka_siirto = self._tekoaly.anna_siirto()
        print(f"Tietokone valitsi: {toka_siirto}")
        self._tekoaly.aseta_siirto(ensimmaisen_siirto)
        return toka_siirto