from model_tl_stc.single_panel import SinglePanel
from model_tl_stc.double_panel import DoublePanel
import unittest

single_pn_a = SinglePanel(mass = 12, thick = 15, modulus = 2.5, damp = 0.1, width = 3, height = 3)
single_pn_b = SinglePanel(mass = 12, thick = 15, modulus = 2.5, damp = 0.1, width = 3, height = 3)
double_pn = DoublePanel(panel_a = single_pn_a, panel_b = single_pn_b, distance = 65, flow_res = 12000, spacing = 450)


low_freq_ref = {'f0' : 94.95611807876597, 'fl' : 846.1538461538461 }
calc_first_ref = [14.583624920952495, 16.591035823303756, 18.66602457407099]
calc_second_ref = [17.767401086571624, 22.496688470741788, 27.85323754133362, 32.77704423094312, 46.30191749508437, 52.32415020213813, 58.54911645443984, 64.36371723492324, 70.385949941977, 76.6109161942787]
calc_third_ref = [81.167249841905, 85.04365036222725, 89.33204914814198, 93.20844966846425, 65.35594301760841, 71.37817572466219, 77.60314197696391, 83.41774275744729]

total_tl_double_ref = {'stc_scale' :  [22.496688470741788, 27.85323754133362, 32.77704423094312, 46.30191749508437, 52.32415020213813, 58.54911645443984, 64.36371723492324, 70.385949941977, 
                                        76.6109161942787, 81.167249841905, 85.04365036222725, 89.33204914814198, 93.20844966846425, 65.35594301760841, 71.37817572466219, 77.60314197696391], 
                       'full_scale' :   [14.583624920952495, 16.591035823303756, 18.66602457407099, 17.767401086571624, 22.496688470741788, 27.85323754133362, 32.77704423094312, 
                                            46.30191749508437, 52.32415020213813, 58.54911645443984, 64.36371723492324, 70.385949941977, 76.6109161942787, 81.167249841905, 85.04365036222725, 
                                            89.33204914814198,  93.20844966846425, 65.35594301760841, 71.37817572466219, 77.60314197696391, 83.41774275744729]}

tl_absorb_ref = [82.80217491715341, 87.39174917732848, 92.5453759671616, 97.27898758038238, 70.36131781859358, 77.44057710243865, 84.86130124687074, 91.89555335185302]

tl_panel_with_arsorb_ref = {'stc_scale' : [22.496688470741788, 27.85323754133362, 32.77704423094312, 46.30191749508437, 52.32415020213813, 58.54911645443984, 64.36371723492324, 
                                            70.385949941977, 76.6109161942787, 82.80217491715341, 87.39174917732848, 92.5453759671616, 97.27898758038238, 70.36131781859358, 77.44057710243865, 
                                            84.86130124687074], 
                             'full_scale' : [14.583624920952495, 16.591035823303756, 18.66602457407099, 17.767401086571624, 22.496688470741788, 27.85323754133362, 32.77704423094312, 
                                            46.30191749508437, 52.32415020213813, 58.54911645443984, 64.36371723492324, 70.385949941977, 76.6109161942787, 82.80217491715341, 87.39174917732848, 
                                            92.5453759671616, 97.27898758038238, 70.36131781859358, 77.44057710243865, 84.86130124687074, 91.89555335185302]}

tl_stud_ref = {'rb': 6.394180126481707,'rm' : 15.262125019078344}

tl_panel_with_stud_ref = {'stc_scale' :[22.496688470741788, 27.85323754133362, 32.77704423094312, 46.30191749508437, 52.32415020213813, 58.54911645443984, 57.969537108441536, 
                                        63.991769815495296, 70.216736067797, 65.90512482282666, 69.78152534314891, 74.06992412906364, 77.94632464938591, 50.09381799853007, 
                                        56.116050705583845, 62.34101695788557], 
                          'full_scale' : [14.583624920952495, 16.591035823303756, 18.66602457407099, 17.767401086571624, 22.496688470741788, 
                                        27.85323754133362, 32.77704423094312, 46.30191749508437, 52.32415020213813, 58.54911645443984, 57.969537108441536, 63.991769815495296, 
                                        70.216736067797, 65.90512482282666, 69.78152534314891, 74.06992412906364, 77.94632464938591, 50.09381799853007, 56.116050705583845, 
                                        62.34101695788557, 68.15561773836895]}

tl_panel_with_stud_and_absorb_ref = {'stc_scale' : [22.496688470741788, 27.85323754133362, 32.77704423094312, 46.30191749508437, 52.32415020213813, 58.54911645443984, 
                                                    57.969537108441536, 63.991769815495296, 70.216736067797, 65.90512482282666, 69.78152534314891, 74.06992412906364, 77.94632464938591, 
                                                    50.09381799853007, 56.116050705583845, 62.34101695788557], 
                                    'full_scale' : [14.583624920952495, 16.591035823303756, 18.66602457407099, 
                                                    17.767401086571624, 22.496688470741788, 27.85323754133362, 32.77704423094312, 46.30191749508437, 52.32415020213813, 58.54911645443984, 
                                                    57.969537108441536, 63.991769815495296, 70.216736067797, 65.90512482282666, 69.78152534314891, 74.06992412906364, 77.94632464938591, 
                                                    50.09381799853007, 56.116050705583845, 62.34101695788557, 68.15561773836895]}

eval_stc_ref = {'stc' : 46, 'total_deficiency' : 15.873029756981474}

get_data_ref = {50: 22.496688470741788, 63: 27.85323754133362, 80: 32.77704423094312, 100: 46.30191749508437, 125: 52.32415020213813, 160: 58.54911645443984, 200: 64.36371723492324, 
                250: 70.385949941977, 315: 76.6109161942787, 400: 82.80217491715341, 500: 87.39174917732848, 630: 92.5453759671616, 800: 97.27898758038238, 1000: 70.36131781859358, 
                1250: 77.44057710243865, 1600: 84.86130124687074}

get_info_ref = {'STC': 46, 'Total Deficiency': 15.873029756981474}

class TestDoublePanel(unittest.TestCase):
    """ test all function in DoublePanel Class, except full_scale_plot(), stc_scale_plot(), get_data_pd() """
    def test_low_frequency(self):
        low_freq_value = double_pn.low_frequency()
        self.assertEqual(low_freq_value, low_freq_ref)

    def test_calculation_first_condition(self):
        calc_first_value = double_pn.calculation_first_condition()
        self.assertEqual(calc_first_value, calc_first_ref)

    def test_calculation_second_condtion(self):
        calc_second_value = double_pn.calculation_second_condtion()
        self.assertEqual(calc_second_value, calc_second_ref)

    def test_calculation_third_condition(self):
        calc_third_value = double_pn.calculation_third_condition()
        self.assertEqual(calc_third_value, calc_third_ref)

    def test_tl_double_panel(self):
        total_tl_double_value = double_pn.tl_double_panel()
        self.assertEqual(total_tl_double_value, total_tl_double_ref)

    def test_tl_absorber(self):
        tl_absorb_value = double_pn.tl_absorber()
        self.assertEqual(tl_absorb_value, tl_absorb_ref)

    def test_tl_panel_and_absorber(self):
        tl_panel_with_arsorb_value = double_pn.tl_panel_and_absorber()
        self.assertEqual(tl_panel_with_arsorb_value, tl_panel_with_arsorb_ref)

    def test_tl_stud(self):
        tl_stud_value = double_pn.tl_stud()
        self.assertEqual(tl_stud_value, tl_stud_ref)

    def test_tl_panel_and_stud(self):
        tl_panel_with_stud_value = double_pn.tl_panel_and_stud()
        self.assertEqual(tl_panel_with_stud_value, tl_panel_with_stud_ref)

    def test_tl_panel_with_stud_and_absorber(self):
        tl_panel_with_stud_and_absorb_value = double_pn.tl_panel_with_stud_and_absorber()
        global TL_FOR_TEST
        TL_FOR_TEST = tl_panel_with_stud_and_absorb_value
        self.assertEqual(tl_panel_with_stud_and_absorb_value, tl_panel_with_stud_and_absorb_ref)

    def test_evaluate_stc(self):
        eval_stc_value = double_pn.evaluate_stc(tl_panel_with_stud_and_absorb_ref)
        self.assertEqual(eval_stc_value, eval_stc_ref)

    def test_get_data(self):
        get_data_value = double_pn.get_data(tl_panel_with_arsorb_ref)
        self.assertEqual(get_data_value, get_data_ref)

    def test_get_info(self):
        get_info_value = double_pn.get_info(tl_panel_with_arsorb_ref)
        self.assertEqual(get_info_value, get_info_ref)