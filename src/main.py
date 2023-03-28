from math import pow
from random import uniform, choice, shuffle
import numpy as np
import pandas as pd

# GP
GP = 'Jeddah'

# DRS Rule
DRS_RULE = True

# FIA
current = '2022'
def FIA(current):
    if current == '2005':
        return 11.0
    elif current == '2006':
        return 12.5
    elif current == '2007':
        return 13.5
    elif current == '2008':
        return 14.0
    elif current == '2009':
        return 13.5
    elif current == '2014':
        return 14.0
    elif current == '2017':
        return 10.0
    elif current == '2018':
        return 9.0
    elif current == '2021':
        return 10.0
    elif current == '2022':
        return 10.5
    elif current == '2026':
        return None

# Failures
FAILURES = ['Gearbox','Engine','Clutch','Driveshaft','Throttle','Brakes','Handling','Puncture','Wheel','Suspension','Steering','Electronics','Hydraulics',
            'Water Leak','Fuel Pressure','Oil Pressure','Exhaust','Differential','Vibration','Halfshaft','Transmission','Alternator','Cooling']

ERRORS = ['Spun-off','Stuck in Gravel', 'Went through Barriers','Damaged his Suspension']

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
        if self.supplier == 'Pirelli':
            tire_supplier_pace = -0.2
            tire_supplier_durability = -2
        elif self.supplier == 'Bridgestone':
            tire_supplier_pace = 0.2
            tire_supplier_durability = 2

        if driver.team.oil == 'Shell':
            fuel_supplier_pace = -0.2
        elif driver.team.oil == 'Petronas':
            fuel_supplier_pace = 0.0
        elif driver.team.oil == 'Aramco':
            fuel_supplier_pace = 0.2

        fuel_left = self.fuel_left(circuit,lap)
        tire_left = self.tire_left(driver,circuit,tire_usage) + tire_supplier_durability
        tire_heat = ((((10*driver.team.manufacturer_tyre_coeff)**2)-3))/7.5
        special_function_for_tire = ((pow(1.022,(100-tire_left)))-1)
        special_function_for_fuel = (fuel_left**(fuel_left/(fuel_left*1.9)))

        if tire_left > 92.5:
            if mode[0] == 'sunday':
                tire_cold = (1.350 - ((100-tire_left)/10))
            else:
                tire_cold = 0.0
        else:
            tire_cold = 0.0

        if tire_left < 45.0:
            if mode[0] == 'sunday':
                tire_cold = -0.650
            else:
                tire_cold = 0.0
        else:
            tire_cold = 0.0

        CL0 = (circuit.laptime * self.laptime_coefficient) + (special_function_for_tire) + (special_function_for_fuel) + (tire_heat + tire_cold) + (tire_supplier_pace) + (fuel_supplier_pace)
    
        # # # Part 2: The Performance of the Car
        if mode[0] == 'saturday':
            performance = ((driver.team.performance(circuit.circuit_type))*0.65) + (driver.team.rating()*0.35)
            CL1 = ((((performance/100)**2)*6.0) - 4)*(-1.0)
        elif mode[0] == 'sunday':
            performance = ((driver.team.performance(circuit.circuit_type))*1.00)
            CL1 = ((((performance/100)**2)*8.0) - 4)*(-1.0)
        
        # # # Part 3: The Performance of the Driver
        # # # 3.1: Purple Lap
        if mode[0] == 'sunday':
            hotlap = 0
            if uniform(0,100) < 10:
                hotlap = (-1.0)*(((driver.fitness/100)**2)/2)
        else:
            hotlap = 0
            if uniform(0,100) < 30:
                hotlap = (-1.0)*(((driver.fitness/100)**2)/2)    

        # # # 3.2: Driver Minor Error Thru' Lap
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

        # # # 3.3: Normal Lap
        CRU, CRD = ((driver.consistency-40)/7.5), ((100-driver.consistency)/5)
        SATURDAY, SUNDAY, WET = [], [], []
        for i in np.arange(driver.qualifying_pace()-CRU,driver.qualifying_pace()+CRD,0.01):
            SATURDAY.append(i)
        for j in np.arange(driver.race_pace()-CRU,driver.race_pace()+CRD,0.01):
            SUNDAY.append(j)
        for j in np.arange(driver.wet-CRU,driver.wet+CRD,0.01):
            WET.append(j)

        if mode[0] == 'saturday':
            if DRS_RULE == True:
                drs = 0
            else:
                drs = 0.305
            engine_mode = (1.250 + ((driver.team.ice)/100))*(-1.0)
            if self.title == 'Wet':
                CL2 = ((((choice(WET)/100)**2)*2.5) + hotlap)*(-1.0) + (engine_mode + (0.305*circuit.drs_points))
            elif self.title == 'Intermediate':
                CL2 = ((((choice(WET)/100)**2)*2.5) + hotlap)*(-1.0) + (engine_mode + (0.305*circuit.drs_points))
            else:
                CL2 = ((((choice(SATURDAY)/100)**2)*1.0) + hotlap)*(-1.0) + (engine_mode + (drs*circuit.drs_points))
        elif mode[0] == 'sunday':
            if tire_left < 40:
                engine_mode = 0.0
            elif lap == circuit.circuit_laps:
                engine_mode = (-1.0)*(0.750 + ((driver.team.ice)/200))
            else:
                engine_mode = 0.5
            if self.title == 'Wet':
                CL2 = ((((choice(WET)/100)**2)*2.5) + hotlap)*(-1.0) + (engine_mode + (0.305*circuit.drs_points))
            elif self.title == 'Intermediate':
                CL2 = ((((choice(WET)/100)**2)*2.5) + hotlap)*(-1.0) + (engine_mode + (0.305*circuit.drs_points))
            else:
                CL2 = ((((choice(SUNDAY)/100)**2)*2.5) + hotlap)*(-1.0) + (engine_mode + (0.305*circuit.drs_points))

        # # # 3.3: The Best Track
        if circuit.location in driver.favorite:
            BEST = uniform(0.050,0.200)
        else:
            BEST = 0

        # # # 3.4: Final Resume
        REACTION = (uniform((((driver.start-15)**2))/10000,(((driver.start+5)**2))/10000) - 0.3)
        STARTING_GRID = ((mode[1]/2.5) - 0.40) - (REACTION*2)
        STARTING_MODE = ((circuit.laptime/25) + STARTING_GRID)

        if mode[0] == 'sunday': 
            if lap == 1:
                return (CL0+(CL1/3)+(CL2/3)) - (BEST) + (STARTING_MODE) - driver.team.concept + (ERROR)
            else:
                return (CL0+CL1+CL2) - (BEST) - driver.team.concept + (ERROR)
        else:
            return (CL0+CL1+CL2) - (BEST) - driver.team.concept + (ERROR)

s = Tire('Soft','Pirelli',1.0,1.00)
m = Tire('Medium','Pirelli',1.7,1.017)
h = Tire('Hard','Pirelli',2.4,1.027)
inter = Tire('Intermediate','Pirelli',2.6,1.165)
w = Tire('Wet','Pirelli',3.6,1.265)

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

monza = Circuit('Monza','Italy','T1',53,FIA(current)+73.50,29,[[s,m],[s,h],[m,s]],2,['Dry','Dry','Dry','Dry','Dry','Dump','Wet']) # S:21 | M:31 | H:41
miami = Circuit('Miami','United States','T1',57,FIA(current)+81.50,26,[[m,h],[s,h],[s,m]],3,['Dry','Dry','Dry','Dry','Dry','Dry','Dry']) # S:19 | M:28 | H:37
jeddah = Circuit('Jeddah','Saudi Arabia','T1',50,FIA(current)+81.00,16,[[m,s,h],[s,s,h],[s,m,h]],3,['Dry','Dry','Dry','Dry','Dry','Dry','Dry']) # S:13 | M:19 | H:24
spa = Circuit('Spa-Francorchamps','Belguim','T2',44,FIA(current)+97.00,24,[[s,m],[s,h],[m,h]],2,['Dry','Dry','Dry','Dry','Dump','Wet','Wet']) # S:18 | M:26 | H:35
sakhir = Circuit('Sakhir','Bahrain','T2',57,FIA(current)+83.50,20,[[s,s,h],[s,m,m],[m,s,m]],3,['Dry','Dry','Dry','Dry','Dry','Dry','Dry']) # S:16 | M:23 | H:29
austin = Circuit('Austin','United States','T3',56,FIA(current)+87.00,26,[[s,s,s,s,s],[m,m,m,m,m],[h,h,h,h,h]],2,['Dry','Dry','Dry','Dry','Dry','Dry','Dump'])
le = Circuit('Le Castellet','France','T2',53,FIA(current)+84.00,16,[[s,s,s,s,s],[m,m,m,m,m],[h,h,h,h,h]],2,['Dry','Dry','Dry','Dry','Dry','Dump','Wet'])
imola = Circuit('Imola','Italy','T3',63,FIA(current)+69.25,26,[[s,s,s,s,s],[m,m,m,m,m],[h,h,h,h,h]],1,['Dry','Dry','Dry','Dry','Dump','Dump','Wet'])
melbourne = Circuit('Melbourne','Australia','T2',58,FIA(current)+70.50,16,[[s,s,s,s,s],[m,m,m,m,m],[h,h,h,h,h]],4,['Dry','Dry','Dry','Dry','Dump','Dump','Wet'])
montreal = Circuit('Montréal','Canada','T2',70,FIA(current)+63.00,16,[[s,s,s,s,s],[m,m,m,m,m],[h,h,h,h,h]],3,['Dry','Dry','Dry','Dry','Dump','Dump','Wet'])
silverstone = Circuit('Silverstone','Great Britain','T3',52,FIA(current)+79.50,26,[[s,s,s,s,s],[m,m,m,m,m],[h,h,h,h,h]],2,['Dry','Dry','Dry','Dump','Dump','Wet','Wet'])
suzuka = Circuit('Suzuka','Japan','T3',53,FIA(current)+82.50,16,[[s,s,s,s,s],[m,m,m,m,m],[h,h,h,h,h]],1,['Dry','Dry','Dry','Dump','Dump','Wet','Wet'])
spielberg = Circuit('Spielberg','Austuria','T3',71,FIA(current)+58.00,26,[[s,s,s,s,s],[m,m,m,m,m],[h,h,h,h,h]],2,['Dry','Dry','Dry','Dry','Dump','Dump','Wet'])
budapest = Circuit('Budapest','Hungary','T4',70,FIA(current)+70.00,30,[[s,s,s,s,s],[m,m,m,m,m],[h,h,h,h,h]],1,['Dry','Dry','Dry','Dump','Dump','Wet','Wet'])
barcelona = Circuit('Barcelona','Spain','T4',66,FIA(current)+71.50,26,[[s,s,s,s,s],[m,m,m,m,m],[h,h,h,h,h]],2,['Dry','Dry','Dry','Dry','Dry','Dump','Wet'])
zandvoort = Circuit('Zandvoort','Netherlands','T4',72,FIA(current)+63.50,26,[[s,s,s,s,s],[m,m,m,m,m],[h,h,h,h,h]],2,['Dry','Dry','Dry','Dry','Dump','Dump','Wet'])
mexico = Circuit('México City','México','T4',71,FIA(current)+70.50,39,[[s,s,s,s,s],[m,m,m,m,m],[h,h,h,h,h]],3,['Dry','Dry','Dry','Dry','Dry','Dry','Dry'])
sao = Circuit('São Paulo','Brazil','T4',71,FIA(current)+63.50,26,[[s,s,s,s,s],[m,m,m,m,m],[h,h,h,h,h]],2,['Dry','Dry','Dry','Dump','Dump','Wet','Wet'])
yas = Circuit('Yas Island','Abu Dhabi','T5',58,FIA(current)+77.00,22,[[s,s,s,s,s],[m,m,m,m,m],[h,h,h,h,h]],2,['Dry','Dry','Dry','Dry','Dry','Dry','Dry'])
singapore = Circuit('Singapore','Singapore','T5',61,FIA(current)+91.00,26,[[s,s,s,s,s],[m,m,m,m,m],[h,h,h,h,h]],3,['Dry','Dry','Dry','Dump','Dump','Wet','Wet'])
baku = Circuit('Baku','Azerbaijan','T5',51,FIA(current)+94.50,12,[[s,s,s,s,s],[m,m,m,m,m],[h,h,h,h,h]],2,['Dry','Dry','Dry','Dry','Dry','Dry','Dump'])
monaco = Circuit('Monte-Carlo','Monaco','T6',78,FIA(current)+63.50,16,[[s,s,s,s,s],[m,m,m,m,m],[h,h,h,h,h]],2,['Dry','Dry','Dry','Dry','Dump','Dump','Wet'])

circuits = [monza,miami,jeddah,
            spa,sakhir,austin,le,imola,melbourne,montreal,
            silverstone,suzuka,spielberg,
            budapest,barcelona,zandvoort,mexico,sao,
            yas,singapore,baku,
            monaco]

# Engines
class Engine():
    def __init__(self,brand,fuel,ice,mgu_k,mgu_h):
        self.brand = brand
        self.fuel = fuel
        self.ice = ice
        self.mgu_k = mgu_k
        self.mgu_h = mgu_h
        self.power = (self.ice + (self.mgu_k/2) + (self.mgu_h/2))/2

HONDA = Engine('Red Bull Powertrains Honda','Aramco',92,92,92)
FERRARI = Engine('Ferrari','Aramco',90,90,90)
RENAULT = Engine('Renault','Aramco',84,84,84)
MERCEDES = Engine('Mercedes','Aramco',86,86,86)

# Teams
class Crew():
    def __init__(self,principal,strategy,pit):
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

RB = Crew('Christian Horner','Perfect','Perfect')
SF = Crew('Mattia Binotto','Bad','Bad')
MER = Crew('Toto Wolff','Bad','Average')
MCL = Crew('Andreas Seidl','Good','Good')
ALP = Crew('Otmar Szafnauer','Good','Good')
AMR = Crew('Mike Krack','Average','Average')
HAAS = Crew('Guenther Steiner','Average','Average')
ALFA = Crew('Frédéric Vasseur','Good','Average')
AT = Crew('Franz Tost','Good','Good')
WIL = Crew('Jost Capito','Perfect','Good')

# Manufacturers
class Manufacturer():
    def __init__(self,title,crew,powertrain,aero,chassis,brakes,reliability,concept,manufacturer_tyre_coeff):
        self.title = title
        self.crew = crew
        self.oil = powertrain.fuel
        self.supplier = powertrain.brand
        self.ice = powertrain.ice
        self.power = powertrain.power
        self.aero = aero
        self.chassis = chassis
        self.brakes = brakes
        self.reliability = reliability
        self.concept = concept
        self.manufacturer_tyre_coeff = manufacturer_tyre_coeff
    def rating(self):
        return ((self.power*14) + (self.aero*10) + (self.brakes*5) + (self.chassis*10) + (self.reliability))/40
    def performance(self,circuit_type):
        if circuit_type == 'T1':
            return ((self.power*6) + (self.chassis*2) + (self.aero*2))/10
        elif circuit_type == 'T2':
            return ((self.aero*6) + (self.brakes*3) + (self.power*2))/10
        elif circuit_type == 'T3':
            return ((self.aero*4) + (self.chassis*4) + (self.power*2))/10
        elif circuit_type == 'T4':
            return ((self.chassis*5) + (self.aero*3) + (self.power*2))/10
        elif circuit_type == 'T5':
            return ((self.power*5) + (self.brakes*3) + (self.aero*2))/10
        elif circuit_type == 'T6':
            return ((self.brakes*5) + (self.chassis*3) + (self.aero*2))/10

redbull = Manufacturer('Oracle Red Bull Racing',RB,HONDA,91,92,91,75,0.00,0.22)
ferrari = Manufacturer('Scuderia Ferrari',SF,FERRARI,92,91,91,70,0.00,0.16)
mercedes = Manufacturer('Mercedes-AMG Petronas F1 Team',MER,MERCEDES,86,94,86,95,0.00,0.19)
mclaren = Manufacturer('McLaren F1 Team',MCL,MERCEDES,82,86,75,90,0.00,0.20)
alpine = Manufacturer('BWT Alpine F1 Team',ALP,RENAULT,80,82,86,70,0.00,0.18)
haas = Manufacturer('Haas F1 Team',HAAS,FERRARI,79,72,79,80,0.00,0.17)
astonmartin = Manufacturer('Aston Martin Aramco Cognizant F1 Team',AMR,MERCEDES,74,84,74,85,0.00,0.16)
alfaromeo = Manufacturer('Alfa Romeo F1 Team Orlen',ALFA,FERRARI,76,72,74,90,0.00,0.16)
alphatauri = Manufacturer('Scuderia AlphaTauri',AT,HONDA,76,72,72,70,0.00,0.16)
williams = Manufacturer('Williams Racing',WIL,MERCEDES,74,74,80,85,0.00,0.21)
manufacturers = [redbull,ferrari,mercedes,mclaren,alpine,haas,astonmartin,alfaromeo,alphatauri,williams]

# Drivers
class Driver():
    def __init__(self,team,name,nationality,number,wet,pace,apex,smoothness,adaptability,consistency,fitness,attack,defence,start,favorite):
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
    def qualifying_pace(self):
        return ((self.pace*5) + (self.apex*2))//7
    def race_pace(self):
        return ((self.apex*5) + (self.smoothness*2) + (self.adaptability*2) + (self.consistency*2) + (self.fitness*2))//13
    def rating(self):
        return (self.qualifying_pace() + self.race_pace())//2
    def tire_harm_by_driver(self,tire_usage):
        variable = ((tire_usage) - (pow(10,-3)*pow(self.smoothness,2))) - 2
        if variable >= 0:
            return (variable/2)
        else:
            return 0

cl16 = Driver(ferrari,'Charles Leclerc','MNK',16,80,95,95,85,87,90,84,86,82,90,['Monte-Carlo','Sakhir','Spielberg','Spa-Francorchamps','Singapore'])
cs55 = Driver(ferrari,'Carlos Sainz Jr.','ESP',55,84,88,88,80,86,89,89,85,83,79,['Monte-Carlo'])
mv1 = Driver(redbull,'Max Verstappen','NED',1,96,93,93,85,94,94,96,94,90,84,['México City','Zandvoort','Spielberg','Imola','São Paulo'])
sp11 = Driver(redbull,'Sergio Pérez','MEX',11,88,85,89,95,87,86,79,89,95,81,['Baku','Jeddah','Monte-Carlo','Sakhir','Singapore'])
lh44 = Driver(mercedes,'Lewis Hamilton','GBR',44,96,93,91,92,94,90,91,91,88,94,['Silverstone','Budapest','São Paulo','Montréal','Yas Island'])
gr63 = Driver(mercedes,'George Russell','GBR',63,84,91,94,80,86,90,96,86,86,86,[])
fa14 = Driver(alpine,'Fernando Alonso','ESP',14,92,91,86,92,92,94,95,88,96,96,['Budapest','Silverstone','Monza','Barcelona','Valencia'])
eo31 = Driver(alpine,'Esteban Ocon','FRA',31,88,87,88,81,82,88,88,88,92,86,[])
km20 = Driver(haas,'Kevin Magnussen','DEN',20,88,84,84,80,86,85,82,85,80,81,[])
ms47 = Driver(haas,'Mick Schumacher','GER',47,77,79,77,76,81,75,80,75,70,70,[])
vb77 = Driver(alfaromeo,'Valtteri Bottas','FIN',77,75,91,90,84,79,90,93,82,91,81,['Sochi'])
gz24 = Driver(alfaromeo,'Zhou Guanyu','CHN',24,72,75,75,80,77,79,77,75,70,70,[])
pg10 = Driver(alphatauri,'Pierre Gasly','FRA',10,84,88,89,82,80,86,85,79,77,70,[])
ys22 = Driver(alphatauri,'Yuki Tsunoda','JPN',22,75,77,75,75,75,80,72,72,72,70,[])
ln4 = Driver(mclaren,'Lando Norris','GBR',4,91,91,91,86,86,90,91,81,81,84,['Spielberg','Sakhir'])
dr3 = Driver(mclaren,'Daniel Ricciardo','AUS',3,80,79,84,84,82,81,75,90,79,81,['Monte-Carlo','Baku','Marina Bay','Shanghai','Budapest'])
sv5 = Driver(astonmartin,'Sebastian Vettel','GER',5,94,94,92,92,87,89,86,91,93,92,['Singapore','India','Suzuka','Sepang','Valencia'])
ls18 = Driver(astonmartin,'Lance Stroll','CAN',18,91,84,86,80,86,85,89,85,89,86,[])
aa23 = Driver(williams,'Alex Albon','THI',23,86,86,81,89,85,82,87,85,75,70,[])
nl6 = Driver(williams,'Nicholas Latifi','CAN',6,72,72,72,72,80,72,72,72,72,72,[])

drivers = [cl16,cs55,mv1,sp11,lh44,gr63,fa14,eo31,km20,ms47,vb77,gz24,pg10,ys22,ln4,dr3,sv5,ls18,aa23,nl6]

# # # END OF THE LINE!
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

    # Final Stage
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

    print(da)

    if keyword == 'race-chart':
        fldriver = list(da['DRIVERS'])[list(da['FL.']).index(min(list(da['FL.'])))]
        print(f'\nFastest Lap | {fldriver} has recorded {min(list(da["FL."]))} on this track.')

# # #

FP1STRATEGY, FP2STRATEGY, FP3STRATEGY = {}, {}, {}
FP1RESULT, FP2RESULT, FP3RESULT = {}, {}, {}

for i in drivers:
    FP1STRATEGY[i.name] = CRC.strategy[0]
    FP2STRATEGY[i.name] = CRC.strategy[1]
    FP3STRATEGY[i.name] = CRC.strategy[2]

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
            current_laptime = round(tire.laptime(driver,circuit,lap,tire_usage,['sunday',0]),3)
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
            chance = 0
            tire = tlist[0]
            tire_usage = 0
            lap_chart, tire_chart = [], []
            for lap in range(circuit.circuit_laps,circuit.circuit_laps+1):
                tire_left = tire.tire_left(driver,circuit,tire_usage)
                current_laptime = round(tire.laptime(driver,circuit,lap,tire_usage,['saturday',0]),3)
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
STRATEGIES = {}

for i in drivers:
    DNF[i.name] = [None]

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
            mechanic_failure_odd = (((((((driver.team.reliability*(-1.0))**3)/60000)+17))/1.7)**3) > uniform(0,75000)
            
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
                    print(f'{lap}/{circuit.circuit_laps} | Disaster for {driver.team.title}! {driver.name} has forced to retire due to {choice(FAILURES)} issue.')
                    lap_chart.append((circuit.laptime + 5)*2)
                    tire_chart.append(tire.title[0])
                    tire_usage += 0
                    DNF[driver.name].append(True)
                elif driver_error_odd == True:
                    print(f'{lap}/{circuit.circuit_laps} | Disaster for {driver.team.title}! {driver.name} {choice(ERRORS)}, he is OUT!')
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
                                if pit_stop >= 5.5:
                                    print(f'{lap}/{circuit.circuit_laps} | Bad news for {driver.team.title}! {pit_stop} secs. pit-stop for {driver.name}')
                                lap_chart.append(current_laptime + pit_stop + 20)
                                tire_chart.append(tire.title[0])
                                tire_usage += 1
                    else:
                        if driver_error_odd_2:
                            print(f'{lap}/{circuit.circuit_laps} | Oh, no! {driver.name} has spun-round.')
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
    ANALYZER(f'Race',W1,data,tirenamedata,'race-chart')

# # #

FP(CRC,FP1STRATEGY,1)
print('* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')
FP(CRC,FP2STRATEGY,2)
print('* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')
FP(CRC,FP3STRATEGY,3)
print('* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')
Q(CRC)
print('* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')
R(CRC,FP1RESULT,FP2RESULT,FP3RESULT)
print('* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')

# # #
# Missing Attribitues
# No tire set limitation for each weekend.
# No changable weather conditions for each session.

# to-do
# Yarış kısmında sürücü-tur değil tur-sürücü for döngüsü kullanılacak.
# Yarış kısmında gerçek zamanlı trafik, kazalar, kapışma vs. eklenecek.
# Safety car eklenecek.
# Acil pit eklenecek.