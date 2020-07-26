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

class SinglePanel():
    """ 
    SinglePanel()
    is used for calculation the Transmission Loss (TL) using material value of Panel,
    with evaluation as Sound Transmission Class (STC) metric.
    """
    def __init__(self, mass : float, thick : float, modulus : float, damp : float, width : float, height : float): #Essential Attribute
        self.mass = mass #mass as Kg unit
        self.thick = thick / 1000 # thickness as mm unit
        self.modulus = modulus * 10 ** 9 #Young modulus as GPa unit
        self.damp = damp #damping ratio
        self.area = width * height #area of Sample as m^2 unit
        self.freq_std = [50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000] #1/3 Octave freq band
        self.c = 343 #speed of airborne sound
        self.height = height # for calculate delta Rm

    def critical_freq(self):  # calc Critical Frequency or Resonant frequency
        return ((self.c ** 2) / 6.283185) * (np.sqrt(self.mass / (((self.modulus) * ((self.thick) ** 3)) / 11.988)))

    def mass_law(self):  # calc TL by mass_law with Bending waves or Resotant transmission
        f = self.freq_std
        cf = self.critical_freq()
        t1 = [(20 * (np.log10(self.mass * self.freq_std[i])) - 44) for i in range(0, len(self.freq_std)) if self.freq_std[i] <= cf]
        t2 = [(20 * (np.log10(self.mass * self.freq_std[i]))) + (10 * np.log10((2 * self.damp * self.freq_std[i]) / (np.pi * cf))) - 48 for i in range(0, len(self.freq_std)) if self.freq_std[i] >= cf]
        return t1 + t2

    def low_frequency(self):  # calc low-frequency correction (TL below 200 Hz)
        cf = self.critical_freq()
        f_low = [50, 63, 80, 100, 125, 160, 200]
        omega_c = 2 * np.pi * cf
        kw = [(2 * np.pi * f_low[i]) / self.c for i in range(0, len(f_low))]
        omega = [(2 * np.pi * f_low[i]) for i in range(0, len(f_low))]
        return [-10 * np.log10(np.log(kw[i] * (self.area ** 0.5))) + 20 * np.log10(1 - (omega[i] / omega_c) ** 2) for i in range(0, len(f_low))]

    def tl_summarize(self):  # tl_summarize formula
        tl = self.mass_law()
        r_low = self.low_frequency()
        cf = self.critical_freq()
        f = self.freq_std

        for i in range(0, len(f)):
            if f[i] <= 200:
                tl[i] = tl[i] + r_low[i]
            else:
                tl[i] = tl[i]
        return {'stc_scale' : [tl[i] for i in range(0, len(f)) if f[i] >= 125 and f[i] <= 4000], 'full_scale' : tl } #[0] for STC / [1] for fullrange tl_summarize

    def evaluate_stc(self):  # Evaluation Standard Transmission loss
        stc_range = [[i - 16, i - 13, i - 10, i - 7, i - 4, i - 1, i, i + 1, i + 2, i + 3, i + 4, i + 4, i + 4, i + 4, i + 4, i + 4] for i in range(150)]  # STC Contourf = [12.45,14,15.45,20.9,22.9,24.9,26.9,28.9,31,32.9,34.8,37,38.9,40.9,17.7,20.8]
        r = self.tl_summarize()['stc_scale']
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

    def plot(self):  # Visualize the Transmission loss data and STC-Contour
        tl = self.tl_summarize()['stc_scale']
        val = self.evaluate_stc()['stc']
        stc_contour = [val - 16, val - 13, val - 10, val - 7, val - 4, val - 1, val, val + 1, val + 2, val + 3, val + 4, val + 4, val + 4, val + 4, val + 4, val + 4]  # STC Contour
        freq_stc = [125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000]  # 1/3 Octave freq band
        x_axis = [i for i in range(0, len(freq_stc))]
        plt.figure(figsize=(18, 8))
        plt.plot(tl, 'b', linewidth=2)
        plt.plot(stc_contour, 'g--', linewidth=1.8)
        plt.annotate('Initials : Peem Srinikorn', xy=(0.85, 0.04), fontsize=12, bbox=dict(facecolor='cyan', alpha=0.5),
                     xycoords='axes fraction')
        plt.title('Single Panel Sound Transmission loss', fontsize=18)
        plt.xlabel('1/3 Octave Frequency [Hz]', fontsize=15)
        plt.ylabel('R Transmiss loss [dB]', fontsize=15)
        plt.legend(['Transmission loss', 'STC {}'.format(stc_contour[6])], fontsize=15, loc='best')
        plt.xticks(x_axis, freq_stc, fontsize=12)
        plt.yticks(fontsize=12)
        plt.grid(linestyle='-', linewidth=0.5)
        return plt.show()

    def get_data(self):  # Data of Trnamission loss in 1/3 Octave frequency band
        tl = self.tl_summarize()['full_scale']
        f = self.freq_std
        return dict(zip(f,tl))

    def get_info(self):  # STC , total deficiency and material property
        stc = self.evaluate_stc()['stc']
        defi = self.evaluate_stc()['total_deficiency']
        mass = self.mass
        thick = self.thick * 1000
        modulus = self.modulus * 10 ** -9
        damp = self.damp
        area = self.area
        return {'STC': stc, 'Total Deficiency': defi, 'Mass (kg)': mass, 'Thickness (mm)': thick, 'Young Modulus (GPa)': modulus, 'Damping Ratio': damp, 'Area (m^2)': area}

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
# if __name__ == '__main__':
#     ### Attribute ##(mass, thick, modulus, damp, width, height): 
#     single_pn = SinglePanel(mass = 7, thick = 10, modulus = 4, damp = 0.1, width = 3, height = 4)
#     single_pn.plot()
#     data = single_pn.get_data()
#     print(data)
#     info = single_pn.get_info()
#     print(info)
############################################################
##### Sound Transmission Loss ##############################
##### Single Panel Predicetive Model #######################
############################################################
############################################################
##### Author : Peem Srinikorn ##############################
##### 29 Oct 2018 ##########################################
############################################################
