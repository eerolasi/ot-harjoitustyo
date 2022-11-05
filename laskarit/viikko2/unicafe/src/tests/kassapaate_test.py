#Luodun kassapäätteen rahamäärä ja myytyjen lounaiden määrä on oikea (rahaa 1000 euroa, lounaita myyty 0)
import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassa = Kassapaate()
        self.maksukortti = Maksukortti(1000)

    def test_kassa_on_olemassa(self):
        self.assertNotEqual(self.kassa, None)

    def test_saldo_alussa(self):
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)

    def test_edullisten_myynti_aluksi(self):
        self.assertEqual(self.kassa.edulliset, 0)

    def test_maukkaiden_myynti_aluksi(self):
        self.assertEqual(self.kassa.maukkaat, 0)

    def test_edullinen_katesiosto_tasarahalla(self):
        self.kassa.syo_edullisesti_kateisella(240)
        self.assertEqual(self.kassa.kassassa_rahaa, 100240)
        self.assertEqual(self.kassa.edulliset, 1)

    def test_maukkaiden_kateisosto_tasarahalla(self):
        self.kassa.syo_maukkaasti_kateisella(400)
        self.assertEqual(self.kassa.kassassa_rahaa, 100400)
        self.assertEqual(self.kassa.maukkaat, 1)

    def test_edullisen_kateisosto_vaihtoraha(self):
        self.assertEqual(self.kassa.syo_edullisesti_kateisella(300), 60)

    def test_maukkaan_kateisosto_vaihtoraha(self):
        self.assertEqual(self.kassa.syo_maukkaasti_kateisella(450), 50)

    def test_edullinen_kateisosto_ei_riittava(self):
        self.assertEqual(self.kassa.syo_edullisesti_kateisella(200), 200)

    def test_maukas_kateisosto_ei_riittava(self):
        self.assertEqual(self.kassa.syo_maukkaasti_kateisella(350), 350)

    def test_edullisen_korttiosto_onnistuu(self):
        self.assertEqual(self.kassa.syo_edullisesti_kortilla(self.maksukortti), True)
        self.assertEqual(self.maksukortti.saldo, 760)
        self.assertEqual(self.kassa.edulliset, 1)

    def test_maukkaan_korttiosto_onnistuu(self):
        self.assertEqual(self.kassa.syo_maukkaasti_kortilla(self.maksukortti), True)
        self.assertEqual(self.maksukortti.saldo, 600)
        self.assertEqual(self.kassa.maukkaat, 1)

    def test_edullisen_korttioston_saldo_ei_riittava(self):
        maksukortti = Maksukortti(200)
        self.assertEqual(self.kassa.syo_edullisesti_kortilla(maksukortti), False)

    def test_maukkaan_korttioston_saldo_ei_riittava(self):
        maksukortti = Maksukortti(300)
        self.assertEqual(self.kassa.syo_maukkaasti_kortilla(maksukortti), False)

    def test_kortille_rahan_lataaminen_positiivisella_summalla(self):
        self.kassa.lataa_rahaa_kortille(self.maksukortti, 200)
        self.assertEqual(self.kassa.kassassa_rahaa, 100200)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 12.00 euroa")

    def test_kortille_rahan_lataaminen_negatiivisella_summalla(self):
        self.kassa.lataa_rahaa_kortille(self.maksukortti, -200)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")





