import unittest
from statistics_service import StatisticsService
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(
            PlayerReaderStub()
        )

    def test_search_palauttaa_jos_nimi_loydetaan_taysin(self):
        player = self.stats.search("Semenko")
        self.assertIsNotNone(player)
        self.assertEqual(player.name, "Semenko")
        self.assertEqual(player.points, 16)

    def test_search_palauttaa_jos_nimi_loydetaan_osittain(self):
        player = self.stats.search("Gretz")
        self.assertIsNotNone(player)
        self.assertEqual(player.name, "Gretzky")

    def test_search_palauttaa_none_jos_ei_loydy(self):
        self.assertIsNone(self.stats.search("Granlund"))

    def test_team_palauttaa_vain_oikean_joukkueen(self):
        edm = self.stats.team("EDM")
        names = {player.name for player in edm}
        self.assertEqual(len(edm), 3)
        self.assertSetEqual(names, {"Semenko", "Kurri", "Gretzky"})

    def test_team_tyhja_jos_ei_loydy(self):
        self.assertEqual(self.stats.team("NYI"), [])

    def test_top_jarjestys_on_laskeva(self):
        expected = ["Gretzky", "Lemieux", "Yzerman", "Kurri", "Semenko"]
        with self.assertRaises(IndexError):
            self.stats.top(10)

    def test_top_nolla_palauttaa_parhaan(self):
        top1 = self.stats.top(0)
        self.assertEqual(len(top1), 1)
        self.assertEqual(top1[0].name, "Gretzky")

    def test_top_palauttaa_pelaajien_maaran(self):
        top3 = self.stats.top(3)
        self.assertEqual(len(top3), 4)
        self.assertEqual([player.name for player in top3],
                         ["Gretzky", "Lemieux", "Yzerman", "Kurri"])

    def test_top_yli_pituuden_palauttaa_kaikki(self):
        with self.assertRaises(IndexError):
            self.stats.top(100)