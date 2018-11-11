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

    def __init__(self,Mass,Thick,Modulus,Damp,width,height): #Essential Attribute
        self.Mass = Mass #Mass as Kg unit
        self.Thick = Thick/1000 # Thickness as mm unit
        self.Modulus = Modulus*10**9 #Young Modulus as GPa unit
        self.Damp = Damp #Damping ratio
        self.Area = width*height #Area of Sample as m^2 unit
        self.f=[50,63,80,100,125,160,200,250,315,400,500,630,800,1000,1250,1600,2000,2500,3150,4000,5000] #1/3 Octave freq band
        self.c = 343 #speed of airborne sound
        self.height = height # for calculate delta Rm

    def Crifreq(self):  # calc Critical Frequency or Resonant frequency
        fc = ((self.c ** 2) / 6.283185) * (np.sqrt(self.Mass / (((self.Modulus) * ((self.Thick) ** 3)) / 11.988)))
        return fc

    def Masslaw(self):  # calc TL by Masslaw with Bending waves or Resotant transmission
        fc = SinglePanel.Crifreq(self)
        f = self.f
        fc = SinglePanel.Crifreq(self)
        T_1 = [(20 * (np.log10(self.Mass * f[i])) - 44) for i in range(0, len(f)) if f[i] <= fc]
        T_2 = [(20 * (np.log10(self.Mass * f[i]))) + (10 * np.log10((2 * self.Damp * f[i]) / (np.pi * fc))) - 48 for i
               in range(0, len(f)) if f[i] >= fc]
        TL = T_1 + T_2
        return TL

    def FqLow(self):  # calc low-frequency correction (TL below 200 Hz)
        fc = SinglePanel.Crifreq(self)
        fLow = [50, 63, 80, 100, 125, 160, 200]
        omegaC = 2 * np.pi * fc
        kw = [(2 * np.pi * fLow[i]) / self.c for i in range(0, len(fLow))]
        omega = [(2 * np.pi * fLow[i]) for i in range(0, len(fLow))]
        Rlow = [-10 * np.log10(np.log(kw[i] * (self.Area ** 0.5))) + 20 * np.log10(1 - (omega[i] / omegaC) ** 2) for i
                in range(0, len(fLow))]
        return Rlow

    def Values(self):  # Summarize formula
        TL = SinglePanel.Masslaw(self)
        Rlow = SinglePanel.FqLow(self)
        fc = SinglePanel.Crifreq(self)
        f = self.f
        for i in range(0, len(f)):
            if f[i] <= 200:
                TL[i] = TL[i] + Rlow[i]
            else:
                TL[i] = TL[i]
        R_TL = [TL[i] for i in range(0, len(f)) if
                f[i] >= 125 and f[i] <= 4000]  # slice data as STC freq range 125 Hz - 4 KHz
        return R_TL, TL #[0] for STC / [1] for fullrange values

    def Eval_STC(self):  # Evaluation Standard Transmission loss
        s = [[i - 16, i - 13, i - 10, i - 7, i - 4, i - 1, i, i + 1, i + 2, i + 3, i + 4, i + 4, i + 4, i + 4, i + 4,
              i + 4] for i in
             range(150)]  # STC Contourf = [12.45,14,15.45,20.9,22.9,24.9,26.9,28.9,31,32.9,34.8,37,38.9,40.9,17.7,20.8]
        f = SinglePanel.Values(self)[0]
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

    def plot(self):  # Visualize the Transmission loss data and STC-Contour
        TL = SinglePanel.Values(self)[0]
        v = SinglePanel.Eval_STC(self)[0]
        s = [v - 16, v - 13, v - 10, v - 7, v - 4, v - 1, v, v + 1, v + 2, v + 3, v + 4, v + 4, v + 4, v + 4,
             v + 4,v+4]  # STC Contour
        f = [125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150,
             4000]  # 1/3 Octave freq band
        xi = [i for i in range(0, len(f))]
        plt.figure(figsize=(18, 8))
        plt.plot(TL, 'b', linewidth=2)
        plt.plot(s, 'g--', linewidth=1.8)
        plt.annotate('Initials : Peem Srinikorn', xy=(0.85, 0.04), fontsize=12, bbox=dict(facecolor='cyan', alpha=0.5),
                     xycoords='axes fraction')
        plt.title('Single Panel Sound Transmission loss', fontsize=18)
        plt.xlabel('1/3 Octave Frequency [Hz]', fontsize=15)
        plt.ylabel('R Transmiss loss [dB]', fontsize=15)
        plt.legend(['Transmission loss', 'STC {}'.format(s[6])], fontsize=15, loc='best')
        plt.xticks(xi, f, fontsize=12)
        plt.yticks(fontsize=12)
        plt.grid(linestyle='-', linewidth=0.5)
        return plt.show()

    def data(self):  # Data of Trnamission loss in 1/3 Octave frequency band
        TL = SinglePanel.Values(self)[1]
        f = self.f
        df = dict(zip(f,TL))
        return df

    def info(self):  # STC , total deficiency and material property
        STC = SinglePanel.Eval_STC(self)[0]
        defi = SinglePanel.Eval_STC(self)[1]
        Mass = self.Mass
        Thick = self.Thick * 1000
        Modulus = self.Modulus * 10 ** -9
        Damp = self.Damp
        Area = self.Area
        d = {'STC': STC, 'Total Deficiency': defi, 'Mass (kg)': Mass, 'Thickness (mm)': Thick,
             'Young Modulus (GPa)': Modulus, 'Damping Ratio': Damp, 'Area (m^2)': Area}
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
if __name__ == '__main__':
    ### Attribute ##(Mass,Thick,Modulus,Damp,Width,Height): 
    Single = SinglePanel(7,10,4,0.1,3,4)
    Single.plot()
    Single.info()
    Single.data()
############################################################
##### Sound Transmission Loss ##############################
##### Single Panel Predicetive Model #######################
############################################################
############################################################
##### Author : Peem Srinikorn ##############################
##### 29 Oct 2018 ##########################################
############################################################
