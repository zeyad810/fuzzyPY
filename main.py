import math
import skfuzzy as fuzz
import numpy as np
from skfuzzy import  control as ctrl
# Inputs --------------------------------------------------------------------------
Temperature  =ctrl.Antecedent(np.arange(10,36 ,1),"Temperature")
Humidity  = ctrl.Antecedent(np.arange(20,81,1),"Humidity")
NumOfPeople =ctrl.Antecedent(np.arange(0,21,1),"NumOfPeople")
TimeOfDay  =ctrl.Antecedent(np.arange(0,24,1),"TimeOfDay")
LightLevel = ctrl.Antecedent(np.arange(0,1001,50),"LightLevel")
# outPuts--------------------------------------------------------------------------
acLevel= ctrl.Consequent(np.arange(0,4,1),"acLevel")
HumidifierLevel = ctrl.Consequent(np.arange(0,4,1),"HumidifierLevel")
LightingLevel = ctrl.Consequent(np.arange(0,4,1),"LightingLevel")
# Input auto membership function--------------------------------------------------
Temperature.automf(3, names=["Cold", "Comfortable", "Hot"])
Humidity.automf(3, names=["Dry", "Normal", "Humid"])
NumOfPeople.automf(3, names=["Few", "Moderate", "Many"])
TimeOfDay.automf(3, names=["Morning", "Afternoon", "Evening"])
LightLevel.automf(3, names=["Dark", "Normal", "Bright"])
# output auto memberr
acLevel.automf(4,names=["Off", "Low", "Medium", "High"])
HumidifierLevel.automf(4,names=["Off", "Low", "Medium", "High"])
LightingLevel.automf(3 , names=["Dim", "Normal","Bright"])
# Create the Rules ------------------------------------------------------------------
rules = [
    ctrl.Rule(Temperature["Hot"] & NumOfPeople["Many"], acLevel["High"]),
    ctrl.Rule(Humidity["Dry"] & Temperature["Cold"], acLevel["Medium"]),
    ctrl.Rule(LightLevel["Dark"] & TimeOfDay["Morning"], LightingLevel["Bright"]),
    ctrl.Rule(Temperature["Comfortable"] & Humidity["Normal"] & LightLevel["Normal"],
              consequent=[acLevel["Off"], HumidifierLevel["Off"], LightingLevel["Normal"]]),
    ctrl.Rule(LightLevel["Bright"] & TimeOfDay["Afternoon"], LightingLevel["Normal"]),
    ctrl.Rule(NumOfPeople["Few"] & Temperature["Cold"], acLevel["Off"]),
    ctrl.Rule(Humidity["Humid"] & Temperature["Hot"],
              consequent=[acLevel["High"], HumidifierLevel["Off"]]),
    ctrl.Rule(Temperature["Cold"] & LightLevel["Bright"],
              consequent=[acLevel["Off"], LightingLevel["Dim"]]),
    ctrl.Rule(NumOfPeople["Many"] & LightLevel["Dark"], LightingLevel["Bright"]),
    ctrl.Rule(TimeOfDay["Evening"] & LightLevel["Normal"], LightingLevel["Dim"])
]
Rules_Aggregation = ctrl.ControlSystem(rules)     # بجمع كل القواعد الى همشى عليها
Rules_Simmulation =ctrl.ControlSystemSimulation(Rules_Aggregation) # بمثلها بستخدمها

#Test Case 1: Cold and Dry Early Morning
Rules_Simmulation.input['Temperature'] = 24    # Comfortable
Rules_Simmulation.input['Humidity'] = 50       # Normal
Rules_Simmulation.input['NumOfPeople'] = 10    # Moderate
Rules_Simmulation.input['TimeOfDay'] = 10      # Morning
Rules_Simmulation.input['LightLevel'] = 500
# Compute the result
Rules_Simmulation.compute()
ac_labels = ["Off", "Low", "Medium", "High"]
humidifier_labels = ["Off", "Low", "Medium", "High"]
lighting_labels = ["Dim", "Normal", "Bright"]

ac_level_rounded=round(Rules_Simmulation.output['acLevel'])
Lighting_Level_rounded=round(Rules_Simmulation.output['LightingLevel'])
Humidifier_Level_rounded=round(Rules_Simmulation.output['HumidifierLevel'])


print("AC Level:", ac_level_rounded,"-",ac_labels[ac_level_rounded] )
print("Humidifier Level:",Humidifier_Level_rounded ,"-",humidifier_labels[Humidifier_Level_rounded])
print("Lighting Level:",Lighting_Level_rounded,"-",lighting_labels[Lighting_Level_rounded])

