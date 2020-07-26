import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

############################################################
##### Sound Transmission Loss ##############################
##### Single Panel Predicetive Model #######################
############################################################
############################################################
##### Author : Peem Srinikorn ##############################
##### 29 Oct 2018 ##########################################
############################################################
########## Reference Equation,formula from Insul ###########
############################################################
##########  Document Reference #############################
############################################################
########## Jason Esan Cambridge (2006). ####################
## Prediction tools for airborne sound insulation- #########
## evaluation and application. Department of Civil #########
########### and Environmental Engineering ##################
############ Division of Applied Acoustics,#################
############ CHALMERS UNIVERSITY OF TECHNOLOGY, Sweden #####
############################################################
########## for study only ##################################
############################################################


class DoublePanel():
    """ 
    DoublePanel()
    is used for calculation the Transmission Loss (TL) using material value of Double Panel, Absorber and Stud,
    with evaluation as Sound Transmission Class (STC) metric and Pandas DataFrame.
    """
    def __init__(self, panel_a : object, panel_b : object, distance : float, flow_res : float, spacing :float):
        self.distance = distance/1000 #distance between Panel_A and Panel_B -> unit millimetre
        self.flow_res = flow_res #flow resistance of Absorber -> Rayl/m
        self.tl_panel_a = panel_a.tl_summarize()['full_scale'] #TL_A
        self.tl_panel_b = panel_b.tl_summarize()['full_scale'] # TL_B
        self.spacing = spacing/1000 # spacing of line connection
        self.mass_a = panel_a.mass
        self.mass_b = panel_b.mass
        self.cf_a = panel_a.critical_freq()
        self.cf_b = panel_b.critical_freq()
        self.height_a = panel_a.height
        self.height_b = panel_b.height
        self.area_a = panel_a.area
        self.area_b = panel_b.area
        self.freq_std = [50, 63, 80,100,125,160,200,250,315,400,500,630,800,1000,1250,1600,2000,2500,3150,4000,5000] #1/3 Octave freq band
        self.c = 343 #speed of airborne sound
        self.p_air = 1.18 # Airborne Sound Density

    def low_frequency(self):
        me = ((self.p_air * (self.c ** 2)) / self.distance) * ((1 / self.mass_a)+(1 / self.mass_b))
        return {'f0' : (1 / (2 * np.pi)) * (np.sqrt(me)), 'fl' : 55 / self.distance }

    def calculation_first_condition(self): # f < f0
        f0 = self.low_frequency()['f0']
        return [20 * np.log10(self.freq_std[i] * (self.mass_a + self.mass_b))-47 for i in range(0,len(self.freq_std)) if self.freq_std[i] < f0]

    def calculation_second_condtion(self): # f > f0 and f < fl
        f0 = self.low_frequency()['f0']
        fl = self.low_frequency()['fl']
        return [self.tl_panel_a[i] + self.tl_panel_b[i] + 20*np.log10(self.freq_std[i] * self.distance) -29 for i in range(0,len(self.freq_std)) if self.freq_std[i] >= f0 and self.freq_std[i] <= fl]

    def calculation_third_condition(self): # f > fl
        fl = self.low_frequency()['fl']
        return [self.tl_panel_a[i] + self.tl_panel_b[i] + 6 for i in range(0,len(self.freq_std)) if self.freq_std[i] > fl]

    def tl_double_panel(self): # Total TL of Double Panel
        total_calc = self.calculation_first_condition() + self.calculation_second_condtion() + self.calculation_third_condition()
        tl_total_double = [total_calc[i] for i in range(0, len(self.freq_std)) if self.freq_std[i] >= 125 and self.freq_std[i] <= 4000]
        return  {'stc_scale' : tl_total_double, 'full_scale' : total_calc}

    def tl_absorber(self): # Absorber Cal
        fl = self.low_frequency()['fl']
        f_absorber = [self.freq_std[i] for i in range(0,len(self.freq_std)) if self.freq_std[i] > fl]
        k_val = [(2 * np.pi * f_absorber[i]) / self.c for i in range(0, len(f_absorber))]
        omega = [(2 * np.pi * f_absorber[i]) for i in range(0, len(f_absorber))]
        prob = [((omega[i] / self.c) * 0.189 * (self.p_air * f_absorber[i] / self.flow_res) ** -0.595) + ( 1j * (omega[i] / self.c) * ((1 + 0.0978 * (self.p_air * f_absorber[i]) / (self.flow_res)) ** -0.7)) for i in range(0, len(f_absorber))]
        alpha = [prob[i].real for i in range(0, len(prob))]
        beta = [prob[i].imag for i in range(0, len(prob))]
        total_calc = [self.tl_panel_a[i] + self.tl_panel_b[i] for i in range(0, len(self.freq_std)) if self.freq_std[i] > fl]
        return [total_calc[i] + 8.6 * alpha[i] * self.distance + 20*np.log10(beta[i] / k_val[i]) for i in range(0, len(f_absorber))] #tl of absorber

    def tl_panel_and_absorber(self): # Total TL Double Panel with Absorber
        total_calc = self.calculation_first_condition() + self.calculation_second_condtion() + self.tl_absorber()
        return {'stc_scale' : [total_calc[i] for i in range(0, len(self.freq_std)) if self.freq_std[i] >= 125 and self.freq_std[i] <= 4000], 'full_scale' : total_calc}

    def tl_stud(self): #stud line connection calculation
        delta_rb = 10*np.log10(self.spacing * self.cf_a)+ 20 * np.log10((self.mass_a / (self.mass_a + self.mass_b))) -18
        fcl = (((self.mass_a * np.sqrt(self.cf_b))+(self.mass_b * np.sqrt(self.cf_a))) / (self.mass_a + self.mass_b)) **2
        delta_rm = 10*np.log10(((self.area_a) / (self.height_a))*((np.pi*fcl) / (2*self.c)))
        return {'rb' : delta_rb, 'rm' :delta_rm }

    def tl_panel_and_stud(self): #Total TL of Double Panel with Stud
        fl = self.low_frequency()['fl']
        delta_rb = self.tl_stud()['rb']
        delta_rm = self.tl_stud()['rm']
        tl_double_panel = self.tl_double_panel()['full_scale']
        calc_first_cond = [ tl_double_panel[i] for i in range(0,len(self.freq_std)) if self.freq_std[i] <= fl*0.5 ]
        calc_second_cond = [ tl_double_panel[i] - delta_rb for i in range(0,len(self.freq_std)) if self.freq_std[i] >= fl*0.5 and self.freq_std[i] <= fl]
        calc_third_cond = [ tl_double_panel[i] - delta_rm for i in range(0,len(self.freq_std)) if self.freq_std[i] >= fl]
        total_calc = calc_first_cond + calc_second_cond + calc_third_cond
        return {'stc_scale' :  [total_calc[i] for i in range(0, len(self.freq_std)) if self.freq_std[i] >= 125 and self.freq_std[i] <= 4000] ,'full_scale' : total_calc}

    def tl_panel_with_stud_and_absorber(self): #Total TL of Double Panel with Absorber and Stud
        fl = self.low_frequency()['fl']
        delta_rb = self.tl_stud()['rb']
        delta_rm = self.tl_stud()['rm']
        tl_double_panel = self.tl_double_panel()['full_scale']
        calc_first_cond = [ tl_double_panel[i] for i in range(0,len(self.freq_std)) if self.freq_std[i] <= 0.5 * fl ]
        calc_second_cond = [ tl_double_panel[i] - delta_rb for i in range(0,len(self.freq_std)) if self.freq_std[i] >= 0.5*fl and self.freq_std[i] <= fl]
        calc_third_cond = [ tl_double_panel[i] - delta_rm for i in range(0,len(self.freq_std)) if self.freq_std[i] >= fl]
        total_calc = calc_first_cond + calc_second_cond + calc_third_cond
        return {'stc_scale' :  [total_calc[i] for i in range(0, len(self.freq_std)) if self.freq_std[i] >= 125 and self.freq_std[i] <= 4000], 'full_scale' : total_calc}

    def evaluate_stc(self, tl_value):  # Evaluation Standard Transmission loss
        stc_range = [[i - 16, i - 13, i - 10, i - 7, i - 4, i - 1, i, i + 1, i + 2, i + 3, i + 4, i + 4, i + 4, i + 4, i + 4, i + 4] for i in range(150)]  # STC Contour = [12.45,14,15.45,20.9,22.9,24.9,26.9,28.9,31,32.9,34.8,37,38.9,40.9,17.7,20.8]
        r = tl_value['stc_scale']
        for idx in range(0, len(stc_range)):  # STC Contour Condition
            for sub_idx in range(0, 16):
                if r[sub_idx] < stc_range[idx][sub_idx]:
                    stc_range[idx][sub_idx] = abs(r[sub_idx] - stc_range[idx][sub_idx])  # TL below STC contour
                else:
                    stc_range[idx][sub_idx] = 0
        total_raw_def = [stc_range[idx] if sum(stc_range[idx]) <= 32 else False for idx in range(0, len(stc_range))]  # total deficiency condition
        total_def = [total_raw_def[idx] for idx in range(0, len(total_raw_def)) if total_raw_def[idx] != False]  # silce total deficiency > 32
        for idx in range(0, len(total_def)):
            for sub_idx in range(0, 16):
                if total_def[idx][sub_idx] > 8: # index more than 8
                    total_def[idx][sub_idx] = False

        total_def_without_false = [stc_val for stc_val in total_def if not any(isinstance(bool_val, (str, bool)) for bool_val in stc_val)] # clear False
        max_stc = (len(total_def_without_false) - 1) # Maximum STC
        sum_def = sum(total_def_without_false[max_stc]) # Deficiency STC
        return {'stc' : max_stc, 'total_deficiency' : sum_def }

    def full_scale_plot(self, tl_value):  # Visualize the Transmission loss data as Full range frequency
        freq = [50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000]  # 1/3 Octave freq band
        x_axis = [i for i in range(0, len(freq))]
        plt.figure(figsize=(18, 8))
        plt.plot(tl_value['full_scale'], 'b', linewidth=2)
        plt.annotate('Initials : Peem Srinikorn', xy=(0.85, 0.04), fontsize=12, bbox=dict(facecolor='cyan', alpha=0.5), xycoords='axes fraction')
        plt.title('Sound Transmission loss ', fontsize=18)
        plt.xlabel('1/3 Octave Frequency [Hz]', fontsize=15)
        plt.ylabel('R Transmiss loss [dB]', fontsize=15)
        plt.legend(['Transmission loss'], fontsize=15, loc='best')
        plt.xticks(x_axis, freq, fontsize=12)
        plt.yticks(fontsize=12)
        plt.grid(linestyle='-', linewidth=0.5)
        return plt.show()

    def stc_scale_plot(self, tl_value):  # Visualize the Transmission loss data as Full range frequency
        freq = [125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000]  # 1/3 Octave freq band
        val = self.evaluate_stc(tl_value)['stc']
        stc_contour = [val - 16, val - 13, val - 10, val - 7, val - 4, val - 1, val, val + 1, val + 2, val + 3, val + 4, val + 4, val + 4, val + 4, val + 4, val + 4]  # STC Contour
        x_axis = [i for i in range(0, len(freq))]
        plt.figure(figsize=(18, 8))
        plt.plot(tl_value['stc_scale'], 'b', linewidth=2)
        plt.plot(stc_contour, 'g--', linewidth=1.8)
        plt.annotate('Initials : Peem Srinikorn', xy=(0.85, 0.04), fontsize=12, bbox=dict(facecolor='cyan', alpha=0.5), xycoords='axes fraction')
        plt.title('Sound Transmission loss ', fontsize=18)
        plt.xlabel('1/3 Octave Frequency [Hz]', fontsize=15)
        plt.ylabel('R Transmiss loss [dB]', fontsize=15)
        plt.legend(['Transmission loss', 'STC {}'.format(stc_contour[6])], fontsize=15, loc='best')
        plt.xticks(x_axis, freq, fontsize=12)
        plt.yticks(fontsize=12)
        plt.grid(linestyle='-', linewidth=0.5)
        return plt.show()

    def get_data_pd(self, tl_value):  # Data of Trnamission loss in 1/3 Octave frequency band
        return pd.DataFrame({'Frequency (Hz)': self.freq_std, 'Transmission loss (dB)': tl_value['full_scale']})

    def get_data(self, tl_value):
        return dict(zip(self.freq_std ,tl_value['stc_scale']))

    def get_info(self, tl_value):  # STC , total deficiency
        return {'STC': self.evaluate_stc(tl_value)['stc'], 'Total Deficiency': self.evaluate_stc(tl_value)['total_deficiency']}

############################################################
##### Sound Transmission Loss ##############################
##### Single Panel Predicetive Model #######################
############################################################
############################################################
##### Author : Peem Srinikorn ##############################
##### 29 Oct 2018 ##########################################
############################################################
########## Reference Equation,formula from Insul ###########
############################################################
##########  Document Reference #############################
############################################################
########## Jason Esan Cambridge (2006). ####################
## Prediction tools for airborne sound insulation- #########
## evaluation and application. Department of Civil #########
########### and Environmental Engineering ##################
############ Division of Applied Acoustics,#################
############ CHALMERS UNIVERSITY OF TECHNOLOGY, Sweden #####
############################################################
########## for study only ##################################
############################################################
