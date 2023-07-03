# Additional Libraries
from random import uniform, choice
import numpy as np
import pandas as pd
from colorama import Fore, Style
import datetime
import sys

# # # DIFFERENCES FROM REAL FORMULA ONE RACING
# There is no red flag feature in this simulation. However, safety car and artificial safety car features are available.
# We assume that each team could find the best strategy and car setup for the feature race in free practice sessions.

# Application Modes
execution = 'simulation' # data or simulation for output/run mode.

# Season (Current) Selection
current = '1998'

# GP Selection
GP = 'Melbourne'

# Spec. Selection
spec = 'Formula 1'

if spec == 'Formula 1':
    verbosity = True # True or False for further telemetry & data.
else:
    verbosity = False

# Error Handling for Vehicle Specs and Spec. Configuration
spec_list = ['Formula 1','Formula 2']
if spec in spec_list:
    pass
else:
    print(f'There is no racing class named {spec}. Try one of these:')
    for i in spec_list:
        print(i)
    print('Program terminated.')
    sys.exit(0)

if spec == 'Formula 1':
    spex = 1.00000
elif spec == 'Super Formula': # Not Active
    spex = 1.11250
elif spec == 'Formula 2':
    spex = 1.12500
elif spec == 'Formula 3': # Not Active
    spex = 1.20000
elif spec == 'Euroformula': # Not Active
    spex = 1.31000
elif spec == 'Hypercar': # Not Active
    spex = 1.37000

# Error Handling for Regulations
reglist = ['1998','2005','2006','2009','2011','2014','2016','2017','2018','2021','2022']
if current in reglist:
    pass
else:
    print(f'There is no regulation changes at {current} season. Try one of these:')
    for i in reglist:
        print(i)
    print('Program terminated.')
    sys.exit(0)

# Error Handling for Verbosity Variable
if verbosity in [True,False]:
    pass
else:
    print(f'Verbosity parameter should set as boolean True or boolean False, not as {type(verbosity)} {verbosity}. Please change it and run again.')
    print('Program terminated.')
    sys.exit(0)

# Error Handling for Execution Variable
if execution in ['data','simulation']:
    pass
else:
    print(f'Execution parameter should set as data or simulation, not as {execution}. Please change it and run again.')
    print('Program terminated.')
    sys.exit(0)

# Tire Supplier Mechanics/Dynamics 
class Tyre():
    def __init__(self,title,pace,durability,type):
        self.title = title
        self.pace = pace
        self.durability = durability
        self.type = type

bridgestone = Tyre('Bridgestone',1.6,2.6,'Grooved')
pirelli = Tyre('Pirelli',0.0,0.0,'Slick')

# Fuel & Fuel Supplier Mechanics/Dynamics 
class Fuel():
    def __init__(self,title,vulnerability,efficiency):
        self.title = title
        self.vulnerability = vulnerability
        self.efficiency = efficiency

shell = Fuel('Shell',-2.5,0.0400)
petronas = Fuel('Petronas',0.0,0.0425)
aramco = Fuel('Aramco',+2.5,0.0450)

# FIA Regulation Selector: 
# Index 0 contains vehicle concept coefficient.
# Index 1-2 for if DRS and ERS rule is active.
# Index 3-4-5 for formula 1 partners.
# Index 6 contains minimum amount of vehicle weight within the regulations.
# Index 7-8-9 for regulation game changer coefficients.
# Index 10 for if fastest lap points eligible.
# Index 11 contains fuel tank capacity.
# Index 12 contains chassis efficiency.
# Index 13-14-15 for regulation game changer coefficients [volume 2].
# Index 16 for overtaking difficulty.

def FIA(C): 
    if C == '1998':
        return [1.18250*(spex),False,False,'DHL',bridgestone,shell,585,4,4,2,False,115,0.0725,11.5,7.5,1,0.251]
    elif C == '2005':
        return [1.09750*(spex),False,False,'DHL',bridgestone,shell,585,3,5,2,False,115,0.0700,11.5,7.5,1,0.251]
    elif C == '2006':
        return [1.11750*(spex),False,False,'DHL',bridgestone,shell,585,3,5,2,False,115,0.0700,10,7,3,0.276]
    elif C == '2009':
        return [1.16500*(spex),False,False,'DHL',pirelli,shell,605,2,5,3,False,115,0.0675,10,10,0,0.251]
    elif C == '2011':
        return [1.15250*(spex),True,True,'DHL',pirelli,shell,640,2,5,3,False,110,0.0675,10,10,0,0.376]
    elif C == '2014':
        return [1.15750*(spex),True,True,'DHL',pirelli,petronas,691,2,3,5,True,109,0.0650,11,6,3,0.301]
    elif C == '2016':
        return [1.07000*(spex),True,True,'DHL',pirelli,petronas,702,2,3,5,True,108,0.0650,11,6,3,0.376]
    elif C == '2017':
        return [1.01750*(spex),True,True,'DHL',pirelli,petronas,728,2,5,3,True,112,0.0650,10,8,2,0.251]
    elif C == '2018':
        return [0.99250*(spex),True,True,'DHL',pirelli,petronas,734,2,5,3,True,116,0.0650,10,8,2,0.351]
    elif C == '2021':
        return [0.99000*(spex),True,True,'DHL',pirelli,aramco,752,2,5,3,True,118,0.0625,10,8,2,0.351]
    elif C == '2022':
        return [1.00000*(spex),True,True,'DHL',pirelli,aramco,798,5,2,3,True,112,0.0625,7,10,3,0.401]

# Visual Plugins
borderline = '* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *'

# Negative Events
FAILURES = ['gearbox','clutch','driveshaft','halfshaft','throttle','brakes','handling','wheel','steering','suspension','puncture',
            'electronics','hydraulics','water leak','fuel pressure','oil pressure','exhaust','differential','vibration',
            'transmission','alternator','turbocharger','cooling','gearbox driveline','engine',

            'engine','engine','engine','engine','engine','engine','engine','engine','engine','engine']

MECHANICALS = ['gearing alingment','gearbox driveline',
               'engine modes','engine braking','engine cooling','brake cooling','exhaust system',
               'optimal tire pressure']

ERRORS = ['spun-off','went through barriers','damaged his suspension','crashed into the walls']

MISTAKES = ['locked his brakes','overflowed off the track','missed the braking point','oversteer at the exit of the corner','understeer at the entry of the corner']

if FIA(current)[2] == True:
    FAILURES.extend(['MGU-K','MGU-H','ERS','control electronics','energy store'])
    MECHANICALS.extend(['MGU-K','MGU-H','ERS','control electronics','energy store'])
else:
    pass

# Tire Mechanics/Dynamics
class Tire():
    def __init__(self,title,supplier,degredation_coefficient,laptime_coefficient):
        self.title = title
        self.supplier = supplier
        self.degredation_coefficient = degredation_coefficient
        self.laptime_coefficient = laptime_coefficient
    def tire_left(self,driver,circuit,tire_usage):
        current_tire_life = circuit.tire_life * (self.degredation_coefficient+driver.team.manufacturer_tyre_coeff)
        tire_left = current_tire_life - (tire_usage + driver.tire_harm_by_driver(tire_usage))
        if tire_usage < 4:
            return round(((tire_left/current_tire_life)*100),3)
        else:
            return round(((tire_left/current_tire_life)*100) + (((10*driver.team.manufacturer_tyre_coeff)**2)-3),3)
    def fuel_left(self,circuit,lap):
        consumption_per_lap = (FIA(current)[11])/(circuit.circuit_laps+0.75)
        return FIA(current)[11] - (lap*consumption_per_lap)
    def laptime(self,driver,circuit,lap,tire_usage,mode):
        # # # 1.0: FUEL & TIRE
        fuel_left = self.fuel_left(circuit,lap)
        tire_left = self.tire_left(driver,circuit,tire_usage) + self.supplier.durability

        if self.title == 'Soft':
            limit = circuit.tire_series[0] - round(((0.5 - driver.team.manufacturer_tyre_coeff)*5.25))
            static = round((((driver.team.manufacturer_tyre_coeff)*1000)/148),3)
            warm = round(static)
        elif self.title == 'Medium':
            limit = circuit.tire_series[1] - round(((0.5 - driver.team.manufacturer_tyre_coeff)*5.25))
            static = round(((((driver.team.manufacturer_tyre_coeff)*1000)/148)*2.5),3)
            warm = round(static)
        elif self.title == 'Hard':
            limit = circuit.tire_series[2] - round(((0.5 - driver.team.manufacturer_tyre_coeff)*5.25))
            static = round(((((driver.team.manufacturer_tyre_coeff)*1000)/148)*3.5),3)
            warm = round(static)
        else:
            limit = ((circuit.tire_series[2])*2) - round(((0.5 - driver.team.manufacturer_tyre_coeff)*5.25))
            static = round(((((driver.team.manufacturer_tyre_coeff)*1000)/148)*2.5),3)
            warm = round(static)
        
        heated = (0.5 - driver.team.manufacturer_tyre_coeff)
        
        if driver.team.manufacturer_tyre_coeff < 0.180:
            swallow = (-1.0)*(0)
        else:
            swallow = (-1.0)*((driver.team.manufacturer_tyre_coeff)/2.5)
        
        if mode[0] != 'saturday':
            if warm >= tire_usage:
                tire_temp = (round((static/2),3)) - (tire_usage*heated)
            elif limit >= tire_usage >= warm + 1:
                if driver.team.manufacturer_tyre_coeff < 0.170:
                    tire_temp = uniform(0.075,0.125)
                else:
                    tire_temp = 0.0
            else:
                tire_temp = (heated/4)*(-1.0)
        else:
            if driver.team.manufacturer_tyre_coeff <= 0.144:
                tire_temp = uniform((driver.team.manufacturer_tyre_coeff/2),(driver.team.manufacturer_tyre_coeff/1))*(-1.0)
            elif 0.145 <= driver.team.manufacturer_tyre_coeff <= 0.164:
                tire_temp = 0.0
            elif 0.165 <= driver.team.manufacturer_tyre_coeff:
                tire_temp = uniform((driver.team.manufacturer_tyre_coeff/2),(driver.team.manufacturer_tyre_coeff/1))
        
        TIRE_EFFECT = ((pow(1.015750,(100-tire_left)))-1) + (tire_temp + swallow)
        FUEL_EFFECT = (fuel_left*driver.team.powertrain.fuel.efficiency)
        CL0 = (circuit.laptime * self.laptime_coefficient) + (TIRE_EFFECT) + (FUEL_EFFECT) + (self.supplier.pace)

        # # # VEHICLE
        # # # 2.1: Weight Adjusment
        banker = (FIA(current)[6] + driver.team.weight)
        if self.title == 'Wet':
            TOTAL_WEIGHT = ((banker)*(FIA(current)[12])) + (((1.0217*circuit.laptime/85.00))*3)
        elif self.title == 'Intermediate':
            TOTAL_WEIGHT = ((banker)*(FIA(current)[12])) + (((1.0170*circuit.laptime/85.00))*3)
        else:
            TOTAL_WEIGHT = ((banker)*(FIA(current)[12]))

        # # # 2.2: Natural Traction Effect
        TRACTION_EFFECT_R,TRACTION_EFFECT_Q = 0,0

        if (W1 and W2 != 'Dry') and (W3 == 'Dry'):
            TRACTION_EFFECT_R = 0.825
        elif (W2 != 'Dry') and (W3 == 'Dry'):
            TRACTION_EFFECT_R = 0.625
        
        if (W1 != 'Dry') and (W2 == 'Dry'):
            TRACTION_EFFECT_Q = 0.625
        else:
            TRACTION_EFFECT_Q = 0

        # # # 2.3: ERS
        if FIA(current)[2] == True:
            ERS = (driver.team.powertrain.power/75)*(-1.0)
        else:
            ERS = 0

        # # # 2.4: Performance of the Car
        if mode[0] == 'saturday':
            performance = ((driver.team.performance(circuit.circuit_type))*1.00)
            if self.title == 'Wet':
                CL1 = (((((performance/100)**2)*9.50) - 4)*(-1.0)) + TOTAL_WEIGHT + TRACTION_EFFECT_Q + ERS
            elif self.title == 'Intermediate':
                CL1 = (((((performance/100)**2)*10.00) - 4)*(-1.0)) + TOTAL_WEIGHT + TRACTION_EFFECT_Q + ERS
            else:
                CL1 = (((((performance/100)**2)*10.25) - 4)*(-1.0)) + TOTAL_WEIGHT + TRACTION_EFFECT_Q + ERS
        elif mode[0] == 'sunday':
            performance = ((driver.team.performance(circuit.circuit_type))*1.00)
            if self.title == 'Wet':
                CL1 = (((((performance/100)**2)*9.50) - 4)*(-1.0)) + TOTAL_WEIGHT + TRACTION_EFFECT_R + (ERS/3)
            elif self.title == 'Intermediate':
                CL1 = (((((performance/100)**2)*10.00) - 4)*(-1.0)) + TOTAL_WEIGHT + TRACTION_EFFECT_R + (ERS/3)
            else:
                CL1 = (((((performance/100)**2)*10.25) - 4)*(-1.0)) + TOTAL_WEIGHT + TRACTION_EFFECT_R + (ERS/3)
        elif mode[0] == 'friday':
            performance = ((driver.team.performance(circuit.circuit_type))*1.00)
            if self.title == 'Wet':
                CL1 = (((((performance/100)**2)*9.50) - 4)*(-1.0)) + TOTAL_WEIGHT + (ERS/3)
            elif self.title == 'Intermediate':
                CL1 = (((((performance/100)**2)*10.00) - 4)*(-1.0)) + TOTAL_WEIGHT + (ERS/3)
            else:
                CL1 = (((((performance/100)**2)*10.25) - 4)*(-1.0)) + TOTAL_WEIGHT + (ERS/3)
        
        # # # 3.0: DRIVER
        # # # 3.1: Car/Driver Chemistry
        CAR_DRIVER_CHEMISTRY_LIST = []
        if mode[0] == 'saturday':
            EFFECT = (0.449) - (driver.adaptability/369)
        else:
            EFFECT = (0.309) - (driver.adaptability/431)
        
        if driver.style[0] == None:
            CAR_DRIVER_CHEMISTRY_LIST.append(0.000)
        else:
            if driver.style[0] == driver.team.characteristic[1]:
                CAR_DRIVER_CHEMISTRY_LIST.append(EFFECT*(-1.0))
            else:
                CAR_DRIVER_CHEMISTRY_LIST.append(EFFECT)

        if driver.style[1] == None:
            CAR_DRIVER_CHEMISTRY_LIST.append(0.000)
        else:
            if driver.style[1] == driver.team.characteristic[2]:
                CAR_DRIVER_CHEMISTRY_LIST.append(EFFECT*(-1.0))
            else:
                CAR_DRIVER_CHEMISTRY_LIST.append(EFFECT)

        CAR_DRIVER_CHEMISTRY = sum(CAR_DRIVER_CHEMISTRY_LIST)

        # # # 3.2: Circuit/Driver Chemistry
        if GP in driver.favorite:
            if mode[0] == 'sunday':
                BEST = uniform((round(((driver.pace-48)/425),3)),(round((driver.pace/425),3)))*(-1.0)
            else:
                BEST = uniform((round(((driver.pace-48)/400),3)),(round((driver.pace/400),3)))*(-1.0)
                
        else:
            BEST = 0

        # # # 3.3: Perfect Lap
        if mode[0] == 'sunday' or 'friday':
            if uniform(0,775) <= (((driver.pace*2)/6.67) + (driver.consistency/14.6)):
                hotlap = (-1.0)*uniform(((driver.pace-28)/299),(driver.pace/299))
            else:
                hotlap = 0
        else:
            if uniform(0,225) <= (((driver.pace*2)/6.67) + (driver.consistency/14.6)):
                hotlap = (-1.0)*uniform(((driver.pace-28)/399),(driver.pace/399))
            else:
                hotlap = 0

        # # # 3.4: Driver Error During the Lap
        if self.title == 'Intermediate':
            error_rate = 11.5 - (((driver.consistency * driver.fitness))**(1/4))
        elif self.title == 'Wet':
            error_rate = 12.5 - (((driver.consistency * driver.fitness))**(1/4))
        else:
            error_rate = 10.5 - (((driver.consistency * driver.fitness))**(1/4))
        
        if (hotlap == 0) and (mode[0] == 'sunday') and (SAFETY_CAR[lap][-1] != 1):
            if uniform(0.01,100.01) <= error_rate:
                ERROR = choice(list(np.arange(2.249, 5.449, 0.001, dtype=float)))
                if len(DNF[driver.name]) > 1:
                    pass
                else:
                    print(f'{Fore.LIGHTYELLOW_EX}ERR | Lap {lap} | {driver.name} made mistake and {choice(MISTAKES)}. He has lost {round(ERROR,3)} seconds!{Style.RESET_ALL}')
            else:
                ERROR = 0
        else:
            ERROR = 0

        # # # 3.5: Performance of the Driver
        CRU, CRD = ((driver.consistency-40)/7.5), ((100-driver.consistency)/5)
        SATURDAY, SUNDAY, WET = [], [], []
        for i in np.arange(driver.qualifying_pace()-CRU,driver.qualifying_pace()+CRD,0.01):
            SATURDAY.append(i)
        for j in np.arange(driver.race_pace()-CRU,driver.race_pace()+CRD,0.01):
            SUNDAY.append(j)
        for j in np.arange(driver.wet-CRU,driver.wet+CRD,0.01):
            WET.append(j)

        if FIA(current)[1] == True:
            # Closed, Open
            drs = [0,(-1.0)*((0.250) + driver.team.drs_delta/200)]
        else:
            drs = [0,0]
        
        if mode[0] == 'saturday':                
            engine_mode = (0.600 + ((driver.team.powertrain.power)/100))*(-1.0) # Mode 3
            
            if self.title == 'Wet':
                CL2 = ((((choice(WET)/100)**2)*4.00) + hotlap)*(-1.0) + (engine_mode + drs[0]) + (ERROR) + (BEST) + (CAR_DRIVER_CHEMISTRY) - (driver.form)
            elif self.title == 'Intermediate':
                CL2 = ((((choice(WET)/100)**2)*3.50) + hotlap)*(-1.0) + (engine_mode + drs[0]) + (ERROR) + (BEST) + (CAR_DRIVER_CHEMISTRY) - (driver.form)
            else:
                CL2 = ((((choice(SATURDAY)/100)**2)*3.25) + hotlap)*(-1.0) + (engine_mode + drs[1]) + (ERROR) + (BEST) + (CAR_DRIVER_CHEMISTRY) - (driver.form)
        
        elif mode[0] == 'sunday' or 'friday':         
            engine_mode = (((driver.team.powertrain.power)/175))*(-1.0) # Mode 2
            
            if self.title == 'Wet':
                CL2 = ((((choice(WET)/100)**1.50)*4.00) + hotlap)*(-1.0) + (engine_mode + drs[0]) + (ERROR) + (BEST) + (CAR_DRIVER_CHEMISTRY) - (driver.form)
            elif self.title == 'Intermediate':
                CL2 = ((((choice(WET)/100)**1.50)*3.50) + hotlap)*(-1.0) + (engine_mode + drs[0]) + (ERROR) + (BEST) + (CAR_DRIVER_CHEMISTRY) - (driver.form)
            else:
                CL2 = ((((choice(SUNDAY)/100)**1.75)*3.25) + hotlap)*(-1.0) + (engine_mode + drs[0]) + (ERROR) + (BEST) + (CAR_DRIVER_CHEMISTRY) - (driver.form)

        # Extreme Track Configuration
        if GP == 'Le Mans':
            CL1 = (CL1*3.0) - 88.75
            CL2 = (CL2*3.0) + 11.25
        else:
            pass

        # # # 4.0: FIVE LIGHTS REACTION
        REACTION = (uniform((((driver.start-15)**2))/10000,(((driver.start+5)**2))/10000) - 0.3)
        STARTING_GRID = ((mode[1]/2.5) - 0.40) - (REACTION*1.25)
        GRID_EFFECT = ((circuit.laptime/7.5) + STARTING_GRID)

        # Driver Performance Rating
        if mode[0] == 'sunday':
            if SAFETY_CAR[lap][-1] == 1:
                DFORM[driver.name].append(0)
            else:
                DFORM[driver.name].append(CL2)

        if mode[0] == 'sunday': 
            if lap == 1:
                return (CL0*1.40) + (CL1/3.30) + (GRID_EFFECT)
            else:
                return (CL0) + (CL1) + (CL2)
        else:
            return (CL0) + (CL1) + (CL2)

# Changeability of Pit Box Strategies
strategy_era = ['1998','2005','2006','2009']
entertainment_era = ['2011','2014','2016','2017','2018','2021','2022']

if current in entertainment_era:
    s = Tire('Soft',FIA(current)[4],1.0,1.0000)
    m = Tire('Medium',FIA(current)[4],1.7,1.0117)
    h = Tire('Hard',FIA(current)[4],2.4,1.0217)
    inter = Tire('Intermediate',FIA(current)[4],2.6,1.2517)
    w = Tire('Wet',FIA(current)[4],2.6,1.3717)
elif current in strategy_era:
    s = Tire('Soft',FIA(current)[4],1.0,1.0000)
    h = Tire('Hard',FIA(current)[4],2.4,1.0217)
    inter, w = Tire('Wet',FIA(current)[4],2.6,1.3717), Tire('Wet',FIA(current)[4],2.6,1.3717)

# Circuits
class Circuit():
    def __init__(self,location,country,circuit_type,circuit_laps,laptime,strategy,drs_points,weather,overtake_difficulty,tire_series,tire_life):
        self.location = location
        self.country = country
        self.circuit_type = circuit_type
        self.circuit_laps = circuit_laps
        self.laptime = laptime
        self.strategy = strategy
        self.drs_points = drs_points
        self.weather = weather
        self.overtake_difficulty = overtake_difficulty
        self.tire_series = tire_series
        self.tire_life = tire_life

# # # STRATEGIES
def STRATEGY(GP):
    if GP == 'Le Mans':
        if current in entertainment_era:
            return [[s,m,m    ,s,s,s,h],[s,s,h  ,s,m,m],[s,m,h  ,s,m,h]]
        elif current in strategy_era:
            return [[s,h,s  ,s,s,s,h],[s,s,h  ,s,s,s,h],[s,h,h  ,s,s,s,s]]
    elif GP == 'Monza':
        if current in entertainment_era:
            return [[s,h    ,s,s,s,m,h,h],[s,m    ,s,s,s,m,h],[m,s    ,s,s,m,m,h]]
        elif current in strategy_era:
            return [[s,s,h  ,s,s,s,h],[s,h  ,s,s,s,s,h],[h,s  ,s,s,s,s,h]]
    elif GP == 'Sochi':
        if current in entertainment_era:
            return [[s,h    ,s,s,s,m,h,h],[s,m    ,s,s,s,m,h],[m,s    ,s,s,m,m,h]]
        elif current in strategy_era:
            return [[s,s,h  ,s,s,s,h],[s,h  ,s,s,s,s,h],[h,s  ,s,s,s,s,h]]
    elif GP == 'Baku':
        if current in entertainment_era:
            return [[s,m,m    ,s,s,m,m,h],[m,h    ,s,s,s,m,h,h],[s,s,h    ,s,s,s,m,h]]
        elif current in strategy_era:
            return [[s,s,h  ,s,s,s,h],[s,h  ,s,s,s,s,h],[h,s  ,s,s,s,s,h]]
    elif GP == 'Las Vegas':
        if current in entertainment_era:
            return [[s,h    ,s,s,s,m,h,h],[s,m    ,s,s,s,m,h],[m,s    ,s,s,m,m,h]]
        elif current in strategy_era:
            return [[s,h  ,s,s,s,s,h],[h,s  ,s,s,s,s,h],[s,s,h  ,s,s,s,h]]
    elif GP == 'Spa-Francorchamps':
        if current in entertainment_era:
            return [[s,h    ,s,s,s,m,h,h],[s,m    ,s,s,s,m,h],[m,s    ,s,s,m,m,h]]
        elif current in strategy_era:
            return [[s,h  ,s,s,s,s,h],[h,s  ,s,s,s,s,h],[s,s,h  ,s,s,s,h]]
    elif GP == 'Sakhir':
        if current in entertainment_era:
            return [[s,s,h  ,s,m,m],[s,m,s    ,s,s,m,h],[m,h  ,s,s,m,h]]
        elif current in strategy_era:
            return [[s,h,s  ,s,s,s,h],[s,s,h  ,s,s,s,h],[s,h,h  ,s,s,s,s]]
    elif GP == 'Zandvoort':
        if current in entertainment_era:
            return [[s,m,m,s,  s,s],[s,m,h,s,  s,s],[m,h,h,  s,s]]
        elif current in strategy_era:
            return [[s,s,h,h  ,s,s,s],[s,s,s,h  ,s,s,h],[s,h,h,s  ,s,s,s]]
    elif GP == 'Budapest':
        if current in entertainment_era:
            return [[m,h,  s,s,h,m],[s,s,m,  s,s,h,h],[s,m,s,  s,s,m,h]]
        elif current in strategy_era:
            return [[s,h,s  ,s,s,s,h],[s,s,h  ,s,s,s,h],[s,h,h  ,s,s,s,s]]
    elif GP == 'Barcelona':
        if current in entertainment_era:
            return [[m,h,  s,s,h,m],[s,s,m,  s,s,h,h],[s,m,s,  s,s,m,h]]
        elif current in strategy_era:
            return [[s,s,h  ,s,s,s,h],[s,h  ,s,s,s,s,h],[h,s  ,s,s,s,s,h]]
    elif GP == 'Monte-Carlo':
        if current in entertainment_era:
            return [[s,s,h  ,s,m,m],[s,s,m    ,s,s,m,h],[s,m,h  ,s,m,h]]
        elif current in strategy_era:
            return [[s,h,s  ,s,s,s,h],[s,s,h  ,s,s,s,h],[s,s,s,h  ,s,s,h]]
    elif GP == 'Singapore':
        if current in entertainment_era:
            return [[s,s,h  ,s,m,m],[s,s,m    ,s,s,m,h],[s,m,h  ,s,m,h]]
        elif current in strategy_era:
            return [[s,h,s  ,s,s,s,h],[s,s,h  ,s,s,s,h],[s,s,s,h  ,s,s,h]]
    elif GP == 'Silverstone':
        if current in entertainment_era:
            return [[s,s,h    ,s,s,m,m],[s,m,s    ,s,s,m,h],[m,h    ,s,s,h,h]]
        elif current in strategy_era:
            return [[s,s,h  ,s,s,s,h],[s,h,s  ,s,s,s,h],[s,s,s,h  ,s,s,h]]
    elif GP == 'Sepang':
        if current in entertainment_era:
            return [[s,s,h    ,s,s,m,m],[s,m,s    ,s,s,m,h],[m,h    ,s,s,h,h]]
        elif current in strategy_era:
            return [[s,s,h  ,s,s,s,h],[s,h  ,s,s,s,s,h],[h,s  ,s,s,s,s,h]]
    elif GP == 'Shanghai':
        if current in entertainment_era:
            return [[s,s,h    ,s,s,m,m],[s,m,s    ,s,s,m,h],[m,h    ,s,s,h,h]]
        elif current in strategy_era:
            return [[s,s,h  ,s,s,s,h],[s,h  ,s,s,s,s,h],[h,s  ,s,s,s,s,h]]
    elif GP == 'Yeongam':
        if current in entertainment_era:
            return [[s,h    ,s,s,s,m,h,h],[s,m    ,s,s,s,m,h],[m,s    ,s,s,m,m,h]]
        elif current in strategy_era:
            return [[s,s,h  ,s,s,s,h],[s,h  ,s,s,s,s,h],[h,s  ,s,s,s,s,h]]
    elif GP == 'India':
        if current in entertainment_era:
            return [[s,m,h  ,s,m,h],[s,s,m    ,s,s,m,h],[s,s,h  ,s,m,m]]
        elif current in strategy_era:
            return [[s,s,s,h  ,s,s,h],[s,s,h  ,s,s,s,h],[s,h,s  ,s,s,s,h]]
    elif GP == 'Le Castellet':
        if current in entertainment_era:
            return [[m,h    ,s,s,h,h],[s,s,h    ,s,s,m,m],[s,s,m    ,s,s,m,m]]
        elif current in strategy_era:
            return [[s,s,h  ,s,s,s,h],[s,h  ,s,s,s,s,h],[h,s  ,s,s,s,s,h]]
    elif GP == 'México City':
        if current in entertainment_era:
            return [[s,h    ,s,s,s,m,h,h],[s,m    ,s,s,s,m,h],[m,s    ,s,s,m,m,h]]
        elif current in strategy_era:
            return [[s,h  ,s,s,s,s,h],[h,s  ,s,s,s,s,h],[s,s,h  ,s,s,s,h]]
    elif GP == 'Valencia':
        if current in entertainment_era:
            return [[s,s,h  ,s,m,m],[s,s,m    ,s,s,m,h],[s,m,h  ,s,m,h]]
        elif current in strategy_era:
            return [[s,s,h  ,s,s,s,h],[s,h,s  ,s,s,s,h],[s,s,s,h  ,s,s,h]]
    elif GP == 'Austin':
        if current in entertainment_era:
            return [[s,s,h    ,s,s,m,m],[s,m,s    ,s,s,m,h],[m,h    ,s,s,h,h]]
        elif current in strategy_era:
            return [[s,h  ,s,s,s,s,h],[h,s  ,s,s,s,s,h],[s,s,h  ,s,s,s,h]]
    elif GP == 'Lusail':
        if current in entertainment_era:
            return [[s,h    ,s,s,s,m,h,h],[s,m    ,s,s,s,m,h],[m,s    ,s,s,m,m,h]]
        elif current in strategy_era:
            return [[s,h  ,s,s,s,s,h],[h,s  ,s,s,s,s,h],[s,s,h  ,s,s,s,h]]
    elif GP == 'Hockenheim':
        if current in entertainment_era:
            return [[s,s,h  ,s,m,m],[s,s,m    ,s,s,m,h],[s,m,m  ,s,m,h]]
        elif current in strategy_era:
            return [[s,s,h  ,s,s,s,h],[s,h,s  ,s,s,s,h],[s,s,s,h  ,s,s,h]]
    elif GP == 'Fuji':
        if current in entertainment_era:
            return [[s,s,h  ,s,m,m],[s,s,m    ,s,s,m,h],[s,m,m  ,s,m,h]]
        elif current in strategy_era:
            return [[s,s,h  ,s,s,s,h],[s,h,s  ,s,s,s,h],[s,s,s,h  ,s,s,h]]
    elif GP == 'Melbourne':
        if current in entertainment_era:
            return [[s,h    ,s,s,m,m,h],[s,m    ,s,s,m,m,h,h],[s,s,m    ,s,s,h,h]]
        elif current in strategy_era:
            return [[s,h  ,s,s,s,s,h],[h,s  ,s,s,s,s,h],[s,s,h  ,s,s,s,h]]
    elif GP == 'Yas Island':
        if current in entertainment_era:
            return [[s,s,h  ,s,m,m],[s,m,s    ,s,s,m,h],[s,m,h  ,s,m,h]]
        elif current in strategy_era:
            return [[s,s,h  ,s,s,s,h],[s,h,s  ,s,s,s,h],[s,s,s,h  ,s,s,h]]
    elif GP == 'Spielberg':
        if current in entertainment_era:
            return [[s,s,h    ,m,m,h],[s,s,m    ,s,m,h],[s,m,s    ,s,m,h,h]]
        elif current in strategy_era:
            return [[s,s,h  ,s,s,s,h],[s,h,s  ,s,s,s,h],[s,s,s,h  ,s,s,h]]
    elif GP == 'Portimão':
        if current in entertainment_era:
            return [[s,h    ,s,s,s,m,h,h],[s,m    ,s,s,s,m,h],[m,s    ,s,s,m,m,h]]
        elif current in strategy_era:
            return [[s,h  ,s,s,s,s,h],[h,s  ,s,s,s,s,h],[s,s,h  ,s,s,s,h]]
    elif GP == 'Jeddah':
        if current in entertainment_era:
            return [[s,s,h  ,s,m,m],[s,m,s    ,s,s,m,h],[s,m,h  ,s,m,h]]
        elif current in strategy_era:
            return [[s,s,s,h  ,s,s,h],[s,s,h  ,s,s,s,h],[s,h,s  ,s,s,s,h]]
    elif GP == 'Nurburg':
        if current in entertainment_era:
            return [[s,h    ,s,s,m,m,h],[s,m    ,s,s,m,m,h,h],[s,s,m    ,s,s,h,h]]
        elif current in strategy_era:
            return [[s,h  ,s,s,s,s,h],[h,s  ,s,s,s,s,h],[s,s,h  ,s,s,s,h]]
    elif GP == 'Kyalami':
        if current in entertainment_era:
            return [[s,s,h    ,s,s,m,m],[s,m,s    ,s,s,m,h],[m,h    ,s,s,h,h]]
        elif current in strategy_era:
            return [[s,s,h  ,s,s,s,h],[s,h,s  ,s,s,s,h],[s,s,s,h  ,s,s,h]]
    elif GP == 'São Paulo':
        if current in entertainment_era:
            return [[s,h    ,s,s,s,m,h,h],[s,m    ,s,s,s,m,h],[m,s    ,s,s,m,m,h]]
        elif current in strategy_era:
            return [[s,h  ,s,s,s,s,h],[h,s  ,s,s,s,s,h],[s,s,h  ,s,s,s,h]]
    elif GP == 'Montréal':
        if current in entertainment_era:
            return [[s,s,h    ,s,s,m,m],[s,m,s    ,s,s,m,h],[m,h    ,s,s,h,h]]
        elif current in strategy_era:
            return [[s,s,h  ,s,s,s,h],[s,h,s  ,s,s,s,h],[s,s,s,h  ,s,s,h]]
    elif GP == 'Imola':
        if current in entertainment_era:
            return [[s,h    ,s,s,s,m,h,h],[s,m    ,s,s,s,m,h],[m,s    ,s,s,m,m,h]]
        elif current in strategy_era:
            return [[s,h  ,s,s,s,s,h],[h,s  ,s,s,s,s,h],[s,s,h  ,s,s,s,h]]
    elif GP == 'Suzuka':
        if current in entertainment_era:
            return [[s,m,s    ,s,m,m,h,h],[s,s,m    ,s,s,h,h],[s,h    ,s,s,m,m,h]]
        elif current in strategy_era:
            return [[s,s,h  ,s,s,s,h],[s,h,s  ,s,s,s,h],[s,h  ,s,s,s,s,h]]
    elif GP == 'Istanbul':
        if current in entertainment_era:
            return [[s,s,h  ,s,m,m],[s,s,m    ,s,s,m,h],[s,m,h  ,s,m,h]]
        elif current in strategy_era:
            return [[s,s,h  ,s,s,s,h],[s,h,s  ,s,s,s,h],[s,s,s,h  ,s,s,h]]
    elif GP == 'Miami':
        if current in entertainment_era:
            return [[s,s,h    ,s,s,m,m],[s,m,s    ,s,s,m,h],[m,h    ,s,s,h,h]]
        elif current in strategy_era:
            return [[s,s,h  ,s,s,s,h],[s,h  ,s,s,s,s,h],[h,s  ,s,s,s,s,h]]
        
# # # AGILITY CIRCUITS
lms = Circuit('Le Mans','France','Agility Circuit',23,FIA(current)[0]*120.75,STRATEGY('Le Mans'),5,['Dry','Dry','Dry','Dry','Dry','Dump','Wet'],'Very Easy',[6,9,11],6) # 2018-present layout.
# monza = Circuit('Monza','Italy','Agility Circuit',53,FIA(current)[0]*41.75,STRATEGY('Monza'),2,['Dry','Dry','Dry','Dry','Dry','Dump','Wet'],'Very Easy',[21,31,41],29) # 1994-1999 layout.
monza = Circuit('Monza','Italy','Agility Circuit',53,FIA(current)[0]*41.25,STRATEGY('Monza'),2,['Dry','Dry','Dry','Dry','Dry','Dump','Wet'],'Very Easy',[21,31,41],29) # 2000-present layout.
sochi = Circuit('Sochi','Russia','Agility Circuit',53,FIA(current)[0]*54.75,STRATEGY('Sochi'),2,['Dry','Dry','Dry','Dry','Dump','Dump','Wet'],'Average',[20,30,40],28) # 2014-present layout.
baku = Circuit('Baku','Azerbaijan','Agility Circuit',51,FIA(current)[0]*62.25,STRATEGY('Baku'),2,['Dry','Dry','Dry','Dry','Dry','Dry','Dump'],'Hard',[16,23,31],21) # 2016-present layout.
lv = Circuit('Las Vegas','United States','Agility Circuit',50,FIA(current)[0]*33.25,STRATEGY('Las Vegas'),2,['Dry','Dry','Dry','Dry','Dry','Dry','Dry'],'Hard',[21,31,41],29) # 2022-present layout.

# # # POWER CIRCUITS
# spa = Circuit('Spa-Francorchamps','Belguim','Power Circuit',44,FIA(current)[0]*62.25,STRATEGY('Spa-Francorchamps'),2,['Dry','Dry','Dry','Dry','Dump','Wet','Wet'],'Very Easy',[18,26,35],24) # 1995-2003 layout.
# spa = Circuit('Spa-Francorchamps','Belguim','Power Circuit',44,FIA(current)[0]*66.50,STRATEGY('Spa-Francorchamps'),[m,s    ,s,s,m,m,h]],2,['Dry','Dry','Dry','Dry','Dump','Wet','Wet'],'Very Easy',[18,26,35],24) # 2004-2006 layout.
spa = Circuit('Spa-Francorchamps','Belguim','Power Circuit',44,FIA(current)[0]*65.25,STRATEGY('Spa-Francorchamps'),2,['Dry','Dry','Dry','Dry','Dump','Wet','Wet'],'Very Easy',[18,26,35],24) # 2007-present layout.
le = Circuit('Le Castellet','France','Power Circuit',53,FIA(current)[0]*52.25,STRATEGY('Le Castellet'),2,['Dry','Dry','Dry','Dry','Dry','Dump','Wet'],'Easy',[16,23,31],21) # 2005-present layout.
# sakhir = Circuit('Sakhir','Bahrain','Power Circuit',57,FIA(current)[0]*17.75,STRATEGY('Sakhir'),3,['Dry'],'Easy',[16,23,29],20) # 2020 extra outer layout.
# sakhir = Circuit('Sakhir','Bahrain','Power Circuit',57,FIA(current)[0]*71.25,STRATEGY('Sakhir'),3,['Dry'],'Easy',[16,23,29],20) # 2010 layout.
sakhir = Circuit('Sakhir','Bahrain','Power Circuit',57,FIA(current)[0]*51.75,STRATEGY('Sakhir'),3,['Dry'],'Easy',[16,23,29],20) # 2004-2009 & 2011-present layout.
austin = Circuit('Austin','United States','Power Circuit',56,FIA(current)[0]*55.75,STRATEGY('Austin'),2,['Dry','Dry','Dry','Dry','Dry','Dry','Dump'],'Very Easy',[19,28,37],26) # 2012-present layout.
mexico = Circuit('México City','México','Power Circuit',71,FIA(current)[0]*38.25,STRATEGY('México City'),3,['Dry'],'Easy',[28,43,57],42) # 2015-present layout.

# QUICKNESS CIRCUITS
# silverstone = Circuit('Silverstone','Great Britain','Quickness Circuit',52,FIA(current)[0]*42.25,STRATEGY('Silverstone'),2,['Dry','Dry','Dry','Dry','Dump','Dump','Wet'],'Very Easy',[14,21,27],18) # 1997-2009 layout.
silverstone = Circuit('Silverstone','Great Britain','Quickness Circuit',52,FIA(current)[0]*48.75,STRATEGY('Silverstone'),2,['Dry','Dry','Dry','Dry','Dump','Dump','Wet'],'Very Easy',[14,21,27],18) # 2010-present layout.
sepang = Circuit('Sepang','Malaysia','Quickness Circuit',56,FIA(current)[0]*54.75,STRATEGY('Sepang'),2,['Dry','Dry','Dry','Dry','Dump','Wet','Wet'],'Very Easy',[18,26,35],24) # 1999-present layout.
shanghai = Circuit('Shanghai','China','Quickness Circuit',56,FIA(current)[0]*54.75,STRATEGY('Shanghai'),2,['Dry','Dry','Dry','Dry','Dump','Dump','Wet'],'Very Easy',[18,26,35],24) # 2004-present layout.
yeongam = Circuit('Yeongam','South Korea','Quickness Circuit',55,FIA(current)[0]*55.25,STRATEGY('Yeongam'),2,['Dry','Dry','Dry','Dry','Dump','Dump','Wet'],'Easy',[20,30,40],28) # 2010-present layout.
india = Circuit('India','India','Quickness Circuit',60,FIA(current)[0]*45.25,STRATEGY('India'),3,['Dry','Dry','Dry','Dry','Dry','Dump','Dump','Wet'],'Easy',[16,23,29],20) # 2011-present layout.

# COMPLETENESS CIRCUITS
# hockenheim = Circuit('Hockenheim','Germany','Completeness Circuit',67,FIA(current)[0]*56.75,STRATEGY('Hockenheim'),2,['Dry','Dry','Dry','Dump','Dump','Wet','Wet'],'Easy',[18,26,35],24) # 1994-2001 layout.
hockenheim = Circuit('Hockenheim','Germany','Completeness Circuit',67,FIA(current)[0]*36.25,STRATEGY('Hockenheim'),2,['Dry','Dry','Dry','Dump','Dump','Wet','Wet'],'Easy',[18,26,35],24) # 2002-present layout.
fuji = Circuit('Fuji','Japan','Completeness Circuit',67,FIA(current)[0]*40.25,STRATEGY('Fuji'),1,['Dry','Dry','Dry','Dry','Dry','Dump','Wet'],'Average',[18,26,35],24) # 2005-present layout.
# melbourne = Circuit('Melbourne','Australia','Completeness Circuit',58,FIA(current)[0]*45.25,STRATEGY('Melbourne'),4,['Dry','Dry','Dry','Dry','Dry','Dump','Wet'],'Hard',[20,30,40],28) # 1996-2020 layout.
melbourne = Circuit('Melbourne','Australia','Completeness Circuit',58,FIA(current)[0]*39.25,STRATEGY('Melbourne'),4,['Dry','Dry','Dry','Dry','Dry','Dump','Wet'],'Hard',[20,30,40],28) # 2021-present layout.
# yas = Circuit('Yas Island','Abu Dhabi','Completeness Circuit',58,FIA(current)[0]*58.75,STRATEGY('Yas Island'),2,['Dry'],'Easy',[16,23,29],20) # 2009-2020 layout.
yas = Circuit('Yas Island','Abu Dhabi','Completeness Circuit',58,FIA(current)[0]*44.75,STRATEGY('Yas Island'),2,['Dry'],'Easy',[16,23,29],20) # 2021-present layout.
spielberg = Circuit('Spielberg','Austuria','Completeness Circuit',71,FIA(current)[0]*26.25,STRATEGY('Spielberg'),2,['Dry','Dry','Dry','Dry','Dry','Dump','Dump'],'Very Easy',[20,30,40],28) # 1996-present layout.
portimao = Circuit('Portimão','Portugal','Completeness Circuit',66,FIA(current)[0]*40.75,STRATEGY('Portimão'),1,['Dry','Dry','Dry','Dry','Dry','Dry','Dump'],'Average',[28,43,57],42) # 2008-present layout.
jeddah = Circuit('Jeddah','Saudi Arabia','Completeness Circuit',50,FIA(current)[0]*49.25,STRATEGY('Jeddah'),3,['Dry'],'Easy',[13,19,24],16) # 2021-present layout.

# ENGINEERING CIRCUITS
nurburg = Circuit('Nurburg','Germany','Engineering Circuit',60,FIA(current)[0]*50.25,STRATEGY('Nurburg'),1,['Dry','Dry','Dry','Dry','Dry','Dump','Wet'],'Hard',[20,30,40],28) # 2002-present layout.
kyalami = Circuit('Kyalami','South Africa','Engineering Circuit',71,FIA(current)[0]*35.75,STRATEGY('kyalami'),2,['Dry'],'Hard',[20,30,40],28) # 2015-present layout.
# sao = Circuit('São Paulo','Brazil','Engineering Circuit',71,FIA(current)[0]*31.25,STRATEGY('São Paulo'),2,['Dry','Dry','Dry','Dry','Dump','Dump','Wet'],'Easy',[28,43,57],42) # 1996-1998 layout.
sao = Circuit('São Paulo','Brazil','Engineering Circuit',71,FIA(current)[0]*30.75,STRATEGY('São Paulo'),2,['Dry','Dry','Dry','Dry','Dump','Dump','Wet'],'Easy',[28,43,57],42) # 1999-present layout.
# montreal = Circuit('Montréal','Canada','Engineering Circuit',70,FIA(current)[0]*35.75,STRATEGY('Montréal'),3,['Dry','Dry','Dry','Dry','Dump','Wet','Wet'],'Hard',[20,30,40],28) # 1996-2001 layout.
montreal = Circuit('Montréal','Canada','Engineering Circuit',70,FIA(current)[0]*33.75,STRATEGY('Montréal'),3,['Dry','Dry','Dry','Dry','Dump','Wet','Wet'],'Hard',[20,30,40],28) # 2002-present layout.
imola = Circuit('Imola','Italy','Engineering Circuit',63,FIA(current)[0]*36.25,STRATEGY('Imola'),1,['Dry','Dry','Dry','Dry','Dump','Dump','Dump'],'Hard',[25,37,50],36) # 2008-present layout.
istanbul = Circuit('Istanbul','Turkey','Engineering Circuit',58,FIA(current)[0]*45.50,STRATEGY('Istanbul'),2,['Dry','Dry','Dry','Dry','Dump','Dump','Wet'],'Very Easy',[16,23,29],20) # 2005-present layout.
lusail = Circuit('Lusail','Qatar','Engineering Circuit',57,FIA(current)[0]*43.25,STRATEGY('Lusail'),1,['Dry'],'Average',[25,37,50],36) # 2004-present layout.
miami = Circuit('Miami','United States','Engineering Circuit',57,FIA(current)[0]*49.75,STRATEGY('Miami'),3,['Dry','Dry','Dry','Dry','Dry','Dump','Wet'],'Easy',[19,28,37],26) # 2022-present layout.

# DOWNFORCE CIRCUITS
zandvoort = Circuit('Zandvoort','Netherlands','Downforce Circuit',72,FIA(current)[0]*31.75,STRATEGY('Zandvoort'),2,['Dry','Dry','Dry','Dry','Dry','Dump','Dump'],'Hard',[13,19,24],16) # 2020-present layout.
budapest = Circuit('Budapest','Hungary','Downforce Circuit',70,FIA(current)[0]*38.75,STRATEGY('Budapest'),1,['Dry','Dry','Dry','Dry','Dump','Dump','Dump'],'Hard',[20,30,40],28) # 2003-present layout.
suzuka = Circuit('Suzuka','Japan','Downforce Circuit',53,FIA(current)[0]*50.75,STRATEGY('Suzuka'),1,['Dry','Dry','Dry','Dry','Dump','Dump','Wet'],'Hard',[16,23,31],21) # 2009-present layout.
barcelona = Circuit('Barcelona','Spain','Downforce Circuit',66,FIA(current)[0]*40.25,STRATEGY('Barcelona'),2,['Dry','Dry','Dry','Dry','Dry','Dump','Dump'],'Hard',[20,30,40],28) # 2007-present layout.

# STREET CIRCUITS
monaco = Circuit('Monte-Carlo','Monaco','Street Circuit',78,FIA(current)[0]*32.25,STRATEGY('Monte-Carlo'),2,['Dry','Dry','Dry','Dry','Dump','Dump','Wet'],'Impossible',[20,30,40],28) # 2003-present layout.
# singapore = Circuit('Singapore','Singapore','Street Circuit',61,FIA(current)[0]*62.75,STRATEGY('Singapore'),3,['Dry','Dry','Dry','Dry','Dump','Dump','Wet'],'Very Hard',[16,23,29],20) # 2008-2012 layout.
# singapore = Circuit('Singapore','Singapore','Street Circuit',61,FIA(current)[0]*62.25,STRATEGY('Singapore'),3,['Dry','Dry','Dry','Dry','Dump','Dump','Wet'],'Very Hard',[16,23,29],20) # 2013-2014 layout.
# singapore = Circuit('Singapore','Singapore','Street Circuit',61,FIA(current)[0]*63.75,STRATEGY('Singapore'),3,['Dry','Dry','Dry','Dry','Dump','Dump','Wet'],'Very Hard',[16,23,29],20) # 2015-2017 layout.
singapore = Circuit('Singapore','Singapore','Street Circuit',61,FIA(current)[0]*59.75,STRATEGY('Singapore'),3,['Dry','Dry','Dry','Dry','Dump','Dump','Wet'],'Very Hard',[16,23,29],20) # 2018-present layout.
valencia = Circuit('Valencia','Spain','Street Circuit',57,FIA(current)[0]*56.25,STRATEGY('Valencia'),2,['Dry','Dry','Dry','Dry','Dry','Dry','Dump'],'Hard',[16,23,29],20) # 2008-present layout.

circuits = [lms,monza,sochi,baku,lv,
            spa,le,sakhir,austin,mexico,
            silverstone,sepang,shanghai,yeongam,india,
            hockenheim,fuji,melbourne,yas,spielberg,portimao,jeddah,
            nurburg,kyalami,sao,montreal,imola,istanbul,lusail,miami,
            zandvoort,budapest,suzuka,barcelona,
            monaco,singapore,valencia]

# Error Handling for Circuit Variable
vtt = 0
for i in circuits:
    if i.location == GP:
        vtt += 1
    else:
        vtt += 0

if vtt != 0:
    pass
else:
    print(f'There is no circuit named {GP}. Try one of these:')
    for i in circuits:
        print(i.location)
    print('Program terminated.')
    sys.exit(0)

# Engines
class Engine():
    def __init__(self,brand,fuel,power,durability):
        self.brand = brand
        self.fuel = fuel
        self.power = power
        self.durability = durability

# Formula 1 Engines
MERCEDES_0 = Engine('Mercedes',FIA(current)[5],91,81) # McLaren
FERRARI_F = Engine('Ferrari',FIA(current)[5],89,86) # Ferrari
FERRARI_0 = Engine('Ferrari',FIA(current)[5],89,86) # Benetton
FERRARI_1 = Engine('Ferrari',FIA(current)[5],89,86) # Minardi
HONDA_F = Engine('Honda',FIA(current)[5],89,72) # Honda
RENAULT_0 = Engine('Renault',FIA(current)[5],84,82) # Williams
RENAULT_1 = Engine('Renault',FIA(current)[5],84,82) # Lotus
RENAULT_2 = Engine('Renault',FIA(current)[5],84,82) # Brabham
TOYOTA_F = Engine('Toyota',FIA(current)[5],77,89) # Toyota
TOYOTA_0 = Engine('Toyota',FIA(current)[5],77,89) # Sauber
TOYOTA_1 = Engine('Toyota',FIA(current)[5],77,89) # Jaguar

# Formula 2 Engines
MECACHROME = Engine('Mecachrome',FIA(current)[5],86,76) # F2 Spec. Only

# Manufacturers
class Manufacturer():
    def __init__(self,title,crew,powertrain,chassis,FW,RW,base,sidepod,suspension,reliability,weight):
        self.title = title
        self.crew = crew
        
        # Base Attributes
        self.powertrain = powertrain
        self.chassis = chassis
        self.FW = FW
        self.RW = RW
        self.base = base
        self.sidepod = sidepod
        self.suspension = suspension
        self.reliability = ((reliability*1.7) + (self.powertrain.durability*3.3))/5
        
        # Calculated Attributes
        self.downforce = (((self.base*FIA(current)[7]) + (self.FW*FIA(current)[8]) + (self.RW*FIA(current)[9]))/10)
        self.drag = ((self.chassis*5) + (self.base*3) + (self.RW*2))/10
        self.vortex = ((self.FW*5) + (self.sidepod*3) + (self.chassis*2))/10
        self.braking = ((self.FW*5) + (self.suspension*5))/10
        
        # Advanced Calculated Attributes
        self.max_speed = round(((self.powertrain.power*10.0) + (self.RW*2.0) + (self.drag*3.0))/15,3)
        self.acceleration = self.powertrain.power
        
        # Extra Calculated Attribute 2
        self.drs_delta = ((self.powertrain.power*2.5) + (self.RW*7.5))/10
        
        # Extra Attributes
        self.weight = weight
        
        # Car Characteristics
        self.downforced = self.vortex + self.downforce
        self.powered = self.max_speed + self.rating()

        if self.downforced > self.powered + 4:
            self.V1 = 'Corners'
        elif self.powered > self.downforced + 8:
            self.V1 = 'Straights'
        else:
            self.V1 = None

        if self.vortex >= self.downforce + 1.5:
            self.V2 = 'Calm'
        elif self.downforce >= self.vortex + 1.5:
            self.V2 = 'Wild'
        else:
            self.V2 = None

        if self.FW > self.RW + 6:
            self.V3 = 'Weak Rear'
        elif self.RW > self.FW + 6:
            self.V3 = 'Weak Front'
        else:
            self.V3 = None

        self.characteristic = [self.V1,self.V2,self.V3]

        # Tire Performance Analysis
        self.manufacturer_tyre_coeff = round(((((self.vortex + self.braking + (self.suspension*2) + self.RW) - (self.drag + self.downforce)))/1450),3)
        if self.manufacturer_tyre_coeff <= 0.120:
            self.manufacturer_tyre_coeff_print = 'Very Bad'
        elif 0.120 <= self.manufacturer_tyre_coeff <= 0.135:
            self.manufacturer_tyre_coeff_print = 'Bad'
        elif 0.135 <= self.manufacturer_tyre_coeff <= 0.160:
            self.manufacturer_tyre_coeff_print = 'Average'
        elif 0.160 <= self.manufacturer_tyre_coeff <= 0.180:
            self.manufacturer_tyre_coeff_print = 'Good'
        elif 0.180 <= self.manufacturer_tyre_coeff:
            self.manufacturer_tyre_coeff_print = 'Perfect'

    def pit(self):
        if self.crew == 'Perfect':
            limit = 2.50
            failure_odd = 5
        elif self.crew == 'Good':
            limit = 3.00
            failure_odd = 10
        elif self.crew == 'Average':
            limit = 3.50
            failure_odd = 25
        elif self.crew == 'Bad':
            limit = 4.00
            failure_odd = 45
        pitt = []
        for i in list(np.arange(2.00,limit,0.01)):
            pitt.append(i)
        for j in list(np.arange(limit+0.5,(limit*(failure_odd/7)),0.5)):
            pitt.append(j)
        return choice(pitt)

    def rating(self):
        return ((self.powertrain.power*((13+FIA(current)[13]))) + (self.downforce*((15+FIA(current)[14]))) + (self.drag*((17+FIA(current)[15]))) + (self.vortex*20) + (self.braking*15))/100
    
    def performance(self,circuit_type):
        if circuit_type == 'Power Circuit':
            if self.V1 == 'Straights':
                return (((((self.max_speed+self.acceleration)/2)*5) + (self.downforce*3) + (self.vortex*2) + (self.braking*1))/11) + 0.298
            elif self.V1 == 'Corners':
                return (((((self.max_speed+self.acceleration)/2)*5) + (self.downforce*3) + (self.vortex*2) + (self.braking*1))/11) + 0.051
            else:
                return (((((self.max_speed+self.acceleration)/2)*5) + (self.downforce*3) + (self.vortex*2) + (self.braking*1))/11)
        elif circuit_type == 'Agility Circuit':
            if self.V1 == 'Straights':
                return ((self.max_speed*5) + (self.braking*3) + (self.vortex*2) + (self.downforce*1))/11 + 0.349
            elif self.V1 == 'Corners':
                return ((self.max_speed*5) + (self.braking*3) + (self.vortex*2) + (self.downforce*1))/11
            else:
                return ((self.max_speed*5) + (self.braking*3) + (self.vortex*2) + (self.downforce*1))/11
        elif circuit_type == 'Quickness Circuit':
            return ((self.max_speed*4) + (self.downforce*4) + (self.vortex*2) + (self.braking*1))/11
        elif circuit_type == 'Completeness Circuit':
            return ((self.downforce*5) + (self.max_speed*3) + (self.vortex*2) + (self.braking*1))/11
        elif circuit_type == 'Engineering Circuit':
            if self.V1 == 'Straights':
                return ((self.downforce*5) + (self.acceleration*3) + (self.vortex*2) + (self.braking*1))/11
            elif self.V1 == 'Corners':
                return ((self.downforce*5) + (self.acceleration*3) + (self.vortex*2) + (self.braking*1))/11 + 0.349
            else:
                return ((self.downforce*5) + (self.acceleration*3) + (self.vortex*2) + (self.braking*1))/11
        elif circuit_type == 'Downforce Circuit':
            if self.V1 == 'Straights':
                return ((self.downforce*5) + (self.vortex*3) + (self.acceleration*2) + (self.braking*1))/11
            elif self.V1 == 'Corners':
                return ((self.downforce*5) + (self.vortex*3) + (self.acceleration*2) + (self.braking*1))/11 + 0.349
            else:
                return ((self.downforce*5) + (self.vortex*3) + (self.acceleration*2) + (self.braking*1))/11
        elif circuit_type == 'Street Circuit':
            return ((self.downforce*4) + (self.braking*4) + (self.vortex*2) + (self.acceleration*1))/11

if spec == 'Formula 1':
    """
print(design('Perfect','Adrian Newey',96,89,89,'Balanced','Low',30.0,7.0,1998,[0,0,0,0,0,0],'West McLaren-Mercedes','MERCEDES_0'))
print(design('Perfect','Aldo Costa',94,91,91,'Balanced','Balanced',30.0,7.0,1998,[0,0,0,0,0,0],'Scuderia Ferrari Vodafone','FERRARI_F'))
print(design('Perfect','Paddy Lowe',89,81,81,'Balanced','Low',25.0,7.0,1998,[0,0,0,0,0,0],'Rothmans Williams-Renault','RENAULT_0'))
print(design('Good','Simone Resta',82,74,72,'Balanced','Low',27.5,5.0,1998,[0,0,0,0,0,0],'Winfield Benetton-Ferrari','FERRARI_0'))
print(design('Good','Pat Symonds',86,81,81,'Balanced','Low',28.0,7.0,1998,[0,0,0,0,0,0],'Honda F1 Team','HONDA_F'))
print(design('Good','John Barnard',91,91,91,'Balanced','High',25.0,5.0,1998,[0,0,0,0,0,0],'BWT Sauber-Toyota','TOYOTA_0'))
print(design('Good','James Allison',84,84,79,'Balanced','High',20.0,5.0,1998,[0,0,0,0,0,0],'Marlboro Team Lotus-Renault','RENAULT_1'))
print(design('Good','Ray Durand',79,79,76,'Front Stiff','Low',18.0,5.0,1998,[0,0,0,0,0,0],'Parmalat Brabham-Renault','RENAULT_2'))
print(design('Good','Anthony Coughlan',80,76,76,'Front Stiff','High',20.0,5.0,1998,[0,0,0,0,0,0],'Mild Seven Toyota Racing','TOYOTA_F'))
print(design('Average','Nick Flynn',80,72,72,'Balanced','Low',23.0,7.0,1998,[0,0,0,0,0,0],'Jaguar Racing Toyota','TOYOTA_1'))
print(design('Bad','Ignacio La Chazelle',66,62,62,'Rear Stiff','Low',18.0,3.0,1998,[0,0,0,0,0,0],'Minardi-Ferrari F1 Team','FERRARI_1'))
    """

    mclaren = Manufacturer('West McLaren-Mercedes','Perfect',MERCEDES_0,85,94,82,97,88,90,60,1.43)
    ferrari = Manufacturer('Scuderia Ferrari Vodafone','Perfect',FERRARI_F,92,91,93,94,86,85,62,0.0)
    williams = Manufacturer('Rothmans Williams-Renault','Perfect',RENAULT_0,84,86,78,80,85,82,50,0.0)
    benetton = Manufacturer('Winfield Benetton-Ferrari','Bad',FERRARI_0,85,79,82,75,79,88,53,3.04)
    honda = Manufacturer('Honda F1 Team','Good',HONDA_F,80,82,84,85,79,80,59,2.26)
    sauber = Manufacturer('BWT Sauber-Toyota','Bad',TOYOTA_0,79,75,79,79,72,80,80,0.0)
    lotus = Manufacturer('Marlboro Team Lotus-Renault','Perfect',RENAULT_1,72,66,74,75,72,66,75,0.0)
    brabham = Manufacturer('Parmalat Brabham-Renault','Perfect',RENAULT_2,69,80,62,64,72,72,50,-1.63)
    toyota = Manufacturer('Mild Seven Toyota Racing','Good',TOYOTA_F,74,72,68,74,65,72,83,+1.45)
    jaguar = Manufacturer('Jaguar Racing Toyota','Good',TOYOTA_1,76,77,68,68,75,76,61,0.0)
    minardi = Manufacturer('Minardi-Ferrari F1 Team','Good',FERRARI_1,68,68,70,69,65,64,59,+4.38)
    manufacturers = [honda,jaguar,lotus,toyota,minardi,sauber,brabham,williams,ferrari,mclaren,benetton]
elif spec == 'Formula 2':
    carlin = Manufacturer('Carlin','Perfect',MECACHROME,91,91,91,91,91,91,91,+0.00)
    manor = Manufacturer('Manor Racing','Good',MECACHROME,91,91,91,89,89,89,89,+0.00)
    dams = Manufacturer('DAMS','Good',MECACHROME,91,91,91,87,87,87,87,+0.00)
    art = Manufacturer('ART Grand Prix','Average',MECACHROME,91,91,91,85,85,85,85,+0.00)
    trident = Manufacturer('Trident Racing','Good',MECACHROME,91,91,91,83,83,83,83,+0.00)
    clark = Manufacturer('Clark Grand Prix Engineering','Good',MECACHROME,91,91,91,81,81,81,81,+0.00)
    stewart = Manufacturer('Stewart Grand Prix','Average',MECACHROME,91,91,91,79,79,79,79,+0.00)
    draco = Manufacturer('Draco Grand Prix Engineering','Average',MECACHROME,91,91,91,79,79,79,79,+0.00)
    falcon = Manufacturer('Falcon Grand Prix','Average',MECACHROME,91,91,91,79,79,79,79,+0.00)
    fortec = Manufacturer('Fortec Motorsport','Average',MECACHROME,91,91,91,79,79,79,79,+0.00)
    sn = Manufacturer('Super Nova Racing','Average',MECACHROME,91,91,91,79,79,79,79,+0.00)
    manufacturers = [art,carlin,clark,dams,draco,falcon,fortec,manor,trident,stewart,sn]

# Drivers
class Driver():
    def __init__(self,team,name,nationality,number,pace,braking,smoothness,adaptability,consistency,fitness,aggression,attack,defence,start,wet,favorite,style):
        self.team = team
        self.name = name
        self.nationality = nationality
        self.number = number
        self.pace = pace
        self.braking = braking
        self.smoothness = smoothness
        self.adaptability = adaptability
        self.consistency = consistency
        self.fitness = fitness
        self.aggression = aggression
        self.attack = attack
        self.defence = defence
        self.start = start
        self.wet = wet
        self.form = uniform(((((fitness*3.5) + (consistency*1.5))/5000)) - 0.025, ((((fitness*3.5) + (consistency*1.5))/5000)) + 0.025)
        self.favorite = favorite
        self.style = style
    
    def real_qualifying_pace(self):
        return round((((self.pace*4) + (self.braking*4) + (self.consistency*3))/11),3)
    def real_race_pace(self):
        return round((((self.pace*6) + (self.braking*8)  + (self.smoothness*6) + (self.adaptability*8) + (self.consistency*8) + (self.fitness*8))/44),3)
    def real_rating(self):
        return round((self.real_qualifying_pace() + self.real_race_pace())/2,3)
    
    def qualifying_pace(self):
        return round(((self.real_qualifying_pace())+75)/1.75,3)
    def race_pace(self):
        return round(((self.real_race_pace())+75)/1.75,3)
    def rating(self):
        return round(((self.real_rating())+75)/1.75,3)

    def tire_harm_by_driver(self,tire_usage):
        variable = ((tire_usage) - (pow(10,-3)*pow(self.smoothness,2))) - 2
        if variable >= 0:
            return (variable/2)
        else:
            return 0
        
if spec == 'Formula 1':
    D1 = Driver(mclaren,"Devon Raleigh",None,None,90,90,88,92,96,92,90,90,86,86,92,[None],[None,None]) # 1998
    D2 = Driver(mclaren,"Nill Rosberg",None,None,94,90,88,96,90,88,88,88,88,90,90,[None],[None,None]) # 1998 - 2000 - 2001
    D3 = Driver(ferrari,"Charles Hérnandez",None,None,90,96,86,86,92,88,86,86,86,88,86,[None],[None,None]) # 1998 - 1999
    D4 = Driver(ferrari,"Herbert Wolf",None,None,88,91,96,91,94,91,84,88,91,91,88,[None],[None,None]) # 1998
    D5 = Driver(williams,"Ken Fassbender",None,None,88,88,88,88,94,94,88,90,90,90,90,[None],[None,None]) # 1998
    D6 = Driver(williams,"Mattia Lori",None,None,77,80,77,72,72,72,77,81,77,72,77,[None],[None,None]) # 1998 - 2000 - 2001
    D7 = Driver(benetton,"Daniil Kovalev",None,None,90,86,80,84,90,80,80,82,82,82,82,[None],[None,None]) # 1998 - 1999
    D8 = Driver(benetton,"Sarvesh Sharaf",None,None,68,68,68,68,70,68,68,68,68,64,68,[None],[None,None]) # 1998
    D9 = Driver(honda,"Jackson Perry",None,None,76,86,84,84,84,72,76,76,76,82,88,['Monte-Carlo'],[None,None]) # 1998
    D10 = Driver(honda,"Katsuno Yoshiro",None,None,82,82,76,76,76,76,88,88,86,88,72,['Suzuka'],[None,None]) # 1998 - 1999
    D17 = Driver(sauber,"Jérémy Claes",None,None,74,74,76,76,76,76,76,76,76,74,74,[None],[None,None]) # 1998 - 2000 - 2001
    D18 = Driver(sauber,"Matteo de Vos",None,None,70,70,70,70,72,76,70,70,70,74,74,[None],[None,None]) # 1998 - 2000 - 2001
    D11 = Driver(lotus,"Sander Metz",None,None,84,84,84,82,86,82,80,88,88,82,90,[None],[None,None]) # 1998
    D12 = Driver(lotus,"Charlie Southgate",None,None,82,82,82,90,86,86,86,80,76,82,76,[None],[None,None]) # 1998 - 1999
    D13 = Driver(brabham,"August Wehner",None,None,79,79,82,82,82,82,79,79,76,76,76,[None],[None,None]) # 1998
    D14 = Driver(brabham,"Marcus Svansson",None,None,84,86,80,80,76,88,86,84,84,82,80,[None],[None,None]) # 1998 - 1999
    D15 = Driver(toyota,"Guillermo Acosta",None,None,75,75,72,75,72,72,75,80,80,80,76,[None],[None,None]) # 1998
    D16 = Driver(toyota,"Aaron Hérnandez",None,None,76,80,76,72,72,72,72,76,76,76,76,[None],[None,None]) # 1998 - 1999
    D19 = Driver(jaguar,"Sam Maloney",None,None,74,74,74,74,74,68,68,68,68,64,68,[None],[None,None]) # 1998 - 2000 - 2001 - 2002
    D20 = Driver(jaguar,"Matt Rockwell",None,None,76,76,70,70,74,68,68,68,68,64,68,[None],[None,None]) # 1998 - 2000 - 2001 - 2002
    D21 = Driver(minardi,"Raul Sanchez",None,None,88,86,88,88,80,80,82,84,76,88,84,[None],[None,None]) # 1998
    D22 = Driver(minardi,"Antonio Bacarrello",None,None,72,72,66,66,72,76,70,70,70,74,74,[None],[None,None]) # 1998 - 1999
    drivers = [D1,D2,D3,D4,D5,D6,D7,D8,D9,D10,D11,D12,D13,D14,D15,D16,D17,D18,D19,D20,D21,D22]

elif spec == 'Formula 2':
    D1 = Driver(art,"Théo Fernandez",None,None,76,77,77,68,82,66,74,72,73,77,76,[None],[None,None])
    D2 = Driver(art,"Stuart Reddsey",None,None,70,70,76,84,69,84,74,75,77,74,74,[None],[None,None])
    D3 = Driver(carlin,"Vincent White",None,None,75,75,70,77,77,73,76,72,77,72,76,[None],[None,None])
    D4 = Driver(carlin,"Derek West",None,None,72,66,59,69,68,64,68,65,68,64,69,[None],[None,None])
    D5 = Driver(clark,"Oleg Rasmussen",None,None,65,69,66,66,67,68,69,69,68,66,69,[None],[None,None])
    D6 = Driver(clark,"Jan Seidel",None,None,67,67,72,77,67,78,71,75,73,71,75,[None],[None,None])
    D7 = Driver(dams,"Alan Reddsey",None,None,72,64,57,66,64,69,69,68,63,68,63,[None],[None,None])
    D8 = Driver(dams,"Alex Rosnersson",None,None,77,75,73,72,73,76,73,78,77,75,72,[None],[None,None])
    D9 = Driver(draco,"Carsen Rodriguez",None,None,75,79,73,74,74,73,77,74,79,78,74,[None],[None,None])
    D10 = Driver(draco,"Heikki Litmanen",None,None,64,70,76,65,72,67,66,67,72,70,67,[None],[None,None])
    D11 = Driver(falcon,"Lewis Simmons",None,None,76,74,71,72,72,76,76,74,71,70,75,[None],[None,None])
    D12 = Driver(falcon,"Daley Harvick",None,None,65,61,64,67,64,66,61,64,64,66,65,[None],[None,None])
    D13 = Driver(fortec,"Juan Angel Ramirez",None,None,64,65,59,64,64,64,59,59,63,64,64,[None],[None,None])
    D14 = Driver(fortec,"Esteban Caillero",None,None,64,65,65,69,68,69,67,63,66,66,65,[None],[None,None])
    D15 = Driver(manor,"Matthew Barker",None,None,76,70,71,76,74,71,75,74,70,72,76,[None],[None,None])
    D16 = Driver(manor,"Kai Yoshiro",None,None,81,85,75,70,85,71,78,79,78,77,79,[None],[None,None])
    D17 = Driver(trident,"Chris Puertas",None,None,71,66,67,66,70,68,70,72,72,71,66,[None],[None,None])
    D18 = Driver(trident,"David Boeck",None,None,72,77,75,66,73,68,71,72,71,73,73,[None],[None,None])
    D19 = Driver(stewart,"Alejandro Macerta",None,None,73,74,73,75,72,70,69,72,70,71,70,[None],[None,None])
    D20 = Driver(stewart,"Rich Douglas",None,None,70,66,68,71,71,66,70,70,68,68,70,[None],[None,None])
    D21 = Driver(sn,"Antonio Raineri",None,None,72,77,77,72,76,72,76,75,73,73,78,[None],[None,None])
    D22 = Driver(sn,"Mauro Milani",None,None,78,76,78,81,75,75,75,76,75,81,77,[None],[None,None])
    drivers = [D1,D2,D3,D4,D5,D6,D7,D8,D9,D10,D11,D12,D13,D14,D15,D16,D17,D18,D19,D20,D21,D22]

# # # End of the Class Deifinition
# # # Algorithm Build-up
errorq = 0
for i in circuits:
    if i.location == GP:
        CRC = i

# Weather Selection
W1 = choice(CRC.weather)
if W1 == 'Dump':
    W2 = choice(['Dry','Dump'])
    if W2 == 'Dry':
        W3 = 'Dry'
    elif W2 == 'Dump':
        W3 = choice(['Dry','Dump'])
elif W1 == 'Wet':
    W2 = choice(['Wet','Dump'])
    if W2 == 'Wet':
        W3 = choice(['Wet','Dump'])
    elif W2 == 'Dump':
        W3 = choice(['Dry','Dump'])
elif W1 == 'Dry':
    W2 = choice(CRC.weather)
    if W2 == 'Dry':
        W3 = 'Dry'
    elif W2 == 'Dump':
        W3 = choice(CRC.weather)
    elif W2 == 'Wet':
        W3 = choice(CRC.weather)

if execution == 'simulation':
    print(f'{CRC.location} GP — {CRC.country} | FP forecast: {W1} | Qualifying forecast: {W2} | Race forecast: {W3}\n{borderline}')

# # #

PIT, GRID, DNF = {}, {}, {}

def ANALYZER(session,data,tirenamedata,keyword):
    teams_, names_, intervals_, gaps_, fls_, laps_, tires_ = [], [], [], [], [], [], []
    osimhen = 0 # total time spent for the race.

    for i in list(data.columns):
        
        # Stage 1
        chart = list(data[i])
        tchart = list(tirenamedata[i])
        
        # Stage 2
        names_.append(i)
        intervals_.append(sum(chart))
        
        fll = min(chart)
        fls_.append(fll)
        
        laps_.append((chart.index(fll)+1))
        tires_.append(tchart[chart.index(min(chart))])
        for j in drivers:
            if j.name == i:
                teams_.append(j.team.title)

    # Stage 3
    df = pd.DataFrame()
    df['MANUFACTURERS'] = teams_
    df['DRIVERS'] = names_

    # Stage 4
    df['INTERVAL'] = intervals_
    df['FL. TEMP'] = fls_
    df['FL.'] = fls_
    df['FL. LAP'] = laps_
    df['FL. TIRE'] = tires_
    newfls_, newintervals_, lastintervals_ = [], [], []
    for i in fls_:
        integer = i//60
        decimal = str(i-(integer*60))[0:6]
        string = str(int(integer)) +':'+ decimal
        newfls_.append(string)
    df['FL.'] = newfls_
    for i in intervals_:
        if i == min(intervals_):
            newintervals_.append(0)
            osimhen = i
        else:
            newintervals_.append(round(i - min(intervals_),3))
    df['INTERVAL'] = newintervals_
    
    # Stage 5: Differences Between Race/Quali Charts
    if keyword == 'race-chart':
        df = df.sort_values('INTERVAL',ascending=True)
        
        for w in list(df['INTERVAL']):
            the_index = list(df['INTERVAL']).index(w)
            if the_index == 0:
                gaps_.append(osimhen)
            else:
                gaps_.append(list(df['INTERVAL'])[the_index] - list(df['INTERVAL'])[the_index-1])
        df['GAP'] = gaps_ 

        for i in list(df['INTERVAL']):
            if i == list(df['INTERVAL'])[0]:
                lastintervals_.append('INTERVAL')
            elif i > (data[list(df['DRIVERS'])[list(df['INTERVAL']).index(list(df['INTERVAL'])[0])]][len(data[list(df['DRIVERS'])[list(df['INTERVAL']).index(list(df['INTERVAL'])[0])]])-1]):
                if 2 > i/(data[list(df['DRIVERS'])[list(df['INTERVAL']).index(list(df['INTERVAL'])[0])]][0]):
                    lastintervals_.append('+1 Lap')
                else:
                    lastintervals_.append(f"+{int(i/(data[list(df['DRIVERS'])[list(df['INTERVAL']).index(list(df['INTERVAL'])[0])]][0]))} Laps")
            else:
                lastintervals_.append(f'+{i}')

        dnfcorrectedintervals_ = []
        for i in lastintervals_:
            if len(DNF[list(df['DRIVERS'])[lastintervals_.index(i)]]) > 1:
                dnfcorrectedintervals_.append('DNF')
            else:
                dnfcorrectedintervals_.append(i)

        df['INTERVAL'] = dnfcorrectedintervals_
        df = df.reset_index()
        df = df.drop(axis=1, columns=['index', 'FL. TEMP'])

        df = df[['MANUFACTURERS', 'DRIVERS', 'INTERVAL', 'GAP', 'FL.', 'FL. LAP', 'FL. TIRE']]

        # Saving Grid Positions into to the Chart
        gridlist = []
        for i in list(df['DRIVERS']):
            gridlist.append(GRID[i])
        df['GRID'] = gridlist

        # Number of Times Pitted?
        aboubakar = list(df['DRIVERS'])
        pitlist = []
        
        for i in aboubakar:
            pitlist.append(sum(PIT[i]))
        
        df['PIT'] = pitlist

    elif keyword == 'quali-chart':
        gap = []
        df = df.sort_values('FL. TEMP',ascending=True)
        df = df.drop(axis=1, columns=['INTERVAL'])
        for i in list(df['FL.']):
            leader = (float(list(df['FL.'])[0].split(':')[0])*60) + float(list(df['FL.'])[0].split(':')[1])
            time = (float(i.split(':')[0])*60) + float(i.split(':')[1])
            if i == list(df['FL.'])[0]:
                gap.append('FASTEST')
            else:
                gap.append(f'+{round(time-leader,3)}')
        df['GAP'] = gap
        df = df.reset_index()
        df = df.drop(axis=1, columns=['index', 'FL. TEMP'])
        
        df = df[['MANUFACTURERS','DRIVERS','FL.','GAP','FL. LAP','FL. TIRE']]

        # Saving Grid Positions into to the Chart
        for i,k in zip(list(df['DRIVERS']),list(range(1,len(list(df.index))+1))):
            GRID[i] = k

    # Final Alingments
    da = pd.DataFrame()
    da = da.reindex(list(range(1,len(list((df.index)))+1)))
    
    if session == 'Qualifying':
        df = df.drop(axis=1, columns=['FL. TIRE'])
        DDD, q1f, q2f, q3f, q1, q2, q3 = {}, [], [], [], [], [], []

        for i in list(data.columns):
            DDD[i] = list(data[i])

        nolandrivers = list(df['DRIVERS'])

        for i in nolandrivers:
            q1f.append(DDD[i][0])
            q2f.append(DDD[i][1])
            q3f.append(DDD[i][2])

        for b,n,m in zip(q1f,q2f,q3f):
            if b == 499.999:
                q1.append('DNF')
            else:
                i = b
                integer = i//60
                decimal = str(i-(integer*60))[0:6]
                string = str(int(integer)) +':'+ decimal
                q1.append(string)

            if n == 499.999:
                q2.append('DNF')
            else:
                i = n
                integer = i//60
                decimal = str(i-(integer*60))[0:6]
                string = str(int(integer)) +':'+ decimal
                q2.append(string)

            if m == 499.999:
                q3.append('DNF')
            else:
                i = m
                integer = i//60
                decimal = str(i-(integer*60))[0:6]
                string = str(int(integer)) +':'+ decimal
                q3.append(string)

        df['L1'] = q1
        df['L2'] = q2
        df['L3'] = q3

    for i in list(df.columns):
        da[i] = list(df[i])

    # DNF/FL. Optimizing for Race Session
    if keyword == 'race-chart':
        dnffloptimizer0, dnffloptimizer1 = [], []
        
        for i,j in zip(list(da['FL. LAP']),list(da['FL.'])):
            if 2 >= i:
                dnffloptimizer0.append('None')
                dnffloptimizer1.append('None')
            else:
                dnffloptimizer0.append(int(i))
                dnffloptimizer1.append(j)

        da['FL.'] = dnffloptimizer1
        da['FL. LAP'] = dnffloptimizer0

    # DNF Optimizing for Free Practice/Qualifying Session
    optimizing, optimizing0 = [], []
    if keyword == 'quali-chart':
        for i,j in zip(list(da['FL.']),list(da['GAP'])):
            if int(i[0]) >= 5:
                optimizing.append('DNF')
                optimizing0.append(None)
            else:
                optimizing.append(i)
                optimizing0.append(j)
        da['FL.'] = optimizing
        da['GAP'] = optimizing0

    # Gap Correction
    newgap = []
    if keyword == 'race-chart':
        for f,p in zip(list(df['INTERVAL']),list(df['GAP'])):
            if f == 'DNF':
                newgap.append('DNF')
            elif (list(df['GAP']).index(p)) == 0:
                seconds = p
                delta = datetime.timedelta(seconds=seconds)
                
                hours, remainder = divmod(delta.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                milliseconds = delta.microseconds // 1000
                
                totaltimehavespent = '{:02d}:{:02d}:{:02d}.{:03d}'.format(hours, minutes, seconds, milliseconds)
                newgap.append(totaltimehavespent)
            else:
                newgap.append(f'+{round(p,3)}')
        da['GAP'] = newgap

    # Final Alignments

    if keyword == 'race-chart':
        da = da[['MANUFACTURERS','DRIVERS','INTERVAL','GAP','FL.','FL. LAP','FL. TIRE','PIT','GRID']]
    else:
        pass

    if session == 'Qualifying':
        fl31, gap31, l131, l231, l331 = [], [], [], [], []
        
        for i in list(da['FL.']):
            if i == 'DNF':
                fl31.append('DNF')
            elif len(str(i.split(':')[1])) != 6:
                missing = 6 - len(str(i.split(':')[1]))
                fff = f"{str(i.split(':')[1])}{str(0)*missing}"
                f = f"{str(i.split(':')[0])}:{fff}"
                fl31.append(f)
            else:
                f = f"{str(i.split(':')[0])}:{str(i.split(':')[1])}"
                fl31.append(f)

        da['FL.'] = fl31

        for i in list(da['L1']):
            if i == 'DNF':
                l131.append('DNF')
            elif len(str(i.split(':')[1])) != 6:
                missing = 6 - len(str(i.split(':')[1]))
                fff = f"{str(i.split(':')[1])}{str(0)*missing}"
                f = f"{str(i.split(':')[0])}:{fff}"
                l131.append(f)
            else:
                f = f"{str(i.split(':')[0])}:{str(i.split(':')[1])}"
                l131.append(f)

        da['L1'] = l131

        for i in list(da['L2']):
            if i == 'DNF':
                l231.append('DNF')
            elif len(str(i.split(':')[1])) != 6:
                missing = 6 - len(str(i.split(':')[1]))
                fff = f"{str(i.split(':')[1])}{str(0)*missing}"
                f = f"{str(i.split(':')[0])}:{fff}"
                l231.append(f)
            else:
                f = f"{str(i.split(':')[0])}:{str(i.split(':')[1])}"
                l231.append(f)

        da['L2'] = l231

        for i in list(da['L3']):
            if i == 'DNF':
                l331.append('DNF')
            elif len(str(i.split(':')[1])) != 6:
                missing = 6 - len(str(i.split(':')[1]))
                fff = f"{str(i.split(':')[1])}{str(0)*missing}"
                f = f"{str(i.split(':')[0])}:{fff}"
                l331.append(f)
            else:
                f = f"{str(i.split(':')[0])}:{str(i.split(':')[1])}"
                l331.append(f)

        da['L3'] = l331
        
        for q in list(da['GAP']):
            try:
                if len(str(q.split('.')[1])) != 3:
                    missing = 3 - len(str(q.split('.')[1]))
                    ttt = f"{str(q.split('.')[1])}{str(0)*missing}"
                    t = f"{str(q.split('.')[0])}.{ttt}"
                    gap31.append(t)
                else:
                    t = f"{str(q.split('.')[0])}.{str(q.split('.')[1])}"
                    gap31.append(t)
            except:
                if q == 'FASTEST':
                    gap31.append('FASTEST')
                else:
                    gap31.append('DNF')

        da['GAP'] = gap31
    
    elif keyword == 'race-chart':
        fl31, gap31, interval31 = [], [], []
               
        for i in list(da['FL.']):
            if i == 'None':
                fl31.append('None')
            elif len(str(i.split(':')[1])) != 6:
                missing = 6 - len(str(i.split(':')[1]))
                fff = f"{str(i.split(':')[1])}{str(0)*missing}"
                f = f"{str(i.split(':')[0])}:{fff}"
                fl31.append(f)
            else:
                f = f"{str(i.split(':')[0])}:{str(i.split(':')[1])}"
                fl31.append(f)

        da['FL.'] = fl31

        for q in list(da['GAP']):
            try:
                if len(str(q.split('.')[1])) != 3:
                    missing = 3 - len(str(q.split('.')[1]))
                    ttt = f"{str(q.split('.')[1])}{str(0)*missing}"
                    t = f"{str(q.split('.')[0])}.{ttt}"
                    gap31.append(t)
                else:
                    t = f"{str(q.split('.')[0])}.{str(q.split('.')[1])}"
                    gap31.append(t)
            except:
                if q == 'DNF':
                    gap31.append('DNF')
                elif q == 'None':
                    gap31.append('None')

        da['GAP'] = gap31

        for q in list(da['INTERVAL']):
            if list(da['INTERVAL']).index(q) == 0:
                interval31.append(q)
            elif q == 'DNF':
                interval31.append('DNF')
            elif q == 'None':
                interval31.append('None')
            else:
                try:
                    if len(str(q.split('.')[1])) != 3:
                        missing = 3 - len(str(q.split('.')[1]))
                        ttt = f"{str(q.split('.')[1])}{str(0)*missing}"
                        t = f"{str(q.split('.')[0])}.{ttt}"
                        interval31.append(t)
                    else:
                        t = f"{str(q.split('.')[0])}.{str(q.split('.')[1])}"
                        interval31.append(t)
                except:
                    interval31.append(q)
                
        da['INTERVAL'] = interval31
    
    else:
        fl31, gap31, interval31 = [], [], []
        
        for i in list(da['FL.']):
            if len(str(i.split(':')[1])) != 6:
                missing = 6 - len(str(i.split(':')[1]))
                fff = f"{str(i.split(':')[1])}{str(0)*missing}"
                f = f"{str(i.split(':')[0])}:{fff}"
                fl31.append(f)
            else:
                f = f"{str(i.split(':')[0])}:{str(i.split(':')[1])}"
                fl31.append(f)

        da['FL.'] = fl31
        
        for q in list(da['GAP']):
            try:
                if len(str(q.split('.')[1])) != 3:
                    missing = 3 - len(str(q.split('.')[1]))
                    ttt = f"{str(q.split('.')[1])}{str(0)*missing}"
                    t = f"{str(q.split('.')[0])}.{ttt}"
                    gap31.append(t)
                else:
                    t = f"{str(q.split('.')[0])}.{str(q.split('.')[1])}"
                    gap31.append(t)
            except:
                gap31.append('FASTEST')

        da['GAP'] = gap31

    return da

# # #

def FP(circuit,tireset,stage,session,weather):
    data,tirenamedata,tireleftdata,c = pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),1
    for driver in drivers:
        if W1 == 'Dry':
            tlist = []
            for i in tireset[driver.name]:
                tlist.append(i)
        elif W1 == 'Dump':
            tlist = [inter,inter,inter]
        elif W1 == 'Wet':
            tlist = [w,w,w]
        tire = tlist[0]
        tire_usage = 0
        lap_chart, tire_chart, tire_left_chart = [], [], []
        for lap in range(1,circuit.circuit_laps+1):
            tire_left = tire.tire_left(driver,circuit,tire_usage)
            current_laptime = round(tire.laptime(driver,circuit,lap,tire_usage,['friday',0]),3)
            if tire_left < 25:
                if len(tlist) == 1:
                    lap_chart.append(current_laptime)
                    tire_chart.append(tire.title[0])
                    tire_usage += 1
                    tire_left_chart.append(f'{tire.title[0]} %{tire_left}')
                else:
                    if lap + 7 > circuit.circuit_laps+1:
                        lap_chart.append(current_laptime)
                        tire_chart.append(tire.title[0])
                        tire_usage += 1
                        tire_left_chart.append(f'{tire.title[0]} %{tire_left}')
                    else:
                        tire_usage = 0
                        tire_left_chart.append(f'{tire.title[0]} %{tire_left}')
                        tlist.pop(0)
                        tire = tlist[0]
                        pit_stop = 2.0
                        lap_chart.append(current_laptime + pit_stop + 20)
                        tire_chart.append(tire.title[0])
                        tire_usage += 1
            else:
                lap_chart.append(current_laptime)
                tire_chart.append(tire.title[0])
                tire_usage += 1
                tire_left_chart.append(f'{tire.title[0]} %{tire_left}')
        c += 1
        data[driver.name], tirenamedata[driver.name], tireleftdata[driver.name] = lap_chart, tire_chart, tire_left_chart
        
        if W1 == 'Dry':
            if stage == 1:
                FP1RESULT[driver.name] = sum(lap_chart)
            elif stage == 2:
                FP2RESULT[driver.name] = sum(lap_chart)
            elif stage == 3:
                FP3RESULT[driver.name] = sum(lap_chart)
        else:
            if stage == 1:
                FP1RESULT[driver.name] = uniform(0,10)
            elif stage == 2:
                FP2RESULT[driver.name] = uniform(6,12)
            elif stage == 3:
                FP3RESULT[driver.name] = uniform(9,18)           

    # End of the Free Practice Session
    print(f'{session} Session | {weather} Conditions | {CRC.location} Grand Prix — {CRC.country}')
    print(ANALYZER(None,data,tirenamedata,'quali-chart'))
    
    if verbosity == True:
        KW = session.lower().split(' ')
        data.to_excel(f'report-{circuit.location.lower()}-gp-{KW[0][0]}{KW[1][0]}{KW[2][0]}-chart.xlsx')
        tireleftdata.to_excel(f'report-{circuit.location.lower()}-gp-{KW[0][0]}{KW[1][0]}{KW[2][0]}-tire.xlsx')

# # #

def Q(circuit,session,weather):
    data,tirenamedata = pd.DataFrame(),pd.DataFrame()
    c = 0
    while c < 3:
        tempdata, temptirenamedata = pd.DataFrame(), pd.DataFrame()
        for driver in drivers:
            if W2 == 'Dry':
                tlist = [s]
            elif W2 == 'Dump':
                tlist = [inter]
            elif W2 == 'Wet':
                tlist = [w]
            tire = tlist[0]
            tire_usage = 0
            lap_chart, tire_chart = [], []
            for lap in range(circuit.circuit_laps,circuit.circuit_laps+1):
                tire_left = tire.tire_left(driver,circuit,tire_usage)

                # track adaptation.
                folks0 = round(((0.499) - (((driver.adaptability)*((333) + (100-driver.adaptability)))/100000) + ((100-driver.adaptability)/100)),3)
                folks1 = round(((0.499) - (((driver.adaptability)*((333) + (100-driver.adaptability)))/100000) + ((100-driver.adaptability)/499)),3)

                if c == 0:
                    current_laptime = round(tire.laptime(driver,circuit,lap,tire_usage,['saturday',0]) + (folks0),3)
                elif c == 1:
                    current_laptime = round(tire.laptime(driver,circuit,lap,tire_usage,['saturday',0]) + (folks1),3)
                else:
                    current_laptime = round(tire.laptime(driver,circuit,lap,tire_usage,['saturday',0]) + (0.000),3)

                DO_NOT_FINISHED = (((((((((((driver.team.reliability + driver.team.powertrain.durability)/2))+(driver.team.powertrain.fuel.vulnerability))*(-1.0))**3)/60000)+17))/1.7)**3) > uniform(0,75000)
                
                if W3 == 'Dump':
                    driver_error_odd = (((((((driver.fitness*(-1.0))**3)/60000)+17))/1.7)**3) > uniform(0,67500)
                    driver_error_odd_2 = (((((((driver.consistency*(-1.0))**3)/60000)+17))/1.7)**3) > uniform(0,52500)
                elif W3 == 'Wet':
                    driver_error_odd = (((((((driver.fitness*(-1.0))**3)/60000)+17))/1.7)**3) > uniform(0,62500)
                    driver_error_odd_2 = (((((((driver.consistency*(-1.0))**3)/60000)+17))/1.7)**3) > uniform(0,50000)
                elif W3 == 'Dry':
                    driver_error_odd = (((((((driver.fitness*(-1.0))**3)/60000)+17))/1.7)**3) > uniform(0,75000)
                    driver_error_odd_2 = (((((((driver.consistency*(-1.0))**3)/60000)+17))/1.7)**3) > uniform(0,57500)
                
                if len(DNF[driver.name]) > 1:
                    lap_chart.append(499.999)
                    tire_chart.append(tire.title[0])
                    tire_usage += 0
                else:
                    if DO_NOT_FINISHED == True:
                        print(f'DNF | Fast Lap {c+1} | {driver.name} has forced to retire due to {choice(FAILURES)} issue. Disaster for {driver.team.title}!')
                        lap_chart.append(499.999)
                        tire_chart.append(tire.title[0])
                        tire_usage += 0
                        DNF[driver.name].append(True)
                    elif driver_error_odd == True:
                        print(f'DNF | Fast Lap {c+1} | {driver.name} {choice(ERRORS)} and, he is OUT! Disaster for {driver.team.title}!')
                        lap_chart.append(499.999)
                        tire_chart.append(tire.title[0])
                        tire_usage += 0
                        DNF[driver.name].append(True)
                    else:
                        if tire_left < 25:
                            if len(tlist) == 1:
                                lap_chart.append(current_laptime)
                                tire_chart.append(tire.title[0])
                                tire_usage += 1
                            else:
                                tire_usage = 0
                                tlist.pop(0)
                                tire = tlist[0]
                                pit_stop = round(driver.team.crew.PIT(),3)
                                lap_chart.append(current_laptime + pit_stop + 20)
                                tire_chart.append(tire.title[0])
                                tire_usage += 1
                        else:
                            if driver_error_odd_2:
                                print(f'INC | Fast Lap {c+1} | Oh, no! {driver.name} has spun-round. He has lost couple seconds.')
                                lap_chart.append(current_laptime + 12.5)
                                tire_chart.append(tire.title[0])
                                tire_usage += 5
                            else:
                                lap_chart.append(current_laptime)
                                tire_chart.append(tire.title[0])
                                tire_usage += 1
            tempdata[driver.name], temptirenamedata[driver.name] = lap_chart, tire_chart
        data = pd.concat([data, tempdata],ignore_index=True)
        tirenamedata = pd.concat([tirenamedata, temptirenamedata],ignore_index=True)
        c += 1
    
    # End of the Qualifying
    print(f'{session} Session | {weather} Conditions | {CRC.location} Grand Prix — {CRC.country}')
    QUALI_CLASSIFICATION = ANALYZER('Qualifying',data,tirenamedata,'quali-chart')
    print(QUALI_CLASSIFICATION)

    # FL Correction
    fls_, dls_ = list(QUALI_CLASSIFICATION['FL.']), []
    for i in fls_:
        i = i.split(':')
        try:
            damn = float(i[0])*60 + float(i[1])
        except:
            damn = 10000.00000
        dls_.append(damn)
    print(f'\nPole Position | {list(QUALI_CLASSIFICATION["DRIVERS"])[dls_.index(min(dls_))]} has clinched the pole position with {fls_[dls_.index(min(dls_))]} in {W2.lower()} conditions.')

# # #
def R(circuit,session,weather):
    
    if verbosity == True:
        racereportfile = open(f'report-full-{GP.lower()}-gp.txt','a',encoding='UTF-8')
    
    BONUS = {}
    for i in drivers:
        BONUS[i.name] = []
    data,tirenamedata,tireperformancedata = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    for lap in range(1,circuit.circuit_laps+1):
        
        if SAFETY_CAR[lap][-1] == 1:
            print(f'{Fore.YELLOW}SFC | Lap {lap} | Safety Car Is Out! Yellow Flags Waving Around the Track.{Style.RESET_ALL}')
        else:
            pass
        
        for driver in drivers:
            tire = TIRE_SETS[driver.name][0]
            tire_left = tire.tire_left(driver,circuit,TIRE_USAGE[driver.name])
            
            current_laptime = round(tire.laptime(driver,circuit,lap,TIRE_USAGE[driver.name],['sunday',GRID[driver.name]]),3)
            DO_NOT_FINISHED = (((((((((((driver.team.reliability + driver.team.powertrain.durability)/2))+(driver.team.powertrain.fuel.vulnerability))*(-1.0))**3)/60000)+17))/1.7)**3) > uniform(0,75000)
            
            if W3 == 'Dump':
                driver_error_odd = (((((((driver.fitness*(-1.0))**3)/60000)+17))/1.7)**3) > uniform(0,67500)
                driver_error_odd_2 = (((((((driver.consistency*(-1.0))**3)/60000)+17))/1.7)**3) > uniform(0,52500)
            elif W3 == 'Wet':
                driver_error_odd = (((((((driver.fitness*(-1.0))**3)/60000)+17))/1.7)**3) > uniform(0,62500)
                driver_error_odd_2 = (((((((driver.consistency*(-1.0))**3)/60000)+17))/1.7)**3) > uniform(0,50000)
            elif W3 == 'Dry':
                driver_error_odd = (((((((driver.fitness*(-1.0))**3)/60000)+17))/1.7)**3) > uniform(0,75000)
                driver_error_odd_2 = (((((((driver.consistency*(-1.0))**3)/60000)+17))/1.7)**3) > uniform(0,57500)

            if len(DNF[driver.name]) > 1:
                LAP_CHART[driver.name].append((round(circuit.laptime + 225,3)))
                TIRE_CHART[driver.name].append(tire.title[0])
                TIRE_USAGE[driver.name] += 0
                TIRE_LEFT[driver.name].append(f'{tire.title[0]} %{tire_left}')

            elif SAFETY_CAR[lap][-1] == 1:
                z = 4
                if tire.title[0] == 'S':
                    pit_intervalx = [circuit.tire_series[0] - z, circuit.tire_series[0] + z]
                elif tire.title[0] == 'M':
                    pit_intervalx = [circuit.tire_series[1] - z, circuit.tire_series[1] + z]
                else:
                    pit_intervalx = [circuit.tire_series[2] - z, circuit.tire_series[2] + z]

                if len(BOX[driver.name]) > 1:
                    if len(TIRE_SETS[driver.name]) == 1:
                        print(f'{Fore.RED}DNF | Lap {lap} | {driver.name} has forced to retire due to severe damage issue. Disaster for {driver.team.title}!{Style.RESET_ALL}')
                        LAP_CHART[driver.name].append((circuit.laptime + 225)*2)
                        TIRE_CHART[driver.name].append(tire.title[0])
                        TIRE_USAGE[driver.name] += 0
                        TIRE_LEFT[driver.name].append(f'{tire.title[0]} %{tire_left}')
                    else:
                        TIRE_USAGE[driver.name] = 0
                        TIRE_SETS[driver.name].pop(0)
                        tire = TIRE_SETS[driver.name][0]
                        STINT[driver.name].append(f'-{tire.title[0]}')
                        pit_stop = round(driver.team.pit() + 6.5,3)

                        if sum(PENALTY[driver.name]) != 0:
                            gabigol = sum(PENALTY[driver.name])
                            pit_stop += sum(PENALTY[driver.name])
                            PENALTY[driver.name].clear()
                            PENALTY[driver.name].append(0)
                            print(f'PIT | Lap {lap} | Pit-stop for {driver.name} but, he has to pay-off his {gabigol} second penalty first. Pit-crew is waiting along.')
                        else:
                            gabigol = 0

                        PIT[driver.name].append(1)
                        print(f'PIT | Lap {lap} | Pit-stop for {driver.name} with {round(pit_stop - gabigol,3)} seconds stationary. He is on {tire.title} compound.')
                        LAP_CHART[driver.name].append((round(circuit.laptime + 125,3)) + pit_stop + 14)
                        TIRE_CHART[driver.name].append(tire.title[0])
                        TIRE_LEFT[driver.name].append(f'{tire.title[0]} %{tire_left}')
                        BOX[driver.name].clear()
                        BOX[driver.name].append(None)
                elif pit_intervalx[1] >= TIRE_USAGE[driver.name] >= pit_intervalx[0]:
                    if len(TIRE_SETS[driver.name]) == 1:
                        LAP_CHART[driver.name].append((round(circuit.laptime + 125,3)))
                        TIRE_CHART[driver.name].append(tire.title[0])
                        TIRE_USAGE[driver.name] += 0.175
                        TIRE_LEFT[driver.name].append(f'{tire.title[0]} %{tire_left}')
                    else:
                        if lap + 7 > circuit.circuit_laps+1:
                            LAP_CHART[driver.name].append((round(circuit.laptime + 125,3)))
                            TIRE_CHART[driver.name].append(tire.title[0])
                            TIRE_USAGE[driver.name] += 0.175
                            TIRE_LEFT[driver.name].append(f'{tire.title[0]} %{tire_left}')
                        else:
                            TIRE_USAGE[driver.name] = 0
                            TIRE_SETS[driver.name].pop(0)
                            tire = TIRE_SETS[driver.name][0]
                            STINT[driver.name].append(f'-{tire.title[0]}')
                            pit_stop = round(driver.team.pit(),3)

                            if sum(PENALTY[driver.name]) != 0:
                                gabigol = sum(PENALTY[driver.name])
                                pit_stop += sum(PENALTY[driver.name])
                                PENALTY[driver.name].clear()
                                PENALTY[driver.name].append(0)
                                print(f'PIT | Lap {lap} | Pit-stop for {driver.name} but, he has to pay-off his {gabigol} second penalty first. Pit-crew is waiting along.')
                            else:
                                gabigol = 0
                        
                            PIT[driver.name].append(1)
                            KTM = round(pit_stop - gabigol,3)
                            if 10 > KTM >= 5.0:
                                print(f'PIT | Lap {lap} | Bad news for {driver.name} with {KTM} seconds stationary. He is on {tire.title} compound.')
                            elif KTM >= 10:
                                print(f'PIT | Lap {lap} | Disaster for {driver.name} with {KTM} seconds stationary. He is on {tire.title} compound.')
                            else:
                                print(f'PIT | Lap {lap} | Pit-stop for {driver.name} with {KTM} seconds stationary. He is on {tire.title} compound.')
                            LAP_CHART[driver.name].append((round(circuit.laptime + 125,3)) + pit_stop + 14) # Pitted Lap
                            TIRE_CHART[driver.name].append(tire.title[0])
                            TIRE_USAGE[driver.name] += 0.175
                            TIRE_LEFT[driver.name].append(f'{tire.title[0]} %{tire_left}')
                else:
                    LAP_CHART[driver.name].append((round(circuit.laptime + 125,3)))
                    TIRE_CHART[driver.name].append(tire.title[0])
                    TIRE_USAGE[driver.name] += 0.175
                    TIRE_LEFT[driver.name].append(f'{tire.title[0]} %{tire_left}')
            else:
                if DO_NOT_FINISHED == True:
                    the_odd = uniform(0.1,100.1)
                    if the_odd < 25.1:
                        print(f'{Fore.LIGHTRED_EX}INC | Lap {lap} | {driver.name} has an issue. He has lost the {choice(MECHANICALS)}! Disaster for {driver.team.title}!{Style.RESET_ALL}')
                        LAP_CHART[driver.name].append(current_laptime)
                        TIRE_CHART[driver.name].append(tire.title[0])
                        TIRE_USAGE[driver.name] += 1
                        TIRE_LEFT[driver.name].append(f'{tire.title[0]} %{tire_left}')
                        MECHANICAL[driver.name].append(True)
                    else:
                        print(f'{Fore.RED}DNF | Lap {lap} | {driver.name} has forced to retire due to {choice(FAILURES)} issue. Disaster for {driver.team.title}!{Style.RESET_ALL}')
                        LAP_CHART[driver.name].append((circuit.laptime + 225)*2)
                        TIRE_CHART[driver.name].append(tire.title[0])
                        TIRE_USAGE[driver.name] += 0
                        TIRE_LEFT[driver.name].append(f'{tire.title[0]} %{tire_left}')

                        if uniform(0.01,100.01) < 20.01:
                            SAFETY_CAR[lap+1].append(1)
                            SAFETY_CAR[lap+2].append(1)
                            SAFETY_CAR[lap+3].append(1)
                            SAFETY_CAR[lap+4].append(1)
                        else:
                            pass

                        DNF[driver.name].append(True)
                elif driver_error_odd == True:
                    kachow = uniform(0.1,100.1)
                    if kachow > 35.5:
                        print(f'{Fore.RED}DNF | Lap {lap} | {driver.name} {choice(ERRORS)} and, he is OUT! Disaster for {driver.team.title}!{Style.RESET_ALL}')
                        LAP_CHART[driver.name].append((circuit.laptime + 225)*2)
                        TIRE_CHART[driver.name].append(tire.title[0])
                        TIRE_USAGE[driver.name] += 0
                        TIRE_LEFT[driver.name].append(f'{tire.title[0]} %{tire_left}')

                        if uniform(0.01,100.01) < 20.01:
                            SAFETY_CAR[lap+1].append(1)
                            SAFETY_CAR[lap+2].append(1)
                            SAFETY_CAR[lap+3].append(1)
                            SAFETY_CAR[lap+4].append(1)
                        else:
                            pass
                        
                        DNF[driver.name].append(True)
                    else:
                        TIRE_USAGE[driver.name] += 5
                        TIRE_LEFT[driver.name].append(f'{tire.title[0]} %{tire_left}')
                        LAP_CHART[driver.name].append(current_laptime + uniform(19.01,39.99))
                        TIRE_CHART[driver.name].append(tire.title[0])
                        TIRE_SETS[driver.name].append(s)
                        print(f'{Fore.LIGHTRED_EX}INC | Lap {lap} | Oh, no! {driver.name} has lost control and crushed into his front-wing. He is willing to box!{Style.RESET_ALL}')                        
                        BOX[driver.name].append(True)
                else:
                    if len(BOX[driver.name]) > 1:
                        if len(TIRE_SETS[driver.name]) == 1:
                            print(f'{Fore.RED}DNF | Lap {lap} | {driver.name} has forced to retire due to severe damage issue. Disaster for {driver.team.title}!{Style.RESET_ALL}')
                            LAP_CHART[driver.name].append((circuit.laptime + 225)*2)
                            TIRE_CHART[driver.name].append(tire.title[0])
                            TIRE_USAGE[driver.name] += 0
                            TIRE_LEFT[driver.name].append(f'{tire.title[0]} %{tire_left}')
                        else:
                            TIRE_USAGE[driver.name] = 0
                            TIRE_SETS[driver.name].pop(0)
                            tire = TIRE_SETS[driver.name][0]
                            STINT[driver.name].append(f'-{tire.title[0]}')
                            pit_stop = round(driver.team.pit() + 6.5,3)

                            if sum(PENALTY[driver.name]) != 0:
                                gabigol = sum(PENALTY[driver.name])
                                pit_stop += sum(PENALTY[driver.name])
                                PENALTY[driver.name].clear()
                                PENALTY[driver.name].append(0)
                                print(f'PIT | Lap {lap} | Pit-stop for {driver.name} but, he has to pay-off his {gabigol} second penalty first. Pit-crew is waiting along.')
                            else:
                                gabigol = 0

                            PIT[driver.name].append(1)
                            print(f'PIT | Lap {lap} | Pit-stop for {driver.name} with {round(pit_stop - gabigol,3)} seconds stationary. He is on {tire.title} compound.')
                            LAP_CHART[driver.name].append(current_laptime + pit_stop + 20)
                            TIRE_CHART[driver.name].append(tire.title[0])
                            TIRE_USAGE[driver.name] += 1
                            TIRE_LEFT[driver.name].append(f'{tire.title[0]} %{tire_left}')
                            BOX[driver.name].clear()
                            BOX[driver.name].append(None)
                    elif tire_left < 25:
                        if len(TIRE_SETS[driver.name]) == 1:
                            LAP_CHART[driver.name].append(current_laptime)
                            TIRE_CHART[driver.name].append(tire.title[0])
                            TIRE_USAGE[driver.name] += 1
                            TIRE_LEFT[driver.name].append(f'{tire.title[0]} %{tire_left}')
                        else:
                            if lap + 7 > circuit.circuit_laps+1:
                                LAP_CHART[driver.name].append(current_laptime)
                                TIRE_CHART[driver.name].append(tire.title[0])
                                TIRE_USAGE[driver.name] += 1
                                TIRE_LEFT[driver.name].append(f'{tire.title[0]} %{tire_left}')
                            else:
                                TIRE_USAGE[driver.name] = 0
                                TIRE_SETS[driver.name].pop(0)
                                tire = TIRE_SETS[driver.name][0]
                                STINT[driver.name].append(f'-{tire.title[0]}')
                                pit_stop = round(driver.team.pit(),3)

                                if sum(PENALTY[driver.name]) != 0:
                                    gabigol = sum(PENALTY[driver.name])
                                    pit_stop += sum(PENALTY[driver.name])
                                    PENALTY[driver.name].clear()
                                    PENALTY[driver.name].append(0)
                                    print(f'PIT | Lap {lap} | Pit-stop for {driver.name} but, he has to pay-off his {gabigol} second penalty first. Pit-crew is waiting along.')
                                else:
                                    gabigol = 0
                            
                                PIT[driver.name].append(1)
                                KTM = round(pit_stop - gabigol,3)
                                if 10 > KTM >= 5.0:
                                    print(f'PIT | Lap {lap} | Bad news for {driver.name} with {KTM} seconds stationary. He is on {tire.title} compound.')
                                elif KTM >= 10:
                                    print(f'PIT | Lap {lap} | Disaster for {driver.name} with {KTM} seconds stationary. He is on {tire.title} compound.')
                                else:
                                    print(f'PIT | Lap {lap} | Pit-stop for {driver.name} with {KTM} seconds stationary. He is on {tire.title} compound.')
                                LAP_CHART[driver.name].append(current_laptime + pit_stop + 20)
                                TIRE_CHART[driver.name].append(tire.title[0])
                                TIRE_USAGE[driver.name] += 1
                                TIRE_LEFT[driver.name].append(f'{tire.title[0]} %{tire_left}')
                    else:
                        if driver_error_odd_2:
                            ickx = uniform(6.501,16.501)
                            print(f'{Fore.LIGHTRED_EX}INC | Lap {lap} | Oh, no! {driver.name} has spun-round. He has lost {round(ickx,3)} seconds.{Style.RESET_ALL}')
                            LAP_CHART[driver.name].append(current_laptime + ickx)
                            TIRE_CHART[driver.name].append(tire.title[0])
                            if W3 != 'Dry':
                                TIRE_USAGE[driver.name] += 0.332
                                TIRE_LEFT[driver.name].append(f'{tire.title[0]} %{tire_left}')
                            else:
                                TIRE_USAGE[driver.name] += 3.332
                                TIRE_LEFT[driver.name].append(f'{tire.title[0]} %{tire_left}')
                        else:
                            if lap + 2 == circuit.circuit_laps:
                                if FIA(current)[10] == True:
                                    if AHEAD[driver.name][-1] >= 24.0 + uniform(0.50,1.00):
                                        TIRE_USAGE[driver.name] = 0
                                        TIRE_SETS[driver.name].pop(0)
                                        tire = TIRE_SETS[driver.name][0]
                                        STINT[driver.name].append(f'-{tire.title[0]}')
                                        pit_stop = round(driver.team.pit(),3)
                                        PIT[driver.name].append(1)
                                        print(f'PIT | Lap {lap} | {driver.name} is gonna attempt the fastest lap! He is in the pits, willing to switch into the {tire.title} compound.')
                                        if 10 > pit_stop >= 5.0:
                                            print(f'PIT | Lap {lap} | Bad news for {driver.name} with {pit_stop} seconds stationary. He is on {tire.title} compound.')
                                        elif pit_stop >= 10:
                                            print(f'PIT | Lap {lap} | Disaster for {driver.name} with {pit_stop} seconds stationary. He is on {tire.title} compound.')
                                        else:
                                            print(f'PIT | Lap {lap} | Pit-stop for {driver.name} with {pit_stop} seconds stationary. He is on {tire.title} compound.')
                                        LAP_CHART[driver.name].append(current_laptime + pit_stop + 20)
                                        TIRE_CHART[driver.name].append(tire.title[0])
                                        TIRE_USAGE[driver.name] += 1
                                        TIRE_LEFT[driver.name].append(f'{tire.title[0]} %{tire_left}')
                                    else:
                                        LAP_CHART[driver.name].append(current_laptime)
                                        TIRE_CHART[driver.name].append(tire.title[0])
                                        TIRE_USAGE[driver.name] += 1
                                        TIRE_LEFT[driver.name].append(f'{tire.title[0]} %{tire_left}')                       
                                else:
                                    LAP_CHART[driver.name].append(current_laptime)
                                    TIRE_CHART[driver.name].append(tire.title[0])
                                    TIRE_USAGE[driver.name] += 1
                                    TIRE_LEFT[driver.name].append(f'{tire.title[0]} %{tire_left}')
                            elif uniform(0.01,100.01) <= ((100-driver.fitness)/125):
                                LAP_CHART[driver.name].append(current_laptime - 0.325)
                                TIRE_CHART[driver.name].append(tire.title[0])
                                TIRE_USAGE[driver.name] += 1
                                TIRE_LEFT[driver.name].append(f'{tire.title[0]} %{tire_left}')
                                PENALTY[driver.name].append(5)
                                print(f'{Fore.CYAN}PEN | Lap {lap} | 5 secs. penalty to {driver.name} for the excessive amount of corner-cutting. {Style.RESET_ALL}')
                            else:
                                LAP_CHART[driver.name].append(current_laptime)
                                TIRE_CHART[driver.name].append(tire.title[0])
                                TIRE_USAGE[driver.name] += 1
                                TIRE_LEFT[driver.name].append(f'{tire.title[0]} %{tire_left}')

            # Mechanical Error
            if SAFETY_CAR[lap][-1] == 1:
                pass
            else:
                if len(MECHANICAL[driver.name]) > 0:
                    LAP_CHART[driver.name][-1] +=  + uniform(1.499,2.999)
                else:
                    pass
        
        if SAFETY_CAR[lap][-1] == 1: # If there is safety car, there will be no pass.
            if SAFETY_CAR[lap+2][-1] != 1: # If there is a safety car scenario, cars has to be lining behind the safety car.
                # Lap by Lap Report for Safety Car
                temp, temptirenamedata = pd.DataFrame(), pd.DataFrame()
                for driver in drivers:
                    temp[driver.name], temptirenamedata[driver.name] = LAP_CHART[driver.name], TIRE_CHART[driver.name]
                TEMP_CLASSIFICATION = ANALYZER(f'LAP {lap} | Race',temp,temptirenamedata,'race-chart')

                driver_names = []
                interval_values = []
                for f,j in zip(list(TEMP_CLASSIFICATION['DRIVERS']),list(TEMP_CLASSIFICATION['INTERVAL'])):
                    try:
                        dolores = float(j[1:]) + 1 - 1
                    except:
                        dolores = circuit.laptime + 125
                    driver_names.append(f)
                    interval_values.append(dolores)

                for j,i in zip(driver_names,interval_values):
                    attacker = j
                    interval = i
                    position = (driver_names.index(attacker)) + 1
                    
                    for L in drivers:
                        if L.name == attacker:
                            attacker_obj = L
                    for K in drivers:
                        if K.name == defender:
                            defender_obj = K
                    
                    following_distance = (0.333)*(position-1)

                    if position == 1:
                        LAP_CHART[attacker_obj.name][-1] = LAP_CHART[attacker_obj.name][-1] + (circuit.laptime + 125)
                    elif len(DNF[attacker]) > 1:
                        LAP_CHART[attacker_obj.name][-1] +=  (circuit.laptime + 125)
                    else:
                        if interval > following_distance:
                            # run faster, catch the que.
                            LAP_CHART[attacker_obj.name][-1] = LAP_CHART[attacker_obj.name][-1] - (interval - following_distance) + (circuit.laptime + 125)
                        else:
                            # slow, slow, slow
                            LAP_CHART[attacker_obj.name][-1] = LAP_CHART[attacker_obj.name][-1] + (following_distance - interval) + (circuit.laptime + 125)
            else:
                pass
        else:
            # Lap by Lap Analysis for Overtaking/Defence Situations
            temp, temptirenamedata = pd.DataFrame(), pd.DataFrame()
            for driver in drivers:
                temp[driver.name], temptirenamedata[driver.name] = LAP_CHART[driver.name], TIRE_CHART[driver.name]
            TEMP_CLASSIFICATION = ANALYZER(f'LAP {lap} | Race',temp,temptirenamedata,'race-chart')

            fls_, dls_ = list(TEMP_CLASSIFICATION['FL.']), []
            pilots = list(TEMP_CLASSIFICATION['DRIVERS'])
            deltas = list(TEMP_CLASSIFICATION['GAP'])

            driver_names = []
            attack_gap = []
            for f,j in zip(pilots,deltas):
                try:
                    dolores = float(j[1:]) + 1 - 1
                except:
                    dolores = 10000.00000       
                driver_names.append(f)
                attack_gap.append(dolores)

            for j,i in zip(driver_names,attack_gap):
                attacker = j
                defender = driver_names[driver_names.index(j)-1]
                gap_in_front = i

                for L in drivers:
                    if L.name == attacker:
                        attacker_obj = L

                for K in drivers:
                    if K.name == defender:
                        defender_obj = K
                
                ACCIDENT = abs((uniform(0,25) + attacker_obj.attack) - (uniform(0,25) + defender_obj.defence))
                
                if lap == 1:
                    BANGER = (uniform(0,100) <= 32.5)
                else:
                    BANGER = (uniform(0,100) <= 7.5)

                if (ACCIDENT <= (attacker_obj.aggression/200) + (defender_obj.aggression/200)) and (BANGER) and (gap_in_front < 1.0):
                    INCIDENT = choice(['DOUBLE DNF','DEFENDER DNF & ATTACKER DAMAGED','ATTACKER DNF & DEFENDER DAMAGED'
                                    'DOUBLE DAMAGED','DEFENDER CLEAR & ATTACKER DAMAGED','ATTACKER CLEAR & DEFENDER DAMAGED',
                                    'DEFENDER DNF & ATTACKER CLEAR','ATTACKER DNF & DEFENDER CLEAR'])
                    
                    PENALTY_ODDS = choice(['ATTACKER ONLY','DEFENDER ONLY',None])
                    
                    if INCIDENT == 'DOUBLE DNF':
                        print(f'{Fore.MAGENTA}INC | Lap {lap} | OOOHHH! {attacker} and {defender} GOT COLLIDED! THEY ARE BOTH OUT!.{Style.RESET_ALL}')
                        BONUS[attacker].append((circuit.laptime + 5)*2)
                        BONUS[defender].append((circuit.laptime + 5)*2)
                        DNF[attacker].append(True)
                        DNF[defender].append(True)
                        SAFETY_CAR[lap+1].append(1)
                        SAFETY_CAR[lap+2].append(1)
                        SAFETY_CAR[lap+3].append(1)
                        SAFETY_CAR[lap+4].append(1)
                    elif INCIDENT == 'DEFENDER DNF & ATTACKER DAMAGED':
                        print(f'{Fore.MAGENTA}INC | Lap {lap} | OOOHHH! {attacker} and {defender} GOT COLLIDED! {defender} IS OUT! {attacker} HAS DAMAGE!.{Style.RESET_ALL}')
                        BONUS[attacker].append(uniform(19.01,39.99))
                        BONUS[defender].append((circuit.laptime + 5)*2)
                        DNF[defender].append(True)
                        BOX[attacker].append(True)
                        SAFETY_CAR[lap+1].append(1)
                        SAFETY_CAR[lap+2].append(1)
                        SAFETY_CAR[lap+3].append(1)
                        SAFETY_CAR[lap+4].append(1)
                    elif INCIDENT == 'ATTACKER DNF & DEFENDER DAMAGED':
                        print(f'{Fore.MAGENTA}INC | Lap {lap} | OOOHHH! {attacker} and {defender} GOT COLLIDED! {attacker} IS OUT! {defender} HAS DAMAGE!.{Style.RESET_ALL}')
                        BONUS[attacker].append((circuit.laptime + 5)*2)
                        BONUS[defender].append(uniform(19.01,39.99))
                        DNF[attacker].append(True)
                        BOX[defender].append(True)
                        SAFETY_CAR[lap+1].append(1)
                        SAFETY_CAR[lap+2].append(1)
                        SAFETY_CAR[lap+3].append(1)
                        SAFETY_CAR[lap+4].append(1)
                    elif INCIDENT == 'DOUBLE DAMAGED':
                        print(f'{Fore.MAGENTA}INC | Lap {lap} | OOOHHH! {attacker} and {defender} GOT COLLIDED! THEY BOTH HAS DAMAGE!.{Style.RESET_ALL}')
                        BONUS[attacker].append(uniform(19.01,39.99))
                        BONUS[defender].append(uniform(19.01,39.99))
                        BOX[attacker].append(True)
                        BOX[defender].append(True)

                        if uniform(0.1,100.1) > 0.40:
                            SAFETY_CAR[lap+1].append(1)
                            SAFETY_CAR[lap+2].append(1)
                            SAFETY_CAR[lap+3].append(1)
                            SAFETY_CAR[lap+4].append(1)

                    elif INCIDENT == 'DEFENDER CLEAR & ATTACKER DAMAGED':
                        print(f'{Fore.MAGENTA}INC | Lap {lap} | OOOHHH! {attacker} and {defender} GOT COLLIDED! {attacker} HAS DAMAGE BUT {defender} HAS NO! {attacker} IS BOXING!.{Style.RESET_ALL}')
                        BONUS[attacker].append(uniform(19.01,39.99))
                        BONUS[defender].append(uniform(0.09,5.91))
                        BOX[attacker].append(True)

                        if uniform(0.1,100.1) > 0.275:
                            SAFETY_CAR[lap+1].append(1)
                            SAFETY_CAR[lap+2].append(1)
                            SAFETY_CAR[lap+3].append(1)
                            SAFETY_CAR[lap+4].append(1)

                    elif INCIDENT == 'ATTACKER CLEAR & DEFENDER DAMAGED':
                        print(f'{Fore.MAGENTA}INC | Lap {lap} | OOOHHH! {attacker} and {defender} GOT COLLIDED! {defender} HAS DAMAGE BUT {attacker} HAS NO! {defender} IS BOXING!.{Style.RESET_ALL}')
                        BONUS[defender].append(uniform(19.01,39.99))
                        BONUS[attacker].append(uniform(0.09,5.91))
                        BOX[defender].append(True)

                        if uniform(0.1,100.1) > 0.275:
                            SAFETY_CAR[lap+1].append(1)
                            SAFETY_CAR[lap+2].append(1)
                            SAFETY_CAR[lap+3].append(1)
                            SAFETY_CAR[lap+4].append(1)
                            
                    elif INCIDENT == 'DEFENDER DNF & ATTACKER CLEAR':
                        print(f'{Fore.MAGENTA}INC | Lap {lap} | OOOHHH! {attacker} and {defender} GOT COLLIDED! {defender} IS OUT! {attacker} HAS NO DAMAGE!.{Style.RESET_ALL}')
                        BONUS[attacker].append(uniform(0.09,5.91))
                        BONUS[defender].append((circuit.laptime + 5)*2)
                        DNF[defender].append(True)
                        SAFETY_CAR[lap+1].append(1)
                        SAFETY_CAR[lap+2].append(1)
                        SAFETY_CAR[lap+3].append(1)
                        SAFETY_CAR[lap+4].append(1)
                    elif INCIDENT == 'ATTACKER DNF & DEFENDER CLEAR':
                        print(f'{Fore.MAGENTA}INC | Lap {lap} | OOOHHH! {attacker} and {defender} GOT COLLIDED! {attacker} IS OUT! {defender} HAS NO DAMAGE!.{Style.RESET_ALL}')
                        BONUS[defender].append(uniform(0.09,5.91))
                        BONUS[attacker].append((circuit.laptime + 5)*2)
                        DNF[attacker].append(True)
                        SAFETY_CAR[lap+1].append(1)
                        SAFETY_CAR[lap+2].append(1)
                        SAFETY_CAR[lap+3].append(1)
                        SAFETY_CAR[lap+4].append(1)
                    else:
                        print(f'{Fore.MAGENTA}INC | Lap {lap} | OOOHHH! {attacker} and {defender} GOT COLLIDED! THEY ARE BOTH OUT!.{Style.RESET_ALL}')
                        BONUS[attacker].append((circuit.laptime + 5)*2)
                        BONUS[defender].append((circuit.laptime + 5)*2)
                        DNF[attacker].append(True)
                        DNF[defender].append(True)
                        SAFETY_CAR[lap+1].append(1)
                        SAFETY_CAR[lap+2].append(1)
                        SAFETY_CAR[lap+3].append(1)
                        SAFETY_CAR[lap+4].append(1)

                    if PENALTY_ODDS == 'ATTACKER ONLY':
                        if len(DNF[attacker]) > 1:
                            pass
                        else:
                            thepen = choice([5,10,15,20])
                            print(f'{Fore.CYAN}PEN | Lap {lap} | {thepen} secs. penalty to {attacker} for the last incident. {Style.RESET_ALL}')
                            PENALTY[attacker].append(thepen)
                    elif PENALTY_ODDS == 'DEFENDER ONLY':
                        if len(DNF[defender]) > 1:
                            pass
                        else:
                            thepen = choice([5,10,15,20])
                            print(f'{Fore.CYAN}PEN | Lap {lap} | {thepen} secs. penalty to {defender} for the last incident. {Style.RESET_ALL}')
                            PENALTY[defender].append(thepen)
                    else:
                        pass

                else:
                    attacker_coming_by = LAP_CHART[attacker][-1] - LAP_CHART[defender][-1] # 0 ile 5 saniye arasında bir değerlendirme
                    attacker_tire_left = TIRE_LEFT[attacker][-1]
                    defender_tire_left = TIRE_LEFT[defender][-1]
                    attacker_tire = TIRE_CHART[attacker][-1]
                    defender_tire = TIRE_CHART[defender][-1]
                    the_gap_in_front = gap_in_front
                    minimum_delta_needed_d = FIA(current)[16]
                    
                    drs_advantage = (-1.0)*((0.250) + attacker_obj.team.drs_delta/200)
                    if circuit.overtake_difficulty == 'Very Hard':
                        minimum_delta_needed_t = 0.150
                    elif circuit.overtake_difficulty == 'Hard':
                        minimum_delta_needed_t = 0.200
                    elif circuit.overtake_difficulty == 'Average':
                        minimum_delta_needed_t = 0.250
                    elif circuit.overtake_difficulty == 'Easy':
                        minimum_delta_needed_t = 0.350
                    elif circuit.overtake_difficulty == 'Very Easy':
                        minimum_delta_needed_t = 0.500
                    elif circuit.overtake_difficulty == 'Impossible':
                        minimum_delta_needed_t = 0.100

                    """
                    if (FIA(current)[1] == True) and (circuit.drs_points >= choice([0,1,2,3,4])) and (lap > 1) and (W3 == 'Dry'):
                        if gap_in_front < 1.0:
                            BONUS[attacker].append(drs_advantage)
                            new_gap = gap_in_front + drs_advantage
                            if new_gap < 0:
                                BONUS[defender].append(0.125)
                            else:
                                if (uniform(0,100) < offset):
                                    if uniform(0,25) + attacker_obj.attack >= uniform(0,25) + defender_obj.defence:
                                        BONUS[attacker].append(0.200 + gap_in_front)
                                        BONUS[defender].append(0.800 + gap_in_front)
                                    else:
                                        BONUS[attacker].append(1.400 - gap_in_front)
                                        BONUS[defender].append(1.150 - gap_in_front)
                                else:
                                    BONUS[attacker].append(0.250 + ((100-attacker_obj.team.vortex)/50))
                        else:
                            pass
                    elif gap_in_front < 0.468:
                        if (uniform(0,100) < offset) and (((attacker_obj.attack/100)) > gap_in_front):
                            if uniform(0,25) + attacker_obj.attack >= uniform(0,25) + defender_obj.defence:
                                BONUS[attacker].append(0.200 + gap_in_front)
                                BONUS[defender].append(0.800 + gap_in_front)
                            else:
                                BONUS[attacker].append(1.400 - gap_in_front)
                                BONUS[defender].append(1.150 - gap_in_front)     
                        else:
                            BONUS[attacker].append(0.250 + ((100-attacker_obj.team.vortex)/50))
                    else:
                        BONUS[attacker].append(1.000 + ((100-attacker_obj.team.vortex)/50))
                    """

        # Lap by Lap Report | Final Shape
        temp, temptirenamedata = pd.DataFrame(), pd.DataFrame()
        for driver in drivers:
            temp[driver.name], temptirenamedata[driver.name] = LAP_CHART[driver.name], TIRE_CHART[driver.name]
        
        TEMP_INFO = f'{session} Session | {weather} Conditions | {CRC.location} Grand Prix — {CRC.country} | Lap {lap}/{CRC.circuit_laps}'
        TEMP_CLASSIFICATION = ANALYZER(f'LAP {lap} | Race',temp,temptirenamedata,'race-chart')

        # Position Saving
        dp = list(TEMP_CLASSIFICATION['DRIVERS'])
        for i in dp:
            ixxxxx = dp.index(i)
            POSITIONS[i].append(ixxxxx+1)

        # Gap Ahead Saving
        d9, d9_new = list(TEMP_CLASSIFICATION['GAP']), []

        for i in d9:
            try:
                ix = i.split('+')
                d9_new.append(float(ix[1]))
            except:
                d9_new.append(0.5)
        d9_new.append(0.5)

        for chaffeur in dp:
            ixxxxx = dp.index(chaffeur)
            gap_ahead = d9_new[ixxxxx+1]
            AHEAD[chaffeur].append(gap_ahead)
    

        fls_, dls_ = list(TEMP_CLASSIFICATION['FL.']), []
        for i in fls_:
            if len(i.split(':')) == 1:
                dls_.append(3600)
            else:
                dls_.append(float(i.split(':')[0])*60 + float(i.split(':')[1]))
        TEMP_FL_INFO = f'\nFastest Lap | {list(TEMP_CLASSIFICATION["DRIVERS"])[dls_.index(min(dls_))]} has recorded {fls_[dls_.index(min(dls_))]} on this track.'
        if verbosity == True:
            racereportfile.write(f'{TEMP_INFO}\n{TEMP_CLASSIFICATION}\n{TEMP_FL_INFO}\n{borderline}\n')
        # # # END OF THE LAP

    # # # END OF THE GP
    # Adding Penalties
    for i in drivers:
        LAP_CHART[i.name][-1] += sum(PENALTY[i.name])

    # Shaping the Results
    for driver in drivers:
        data[driver.name], tirenamedata[driver.name], tireperformancedata[driver.name] = LAP_CHART[driver.name], TIRE_CHART[driver.name], TIRE_LEFT[driver.name]

    if verbosity == True:
        KW = session.lower()
        data.to_excel(f'report-{circuit.location.lower()}-gp-{KW}-chart.xlsx')
        tireperformancedata.to_excel(f'report-{circuit.location.lower()}-gp-{KW}-tire.xlsx')
    
    print(borderline)
    print(f'{session} Session | {weather} Conditions | {CRC.location} Grand Prix — {CRC.country} | {CRC.circuit_laps} Laps')
    
    RACE_CLASSIFICATION = ANALYZER(f'Race',data,tirenamedata,'race-chart')

    # Penalty Correction
    penalties = []

    for i in RACE_CLASSIFICATION['DRIVERS'].to_list():
        if sum(PENALTY[i]) != 0:
            penalties.append(f'+{sum(PENALTY[i])} secs.')
        else:
            penalties.append(None)

    RACE_CLASSIFICATION['PENALTY'] = penalties
    RACE_CLASSIFICATION = RACE_CLASSIFICATION[['MANUFACTURERS','DRIVERS','INTERVAL','GAP','FL.','FL. LAP','FL. TIRE','PIT','PENALTY','GRID']]

    # Stint Correction
    stintsx = []

    for i in RACE_CLASSIFICATION['DRIVERS'].to_list():
        txtx = ''
        
        for q in STINT[i]:
            txtx += str(q)
        
        stintsx.append(txtx)
    
    RACE_CLASSIFICATION['STINT'] = stintsx
    RACE_CLASSIFICATION = RACE_CLASSIFICATION[['MANUFACTURERS','DRIVERS','INTERVAL','GAP','FL.','FL. LAP','FL. TIRE','STINT','PIT','PENALTY','GRID']]
    
    # Minor Bug Trade-Off
    i0 = list(RACE_CLASSIFICATION['INTERVAL'])
    i1 = list(RACE_CLASSIFICATION['GAP'])
    i0[0] = i1[0]
    i1[0] = 'GAP'

    RACE_CLASSIFICATION['INTERVAL'] = i0
    RACE_CLASSIFICATION['GAP'] = i1
    RACE_CLASSIFICATION = RACE_CLASSIFICATION[['MANUFACTURERS','DRIVERS','INTERVAL','GAP','FL.','FL. LAP','FL. TIRE','STINT','PIT','PENALTY','GRID']]
    print(RACE_CLASSIFICATION)
    
    # FL Correction
    fls_, dls_ = list(RACE_CLASSIFICATION['FL.']), []
    for i in fls_:
        if len(i.split(':')) == 1:
            dls_.append(3600)
        else:
            dls_.append(float(i.split(':')[0])*60 + float(i.split(':')[1]))
    print(f'\nFastest Lap | {list(RACE_CLASSIFICATION["DRIVERS"])[dls_.index(min(dls_))]} has recorded {fls_[dls_.index(min(dls_))]} on this track.')

# # # Control Room

if execution == 'simulation':
    # Strategy Preperations
    FP1STRATEGY, FP2STRATEGY, FP3STRATEGY = {}, {}, {}
    FP1RESULT, FP2RESULT, FP3RESULT = {}, {}, {}

    for i in drivers:
        FP1STRATEGY[i.name] = CRC.strategy[0]
        FP2STRATEGY[i.name] = CRC.strategy[1]
        FP3STRATEGY[i.name] = CRC.strategy[2]

    # Free Practice Sessions
    FP(CRC,FP1STRATEGY,1,'Free Practice 1',W1)
    print(borderline)
    FP(CRC,FP2STRATEGY,2,'Free Practice 2',W1)
    print(borderline)
    FP(CRC,FP3STRATEGY,3,'Free Practice 3',W1)
    print(borderline)

    # Dictionary Definitions
    DNF = {}

    for i in drivers:
        DNF[i.name] = [None]

    # Qualifying Session
    Q(CRC,'Qualifying',W2)
    print(borderline)

    # Dictionary Definitions
    DFORM = {}

    STRATEGIES = {}

    LAP_CHART = {}
    TIRE_CHART = {}
    TIRE_LEFT = {}

    TIRE_USAGE = {}
    TIRE_SETS = {}

    DNF = {}
    MECHANICAL = {}
    BOX = {}

    PENALTY = {}

    SAFETY_CAR = {}

    POSITIONS = {}

    AHEAD = {}

    STINT = {}

    for i in drivers:
        DFORM[i.name] = []
        LAP_CHART[i.name] = []
        TIRE_LEFT[i.name] = []
        TIRE_CHART[i.name] = []
        DNF[i.name] = [None]
        MECHANICAL[i.name] = []
        BOX[i.name] = [None]
        PENALTY[i.name] = [0]
        TIRE_USAGE[i.name] = 0
        TIRE_SETS[i.name] = []
        POSITIONS[i.name] = []
        AHEAD[i.name] = []
        PIT[i.name] = []
        STINT[i.name] = []

    for i in range(1,101):
        SAFETY_CAR[i] = [0]

    # Strategy Plannings
    if W3 == 'Dry':
        chart = {}
        for i in drivers:
            chart[i.name] = [FP1RESULT[i.name],FP2RESULT[i.name],FP3RESULT[i.name]]
            tireset = (chart[i.name].index(min(chart[i.name]))) + 1
            if tireset == 1:
                for q in CRC.strategy[0]:
                    TIRE_SETS[i.name].append(q)
                STINT[i.name].append(CRC.strategy[0][0].title[0])
            elif tireset == 2:
                for q in CRC.strategy[1]:
                    TIRE_SETS[i.name].append(q)
                STINT[i.name].append(CRC.strategy[0][0].title[0])
            elif tireset == 3:
                for q in CRC.strategy[2]:
                    TIRE_SETS[i.name].append(q)
                STINT[i.name].append(CRC.strategy[0][0].title[0])
    elif W3 == 'Dump':
        for i in drivers:
            for q in [inter,inter,inter,inter]:
                TIRE_SETS[i.name].append(q)
            STINT[i.name].append(inter.title[0])
    elif W3 == 'Wet':
        for i in drivers:
            for q in [w,w,w,w]:
                TIRE_SETS[i.name].append(q)
            STINT[i.name].append(w.title[0])

    # Race Session
    R(CRC,'Race',W3)
    print(borderline)

elif execution == 'data':
    print("Manufacturers' Rating from Best to Worst:")
    MF_N, MF_E, MF_P, MF_D, MF_AS, MF_SLS, MF_C0, MF_C1, MF_C2 = [], [], [], [], [], [], [], [], []
    TP = []
    MF = pd.DataFrame()
    for i in manufacturers:
        MF_N.append(i.title)
        MF_E.append(i.powertrain.brand)
        MF_P.append(i.rating())
        MF_D.append(i.downforce)
        MF_AS.append(i.vortex)
        MF_SLS.append(i.max_speed)
        MF_C0.append(i.characteristic[0])
        MF_C1.append(i.characteristic[1])
        MF_C2.append(i.characteristic[2])
        TP.append(i.manufacturer_tyre_coeff_print)
    MF['Manufacturer'] = MF_N
    MF['Engine'] = MF_E
    MF['Rating'] = MF_P
    MF['Downforce'] = MF_D
    MF['Airflow Sensivity'] = MF_AS
    MF['Straight Line Speed'] = MF_SLS
    MF['Attitude'] = MF_C1
    MF['Favourite'] = MF_C0
    MF['Flaw'] = MF_C2
    MF['Tire Performance Rating'] = TP
    MF = MF.sort_values('Rating',ascending=False)
    MF = MF.reset_index()
    MF = MF.drop(axis=1, columns=['index'])
    print(MF)

    # # #

    print(f"\nDrivers' Rating from Best to Worst:")
    D_N, D_T, D_Q, D_R, D_O, D_S, D_FF = [],[],[],[],[],[],[]
    DR = pd.DataFrame()
    for i in drivers:
        D_N.append(i.name)
        D_T.append(i.team.title)
        D_Q.append(i.real_qualifying_pace())
        D_R.append(i.real_race_pace())
        D_O.append(i.real_rating())
        D_S.append(i.style[0])
        D_FF.append(i.style[1])
    DR['Driver'] = D_N
    DR['Team'] = D_T
    DR['Overall'] = D_O
    DR['Quali Pace'] = D_Q
    DR['Race Pace'] = D_R
    DR['Attitude'] = D_S
    DR['Favourite'] = D_FF
    DR = DR.sort_values('Overall',ascending=False)
    DR = DR.reset_index()
    DR = DR.drop(axis=1, columns=['index'])
    print(DR)