import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 

class SinglePanel_B(): 
    
    def __init__(self,Mass,Thick,Modulus,Damp,Area): #Essential Attribute
        self.Mass = Mass #Mass as Kg unit  
        self.Thick = Thick/1000 # Thickness as mm unit
        self.Modulus = Modulus*10**9 #Young Modulus as GPa unit
        self.Damp = Damp #Damping ratio
        self.Area = Area #Area of Sample as m^2 unit 
        self.f=[50,63,80,100,125,160,200,250,315,400,500,630,800,1000,1250,1600,2000,2500,3150,4000,5000] #1/3 Octave freq band
        self.c = 343 #speed of airborne sound 

    def __repr__(self):
        return self.Mass

    def Crifreq(self): # calc Critical Frequency or Resonant frequency
        fc = ((self.c**2)/6.283185)*(np.sqrt(self.Mass/(((self.Modulus)*((self.Thick)**3))/11.988)))
        return fc 
    
    def Masslaw(self): # calc TL by Masslaw with Bending waves or Resotant transmission
        fc=SinglePanel_B.Crifreq(self)
        f = self.f
        fc = SinglePanel_B.Crifreq(self)
        T_1 = [(20*(np.log10(self.Mass*f[i]))-44) for i in range(0,len(f)) if f[i] <= fc]
        T_2 = [(20*(np.log10(self.Mass*f[i])))+(10*np.log10((2*self.Damp*f[i])/(np.pi*fc)))-48 for i in range(0,len(f)) if f[i] >= fc]
        TL = T_1 + T_2
        return TL
    
    def FqLow(self): # calc low-frequency correction (TL below 200 Hz)
        fc = SinglePanel_B.Crifreq(self)
        fLow = [50,63,80,100,125,160,200]
        omegaC = 2*np.pi*fc
        kw = [(2*np.pi*fLow[i])/self.c for i in range(0,len(fLow)) ]
        omega = [(2*np.pi*fLow[i]) for i in range(0,len(fLow))] 
        Rlow = [-10*np.log10(np.log(kw[i]*(self.Area**0.5)))+20*np.log10(1-(omega[i]/omegaC)**2) for i in range(0,len(fLow))]
        return Rlow
    
    def Cal(self): # Summarize formula
        TL = SinglePanel_B.Masslaw(self)
        Rlow = SinglePanel_B.FqLow(self)
        fc = SinglePanel_B.Crifreq(self)
        f = self.f
        for i in range(0,len(f)):
            if f[i] <= 200: 
                TL[i] = TL[i] + Rlow[i]
            else: 
                TL[i] = TL[i]
                
        R_TL = [TL[i] for i in range(0,len(f)) if f[i] >= 125 and f[i] <= 4000] #slice data as STC freq range 125 Hz - 4 KHz
        return R_TL,TL
    
