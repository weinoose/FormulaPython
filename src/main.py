from math import pow
from random import uniform, choice
import numpy as np
import pandas as pd

# GP Selection
GP = 'Sakhir'

# Tire Supplier
class Tyre():
    def __init__(self,title,pace,durability):
        self.title = title
        self.pace = pace
        self.durability = durability

bridgestone = Tyre('Bridgestone',2.2,4.2)
pirelli = Tyre('Pirelli',-0.2,-2.0)

# Fuel
class Fuel():
    def __init__(self,title,injection,vulnerability):
        self.title = title
        self.injection = injection
        self.vulnerability = vulnerability

shell = Fuel('Shell',-0.3,-3.5)
petronas = Fuel('Petronas',-0.0,-0.0)
aramco = Fuel('Aramco',+0.3,+3.5)

# FIA: Chassis Design / DRS / ERS / Logistics Sponsor / Tire Supplier / Fuel Supplier / Min. Weight
current = '2022'
def FIA(current): 
    if current == '2005':
        return [-3.5,False,False,'DHL',bridgestone,shell,585]
    elif current == '2006':
        return [-2.2,False,False,'DHL',bridgestone,shell,585]
    elif current == '2007':
        return [-1.2,False,False,'DHL',bridgestone,shell,585]
    elif current == '2008':
        return [-0.0,False,False,'DHL',bridgestone,shell,585]
    elif current == '2009':
        return [+0.5,False,False,'DHL',bridgestone,shell,605]
    elif current == '2012':
        return [+2.0,True,False,'DHL',pirelli,shell,640]
    elif current == '2014':
        return [+3.0,True,True,'DHL',pirelli,petronas,691]
    elif current == '2016':
        return [-1.0,True,True,'DHL',pirelli,petronas,702]
    elif current == '2017':
        return [-2.0,True,True,'DHL',pirelli,petronas,728]
    elif current == '2018':
        return [-2.5,True,True,'DHL',pirelli,petronas,734]
    elif current == '2021':
        return [-1.5,True,True,'DHL',pirelli,aramco,752]
    elif current == '2022':
        return [-0.0,True,True,'DHL',pirelli,aramco,798]
    elif current == '2026':
        return [None,True,True,'DHL',pirelli,aramco,None]

# Failures
FAILURES = ['Engine','Gearbox','Clutch','Driveshaft','Halfshaft','Throttle','Brakes','Handling','Wheel','Steering','Suspension','Puncture',
            'Electronics','Hydraulics','Water Leak','Fuel Pressure','Oil Pressure','Exhaust','Differential','Vibration',
            'Transmission','Alternator','Turbocharger','Cooling','Engine','Engine','Engine','Engine','Engine','Engine',
            'Engine','Engine','Engine','Engine','Engine']

ERRORS = ['Spun-off','Went through Barriers','Damaged his Suspension']

# Tires
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
        return (circuit.circuit_laps+1) - lap
    def laptime(self,driver,circuit,lap,tire_usage,mode):
        # # # Part 1: Fuel and Tire
        fuel_injection = driver.team.powertrain.fuel.injection
        fuel_left = self.fuel_left(circuit,lap)
        
        tire_supplier_pace = self.supplier.pace
        tire_supplier_durability = self.supplier.durability
        tire_heat = ((((10*driver.team.manufacturer_tyre_coeff)**2)-3))/9.0
        tire_left = self.tire_left(driver,circuit,tire_usage) + tire_supplier_durability
        
        special_function_for_tire = ((pow(1.022,(100-tire_left)))-1)
        special_function_for_fuel = (fuel_left**(fuel_left/(fuel_left*1.9)))

        if mode[0] == 'sunday' or 'friday':
            if tire_left > 92.5:
                if mode[0] == 'sunday' or 'friday':
                    tire_cold = (1.350 - ((100-tire_left)/10))
                else:
                    tire_cold = 0.0
            else:
                tire_cold = 0.0
        else:
            tire_cold = 0.0

        if tire_left < 45.0:
            if mode[0] == 'sunday' or 'friday':
                tire_cold = -0.250
            else:
                tire_cold = 0.0
        else:
            tire_cold = 0.0

        CL0 = (circuit.laptime * self.laptime_coefficient) + (special_function_for_tire) + (special_function_for_fuel) + (tire_heat + tire_cold) + (tire_supplier_pace) + (fuel_injection)
    
        # # # Part 2: The Performance of the Car
        if mode[0] == 'saturday':
            performance = ((driver.team.performance(circuit.circuit_type))*1.00)
            CL1 = ((((performance/100)**2)*6.25) - 4)*(-1.0)
        elif mode[0] == 'sunday' or 'friday':
            performance = ((driver.team.performance(circuit.circuit_type))*1.00)
            CL1 = ((((performance/100)**2)*8.25) - 4)*(-1.0)
        
        # # # Part 3: The Performance of the Driver
        # # # 3.1: Purple Lap
        if mode[0] == 'sunday' or 'friday':
            hotlap = 0
            if uniform(0,100) < 10:
                hotlap = (-1.0)*(((driver.fitness/100)**2)/2)
        else:
            hotlap = 0
            if uniform(0,100) < 30:
                hotlap = (-1.0)*(((driver.fitness/100)**2)/2)    

        # # # 3.2: Driver Error During the Lap
        incident = uniform(0.01,100.01)
        ERROR = 0
        if self.title == 'Intermediate':
            error_rate = ((driver.consistency * driver.fitness) - 1000)/104.5
        elif self.title == 'Wet':
            error_rate = ((driver.consistency * driver.fitness) - 1000)/97.5
        else:
            error_rate = ((driver.consistency * driver.fitness) - 1000)/90.5
        if incident > error_rate:
            if hotlap == 0:
                ERROR = choice([(incident - error_rate)/10,(incident - error_rate)/25,(incident - error_rate)/50,(incident - error_rate)/75,(incident - error_rate)/100])

        # # # 3.3: Best Track, Best Lap
        if circuit.location in driver.favorite:
            if mode[0] == 'sunday':
                BEST = uniform(0.000,0.200)
            else:
                BEST = 0
        else:
            BEST = 0

        # # # 3.4: Normal Lap
        CRU, CRD = ((driver.consistency-40)/7.5), ((100-driver.consistency)/5)
        SATURDAY, SUNDAY, WET = [], [], []
        for i in np.arange(driver.qualifying_pace()-CRU,driver.qualifying_pace()+CRD,0.01):
            SATURDAY.append(i)
        for j in np.arange(driver.race_pace()-CRU,driver.race_pace()+CRD,0.01):
            SUNDAY.append(j)
        for j in np.arange(driver.wet-CRU,driver.wet+CRD,0.01):
            WET.append(j)

        
        if mode[0] == 'saturday':
            
            if FIA(current)[1] == True:
                drs = 0
            else:
                drs = 0.305
            engine_mode = (1.250 + ((driver.team.powertrain.power)/100))*(-1.0)
            
            if self.title == 'Wet':
                CL2 = ((((choice(WET)/100)**2)*2.25) + hotlap)*(-1.0) + (engine_mode + (0.305*circuit.drs_points)) + (ERROR) - (BEST)
            elif self.title == 'Intermediate':
                CL2 = ((((choice(WET)/100)**2)*2.25) + hotlap)*(-1.0) + (engine_mode + (0.305*circuit.drs_points)) + (ERROR) - (BEST)
            else:
                CL2 = ((((choice(SATURDAY)/100)**2)*0.75) + hotlap)*(-1.0) + (engine_mode + (drs*circuit.drs_points)) + (ERROR) - (BEST)
        elif mode[0] == 'sunday' or 'friday':
            
            if mode[0] == 'friday':
                engine_mode = 1.5
            elif mode[0] == 'sunday':
                if tire_left < 40:
                    engine_mode = (-1.0)*(0.250 + ((driver.team.powertrain.power)/200))
                elif lap == circuit.circuit_laps:
                    engine_mode = (-1.0)*(0.750 + ((driver.team.powertrain.power)/200))
                else:
                    engine_mode = 0.0
            
            if self.title == 'Wet':
                CL2 = ((((choice(WET)/100)**1.50)*2.25) + hotlap)*(-1.0) + (engine_mode + (0.305*circuit.drs_points)) + (ERROR) - (BEST)
            elif self.title == 'Intermediate':
                CL2 = ((((choice(WET)/100)**1.50)*2.25) + hotlap)*(-1.0) + (engine_mode + (0.305*circuit.drs_points)) + (ERROR) - (BEST)
            else:
                CL2 = ((((choice(SUNDAY)/100)**1.75)*2.25) + hotlap)*(-1.0) + (engine_mode + (0.305*circuit.drs_points)) + (ERROR) - (BEST)

        # # # Part 4: The Performance of the Car Design
        if driver.style == 'Stiff Front':
            DRIVING_STYLE = (driver.team.FW - driver.team.RW)/250
        elif driver.style == 'Stiff Rear':
            DRIVING_STYLE = (driver.team.RW - driver.team.RW)/250
        elif driver.style == 'Balanced':
            if (abs(driver.team.FW - driver.team.RW)) > 7:
                DRIVING_STYLE = (((abs(driver.team.FW - driver.team.RW)))/250)*(-1.0)
            else:
                DRIVING_STYLE = ((abs(driver.team.FW - driver.team.RW)))/250
        elif driver.style == 'Unbalanced':
            if (abs(driver.team.FW - driver.team.RW)) > 7:
                DRIVING_STYLE = ((abs(driver.team.FW - driver.team.RW)))/250
            else:
                DRIVING_STYLE = (((abs(driver.team.FW - driver.team.RW)))/250)*(-1.0)
        
        CAR_DESIGN = (((driver.team.weight)*0.03)/1) - (driver.team.concept) - (DRIVING_STYLE)

        # # # Part 5: 5 Lights Reaction
        REACTION = (uniform((((driver.start-15)**2))/10000,(((driver.start+5)**2))/10000) - 0.3)
        STARTING_GRID = ((mode[1]/2.5) - 0.40) - (REACTION*2)
        STARTING_MODE = ((circuit.laptime/25) + STARTING_GRID)

        if mode[0] == 'sunday': 
            if lap == 1:
                return (CL0+(CL1/3)+(CL2/3)) - (BEST) + (STARTING_MODE) + (CAR_DESIGN)
            else:
                return (CL0) + (CL1) + (CL2) - (BEST) + (CAR_DESIGN)
        else:
            return (CL0) + (CL1) + (CL2) - (BEST) + (CAR_DESIGN)

s = Tire('Soft',FIA(current)[4],1.0,1.00)
m = Tire('Medium',FIA(current)[4],1.7,1.017)
h = Tire('Hard',FIA(current)[4],2.4,1.027)
inter = Tire('Intermediate',FIA(current)[4],2.6,1.165)
w = Tire('Wet',FIA(current)[4],3.6,1.265)

# Circuits
class Circuit():
    def __init__(self,location,country,circuit_type,circuit_laps,laptime,tire_life,strategy,drs_points,weather):
        self.location = location
        self.country = country
        self.circuit_type = circuit_type
        self.circuit_laps = circuit_laps
        self.laptime = laptime
        self.tire_life = tire_life
        self.strategy = strategy
        self.drs_points = drs_points
        self.weather = weather

monza = Circuit('Monza','Italy','T1',53,FIA(current)[0]+83.00,29,[[s,h],[m,h],[s,m]],2,['Dry','Dry','Dry','Dry','Dry','Dump','Wet']) # S:21 | M:31 | H:41
mexico = Circuit('México City','México','T1',71,FIA(current)[0]+81.00,42,[[s,m],[m,s],[s,h]],3,['Dry','Dry','Dry','Dry','Dry','Dry','Dry']) # S:28 | M:43 | H:57
miami = Circuit('Miami','United States','T1',57,FIA(current)[0]+91.75,26,[[s,h],[m,h],[s,m]],3,['Dry','Dry','Dry','Dry','Dry','Dry','Dry']) # S:19 | M:28 | H:37
jeddah = Circuit('Jeddah','Saudi Arabia','T1',50,FIA(current)[0]+91.50,16,[[s,s,h],[s,m,m],[s,m,h]],3,['Dry','Dry','Dry','Dry','Dry','Dry','Dry']) # S:13 | M:19 | H:24
sakhir = Circuit('Sakhir','Bahrain','T2',57,FIA(current)[0]+93.50,20,[[s,s,h],[s,m,m],[m,s,m]],3,['Dry','Dry','Dry','Dry','Dry','Dry','Dry']) # S:16 | M:23 | H:29
austin = Circuit('Austin','United States','T2',56,FIA(current)[0]+97.50,26,[[s,h],[m,h],[s,s,m]],2,['Dry','Dry','Dry','Dry','Dry','Dry','Dump']) # S:19 | M:28 | H:37
le = Circuit('Le Castellet','France','T2',53,FIA(current)[0]+94.50,21,[[m,h],[s,s,m],[s,s,h]],2,['Dry','Dry','Dry','Dry','Dry','Dump','Wet']) # S:16 | M:23 | H:31
melbourne = Circuit('Melbourne','Australia','T2',58,FIA(current)[0]+81.50,28,[[s,h],[m,h],[s,s,m]],4,['Dry','Dry','Dry','Dry','Dry','Dump','Wet']) # S:20 | M:30 | H:40
montreal = Circuit('Montréal','Canada','T2',70,FIA(current)[0]+75.00,16,[[m,h,h],[s,s,m,h],[s,s,h,h]],3,['Dry','Dry','Dry','Dry','Dump','Dump','Wet']) # S:13 | M:19 | H:24
silverstone = Circuit('Silverstone','Great Britain','T3',52,FIA(current)[0]+90.00,18,[[m,h],[s,s,m],[s,s,h]],2,['Dry','Dry','Dry','Dump','Dump','Wet','Wet']) # S:14 | M:21 | H:27
spielberg = Circuit('Spielberg','Austuria','T3',71,FIA(current)[0]+68.25,18,[[s,h,h],[m,h,h],[m,m,h]],2,['Dry','Dry','Dry','Dry','Dump','Dump','Wet']) # S:14 | M:21 | H:27
imola = Circuit('Imola','Italy','T3',63,FIA(current)[0]+79.00,36,[[s,h],[m,h],[s,m]],1,['Dry','Dry','Dry','Dry','Dump','Dump','Wet']) # S:25 | M:37 | H:50
suzuka = Circuit('Suzuka','Japan','T3',53,FIA(current)[0]+92.50,21,[[m,h],[s,s,m],[s,s,h]],1,['Dry','Dry','Dry','Dump','Dump','Wet','Wet']) # S:16 | M:23 | H:31
spa = Circuit('Spa-Francorchamps','Belguim','T4',44,FIA(current)[0]+107.00,24,[[s,h],[m,h],[s,m]],2,['Dry','Dry','Dry','Dry','Dump','Wet','Wet']) # S:18 | M:26 | H:35
budapest = Circuit('Budapest','Hungary','T4',70,FIA(current)[0]+80.50,28,[[m,h],[s,s,m],[s,s,h]],1,['Dry','Dry','Dry','Dump','Dump','Wet','Wet']) # S:20 | M:30 | H:40
barcelona = Circuit('Barcelona','Spain','T4',66,FIA(current)[0]+81.75,28,[[m,h],[s,s,m],[s,s,h]],2,['Dry','Dry','Dry','Dry','Dry','Dump','Wet']) # S:20 | M:30 | H:40
zandvoort = Circuit('Zandvoort','Netherlands','T4',72,FIA(current)[0]+73.25,16,[[m,h,h],[s,s,m,h],[s,s,h,h]],2,['Dry','Dry','Dry','Dry','Dump','Dump','Wet']) # S:13 | M:19 | H:24
sao = Circuit('São Paulo','Brazil','T4',71,FIA(current)[0]+74.00,42,[[s,m],[m,s],[s,h]],2,['Dry','Dry','Dry','Dump','Dump','Wet','Wet']) # S:28 | M:43 | H:57
yas = Circuit('Yas Island','Abu Dhabi','T5',58,FIA(current)[0]+86.50,20,[[s,s,h],[s,m,m],[m,s,m]],2,['Dry','Dry','Dry','Dry','Dry','Dry','Dry']) # S:16 | M:23 | H:29
singapore = Circuit('Singapore','Singapore','T5',61,FIA(current)[0]+101.50,20,[[s,s,h],[s,m,m],[m,s,m]],3,['Dry','Dry','Dry','Dump','Dump','Wet','Wet']) # S:16 | M:23 | H:29
baku = Circuit('Baku','Azerbaijan','T5',51,FIA(current)[0]+104.50,21,[[m,h],[s,s,m],[s,s,h]],2,['Dry','Dry','Dry','Dry','Dry','Dry','Dry']) # S:16 | M:23 | H:31
monaco = Circuit('Monte-Carlo','Monaco','T6',78,FIA(current)[0]+74.50,28,[[s,s,h],[s,m,m],[m,s,m]],2,['Dry','Dry','Dry','Dry','Dump','Dump','Wet']) # S:20 | M:30 | H:40

circuits = [monza,mexico,miami,jeddah,
            sakhir,austin,le,melbourne,montreal,
            silverstone,spielberg,imola,suzuka,
            spa,budapest,barcelona,zandvoort,sao,
            yas,singapore,baku,
            monaco]

# Engines
class Engine():
    def __init__(self,brand,fuel,power,reliability):
        self.brand = brand
        self.fuel = fuel
        self.power = power
        self.reliability = reliability

HONDA = Engine('Red Bull Powertrains Honda',FIA(current)[5],94,75)
FERRARI = Engine('Ferrari',FIA(current)[5],91,70)
RENAULT = Engine('Renault',FIA(current)[5],84,70)
MERCEDES = Engine('Mercedes',FIA(current)[5],86,90)

# Crews
class Crew():
    def __init__(self,principal,pit):
        self.name = principal
        self.pit = pit
    def PIT(self):
        if self.pit == 'Perfect':
            limit = 2.50
            failure_odd = 5
        elif self.pit == 'Good':
            limit = 3.00
            failure_odd = 10
        elif self.pit == 'Average':
            limit = 3.50
            failure_odd = 25
        elif self.pit == 'Bad':
            limit = 4.00
            failure_odd = 45
        pitt = []
        for i in list(np.arange(2.00,limit,0.01)):
            pitt.append(i)
        for j in list(np.arange(limit+0.5,(limit*(failure_odd/7)),0.5)):
            pitt.append(j)
        return choice(pitt)

RB = Crew('Christian Horner','Perfect')
SF = Crew('Mattia Binotto','Average')
MER = Crew('Toto Wolff','Good')
MCL = Crew('Andreas Seidl','Perfect')
ALP = Crew('Otmar Szafnauer','Average')
AMR = Crew('Mike Krack','Average')
HAAS = Crew('Guenther Steiner','Good')
ALFA = Crew('Frédéric Vasseur','Good')
AT = Crew('Franz Tost','Good')
WIL = Crew('Jost Capito','Good')

# Manufacturers
class Manufacturer():
    def __init__(self,title,crew,powertrain,front_wing,rear_wing,chassis,brakes,weight,concept,manufacturer_tyre_coeff):
        self.title = title
        self.crew = crew
        self.powertrain = powertrain
        self.FW = front_wing
        self.RW = rear_wing
        self.chassis = chassis
        self.brakes = brakes
        self.weight = weight
        self.concept = concept
        self.manufacturer_tyre_coeff = manufacturer_tyre_coeff
    def rating(self):
        return ((self.powertrain.power*15) + (self.FW*10) + (self.RW*10) + (self.brakes*5) + (self.chassis*10))/50
    def performance(self,circuit_type):
        if circuit_type == 'T1':
            return ((self.powertrain.power*5) + (self.RW*3) + (self.chassis*2))/10
        elif circuit_type == 'T2':
            return ((self.chassis*4) + (self.brakes*4) + (self.RW*2) + (self.powertrain.power))/11
        elif circuit_type == 'T3':
            return ((self.RW*5) + (self.FW*3) + (self.powertrain.power*2))/10
        elif circuit_type == 'T4':
            return ((self.chassis*5) + (self.brakes*3) + (self.RW*2) + (self.powertrain.power))/11
        elif circuit_type == 'T5':
            return ((self.powertrain.power*5) + (self.FW*3) + (self.brakes*2))/10
        elif circuit_type == 'T6':
            return ((self.FW*5) + (self.brakes*3) + (self.chassis*2))/10

# 0.05 sec. improvement for 1 piece of upgrade (overall)
redbull = Manufacturer('Oracle Red Bull Racing',RB,HONDA,86,94,96,91,+10,0.00,0.20)
ferrari = Manufacturer('Scuderia Ferrari',SF,FERRARI,91,94,92,92,0,0.00,0.16)
mercedes = Manufacturer('Mercedes-AMG Petronas F1 Team',MER,MERCEDES,86,86,92,91,0,0.00,0.18)
alpine = Manufacturer('BWT Alpine F1 Team',ALP,RENAULT,82,82,82,82,0,0.00,0.18)
mclaren = Manufacturer('McLaren F1 Team',MCL,MERCEDES,75,86,80,75,0,0.00,0.20)
haas = Manufacturer('Haas F1 Team',HAAS,FERRARI,76,76,76,82,0,0.00,0.17)
astonmartin = Manufacturer('Aston Martin Aramco Cognizant F1 Team',AMR,MERCEDES,76,72,89,72,0,0.00,0.16)
alfaromeo = Manufacturer('Alfa Romeo F1 Team Orlen',ALFA,FERRARI,78,78,72,74,-10,0.00,0.16)
alphatauri = Manufacturer('Scuderia AlphaTauri',AT,HONDA,74,74,74,76,0,0.00,0.16)
williams = Manufacturer('Williams Racing',WIL,MERCEDES,76,76,76,76,0,0.00,0.21)
manufacturers = [redbull,ferrari,mercedes,alpine,mclaren,haas,astonmartin,alfaromeo,alphatauri,williams]

# Drivers
class Driver():
    def __init__(self,team,name,nationality,number,wet,pace,apex,smoothness,adaptability,consistency,fitness,attack,defence,start,favorite,style):
        self.team = team
        self.name = name
        self.nationality = nationality
        self.number = number
        self.wet = wet
        self.pace = pace
        self.apex = apex
        self.smoothness = smoothness
        self.adaptability = adaptability
        self.consistency = consistency
        self.fitness = fitness
        self.attack = attack
        self.defence = defence
        self.start = start
        self.favorite= favorite
        self.style = style
    def qualifying_pace(self):
        return round(((self.pace*5) + (self.apex*2))/7,1)
    def race_pace(self):
        return round(((self.apex*5) + (self.smoothness*2) + (self.adaptability*2) + (self.consistency*2) + (self.fitness*2))/13,1)
    def rating(self):
        return round((self.qualifying_pace() + self.race_pace())/2,1)
    def tire_harm_by_driver(self,tire_usage):
        variable = ((tire_usage) - (pow(10,-3)*pow(self.smoothness,2))) - 2
        if variable >= 0:
            return (variable/2)
        else:
            return 0

mv1 = Driver(redbull,'Max Verstappen','NED',1,96,94,88,92,98,98,98,96,92,84,['México City','Zandvoort','Spielberg','Imola','Spa-Francorchamps'],'Unbalanced')
cl16 = Driver(ferrari,'Charles Leclerc','MNK',16,80,92,94,86,84,94,94,86,82,90,['Monte-Carlo','Spa-Francorchamps','Spielberg','Melbourne','Sakhir'],'Stiff Front')
gr63 = Driver(mercedes,'George Russell','GBR',63,80,92,94,84,84,90,96,86,86,86,[],'Balanced')
ln4 = Driver(mclaren,'Lando Norris','GBR',4,92,92,92,88,88,90,90,81,81,84,['Spielberg','Sakhir'],'Balanced')
lh44 = Driver(mercedes,'Lewis Hamilton','GBR',44,94,90,88,94,94,94,88,92,88,94,['Silverstone','Budapest','São Paulo','Montréal','Yas Island'],'Balanced')
sv5 = Driver(astonmartin,'Sebastian Vettel','GER',5,92,90,90,90,86,90,94,91,93,92,['Singapore','India','Suzuka','Sepang','Valencia'],'Stiff Rear')
fa14 = Driver(alpine,'Fernando Alonso','ESP',14,90,88,88,86,94,96,96,88,96,96,['Budapest','Silverstone','Monza','Barcelona','Valencia'],'Stiff Front')
vb77 = Driver(alfaromeo,'Valtteri Bottas','FIN',75,80,88,90,84,88,92,92,82,91,81,['Sochi'],'Stiff Rear')
sp11 = Driver(redbull,'Sergio Pérez','MEX',11,91,90,86,96,94,86,84,90,96,81,['Baku','Jeddah','Monte-Carlo','Sakhir','Singapore'],'Balanced')
eo31 = Driver(alpine,'Esteban Ocon','FRA',31,86,88,88,84,82,88,88,88,92,86,[],'Balanced')
cs55 = Driver(ferrari,'Carlos Sainz Jr.','ESP',55,88,88,88,80,86,84,90,85,83,79,['Monte-Carlo'],'Balanced')
ls18 = Driver(astonmartin,'Lance Stroll','CAN',18,91,84,86,80,86,86,86,86,86,86,[],'Balanced')
pg10 = Driver(alphatauri,'Pierre Gasly','FRA',10,88,84,84,82,88,80,86,79,77,70,[],'Balanced')
aa23 = Driver(williams,'Alex Albon','THI',23,86,86,81,89,81,81,86,86,75,70,[],'Balanced')
km20 = Driver(haas,'Kevin Magnussen','DEN',20,84,84,84,80,86,84,82,84,80,80,[],'Balanced')
dr3 = Driver(mclaren,'Daniel Ricciardo','AUS',3,86,90,80,76,82,76,68,90,80,82,['Monte-Carlo','Baku','Marina Bay','Shanghai','Budapest'],'Stiff Rear')
yt22 = Driver(alphatauri,'Yuki Tsunoda','JPN',22,76,82,82,80,80,80,76,76,76,70,[],'Balanced')
ms47 = Driver(haas,'Mick Schumacher','GER',47,76,82,82,76,82,76,80,76,70,70,[],'Balanced')
gz24 = Driver(alfaromeo,'Zhou Guanyu','CHN',24,72,80,80,80,76,80,80,76,70,70,[],'Balanced')
nl6 = Driver(williams,'Nicholas Latifi','CAN',6,72,72,72,72,80,72,72,72,72,72,[],'Balanced')

drivers = [mv1,cl16,gr63,ln4,lh44,sv5,fa14,vb77,sp11,eo31,cs55,ls18,pg10,aa23,km20,dr3,yt22,ms47,gz24,nl6]

# # # END OF THE LINE
# # # START

for i in circuits:
    try:
        if i.location == GP:
            CRC = i
    except:
        print(f'No circuit within location named {GP} was found.')

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

print(f'{CRC.location} GP — {CRC.country} | FP forecast: {W1} | Qualifying forecast: {W2} | Race forecast: {W3}\n* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')

# # #
GRID, DNF = {}, {}
def ANALYZER(session,weather,data,tirenamedata,keyword):
    teams_, names_, intervals_, fls_, laps_, tires_ = [], [], [], [], [], []

    for i in list(data.columns):
        # Stage 1
        chart = list(data[i])
        tchart = list(tirenamedata[i])
        
        # Stage 2
        names_.append(i)
        intervals_.append(sum(chart))
        fls_.append(min(chart))
        laps_.append(list(data.index)[chart.index(min(chart))]+1)
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
        else:
            newintervals_.append(round(i - min(intervals_),3))
    df['INTERVAL'] = newintervals_
    # Stage 5
    if keyword == 'race-chart':
        df = df.sort_values('INTERVAL',ascending=True)
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
    elif keyword == 'quali-chart':
        gap = []
        df = df.sort_values('FL. TEMP',ascending=True)
        df = df.drop(axis=1, columns=['INTERVAL','FL. LAP','FL. TIRE'])
        for i in list(df['FL.']):
            leader = (float(list(df['FL.'])[0].split(':')[0])*60) + float(list(df['FL.'])[0].split(':')[1])
            time = (float(i.split(':')[0])*60) + float(i.split(':')[1])
            if i == list(df['FL.'])[0]:
                gap.append('FASTEST')
            else:
                gap.append(f'+{round(time-leader,3)}')
        df['GAP'] = gap
        df['FL. LAP'] = laps_
        df['FL. TIRE'] = tires_
        df = df.reset_index()
        df = df.drop(axis=1, columns=['index', 'FL. TEMP'])

    # Final Alingments
    da = pd.DataFrame()
    da = da.reindex(list(range(1,len(list((df.index)))+1)))
    if session == 'Qualifying':
        df = df.drop(axis=1, columns=['FL. LAP','FL. TIRE'])
    for i in list(df.columns):
        da[i] = list(df[i])
    print(f'{session} Session | {weather} Conditions | {CRC.location} Grand Prix — {CRC.country}')

    # Saving Grid Positions
    if session == 'Qualifying':
        for i,k in zip(list(da['DRIVERS']),list(range(1,len(list(da.index))+1))):
            GRID[i] = k
    gridlist = []
    if session == 'Race':
        for i in list(da['DRIVERS']):
            gridlist.append(GRID[i])
        da['GRID'] = gridlist

    # DNF FL. Optimizing for Race-Chart
    if keyword == 'race-chart':
        dnffloptimizer0, dnffloptimizer1 = [], []
        
        for i,j in zip(list(da['FL. LAP']),list(da['FL.'])):
            if i == 1:
                dnffloptimizer0.append('NaN')
                dnffloptimizer1.append('NaN')
            else:
                dnffloptimizer0.append(int(i))
                dnffloptimizer1.append(j)

        da['FL.'] = dnffloptimizer1
        da['FL. LAP'] = dnffloptimizer0

    # DNF Optimizing for Quali
    optimizing, optimizing0 = [], []
    if keyword == 'quali-chart':
        for i,j in zip(list(da['FL.']),list(da['GAP'])):
            if i == '3:0.0':
                optimizing.append('DNF')
                optimizing0.append(None)
            else:
                optimizing.append(i)
                optimizing0.append(j)
        da['FL.'] = optimizing
        da['GAP'] = optimizing0

    print(da)

    # FL Alignment
    if keyword == 'race-chart':
        try:
            topg = min(fls_)
            integer0 = topg//60
            decimal0 = str(topg-(integer0*60))[0:6]
            actualtopg = str(int(integer0)) +':'+ decimal0
            fldriver = list(da['DRIVERS'])[list(da['FL.']).index(actualtopg)]
            print(f'\nFastest Lap | {fldriver} has recorded {actualtopg} on this track.')
        except:
            print(f'\nFastest Lap | No fastest lap has recorded on this track.')

# # #

def FP(circuit,tireset,stage):
    data,tirenamedata,c = pd.DataFrame(),pd.DataFrame(),1
    for driver in drivers:
        if W1 == 'Dry':
            tlist = []
            for i in tireset[driver.name]:
                tlist.append(i)
        elif W1 == 'Dump':
            tlist = [inter,inter,inter,inter,inter]
        elif W1 == 'Wet':
            tlist = [w,w,w,w,w]
        tire = tlist[0]
        tire_usage = 0
        lap_chart, tire_chart = [], []
        for lap in range(1,circuit.circuit_laps+1):
            tire_left = tire.tire_left(driver,circuit,tire_usage)
            current_laptime = round(tire.laptime(driver,circuit,lap,tire_usage,['friday',0]),3)
            if tire_left < 25:
                if len(tlist) == 1:
                    lap_chart.append(current_laptime)
                    tire_chart.append(tire.title[0])
                    tire_usage += 1
                else:
                    if lap + 10 > circuit.circuit_laps+1:
                        lap_chart.append(current_laptime)
                        tire_chart.append(tire.title[0])
                        tire_usage += 1
                    else:
                        tire_usage = 0
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
        c += 1
        data[driver.name], tirenamedata[driver.name] = lap_chart, tire_chart
        if stage == 1:
            FP1RESULT[driver.name] = sum(lap_chart)
        elif stage == 2:
            FP2RESULT[driver.name] = sum(lap_chart)
        elif stage == 3:
            FP3RESULT[driver.name] = sum(lap_chart)
    # Analyzing
    ANALYZER(f'Free Practice {stage}',W1,data,tirenamedata,'quali-chart')

# # #

def Q(circuit):
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
                mechanic_failure_odd = ((((((((driver.team.powertrain.reliability+reliability_defict)*(-1.0))**3)/60000)+17))/1.7)**3) > uniform(0,75000)
                
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
                    lap_chart.append(180.0)
                    tire_chart.append(tire.title[0])
                    tire_usage += 0
                else:
                    if mechanic_failure_odd == True:
                        print(f'DNF | {driver.name} has forced to retire due to {choice(FAILURES)} issue. Disaster for {driver.team.title}!')
                        lap_chart.append(180.0)
                        tire_chart.append(tire.title[0])
                        tire_usage += 0
                        DNF[driver.name].append(True)
                    elif driver_error_odd == True:
                        print(f'DNF | {driver.name} {choice(ERRORS)} and, he is OUT! Disaster for {driver.team.title}!')
                        lap_chart.append(180.0)
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
                                print(f'INC | Oh, no! {driver.name} has spun-round. He has lost couple seconds.')
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
    # Analyzing
    ANALYZER('Qualifying',W2,data,tirenamedata,'quali-chart')

# # #

def R(circuit,FP1,FP2,FP3):
    # Stage 1: Strategy Definition
    chart = {}
    for i in drivers:
        chart[i.name] = [FP1[i.name],FP2[i.name],FP3[i.name]]
        tireset = (chart[i.name].index(min(chart[i.name]))) + 1
        if tireset == 1:
            STRATEGIES[i.name] = circuit.strategy[0]
        elif tireset == 2:
            STRATEGIES[i.name] = circuit.strategy[1]
        elif tireset == 3:
            STRATEGIES[i.name] = circuit.strategy[2]
    # Stage 2: Racing Alogirthm
    data,tirenamedata,c = pd.DataFrame(),pd.DataFrame(),1
    for driver in drivers:
        if W3 == 'Dry':
            tlist = []
            for i in STRATEGIES[driver.name]:
                tlist.append(i)
        elif W3 == 'Dump':
            tlist = [inter,inter,inter,inter,inter]
        elif W3 == 'Wet':
            tlist = [w,w,w,w,w]
        tire = tlist[0]
        tire_usage = 0
        lap_chart, tire_chart = [], []
        for lap in range(1,circuit.circuit_laps+1):
            tire_left = tire.tire_left(driver,circuit,tire_usage)
            current_laptime = round(tire.laptime(driver,circuit,lap,tire_usage,['sunday',GRID[driver.name]]),3)

            reliability_defict = driver.team.powertrain.fuel.vulnerability
            mechanic_failure_odd = ((((((((driver.team.powertrain.reliability+reliability_defict)*(-1.0))**3)/60000)+17))/1.7)**3) > uniform(0,75000)
            
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
                lap_chart.append((circuit.laptime + 5)*2)
                tire_chart.append(tire.title[0])
                tire_usage += 0
            else:
                if mechanic_failure_odd == True:
                    print(f'DNF | Lap {lap} | {driver.name} has forced to retire due to {choice(FAILURES)} issue. Disaster for {driver.team.title}!')
                    lap_chart.append((circuit.laptime + 5)*2)
                    tire_chart.append(tire.title[0])
                    tire_usage += 0
                    DNF[driver.name].append(True)
                elif driver_error_odd == True:
                    print(f'DNF | Lap {lap} | {driver.name} {choice(ERRORS)} and, he is OUT! Disaster for {driver.team.title}!')
                    lap_chart.append((circuit.laptime + 5)*2)
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
                            if lap + 10 > circuit.circuit_laps+1:
                                lap_chart.append(current_laptime)
                                tire_chart.append(tire.title[0])
                                tire_usage += 1
                            else:
                                tire_usage = 0
                                tlist.pop(0)
                                tire = tlist[0]
                                pit_stop = round(driver.team.crew.PIT(),3)
                                if 10 > pit_stop >= 5.0:
                                    print(f'PIT | Lap {lap} | Bad news for {driver.team.title}! {pit_stop} secs. for {driver.name}')
                                elif pit_stop >= 10:
                                    print(f'PIT | Lap {lap} | Disaster for {driver.team.title}! {pit_stop} secs. for {driver.name}')
                                lap_chart.append(current_laptime + pit_stop + 20)
                                tire_chart.append(tire.title[0])
                                tire_usage += 1
                    else:
                        if driver_error_odd_2:
                            print(f'INC | Lap {lap} | Oh, no! {driver.name} has spun-round. He has lost couple seconds.')
                            lap_chart.append(current_laptime + 12.5)
                            tire_chart.append(tire.title[0])
                            tire_usage += 5
                        else:
                            lap_chart.append(current_laptime)
                            tire_chart.append(tire.title[0])
                            tire_usage += 1
        c += 1
        data[driver.name], tirenamedata[driver.name] = lap_chart, tire_chart
    print('* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')
    ANALYZER(f'Race',W3,data,tirenamedata,'race-chart')

# # # Action

FP1STRATEGY, FP2STRATEGY, FP3STRATEGY = {}, {}, {}
FP1RESULT, FP2RESULT, FP3RESULT = {}, {}, {}

for i in drivers:
    FP1STRATEGY[i.name] = CRC.strategy[0]
    FP2STRATEGY[i.name] = CRC.strategy[1]
    FP3STRATEGY[i.name] = CRC.strategy[2]

FP(CRC,FP1STRATEGY,1)
print('* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')
FP(CRC,FP2STRATEGY,2)
print('* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')
FP(CRC,FP3STRATEGY,3)
print('* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')

DNF = {}
for i in drivers:
    DNF[i.name] = [None]

Q(CRC)
print('* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')

STRATEGIES = {}
DNF = {}
for i in drivers:
    DNF[i.name] = [None]

R(CRC,FP1RESULT,FP2RESULT,FP3RESULT)
print('* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')

# # #
# Missing Attribitues for v1.0
# No tire set limitation for each weekend.
# No changable weather conditions for each session.

# to-do
# real-time racing / invert for loop for racing function.
# safety car.
# emergency pit / safety car pit.