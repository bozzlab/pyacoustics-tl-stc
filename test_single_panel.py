from model_tl_stc.single_panel import SinglePanel
import unittest

single_pn = SinglePanel(mass = 7, thick = 10, modulus = 4, damp = 0.1, width = 3, height = 4)

mass_law_ref = [6.881360887005513, 8.888771789356774, 10.963760540124007, 12.901960800285138, 14.840161060446263, 16.98436045340363, 18.922560713564764, 20.86076097372589, 
                    22.86817187607714, 24.94316062684439, 26.881360887005513, 28.888771789356767, 30.963760540124, 32.90196080028514, 34.84016106044626, 36.98436045340364, 38.92256071356476, 
                    40.86076097372589, 27.55707079927498, 30.66955392542583, 33.57685431566752]

low_freq_ref= [-0.6273546031272578, -1.4214890827459246, -2.1150965832166233, -2.678296447364831, -3.1800911451218017, -3.6809941617522903, -4.097270185934576]

critical_freq_ref = 2712.0693113483285

summarize_ref = {'stc_scale' : [11.660069915324462, 13.303366291651342, 14.825290527630187, 20.86076097372589, 22.86817187607714, 24.94316062684439, 26.881360887005513,  28.888771789356767, 
                                30.963760540124, 32.90196080028514, 34.84016106044626, 36.98436045340364, 38.92256071356476, 40.86076097372589, 27.55707079927498, 30.66955392542583], 
                'full_scale' : [6.2540062838782555, 7.467282706610849, 8.848663956907384, 10.223664352920308, 11.660069915324462, 13.303366291651342, 14.825290527630187, 20.86076097372589, 
                                22.86817187607714, 24.94316062684439, 26.881360887005513, 28.888771789356767, 30.963760540124, 32.90196080028514, 34.84016106044626, 36.98436045340364, 
                                38.92256071356476, 40.86076097372589, 27.55707079927498, 30.66955392542583, 33.57685431566752] }

eval_stc_ref = {'stc' : 29, 'total_deficiency' : 25.5786618475595}
get_data_ref = {50: 6.2540062838782555, 63: 7.467282706610849, 80: 8.848663956907384, 100: 10.223664352920308, 125: 11.660069915324462, 160: 13.303366291651342, 
                200: 14.825290527630187, 250: 20.86076097372589, 315: 22.86817187607714, 400: 24.94316062684439, 500: 26.881360887005513, 630: 28.888771789356767, 
                800: 30.963760540124, 1000: 32.90196080028514, 1250: 34.84016106044626, 1600: 36.98436045340364, 2000: 38.92256071356476, 2500: 40.86076097372589, 
                3150: 27.55707079927498, 4000: 30.66955392542583, 5000: 33.57685431566752}
get_info_ref = {'STC': 29, 'Total Deficiency': 25.5786618475595, 'Mass (kg)': 7, 'Thickness (mm)': 10.0, 'Young Modulus (GPa)': 4.0, 'Damping Ratio': 0.1, 'Area (m^2)': 12}

class TestSinglePanel(unittest.TestCase):
    """ test all function in SinglePanel Class, except plot() """
    def test_mass_law(self):
        mass_law_value = single_pn.mass_law()
        self.assertEqual(mass_law_value, mass_law_ref)

    def test_critical_freq(self):
        critical_freq_value = single_pn.critical_freq()
        self.assertEqual(critical_freq_value, critical_freq_ref)

    def test_low_frequency(self):
        low_freq_value = single_pn.low_frequency()
        self.assertEqual(low_freq_value, low_freq_ref)
    
    def test_summarize(self):
        summarize_value = single_pn.tl_summarize()
        self.assertEqual(summarize_value, summarize_ref)

    def test_evaluate_stc(self):
        eval_stc_value = single_pn.evaluate_stc()
        self.assertEqual(eval_stc_value, eval_stc_ref)

    def test_get_data(self):
        get_data_value = single_pn.get_data()
        self.assertEqual(get_data_value, get_data_ref)

    def test_get_info(self):
        get_info_value = single_pn.get_info()
        self.assertEqual(get_info_value, get_info_ref)
