from SinglePanel_A import SinglePanel_A
from SinglePanel_B import SinglePanel_B
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

class Double():
    def __init__(self,Panel_A,Panel_B,d,p,flow): #distance
        self.d = d/1000 #distance between Panel_A and Panel_B -> unit millimetre
        self.p = p #density of Absorber -> kg/m^3
        self.flow = flow #flow resistance of Absorber -> Rayl/m
        self.Panel_A = Panel_A.Cal()[1] #TL_A
        self.Panel_B = Panel_B.Cal()[1] # TL_B
        self.Mass_A = Panel_A.Mass
        self.Mass_B = Panel_B.Mass
        self.f = [50,63,80,100,125,160,200,250,315,400,500,630,800,1000,1250,1600,2000,2500,3150,4000,5000] #1/3 Octave freq band
        self.c = 343 #speed of airborne sound
        self.pair = 1.18 # Airborne Sound Density

    def __repr__(self): #represent variable
        distance = self.d
        density = self.p
        flow_res = self.flow

    def freq(self):
        me = ((self.pair*(self.c**2))/self.d)*((1/self.Mass_A)+(1/self.Mass_B))
        f0 = (1/(2*np.pi))*(np.sqrt(me))
        fl = 55/self.d
        return f0,fl

    def Con1(self): # f < f0
        f0 = Double.freq(self)[0]
        f = self.f
        TL_con1 = [20*np.log10(f[i]*(self.Mass_A+self.Mass_B))-47 for i in range(0,len(f)) if f[i] < f0]
        return TL_con1

    def Con2(self): # f > f0 and f < fl
        R_A = self.Panel_A
        R_B = self.Panel_B
        f = self.f
        f0 = Double.freq(self)[0]
        fl = Double.freq(self)[1]
        TL_Con2 = [ R_A[i] + R_B[i] + 20*np.log10(f[i]*self.d) -29 for i in range(0,len(f)) if f[i] >= f0 and f[i] <= fl]
        return TL_Con2

    def Con3(self): # f > fl
        R_A = self.Panel_A
        R_B = self.Panel_B
        f = self.f
        fl = Double.freq(self)[1]
        TL_Con3 = [ R_A[i] + R_B[i] + 6 for i in range(0,len(f)) if f[i] > fl ]
        return TL_Con3

    def Total_db(self): # Total TL of Double Panel
        R1 = Double.Con1(self)
        R2 = Double.Con2(self)
        R3 = Double.Con3(self)
        R_Total = R1 + R2 + R3
        return R_Total

    def Absorber(self): # Absorber Cal
        f = self.f
        fl = Double.freq(self)[1]
        f_ab = [f[i] for i in range(0,len(f)) if f[i] > fl]
        R_A = self.Panel_A
        R_B = self.Panel_B
        k = [(2 * np.pi * f_ab[i]) / self.c for i in range(0, len(f_ab))]
        omega = [(2 * np.pi * f_ab[i]) for i in range(0, len(f_ab))]
        prob = [((omega[i] / self.c) * 0.189 * (self.p*f_ab[i] / self.flow) ** -0.595) + ( 1j * (omega[i] / self.c) * (1 + 0.0978 * ((self.p * f_ab[i]) / self.flow) ** -0.7)) for i in range(0, len(f_ab))]
        alpha = [prob[i].real for i in range(0, len(prob))]
        beta = [prob[i].imag for i in range(0, len(prob))]
        TL = [R_A[i] + R_B[i] for i in range(0, len(f)) if f[i] > fl]
        TL_Ab = [TL[i] + 8.6 * alpha[i] * self.d + 2 - np.log10(beta[i] / k[i]) for i in range(0, len(f_ab))]
        return TL_Ab

    def Total_Ab(self): # Total TL Double Panel with Absorber
        R_TL = Double.Con1(self) + Double.Con2(self)
        R_Ab = R_TL + Double.Absorber(self)
        return R_Ab

    
