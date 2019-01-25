from DoublePanel import DoublePanel
from SinglePanel_A import SinglePanel_A
from SinglePanel_B import SinglePanel_B
from SinglePanel import SinglePanel
from Show import Show

###############################################################################
###############################################################################
####### Author : Peem Srinikorn ###############################################
###############################################################################
###############################################################################
# for SinglePanel must use .values for display output as list  #################
# // SinglePanel_A, _B are no plot and evaluate function itself ###############
# for DoublePanel must use .Total_Db or Total_Ab for display output as list ###
# [0] for STC 125 Hz - 4,000 Hz / [1] for fullrange values ####################
# SinglePanel can use by directly. ############################################
# No need to cross function from Show to plot and evalation. ##################
# Show(your_values()) -> Show has attribute as following below ################
# Show.plot -> Ploting TL as full range frequency 50 Hz - 5,000 Hz ############
# Show.plot_STC -> Ploting TL with STC line  ##################################
# Show.data -> read TL values as dictionary format ############################
# Show.data_pd -> read TL values as Table DataFrame ###########################
# Show.info -> read STC and Deficiency as Dictionary ##########################
###############################################################################
### SinglePanel(Mass,Thick,Modulus,Damping,Width,Height) ######################
### DoublePanel -> Attribute ##################################################
## (TL_Panel_A,TL_Panel_B,Distance,DensityAbsorber,FlowResistance,SpacingStud)#
###############################################################################
### Example ###################################################################
###############################################################################
###############################################################################

if __name__ =='__main__':
  
    #Attribute SinglePanel ([Mass(kg)],[Thickness(mm)],[Modulus(GPa)],[Damping Ratio],[Width(m)],[Height(m)])
    Panel_A = SinglePanel_A(12,15,2.5,0.1,3,3)
    Panel_B = SinglePanel_B(12,15,2.5,0.1,3,3)
    #Attribute DoublePanel ([Panel_A],[Panel_B],[Distance of Panel_A , Panel_B (mm)] ,[Flow Resistance], [Spacing Stud (mm)])
    Double = DoublePanel(Panel_A,Panel_B,65,12000,450)
    #Arrtribute Show ([Total_Values])
    # for DoublePanel -> [Total_Double() , Total_Double_Absorb() , Total_Double_Stud() , Total_Double_Absorb_Stud()]
    # for SingelPanel -> [ Values() ]
    Show = Show(Double.Total_Double())
    # Show function 
    Show.plot() #plot all full range frequency 50 Hz - 5,000 Hz 
    Show.plot_STC() #plot as STC range frequency 125 Hz - 4,000 Hz 
    Show.data() #read TL data as Dictionary 
    Show.data_pd() #read TL data as DataFrames
    Show.info() #read STC and Deficiency Values as Dictionary

###############################################################################
###############################################################################
####### Author : Peem Srinikorn ###############################################
###############################################################################
###############################################################################
