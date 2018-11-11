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

class DoublePanel():
    def __init__(self,Panel_A,Panel_B,d,flow,spacing): #distance
        self.d = d/1000 #distance between Panel_A and Panel_B -> unit millimetre
        self.flow = flow #flow resistance of Absorber -> Rayl/m
        self.Panel_A = Panel_A.Values()[1] #TL_A
        self.Panel_B = Panel_B.Values()[1] # TL_B
        self.spac = spacing/1000 # spacing of line connection
        self.Mass_A = Panel_A.Mass
        self.Mass_B = Panel_B.Mass
        self.fc_A = Panel_A.Crifreq()
        self.fc_B = Panel_B.Crifreq()
        self.Height_A = Panel_A.height
        self.Height_B = Panel_B.height
        self.Area_A = Panel_A.Area
        self.Area_B = Panel_B.Area
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
        f0 = DoublePanel.freq(self)[0]
        f = self.f
        TL_con1 = [20*np.log10(f[i]*(self.Mass_A+self.Mass_B))-47 for i in range(0,len(f)) if f[i] < f0]
        return TL_con1

    def Con2(self): # f > f0 and f < fl
        R_A = self.Panel_A
        R_B = self.Panel_B
        f = self.f
        f0 = DoublePanel.freq(self)[0]
        fl = DoublePanel.freq(self)[1]
        TL_Con2 = [ R_A[i] + R_B[i] + 20*np.log10(f[i]*self.d) -29 for i in range(0,len(f)) if f[i] >= f0 and f[i] <= fl]
        return TL_Con2

    def Con3(self): # f > fl
        R_A = self.Panel_A
        R_B = self.Panel_B
        f = self.f
        fl = DoublePanel.freq(self)[1]
        TL_Con3 = [ R_A[i] + R_B[i] + 6 for i in range(0,len(f)) if f[i] > fl ]
        return TL_Con3

    def Total_Double(self): # Total TL of Double Panel
        f = self.f
        R1 = DoublePanel.Con1(self)
        R2 = DoublePanel.Con2(self)
        R3 = DoublePanel.Con3(self)
        R_Total = R1 + R2 + R3
        R_TotalSTC = [R_Total[i] for i in range(0, len(f)) if f[i] >= 125 and f[i] <= 4000]
        return R_TotalSTC,R_Total

    def Absorber(self): # Absorber Cal
        f = self.f
        fl = DoublePanel.freq(self)[1]
        f_ab = [f[i] for i in range(0,len(f)) if f[i] > fl]
        R_A = self.Panel_A
        R_B = self.Panel_B
        k = [(2 * np.pi * f_ab[i]) / self.c for i in range(0, len(f_ab))]
        omega = [(2 * np.pi * f_ab[i]) for i in range(0, len(f_ab))]
        prob = [((omega[i] / self.c) * 0.189 * (self.pair*f_ab[i] / self.flow) ** -0.595) + ( 1j * (omega[i] / self.c) * ((1 + 0.0978 * (self.pair * f_ab[i]) / (self.flow)) ** -0.7)) for i in range(0, len(f_ab))]
        alpha = [prob[i].real for i in range(0, len(prob))]
        beta = [prob[i].imag for i in range(0, len(prob))]
        TL = [R_A[i] + R_B[i] for i in range(0, len(f)) if f[i] > fl]
        TL_Ab = [TL[i] + 8.6 * alpha[i] * self.d + 20*np.log10(beta[i] / k[i]) for i in range(0, len(f_ab))]
        return TL_Ab

    def Total_Double_Absorb(self): # Total TL Double Panel with Absorber
        f = self.f
        R_TL = DoublePanel.Con1(self) + DoublePanel.Con2(self)
        R_Ab = R_TL + DoublePanel.Absorber(self)
        R_AbSTC = [R_Ab[i] for i in range(0, len(f)) if f[i] >= 125 and f[i] <= 4000]
        return R_AbSTC,R_Ab

    def Stud(self): #stud line connection calculation
        deltaRb = 10*np.log10(self.spac*self.fc_A)+ 20*np.log10((self.Mass_A/(self.Mass_A+self.Mass_B)))-18
        fcl = (((self.Mass_A*np.sqrt(self.fc_B))+(self.Mass_B*np.sqrt(self.fc_A)))/(self.Mass_A+self.Mass_B))**2
        deltaRm = 10*np.log10(((self.Area_A)/(self.Height_A))*((np.pi*fcl)/(2*self.c)))

        return deltaRb,deltaRm

    def Total_Double_Stud(self): #Total TL of Double Panel with Stud
        f = self.f
        fl = DoublePanel.freq(self)[1]
        deltaRb = DoublePanel.Stud(self)[0]
        deltaRm = DoublePanel.Stud(self)[1]
        R = DoublePanel.Total_Double(self)[1]
        R_1 = [ R[i] for i in range(0,len(f)) if f[i] <= fl*0.5 ]
        R_2 = [ R[i]-deltaRb for i in range(0,len(f)) if f[i] >= fl*0.5 and f[i] <= fl]
        R_3 = [ R[i]-deltaRm for i in range(0,len(f)) if f[i] >= fl]
        R_Total = R_1+R_2+R_3
        R_TDS_STC = [R_Total[i] for i in range(0, len(f)) if f[i] >= 125 and f[i] <= 4000]
        return R_TDS_STC,R_Total

    def Total_Double_Absorb_Stud(self): #Total TL of Double Panel with Absorber and Stud
        f = self.f
        fl = DoublePanel.freq(self)[1]
        deltaRb = DoublePanel.Stud(self)[0]
        deltaRm = DoublePanel.Stud(self)[1]
        R = DoublePanel.Total_Double_Absorb(self)[1]
        R_1 = [ R[i] for i in range(0,len(f)) if f[i] <= 0.5 * fl ]
        R_2 = [ R[i]-deltaRb for i in range(0,len(f)) if f[i] >= 0.5*fl and f[i] <= fl]
        R_3 = [ R[i]-deltaRm for i in range(0,len(f)) if f[i] >= fl]
        R_Total = R_1+R_2+R_3
        R_TDAS_STC = [R_Total[i] for i in range(0, len(f)) if f[i] >= 125 and f[i] <= 4000]
        return R_TDAS_STC, R_Total

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
