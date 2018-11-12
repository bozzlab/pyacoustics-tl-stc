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

class Show():
    def __init__(self,plot):
        self.STC = plot[0]
        self.TL = plot[1]

    def Eval_STC(self):  # Evaluation Standard Transmission loss
        s = [[i - 16, i - 13, i - 10, i - 7, i - 4, i - 1, i, i + 1, i + 2, i + 3, i + 4, i + 4, i + 4, i + 4, i + 4,
              i + 4] for i in range(150)]  # STC Contourf 
        f = self.STC
        for x in range(0, len(s)):  # STC Contour Condition
            for y in range(0, 16):
                if f[y] < s[x][y]:
                    s[x][y] = abs(f[y] - s[x][y])  # TL below STC contour
                else:
                    s[x][y] = 0
        x = [s[t] if sum(s[t]) <= 32 else False for t in range(0, len(s))]  # total deficiency condition
        y = [x[t] for t in range(0, len(x)) if x[t] != False]  # silce total deficiency > 32
        for i_1 in range(0, len(y)):
            for i_2 in range(0, 16):
                if y[i_1][i_2] > 8: # index more than 8
                    y[i_1][i_2] = False

        num = [z for z in y if not any(isinstance(e, (str, bool)) for e in z)] # clear False
        STC = (len(num) - 1) # Maximum STC
        Def = sum(num[STC]) # Deficiency STC
        return STC, Def

    def plot_STC(self):  # Visualize the Transmission loss data and STC-Contour
        TL = self.STC
        v = Show.Eval_STC(self)[0]
        s = [v - 16, v - 13, v - 10, v - 7, v - 4, v - 1, v, v + 1, v + 2, v + 3, v + 4, v + 4, v + 4, v + 4,
             v + 4]  # STC Contour
        f = [125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150,
             4000]  # 1/3 Octave freq band
        xi = [i for i in range(0, len(f))]
        plt.figure(figsize=(18, 8))
        plt.plot(TL, 'b', linewidth=2)
        plt.plot(s, 'g--', linewidth=1.8)
        plt.annotate('Initials : Peem Srinikorn', xy=(0.85, 0.04), fontsize=12, bbox=dict(facecolor='cyan', alpha=0.5),
                     xycoords='axes fraction')
        plt.title('Sound Transmission loss', fontsize=18)
        plt.xlabel('1/3 Octave Frequency [Hz]', fontsize=15)
        plt.ylabel('R Transmiss loss [dB]', fontsize=15)
        plt.legend(['Transmission loss', 'STC {}'.format(s[6])], fontsize=15, loc='best')
        plt.xticks(xi, f, fontsize=12)
        plt.yticks(fontsize=12)
        plt.grid(linestyle='-', linewidth=0.5)
        return plt.show()

    def plot(self):  # Visualize the Transmission loss data as Full range frequency
        TL = self.TL
        f = [50,63,80,100,125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150,
             4000,5000]  # 1/3 Octave freq band
        xi = [i for i in range(0, len(f))]
        plt.figure(figsize=(18, 8))
        plt.plot(TL, 'b', linewidth=2)
        plt.annotate('Initials : Peem Srinikorn', xy=(0.85, 0.04), fontsize=12, bbox=dict(facecolor='cyan', alpha=0.5),
                     xycoords='axes fraction')
        plt.title('Sound Transmission loss ', fontsize=18)
        plt.xlabel('1/3 Octave Frequency [Hz]', fontsize=15)
        plt.ylabel('R Transmiss loss [dB]', fontsize=15)
        plt.legend(['Transmission loss'], fontsize=15, loc='best')
        plt.xticks(xi, f, fontsize=12)
        plt.yticks(fontsize=12)
        plt.grid(linestyle='-', linewidth=0.5)
        return plt.show()

    def data_pd(self):  # Data of Trnamission loss in 1/3 Octave frequency band
        TL = self.TL
        f = [50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150,
             4000, 5000]
        df = pd.DataFrame({'Frequency (Hz)': f, 'Transmission loss (dB)': TL})
        return df

    def data(self):
        TL = self.TL
        f = [50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150,
             4000, 5000]
        R = dict(zip(f ,TL))
        return R

    def info(self):  # STC , total deficiency
        STC = Show.Eval_STC(self)[0]
        defi = Show.Eval_STC(self)[1]
        d = {'STC': STC, 'Total Deficiency': defi}
        return d

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
