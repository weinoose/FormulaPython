# Additional Libraries
from random import uniform, choice
import numpy as np
import pandas as pd
from colorama import Fore, Style
import datetime
import sys

# Application Modes
execution = 'simulation' # data or simulation for output/run mode.

# Season (Current) Selection
current = '2022'

# GP Selection
GP = 'Sakhir'

# Spec. Selection
spec = 'Formula 1'

if spec == 'Formula 1':
    verbosity = False # True or False for further telemetry & data.
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

def FIA(C): 
    if C == '1998':
        return [1.18250*(spex),False,False,'DHL',bridgestone,shell,585,3,5,2,False,115,0.0725]
    elif C == '2005':
        return [1.09750*(spex),False,False,'DHL',bridgestone,shell,585,3,5,2,False,115,0.0700]
    elif C == '2006':
        return [1.11750*(spex),False,False,'DHL',bridgestone,shell,585,3,5,2,False,115,0.0700]
    elif C == '2009':
        return [1.16500*(spex),False,False,'DHL',pirelli,shell,605,2,5,3,False,115,0.0675]
    elif C == '2011':
        return [1.15250*(spex),True,True,'DHL',pirelli,shell,640,2,5,3,False,110,0.0675]
    elif C == '2014':
        return [1.15750*(spex),True,True,'DHL',pirelli,petronas,691,2,3,5,True,109,0.0650]
    elif C == '2016':
        return [1.07000*(spex),True,True,'DHL',pirelli,petronas,702,2,3,5,True,108,0.0650]
    elif C == '2017':
        return [1.01750*(spex),True,True,'DHL',pirelli,petronas,728,2,5,3,True,112,0.0650]
    elif C == '2018':
        return [0.99250*(spex),True,True,'DHL',pirelli,petronas,734,2,5,3,True,116,0.0650]
    elif C == '2021':
        return [0.99000*(spex),True,True,'DHL',pirelli,aramco,752,2,5,3,True,118,0.0625]
    elif C == '2022':
        return [1.00000*(spex),True,True,'DHL',pirelli,aramco,798,5,2,3,True,112,0.0625]

# Visual Plugins
borderline = '* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *'

# Negative Events
FAILURES = ['gearbox','clutch','driveshaft','halfshaft','throttle','brakes','handling','wheel','steering','suspension','puncture',
            'electronics','hydraulics','water leak','fuel pressure','oil pressure','exhaust','differential','vibration',
            'transmission','alternator','turbocharger','cooling','gearbox driveline','engine',

            'engine','engine','engine','engine','engine','engine','engine','engine','engine','engine']

MECHANICALS = ['gearing alingment','gearbox driveline'
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
                CL1 = (((((performance/100)**2)*9.50) - 4)*(-1.0)) + TOTAL_WEIGHT + TRACTION_EFFECT_Q + ERS - driver.team.development
            elif self.title == 'Intermediate':
                CL1 = (((((performance/100)**2)*10.00) - 4)*(-1.0)) + TOTAL_WEIGHT + TRACTION_EFFECT_Q + ERS - driver.team.development
            else:
                CL1 = (((((performance/100)**2)*10.25) - 4)*(-1.0)) + TOTAL_WEIGHT + TRACTION_EFFECT_Q + ERS - driver.team.development
        elif mode[0] == 'sunday':
            performance = ((driver.team.performance(circuit.circuit_type))*1.00)
            if self.title == 'Wet':
                CL1 = (((((performance/100)**2)*9.50) - 4)*(-1.0)) + TOTAL_WEIGHT + TRACTION_EFFECT_R + (ERS/3) - driver.team.development
            elif self.title == 'Intermediate':
                CL1 = (((((performance/100)**2)*10.00) - 4)*(-1.0)) + TOTAL_WEIGHT + TRACTION_EFFECT_R + (ERS/3) - driver.team.development
            else:
                CL1 = (((((performance/100)**2)*10.25) - 4)*(-1.0)) + TOTAL_WEIGHT + TRACTION_EFFECT_R + (ERS/3) - driver.team.development
        elif mode[0] == 'friday':
            performance = ((driver.team.performance(circuit.circuit_type))*1.00)
            if self.title == 'Wet':
                CL1 = (((((performance/100)**2)*9.50) - 4)*(-1.0)) + TOTAL_WEIGHT + (ERS/3) - driver.team.development
            elif self.title == 'Intermediate':
                CL1 = (((((performance/100)**2)*10.00) - 4)*(-1.0)) + TOTAL_WEIGHT + (ERS/3) - driver.team.development
            else:
                CL1 = (((((performance/100)**2)*10.25) - 4)*(-1.0)) + TOTAL_WEIGHT + (ERS/3) - driver.team.development
        
        # # # 3.0: DRIVER
        # # # 3.1: Car/Driver Chemistry
        if driver.style != driver.team.style:
            CAR_DRIVER_CHEMISTRY = 0
        else:
            CAR_DRIVER_CHEMISTRY = uniform(((driver.adaptability-48)/777),(driver.adaptability/777))*(-1.0)

        # # # 3.2: Circuit/Driver Chemistry
        if circuit.location in driver.favorite:
            if mode[0] == 'sunday':
                BEST = uniform((round(((driver.pace-48)/400),3)),(round((driver.pace/400),3)))
            else:
                BEST = uniform((round(((driver.pace-48)/425),3)),(round((driver.pace/425),3)))
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
            error_rate = 12.5 - (((driver.consistency * driver.fitness))**(1/4))
        elif self.title == 'Wet':
            error_rate = 14.5 - (((driver.consistency * driver.fitness))**(1/4))
        else:
            error_rate = 10.5 - (((driver.consistency * driver.fitness))**(1/4))
        
        if (hotlap == 0) and (mode[0] == 'sunday') and (SAFETY_CAR[lap][-1] != 1):
            if uniform(0.01,100.01) <= error_rate:
                ERROR = choice(list(np.arange(2.249, 5.449, 0.001, dtype=float)))
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
                CL2 = ((((choice(WET)/100)**2)*4.00) + hotlap)*(-1.0) + (engine_mode + drs[0]) + (ERROR) - (BEST) + (CAR_DRIVER_CHEMISTRY) - (driver.form)
            elif self.title == 'Intermediate':
                CL2 = ((((choice(WET)/100)**2)*3.50) + hotlap)*(-1.0) + (engine_mode + drs[0]) + (ERROR) - (BEST) + (CAR_DRIVER_CHEMISTRY) - (driver.form)
            else:
                CL2 = ((((choice(SATURDAY)/100)**2)*3.25) + hotlap)*(-1.0) + (engine_mode + drs[1]) + (ERROR) - (BEST) + (CAR_DRIVER_CHEMISTRY) - (driver.form)
        
        elif mode[0] == 'sunday' or 'friday':         
            engine_mode = (((driver.team.powertrain.power)/175))*(-1.0) # Mode 2
            
            if self.title == 'Wet':
                CL2 = ((((choice(WET)/100)**1.50)*4.00) + hotlap)*(-1.0) + (engine_mode + drs[0]) + (ERROR) - (BEST) + (CAR_DRIVER_CHEMISTRY) - (driver.form)
            elif self.title == 'Intermediate':
                CL2 = ((((choice(WET)/100)**1.50)*3.50) + hotlap)*(-1.0) + (engine_mode + drs[0]) + (ERROR) - (BEST) + (CAR_DRIVER_CHEMISTRY) - (driver.form)
            else:
                CL2 = ((((choice(SUNDAY)/100)**1.75)*3.25) + hotlap)*(-1.0) + (engine_mode + drs[0]) + (ERROR) - (BEST) + (CAR_DRIVER_CHEMISTRY) - (driver.form)
        
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
    inter = Tire('Intermediate',FIA(current)[4],2.4,1.2517)
    w = Tire('Wet',FIA(current)[4],2.8,1.3717)
elif current in strategy_era:
    s = Tire('Soft',FIA(current)[4],1.0,1.0000)
    h = Tire('Hard',FIA(current)[4],2.4,1.0217)
    inter, w = Tire('Wet',FIA(current)[4],2.8,1.3717), Tire('Wet',FIA(current)[4],2.8,1.3717) # same compound.

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
sochi = Circuit('Sochi','Russia','Agility Circuit',53,FIA(current)[0]*54.75,STRATEGY('Sochi'),2,['Dry','Dry','Dry','Dry','Dump','Dump','Wet'],'Hard',[20,30,40],28) # 2014-present layout.
baku = Circuit('Baku','Azerbaijan','Agility Circuit',51,FIA(current)[0]*62.25,STRATEGY('Baku'),2,['Dry','Dry','Dry','Dry','Dry','Dry','Dump'],'Very Hard',[16,23,31],21) # 2016-present layout.

# # # POWER CIRCUITS
# spa = Circuit('Spa-Francorchamps','Belguim','Power Circuit',44,FIA(current)[0]*62.25,STRATEGY('Spa-Francorchamps'),2,['Dry','Dry','Dry','Dry','Dump','Wet','Wet'],'Easy',[18,26,35],24) # 1995-2003 layout.
# spa = Circuit('Spa-Francorchamps','Belguim','Power Circuit',44,FIA(current)[0]*66.50,STRATEGY('Spa-Francorchamps'),[m,s    ,s,s,m,m,h]],2,['Dry','Dry','Dry','Dry','Dump','Wet','Wet'],'Easy',[18,26,35],24) # 2004-2006 layout.
spa = Circuit('Spa-Francorchamps','Belguim','Power Circuit',44,FIA(current)[0]*65.25,STRATEGY('Spa-Francorchamps'),2,['Dry','Dry','Dry','Dry','Dump','Wet','Wet'],'Easy',[18,26,35],24) # 2007-present layout.
# sakhir = Circuit('Sakhir','Bahrain','Power Circuit',57,FIA(current)[0]*17.75,STRATEGY('Sakhir'),3,['Dry'],'Easy',[16,23,29],20) # 2020 extra outer layout.
# sakhir = Circuit('Sakhir','Bahrain','Power Circuit',57,FIA(current)[0]*71.25,STRATEGY('Sakhir'),3,['Dry'],'Easy',[16,23,29],20) # 2010 layout.
sakhir = Circuit('Sakhir','Bahrain','Power Circuit',57,FIA(current)[0]*51.75,STRATEGY('Sakhir'),3,['Dry'],'Easy',[16,23,29],20) # 2004-2009 & 2011-present layout.

# QUICKNESS CIRCUITS
# silverstone = Circuit('Silverstone','Great Britain','Quickness Circuit',52,FIA(current)[0]*42.25,STRATEGY('Silverstone'),2,['Dry','Dry','Dry','Dry','Dump','Dump','Wet'],'Easy',[14,21,27],18) # 1997-2009 layout.
silverstone = Circuit('Silverstone','Great Britain','Quickness Circuit',52,FIA(current)[0]*48.75,STRATEGY('Silverstone'),2,['Dry','Dry','Dry','Dry','Dump','Dump','Wet'],'Easy',[14,21,27],18) # 2010-present layout.
sepang = Circuit('Sepang','Malaysia','Quickness Circuit',56,FIA(current)[0]*54.75,STRATEGY('Sepang'),2,['Dry','Dry','Dry','Dry','Dump','Wet','Wet'],'Very Easy',[18,26,35],24) # 1999-present layout.
shanghai = Circuit('Shanghai','China','Quickness Circuit',56,FIA(current)[0]*54.75,STRATEGY('Shanghai'),2,['Dry','Dry','Dry','Dry','Dump','Dump','Wet'],'Very Easy',[18,26,35],24) # 2004-present layout.
yeongam = Circuit('Yeongam','South Korea','Quickness Circuit',55,FIA(current)[0]*55.25,STRATEGY('Yeongam'),2,['Dry','Dry','Dry','Dry','Dump','Dump','Wet'],'Easy',[20,30,40],28) # 2010-present layout.
india = Circuit('India','India','Quickness Circuit',60,FIA(current)[0]*45.25,STRATEGY('India'),3,['Dry','Dry','Dry','Dry','Dry','Dump','Dump','Wet'],'Easy',[16,23,29],20) # 2011-present layout.

# STRENGTH CIRCUITS
le = Circuit('Le Castellet','France','Strength Circuit',53,FIA(current)[0]*52.25,STRATEGY('Le Castellet'),2,['Dry','Dry','Dry','Dry','Dry','Dump','Wet'],'Easy',[16,23,31],21) # 2005-present layout.
mexico = Circuit('México City','México','Strength Circuit',71,FIA(current)[0]*38.75,STRATEGY('México City'),3,['Dry'],'Easy',[28,43,57],42) # 2015-present layout.
valencia = Circuit('Valencia','Spain','Strength Circuit',57,FIA(current)[0]*56.25,STRATEGY('Valencia'),2,['Dry','Dry','Dry','Dry','Dry','Dry','Dump'],'Hard',[16,23,29],20) # 2008-present layout.
austin = Circuit('Austin','United States','Strength Circuit',56,FIA(current)[0]*55.75,STRATEGY('Austin'),2,['Dry','Dry','Dry','Dry','Dry','Dry','Dump'],'Very Easy',[19,28,37],26) # 2012-present layout.
lusail = Circuit('Lusail','Qatar','Strength Circuit',57,FIA(current)[0]*43.25,STRATEGY('Lusail'),1,['Dry'],'Easy',[25,37,50],36) # 2004-present layout.

# COMPLETENESS CIRCUITS
# hockenheim = Circuit('Hockenheim','Germany','Completeness Circuit',67,FIA(current)[0]*56.75,STRATEGY('Hockenheim'),2,['Dry','Dry','Dry','Dump','Dump','Wet','Wet'],'Average',[18,26,35],24) # 1994-2001 layout.
hockenheim = Circuit('Hockenheim','Germany','Completeness Circuit',67,FIA(current)[0]*36.25,STRATEGY('Hockenheim'),2,['Dry','Dry','Dry','Dump','Dump','Wet','Wet'],'Average',[18,26,35],24) # 2002-present layout.
fuji = Circuit('Fuji','Japan','Completeness Circuit',67,FIA(current)[0]*40.25,STRATEGY('Fuji'),1,['Dry','Dry','Dry','Dry','Dry','Dump','Wet'],'Average',[18,26,35],24) # 2005-present layout.
# melbourne = Circuit('Melbourne','Australia','Completeness Circuit',58,FIA(current)[0]*45.25,STRATEGY('Melbourne'),4,['Dry','Dry','Dry','Dry','Dry','Dump','Wet'],'Hard',[20,30,40],28) # 1996-2020 layout.
melbourne = Circuit('Melbourne','Australia','Completeness Circuit',58,FIA(current)[0]*39.25,STRATEGY('Melbourne'),4,['Dry','Dry','Dry','Dry','Dry','Dump','Wet'],'Hard',[20,30,40],28) # 2021-present layout.
# yas = Circuit('Yas Island','Abu Dhabi','Completeness Circuit',58,FIA(current)[0]*58.75,STRATEGY('Yas Island'),2,['Dry'],'Average',[16,23,29],20) # 2009-2020 layout.
yas = Circuit('Yas Island','Abu Dhabi','Completeness Circuit',58,FIA(current)[0]*44.75,STRATEGY('Yas Island'),2,['Dry'],'Average',[16,23,29],20) # 2021-present layout.
spielberg = Circuit('Spielberg','Austuria','Completeness Circuit',71,FIA(current)[0]*26.25,STRATEGY('Spielberg'),2,['Dry','Dry','Dry','Dry','Dry','Dump','Dump'],'Very Easy',[20,30,40],28) # 1996-present layout.
portimao = Circuit('Portimão','Portugal','Completeness Circuit',66,FIA(current)[0]*40.75,STRATEGY('Portimão'),1,['Dry','Dry','Dry','Dry','Dry','Dry','Dump'],'Average',[28,43,57],42) # 2008-present layout.
jeddah = Circuit('Jeddah','Saudi Arabia','Completeness Circuit',50,FIA(current)[0]*49.25,STRATEGY('Jeddah'),3,['Dry'],'Average',[13,19,24],16) # 2021-present layout.

# DOWNFORCE CIRCUITS
nurburg = Circuit('Nurburg','Germany','Downforce Circuit',60,FIA(current)[0]*50.25,STRATEGY('Nurburg'),1,['Dry','Dry','Dry','Dry','Dry','Dump','Wet'],'Average',[20,30,40],28) # 2002-present layout.
kyalami = Circuit('Kyalami','South Africa','Downforce Circuit',71,FIA(current)[0]*35.75,STRATEGY('kyalami'),2,['Dry'],'Average',[20,30,40],28) # 2015-present layout.
# sao = Circuit('São Paulo','Brazil','Downforce Circuit',71,FIA(current)[0]*31.25,STRATEGY('São Paulo'),2,['Dry','Dry','Dry','Dry','Dump','Dump','Wet'],'Average',[28,43,57],42) # 1996-1998 layout.
sao = Circuit('São Paulo','Brazil','Downforce Circuit',71,FIA(current)[0]*30.75,STRATEGY('São Paulo'),2,['Dry','Dry','Dry','Dry','Dump','Dump','Wet'],'Average',[28,43,57],42) # 1999-present layout.
# montreal = Circuit('Montréal','Canada','Downforce Circuit',70,FIA(current)[0]*35.75,STRATEGY('Montréal'),3,['Dry','Dry','Dry','Dry','Dump','Wet','Wet'],'Hard',[20,30,40],28) # 1996-2001 layout.
montreal = Circuit('Montréal','Canada','Downforce Circuit',70,FIA(current)[0]*33.75,STRATEGY('Montréal'),3,['Dry','Dry','Dry','Dry','Dump','Wet','Wet'],'Hard',[20,30,40],28) # 2002-present layout.
imola = Circuit('Imola','Italy','Downforce Circuit',63,FIA(current)[0]*36.25,STRATEGY('Imola'),1,['Dry','Dry','Dry','Dry','Dump','Dump','Dump'],'Hard',[25,37,50],36) # 2008-present layout.
suzuka = Circuit('Suzuka','Japan','Downforce Circuit',53,FIA(current)[0]*50.75,STRATEGY('Suzuka'),1,['Dry','Dry','Dry','Dry','Dump','Dump','Wet'],'Hard',[16,23,31],21) # 2009-present layout.
istanbul = Circuit('Istanbul','Turkey','Downforce Circuit',58,FIA(current)[0]*45.50,STRATEGY('Istanbul'),2,['Dry','Dry','Dry','Dry','Dump','Dump','Wet'],'Very Easy',[16,23,29],20) # 2005-present layout.
miami = Circuit('Miami','United States','Downforce Circuit',57,FIA(current)[0]*49.75,STRATEGY('Miami'),3,['Dry','Dry','Dry','Dry','Dry','Dump','Wet'],'Easy',[19,28,37],26) # 2022-present layout.

# ENGINEERING CIRCUITS
zandvoort = Circuit('Zandvoort','Netherlands','Engineering Circuit',72,FIA(current)[0]*31.75,STRATEGY('Zandvoort'),2,['Dry','Dry','Dry','Dry','Dry','Dump','Dump'],'Average',[13,19,24],16) # 2020-present layout.
budapest = Circuit('Budapest','Hungary','Engineering Circuit',70,FIA(current)[0]*38.75,STRATEGY('Budapest'),1,['Dry','Dry','Dry','Dry','Dump','Dump','Dump'],'Very Hard',[20,30,40],28) # 2003-present layout.
barcelona = Circuit('Barcelona','Spain','Engineering Circuit',66,FIA(current)[0]*40.25,STRATEGY('Barcelona'),2,['Dry','Dry','Dry','Dry','Dry','Dump','Dump'],'Hard',[20,30,40],28) # 2007-present layout.

# STREET CIRCUITS
monaco = Circuit('Monte-Carlo','Monaco','Street Circuit',78,FIA(current)[0]*32.25,STRATEGY('Monte-Carlo'),2,['Dry','Dry','Dry','Dry','Dump','Dump','Wet'],'Very Hard',[20,30,40],28) # 2003-present layout.
# singapore = Circuit('Singapore','Singapore','Street Circuit',61,FIA(current)[0]*62.75,STRATEGY('Singapore'),3,['Dry','Dry','Dry','Dry','Dump','Dump','Wet'],'Very Hard',[16,23,29],20) # 2008-2012 layout.
# singapore = Circuit('Singapore','Singapore','Street Circuit',61,FIA(current)[0]*62.25,STRATEGY('Singapore'),3,['Dry','Dry','Dry','Dry','Dump','Dump','Wet'],'Very Hard',[16,23,29],20) # 2013-2014 layout.
# singapore = Circuit('Singapore','Singapore','Street Circuit',61,FIA(current)[0]*63.75,STRATEGY('Singapore'),3,['Dry','Dry','Dry','Dry','Dump','Dump','Wet'],'Very Hard',[16,23,29],20) # 2015-2017 layout.
singapore = Circuit('Singapore','Singapore','Street Circuit',61,FIA(current)[0]*59.75,STRATEGY('Singapore'),3,['Dry','Dry','Dry','Dry','Dump','Dump','Wet'],'Very Hard',[16,23,29],20) # 2018-present layout.

circuits = [lms,monza,sochi,baku,
            spa,sakhir,
            silverstone,sepang,shanghai,yeongam,india,
            le,mexico,valencia,austin,lusail,
            hockenheim,fuji,melbourne,yas,spielberg,portimao,jeddah,
            nurburg,kyalami,sao,montreal,imola,suzuka,istanbul,miami,
            zandvoort,budapest,barcelona,
            monaco,singapore]

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
HONDA_0 = Engine('Red Bull Powertrains Honda',FIA(current)[5],93,77) # Red Bull
HONDA_1 = Engine('Red Bull Powertrains Honda',FIA(current)[5],93,77) # AlphaTauri
FERRARI_F = Engine('Ferrari',FIA(current)[5],91,72) # Ferrari
FERRARI_0 = Engine('Ferrari',FIA(current)[5],91,72) # Haas
FERRARI_1 = Engine('Ferrari',FIA(current)[5],91,72) # Alfa Romeo
RENAULT_F = Engine('Renault',FIA(current)[5],87,72) # Alpine
MERCEDES_F = Engine('Mercedes',FIA(current)[5],87,92) # Mercedes
MERCEDES_0 = Engine('Mercedes',FIA(current)[5],87,92) # Williams
MERCEDES_1 = Engine('Mercedes',FIA(current)[5],87,92) # Aston Martin
MERCEDES_2 = Engine('Mercedes',FIA(current)[5],87,92) # McLaren

# Formula 2 Engines
MECACHROME = Engine('Mecachrome',FIA(current)[5],86,76)

# Manufacturers
class Manufacturer():
    def __init__(self,title,crew,powertrain,chassis,FW,RW,base,sidepod,suspension,reliability,weight,style,development):
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
        self.downforce = ((self.base*FIA(current)[7]) + (self.FW*FIA(current)[8]) + (self.RW*FIA(current)[9]))/10
        self.vortex = ((self.FW*5) + (self.sidepod*3) + (self.chassis*2))/10
        self.braking = ((self.FW*5) + (self.suspension*5))/10
        # Extra Calculated Attribute 1
        self.drag = ((self.chassis*5) + (self.base*3) + (self.RW*2))/10
        # Advanced Calculated Attributes
        self.max_speed = ((self.powertrain.power*7.5) + (self.RW*2.5))/10
        self.acceleration = ((self.powertrain.power*6.5) + (self.drag*3.5))/10
        # Extra Calculated Attribute 2
        self.drs_delta = ((self.powertrain.power*2.5) + (self.RW*7.5))/10
        # Extra Attributes
        self.development = development
        self.weight = weight
        self.style = style
        # Tire Performance Analysis
        thing = ((self.vortex + self.braking + (self.suspension*2) + self.RW) - (self.drag + self.downforce))
        self.manufacturer_tyre_coeff = round(((thing)/1450),3)

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
        return ((self.powertrain.power*20) + (self.downforce*25) + (self.drag*20) + (self.vortex*20) + (self.braking*15))/100
    
    def performance(self,circuit_type):
        if circuit_type == 'Power Circuit':
            return ((((self.max_speed+self.acceleration)/2)*5) + (self.downforce*3) + (self.vortex*2) + (self.braking*1))/11
        elif circuit_type == 'Agility Circuit':
            return ((self.max_speed*5) + (self.braking*3) + (self.vortex*2) + (self.downforce*1))/11
        elif circuit_type == 'Quickness Circuit':
            return ((self.max_speed*5) + (self.downforce*3) + (self.vortex*2) + (self.braking*1))/11
        elif circuit_type == 'Strength Circuit':
            return ((self.drag*5) + (self.braking*3) + (self.downforce*2) + (self.vortex*1))/11
        elif circuit_type == 'Completeness Circuit':
            return ((self.downforce*5) + (self.max_speed*3) + (self.vortex*2) + (self.braking*1))/11
        elif circuit_type == 'Downforce Circuit':
            return ((self.downforce*5) + (self.acceleration*3) + (self.vortex*2) + (self.braking*1))/11
        elif circuit_type == 'Engineering Circuit':
            return ((self.downforce*5) + (self.vortex*3) + (self.acceleration*2) + (self.braking*1))/11
        elif circuit_type == 'Street Circuit':
            return ((self.braking*5) + (self.downforce*2) + (self.vortex*1) + (self.drag*3))/11

if spec == 'Formula 1':
    mercedes = Manufacturer('Mercedes-AMG Petronas F1 Team','Good',MERCEDES_F,91,89,84,89,79,89,106,+0.00,'Balanced',0.000)
    redbull = Manufacturer('Oracle Red Bull Racing','Perfect',HONDA_0,89,89,92,94,92,92,86,+5.00,'Unbalanced',0.000)
    ferrari = Manufacturer('Scuderia Ferrari','Average',FERRARI_F,96,96,89,91,94,79,79,+0.00,'Stiff Front',0.000)
    mclaren = Manufacturer('McLaren F1 Team','Perfect',MERCEDES_2,79,84,79,84,84,84,106,+0.00,'Unbalanced',0.000)
    alpine = Manufacturer('BWT Alpine F1 Team','Good',RENAULT_F,86,82,82,86,86,82,82,+0.00,'Stiff Front',0.000)
    alphatauri = Manufacturer('Scuderia AlphaTauri','Good',HONDA_1,77,77,84,84,75,75,82,+0.00,'Balanced',0.000)
    astonmartin = Manufacturer('Aston Martin Aramco Cognizant F1 Team','Average',MERCEDES_1,79,79,79,81,81,79,104,+0.00,'Unbalanced',0.000)
    williams = Manufacturer('Williams Racing','Good',MERCEDES_0,77,77,77,77,84,88,104,+0.00,'Stiff Front',0.000)
    alfaromeo = Manufacturer('Alfa Romeo F1 Team Orlen','Good',FERRARI_1,86,84,79,79,79,79,84,-5.00,'Unbalanced',0.000)
    haas = Manufacturer('Haas F1 Team','Good',FERRARI_0,81,81,81,79,79,79,86,+0.00,'Balanced',0.000)
    manufacturers = [mercedes,redbull,ferrari,mclaren,alpine,alphatauri,astonmartin,williams,alfaromeo,haas]
elif spec == 'Formula 2':
    prema = Manufacturer('Prema Racing','Good',MECACHROME,91,91,91,85,85,85,85,+0.00,None,0.000) # 4th best.
    virtuosi = Manufacturer('Virtuosi Racing','Average',MECACHROME,91,91,91,79,79,79,79,+0.00,None,0.000) # 7th best.
    carlin = Manufacturer('Carlin','Perfect',MECACHROME,91,91,91,89,89,89,89,+0.00,None,0.000) # 2nd best.
    hitech = Manufacturer('Hitech Grand Prix','Average',MECACHROME,91,91,91,83,83,83,83,+0.00,None,0.000) # 5th best.
    art = Manufacturer('ART Grand Prix','Perfect',MECACHROME,91,91,91,87,87,87,87,+0.00,None,0.000) # 3rd best.
    mp = Manufacturer('MP Motorsport','Good',MECACHROME,91,91,91,91,91,91,91,+0.00,None,0.000) # best.
    campos = Manufacturer('Campos Racing','Average',MECACHROME,91,91,91,79,79,79,79,+0.00,None,0.000) # 11th best.
    dams = Manufacturer('DAMS','Good',MECACHROME,91,91,91,81,81,81,81,+0.00,None,0.000) # 6th best.
    trident = Manufacturer('Trident','Average',MECACHROME,91,91,91,79,79,79,79,+0.00,None,0.000) # 9th best.
    charouz = Manufacturer('Charouz Racing System','Bad',MECACHROME,91,91,91,79,79,79,79,+0.00,None,0.000) # 8th best.
    van = Manufacturer('Van Amersfoot Racing','Perfect',MECACHROME,91,91,91,79,79,79,79,+0.00,None,0.000) # 10th best.
    manufacturers = [prema,virtuosi,carlin,hitech,art,mp,campos,dams,trident,charouz,van]

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
        self.favorite= favorite
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
    VER = Driver(redbull,'Max Verstappen','NET',1,90,93,92,95,93,95,95,95,87,86,94,['México City','Zandvoort','Spielberg','Imola','Spa-Francorchamps'],'Unbalanced') # 92.187 > 92
    LEC = Driver(ferrari,'Charles Leclerc','MNK',16,93,94,89,92,92,88,88,86,86,90,86,['Monte-Carlo','Spa-Francorchamps','Monza','Sakhir','Spielberg'],'Balanced') # 90.989 > 91
    HAM = Driver(mercedes,'Lewis Hamilton','GBR',44,89,89,91,92,91,93,91,92,91,93,92,['Silverstone','Barcelona','Budapest','São Paulo','Montréal','Yas Island'],'Balanced') # 90.97 > 91
    VET = Driver(astonmartin,'Sebastian Vettel','GER',5,89,91,90,94,88,89,92,94,93,91,93,['Monte-Carlo','Singapore','India','Suzuka','Sepang','Valencia','Montréal'],'Stiff Rear') # 90.457 > 90
    ALO = Driver(alpine,'Fernando Alonso','ESP',14,87,89,92,93,90,95,86,93,94,94,91,['Budapest','Silverstone','Monza','Barcelona','Valencia','Singapore'],'Stiff Front') # 90.272 > 90
    PER = Driver(redbull,'Sergio Pérez','MEX',11,86,90,94,91,87,92,85,91,95,92,90,['Baku','Jeddah','Monte-Carlo'],'Balanced') # 89.16 > 89
    NOR = Driver(mclaren,'Lando Norris','GBR',4,92,91,87,92,85,94,83,87,87,86,87,['Sochi','Spielberg','Imola'],None) # 88.586 > 89
    RUS = Driver(mercedes,'George Russell','GBR',63,91,92,87,90,86,94,90,86,86,87,86,['São Paulo','Budapest','Barcelona'],None) # 88.561 > 89
    SAI = Driver(ferrari,'Carlos Sainz Jr.','ESP',55,87,88,85,89,90,91,84,89,88,85,88,['Monte-Carlo','Silverstone'],'Balanced') # 88.122 > 88
    BOT = Driver(alfaromeo,'Valtteri Bottas','FIN',77,89,88,87,89,89,84,80,85,92,89,84,['Sochi','Spielberg','Silverstone'],'Stiff Rear') # 87.192 > 87
    OCO = Driver(alpine,'Esteban Ocon','FRA',31,85,88,87,88,86,91,94,90,90,88,87,['Budapest'],None) # 87.387 > 87
    STR = Driver(astonmartin,'Lance Stroll','CAN',18,83,83,85,88,86,90,93,88,89,85,89,['Baku'],None) # 86.478 > 86
    GAS = Driver(alphatauri,'Pierre Gasly','FRA',10,86,86,85,86,85,85,81,84,81,87,85,['Monza'],None) # 85.414 > 85
    MAG = Driver(haas,'Kevin Magnussen','DEN',20,81,85,85,87,83,86,90,86,85,84,84,['São Paulo'],None) # 84.376 > 84
    RIC = Driver(mclaren,'Daniel Ricciardo','AUS',3,79,84,84,84,80,80,89,91,85,87,84,['Monte-Carlo','Baku','Singapore','Shanghai','Budapest'],'Stiff Rear') # 83.183 > 83
    ALB = Driver(williams,'Alex Albon','THI',23,82,82,88,85,84,87,81,82,80,84,81,['Sakhir'],'Stiff Front') # 82.872 > 83
    TSU = Driver(alphatauri,'Yuki Tsunoda','JPN',22,87,81,81,85,80,84,87,84,83,87,80,['Sakhir'],'Balanced') # 82.866 > 83
    PIA = Driver(alpine,'Oscar Piastri','AUS',None,87,82,82,81,82,86,80,80,80,81,82,[None],None) # 82.488 > 83
    MSC = Driver(haas,'Mick Schumacher','GER',47,80,80,82,82,79,81,85,88,84,83,83,['Spielberg'],'Balanced') # 81.676 > 82
    DEV = Driver(mercedes,'Nyck de Vries','NET',None,81,81,83,85,79,82,82,82,82,83,83,[None],None) # 81.638 > 82
    RAI = Driver(None,'Kimi Raikkonen','FIN',None,76,91,81,96,71,71,81,89,81,81,81,['Spa-Francorchamps','Melbourne','Suzuka','São Paulo','Budapest'],'Stiff Front') # 80.859 > # 81
    HUL = Driver(astonmartin,'Nico Hulkenberg','GER',None,84,84,80,80,77,81,79,79,79,82,77,[None],None) # 80.116 > # 80
    GIO = Driver(ferrari,'Antonio Giovinazzi','ITA',None,81,78,77,83,81,83,77,83,77,80,77,[None],None) # 79.685 > # 80
    ZHO = Driver(alfaromeo,'Zhou Guanyu','CHN',24,77,77,79,79,79,79,74,77,77,79,79,[None],None) # 77.959 > # 78
    VAN = Driver(mclaren,'Stoffel Vandoorne','BEL',None,77,77,77,77,77,77,76,77,77,77,78,[None],None) # 77.105 > # 77
    MAZ = Driver(None,'Nikita Mazepin','RUS',None,76,76,72,76,76,76,95,76,76,76,76,[None],None) # 76.853 > 77
    LAT = Driver(williams,'Nicholas Latifi','CAN',6,74,74,74,74,74,74,88,74,74,74,74,[None],None) # 75.684 > 76
    KUB = Driver(alfaromeo,'Robert Kubica','POL',None,73,73,73,73,73,73,73,73,73,73,73,[None],None) # 74.00 > 74
    BUE = Driver(redbull,'Sébastien Buemi','SUI',None,72,72,95,72,72,72,72,72,72,72,72,[None],None) # 73.811 > 74
    AIT = Driver(williams,'Jack Aitken','GBR',None,70,70,70,70,70,70,70,70,70,70,70,[None],None) # 70.00 > 70
    FIT = Driver(haas,'Pietro Fittipaldi','BRA',None,69,69,69,69,69,69,69,69,69,69,69,[None],None) # 69.00 > 69
    drivers = [VER,LEC,HAM,VET,ALO,PER,NOR,RUS,SAI,BOT,OCO,STR,GAS,MAG,RIC,ALB,TSU,MSC,ZHO,LAT]

elif spec == 'Formula 2':
    LAW = Driver(carlin,'Liam Lawson','NZL',None,82,82,82,82,80,82,82,82,82,82,82,[None],None) # 81.546 > 82
    DOO = Driver(virtuosi,'Jack Doohan','AUS',None,84,84,79,79,79,76,80,80,80,80,80,[None],None) # 81.340 > # 81
    IWA = Driver(dams,'Ayumu Iwasa','JPN',None,82,82,80,80,77,77,77,77,77,77,77,[None],None) # 80.090 > # 80
    DRU = Driver(mp,'Felipe Drugovich','BRA',None,78,79,78,78,78,78,78,78,78,78,78,[None],None) # 78.142 > # 78
    POU = Driver(art,'Théo Pourchaire','FRA',None,82,74,80,80,80,80,80,80,80,80,70,[None],None) # 77.854 > # 78
    VER = Driver(trident,'Richard Verschoor','NET',None,79,76,76,76,79,79,79,79,79,79,79,[None],None) # 77.704 > # 78
    VES = Driver(art,'Frederik Vesti','DEN',None,77,76,79,79,79,79,79,79,79,79,77,[None],None) # 77.682 > # 78
    SAR = Driver(carlin,'Logan Sargeant','USA',None,79,74,80,80,80,80,80,81,80,80,70,[None],None) # 77.481 > # 77
    HAU = Driver(prema,'Dennis Hauger','DEN',None,76,76,79,79,79,79,79,79,77,77,76,[None],None) # 77.431 > # 77
    DAR = Driver(prema,'Jehan Daruvala','IND',None,76,76,79,79,79,79,79,79,77,77,76,[None],None) # 77.431 > # 77
    BOS = Driver(campos,'Ralph Boschung','SUI',None,76,76,76,76,76,76,76,76,76,76,76,[None],None) # 76.000 > # 76
    COR = Driver(van,'Amaury Cordeel','BEL',None,76,76,76,76,76,76,76,76,76,76,76,[None],None) # 76.000 > # 76
    FIT = Driver(charouz,'Enzo Fittipaldi','BRA',None,72,72,74,74,76,76,76,76,76,76,70,[None],None) # 73.591 > # 74
    VIP = Driver(hitech,'Jüri Vips','EST',None,72,72,74,74,74,76,76,76,74,74,74,[None],None) # 73.136 > # 73
    NIS = Driver(dams,'Roy Nissany','ISR',None,68,70,74,74,74,74,74,74,74,74,74,[None],None) # 71.410 > # 71
    BEC = Driver(van,'David Beckmann','GER',None,68,70,74,74,74,74,74,74,74,74,74,[None],None) # 71.410 > # 71
    ARM = Driver(hitech,'Marcus Armstrong','AUS',None,68,70,74,74,74,74,74,74,74,74,74,[None],None) # 71.410 > # 71
    SAT = Driver(virtuosi,'Marino Sato','JPN',None,66,68,74,72,72,72,72,72,72,72,72,[None],None) # 69.546 > # 70
    NOV = Driver(mp,'Clément Novalak','FRA',None,66,68,74,72,72,72,72,72,72,72,72,[None],None) # 69.546 > # 70
    WIL = Driver(trident,'Calan Williams','AUS',None,70,70,74,64,64,72,84,66,66,66,66,[None],None) # 68.546 > # 69
    CAL = Driver(campos,'Olli Caldwell','GBR',None,70,70,74,64,64,72,84,66,66,66,66,[None],None) # 68.546 > # 69
    BOL = Driver(charouz,'Cem Bölükbaşı','TUR',None,62,68,72,72,72,72,80,86,66,86,66,[None],None) # 68.409 > # 68
    drivers = [LAW,DOO,IWA,DRU,POU,VER,VES,SAR,HAU,DAR,BOS,COR,FIT,VIP,NIS,BEC,ARM,SAT,NOV,WIL,CAL,BOL]

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
        df = df.drop(axis=1, columns=['FL. LAP','FL. TIRE'])
    for i in list(df.columns):
        da[i] = list(df[i])

    # DNF/FL. Optimizing for Race Session
    if keyword == 'race-chart':
        dnffloptimizer0, dnffloptimizer1 = [], []
        
        for i,j in zip(list(da['FL. LAP']),list(da['FL.'])):
            if 2 >= i:
                dnffloptimizer0.append('NaN')
                dnffloptimizer1.append('NaN')
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
                current_laptime = round(tire.laptime(driver,circuit,lap,tire_usage,['saturday',0]),3)
                
                reliability_defict = driver.team.powertrain.fuel.vulnerability
                mechanic_failure_odd = ((((((((driver.team.reliability+reliability_defict)*(-1.0))**3)/60000)+17))/1.7)**3) > uniform(0,75000)
                
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
                    if mechanic_failure_odd == True:
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

            reliability_defict = driver.team.powertrain.fuel.vulnerability
            mechanic_failure_odd = ((((((((driver.team.reliability+reliability_defict)*(-1.0))**3)/60000)+17))/1.7)**3) > uniform(0,75000)
            
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
                LAP_CHART[driver.name].append((round(circuit.laptime + 125,3)))
                TIRE_CHART[driver.name].append(tire.title[0])
                TIRE_USAGE[driver.name] += 0
                TIRE_LEFT[driver.name].append(f'{tire.title[0]} %{tire_left}')

            elif SAFETY_CAR[lap][-1] == 1:
                if len(BOX[driver.name]) > 1:
                    if len(TIRE_SETS[driver.name]) == 1:
                        print(f'{Fore.RED}DNF | Lap {lap} | {driver.name} has forced to retire due to severe damage issue. Disaster for {driver.team.title}!{Style.RESET_ALL}')
                        LAP_CHART[driver.name].append((circuit.laptime + 75)*2)
                        TIRE_CHART[driver.name].append(tire.title[0])
                        TIRE_USAGE[driver.name] += 0
                        TIRE_LEFT[driver.name].append(f'{tire.title[0]} %{tire_left}')
                    else:
                        TIRE_USAGE[driver.name] = 0
                        TIRE_SETS[driver.name].pop(0)
                        tire = TIRE_SETS[driver.name][0]
                        STINT[driver.name].append(f'-{tire.title[0]}')
                        pit_stop = round(driver.team.pit() + 6.5,3)
                        PIT[driver.name].append(1)
                        print(f'PIT | Lap {lap} | Pit-stop for {driver.name} with {pit_stop} seconds stationary. He is on {tire.title} compound.')
                        LAP_CHART[driver.name].append((round(circuit.laptime + 125,3)) + pit_stop + 14)
                        TIRE_CHART[driver.name].append(tire.title[0])
                        TIRE_LEFT[driver.name].append(f'{tire.title[0]} %{tire_left}')
                        BOX[driver.name].clear()
                        BOX[driver.name].append(None)
                elif tire_left < 59.95:
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
                            PIT[driver.name].append(1)
                            if 10 > pit_stop >= 5.0:
                                print(f'PIT | Lap {lap} | Bad news for {driver.name} with {pit_stop} seconds stationary. He is on {tire.title} compound.')
                            elif pit_stop >= 10:
                                print(f'PIT | Lap {lap} | Disaster for {driver.name} with {pit_stop} seconds stationary. He is on {tire.title} compound.')
                            else:
                                print(f'PIT | Lap {lap} | Pit-stop for {driver.name} with {pit_stop} seconds stationary. He is on {tire.title} compound.')
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
                if mechanic_failure_odd == True:
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
                        LAP_CHART[driver.name].append((circuit.laptime + 75)*2)
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
                        LAP_CHART[driver.name].append((circuit.laptime + 75)*2)
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
                            LAP_CHART[driver.name].append((circuit.laptime + 75)*2)
                            TIRE_CHART[driver.name].append(tire.title[0])
                            TIRE_USAGE[driver.name] += 0
                            TIRE_LEFT[driver.name].append(f'{tire.title[0]} %{tire_left}')
                        else:
                            TIRE_USAGE[driver.name] = 0
                            TIRE_SETS[driver.name].pop(0)
                            tire = TIRE_SETS[driver.name][0]
                            STINT[driver.name].append(f'-{tire.title[0]}')
                            pit_stop = round(driver.team.pit() + 6.5,3)
                            PIT[driver.name].append(1)
                            print(f'PIT | Lap {lap} | Pit-stop for {driver.name} with {pit_stop} seconds stationary. He is on {tire.title} compound.')
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
                                PIT[driver.name].append(1)
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
                                PENALTY[driver.name].append(3)
                                print(f'{Fore.CYAN}PEN | Lap {lap} | 3 secs. penalty to {driver.name} for the excessive amount of corner-cutting. {Style.RESET_ALL}')
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
        
        if SAFETY_CAR[lap][-1] == 1: # If there is a safety car scenario, cars has to be lining behind the safety car.
            if SAFETY_CAR[lap+2][-1] != 1:
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
        
        else: # If there is safety car, there will be no pass.
            # Lap by Lap Report for Overtake Analysis
            temp, temptirenamedata = pd.DataFrame(), pd.DataFrame()
            for driver in drivers:
                temp[driver.name], temptirenamedata[driver.name] = LAP_CHART[driver.name], TIRE_CHART[driver.name]
            TEMP_CLASSIFICATION = ANALYZER(f'LAP {lap} | Race',temp,temptirenamedata,'race-chart')

            # Bug Dealer
            if lap == 1:
                pass
            else:         
                dp0 = list(TEMP_CLASSIFICATION['DRIVERS'])
        
                for i in dp0:
                    for Q in drivers:
                        if Q.name == i:
                            driver = Q

                    now0 = dp0.index(i)+1
                    then0 = POSITIONS[i][-1]

                    if then0 < now0:
                        pass
                    elif then0 == now0:
                        pass
                    else:
                        compound_left = float((TIRE_LEFT[driver.name][-1]).split('%')[1])
                        power_of_the_dog_0 = (driver.team.performance(circuit.circuit_type))*2.0
                        power_of_the_dog_1 = (compound_left/1.15)*1.5
                        power_of_the_dog_2 = (power_of_the_dog_0 + power_of_the_dog_1)**2
                        if tire.title == 'Soft':
                            power_of_the_dog_3 = 50000
                        elif tire.title == 'Medium':
                            power_of_the_dog_3 = 28750
                        elif tire.title == 'Hard':
                            power_of_the_dog_3 = 7500
                        else:
                            power_of_the_dog_3 = 50000

                        cakal = (then0 - now0)
                        dealer = 10**5.5
                        F = round(driver.attack/1000,3)
                        the_calculation = round(((1.0) - ((((power_of_the_dog_2 + power_of_the_dog_3)/dealer))*cakal))*1.13,3)
                        LAP_CHART[i][-1] += uniform(the_calculation-(round(0.125 - F,3)),the_calculation+(F))

            # Real-time Racing | Overtakes and Defence Positions
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

                drs_advantage = (((-1.0)*((0.250) + attacker_obj.team.RW/200))/1.5)

                if circuit.overtake_difficulty == 'Very Hard':
                    offset = 7.5
                elif circuit.overtake_difficulty == 'Hard':
                    offset = 12.5
                elif circuit.overtake_difficulty == 'Average':
                    offset = 22.5
                elif circuit.overtake_difficulty == 'Easy':
                    offset = 37.5
                elif circuit.overtake_difficulty == 'Very Easy':
                    offset = 50
                
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
                        BONUS[defender].append(8.750)
                        BOX[attacker].append(True)

                        if uniform(0.1,100.1) > 0.275:
                            SAFETY_CAR[lap+1].append(1)
                            SAFETY_CAR[lap+2].append(1)
                            SAFETY_CAR[lap+3].append(1)
                            SAFETY_CAR[lap+4].append(1)

                    elif INCIDENT == 'ATTACKER CLEAR & DEFENDER DAMAGED':
                        print(f'{Fore.MAGENTA}INC | Lap {lap} | OOOHHH! {attacker} and {defender} GOT COLLIDED! {defender} HAS DAMAGE BUT {attacker} HAS NO! {defender} IS BOXING!.{Style.RESET_ALL}')
                        BONUS[defender].append(uniform(19.01,39.99))
                        BONUS[attacker].append(8.750)
                        BOX[defender].append(True)

                        if uniform(0.1,100.1) > 0.275:
                            SAFETY_CAR[lap+1].append(1)
                            SAFETY_CAR[lap+2].append(1)
                            SAFETY_CAR[lap+3].append(1)
                            SAFETY_CAR[lap+4].append(1)
                            
                    elif INCIDENT == 'DEFENDER DNF & ATTACKER CLEAR':
                        print(f'{Fore.MAGENTA}INC | Lap {lap} | OOOHHH! {attacker} and {defender} GOT COLLIDED! {defender} IS OUT! {attacker} HAS NO DAMAGE!.{Style.RESET_ALL}')
                        BONUS[attacker].append(8.750)
                        BONUS[defender].append((circuit.laptime + 5)*2)
                        DNF[defender].append(True)
                        SAFETY_CAR[lap+1].append(1)
                        SAFETY_CAR[lap+2].append(1)
                        SAFETY_CAR[lap+3].append(1)
                        SAFETY_CAR[lap+4].append(1)
                    elif INCIDENT == 'ATTACKER DNF & DEFENDER CLEAR':
                        print(f'{Fore.MAGENTA}INC | Lap {lap} | OOOHHH! {attacker} and {defender} GOT COLLIDED! {attacker} IS OUT! {defender} HAS NO DAMAGE!.{Style.RESET_ALL}')
                        BONUS[defender].append(8.750)
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

            # Laptime Trade-Off.
            for i in BONUS:
                LAP_CHART[i][-1] = sum(BONUS[i]) + LAP_CHART[i][-1]

        BONUS = {}
        for i in drivers:
            BONUS[i.name] = []

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
    i1[0] = None

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
            STINT[i.name].append(CRC.strategy[0][0].title[0])
    elif W3 == 'Wet':
        for i in drivers:
            for q in [w,w,w,w]:
                TIRE_SETS[i.name].append(q)
            STINT[i.name].append(CRC.strategy[0][0].title[0])

    # Race Session
    R(CRC,'Race',W3)
    print(borderline)

elif execution == 'data':
    borderline = '* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *'
    
    # # #

    print(f"{borderline}\nManufacturers' Rating from Best to Worst:")
    MF_N, MF_E, MF_P = [], [], []
    TP = []
    MF = pd.DataFrame()
    for i in manufacturers:
        MF_N.append(i.title)
        MF_E.append(i.powertrain.brand)
        MF_P.append(i.rating())
        TP.append(i.manufacturer_tyre_coeff_print)
    MF['Manufacturer'] = MF_N
    MF['Engine'] = MF_E
    MF['Overall'] = MF_P
    MF['Tire Performance Quality'] = TP
    MF = MF.sort_values('Overall',ascending=False)
    MF = MF.reset_index()
    MF = MF.drop(axis=1, columns=['index'])
    print(MF)

    # # #

    print(f"{borderline}\nDrivers' Rating from Best to Worst:")
    D_N, D_T, D_Q, D_R, D_O = [],[],[],[],[]
    DR = pd.DataFrame()
    for i in drivers:
        D_N.append(i.name)
        D_T.append(i.team.title)
        D_Q.append(i.real_qualifying_pace())
        D_R.append(i.real_race_pace())
        D_O.append(i.real_rating())
    DR['Driver'] = D_N
    DR['Team'] = D_T
    DR['Overall'] = D_O
    DR['Quali Pace'] = D_Q
    DR['Race Pace'] = D_R
    DR = DR.sort_values('Overall',ascending=False)
    DR = DR.reset_index()
    DR = DR.drop(axis=1, columns=['index'])
    print(DR)
    print(f'{borderline}')

# # # DIFFERENCES FROM REAL FORMULA ONE RACING
# No red flag and no artificial safety car exist, only safety car.
# No changable weather conditions for each session.
# No penalty paying during pit-stops. It has to be added after the race.
# We assume that every year of formula racing has the same post-race points distribution, contrary to the truth.
# We assume that each team find the best strategy and car setup for the feature race.
# We assume that each circuit has the same amount of fuel consumption. However, it is changable fuel supplier to fuel supplier.
# We assume that blown diffuser never banned in the era of between 2009 and 2011, and cars never slowed down for 2012 season.
# We assume that engines were frozen at 2006 not 2007, contrary to the truth.
# We assume that there were no prohibition for tire changes at 2005, contrary to the truth.
# During the era between [1998-2008], contrary to the truth, we assume that Bridgestone is the only tire manufacturer.
# During the era between [1998-2009], refuelling is not active contrary to the truth. Hence, drivers starts the races with full tank.