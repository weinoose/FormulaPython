def upgrade(engineer_crew,designer,cto,aerodynamicst,min_budget,max_budget,spent_budget):
    # budget unit is million.
    min_point = ((((designer*5) + (cto*3) + (aerodynamicst*2))/10)/110)
    max_point = ((((designer*5) + (cto*3) + (aerodynamicst*2))/10)/90)
    
    limit = max_budget - min_budget
    spent = (spent_budget + 0.1) - min_budget

    from random import uniform
    phase_1 = uniform(min_point,max_point)    
    phase_2 = (spent/limit) + 0.5

    if engineer_crew == 'Perfect':
        phase_3 = uniform(0.35,0.75)
    elif engineer_crew == 'Good':
        phase_3 = uniform(0.10,0.50)
    elif engineer_crew == 'Average':
        phase_3 = uniform(-0.15,0.25)
    elif engineer_crew == 'Bad':
        phase_3 = uniform(0.00,0.40)*(-1.0)
    elif engineer_crew == 'Very Bad':
        phase_3 = uniform(0.25,0.60)*(-1.0)

    return ((((round(((phase_1) + (phase_2) + (phase_3)),3))*1.417)**1.3)/1.3)

def design(designer_name,designer,cto,aerodynamicst,focus,focus_r,min_budget,max_budget,spent_budget,engineer_crew,pit_package,FW_R,RW_R,chassis_R,base_R,sidepod_R,suspension_R): 
    # budgest unit is million.
    
    from random import uniform, choice
    limit = max_budget - min_budget
    spent = (spent_budget + 0.1) - min_budget
    phase_1 = ((spent/limit) + 0.5)*13.75

    if engineer_crew == 'Perfect':
        phase_3 = uniform(2.50,5.00)
    elif engineer_crew == 'Good':
        phase_3 = uniform(0.50,2.49)
    elif engineer_crew == 'Average':
        phase_3 = uniform(0.00,0.49)
    elif engineer_crew == 'Bad':
        phase_3 = uniform(0.50,2.49)*(-1.0)
    elif engineer_crew == 'Very Bad':
        phase_3 = uniform(2.50,5.00)*(-1.0)

    if focus == 'Front Stiff': 
        FW = 45 + phase_1 + phase_3 +  uniform(((((designer*4.5) + (cto*2.5) + (aerodynamicst*4.5))/50))-5.5,((((designer*4.5) + (cto*2.5) + (aerodynamicst*4.5))/50))+5.5) + FW_R
        RW = 45 + phase_1 + phase_3 +  uniform(((((designer*3.5) + (cto*1.5) + (aerodynamicst*3.5))/50))-5.5,((((designer*3.5) + (cto*1.5) + (aerodynamicst*3.5))/50))+5.5) + RW_R
        CHASSIS = 45 + phase_1 + phase_3 +  uniform(((((designer*4.5) + (cto*4.5) + (aerodynamicst*2.5))/50))-5.5,((((designer*4.5) + (cto*4.5) + (aerodynamicst*2.5))/50))+5.5) + chassis_R
        BASE = 45 + phase_1 + phase_3 +  uniform(((((designer*4) + (cto*3) + (aerodynamicst*3))/50))-5.5,((((designer*4) + (cto*3) + (aerodynamicst*3))/50))+5.5) + base_R
        SIDEPOD = 45 + phase_1 + phase_3 +  uniform(((((designer*5) + (cto*3) + (aerodynamicst*2))/50))-5.5,((((designer*5) + (cto*3) + (aerodynamicst*2))/50))+5.5) + sidepod_R
        SUSPENSION = 45 + phase_1 + phase_3 +  uniform(((((designer*2.5) + (cto*4.5) + (aerodynamicst*1.5))/50))-5.5,((((designer*2.5) + (cto*4.5) + (aerodynamicst*1.5))/50))+5.5) + suspension_R
        dlung = choice([1,0,-1,-1,-1])
        if dlung == 1:
            WEIGHT = f'+{uniform(1.01,4.98)}'
        elif dlung == -1:
            WEIGHT = f'-{uniform(1.01,4.98)}'
        else:
            WEIGHT = f'Optimal Weight'
    elif focus == 'Rear Stiff':
        FW = 45 + phase_1 + phase_3 +  uniform(((((designer*3.5) + (cto*1.5) + (aerodynamicst*3.5))/50))-5.5,((((designer*3.5) + (cto*1.5) + (aerodynamicst*3.5))/50))+5.5) + FW_R
        RW = 45 + phase_1 + phase_3 +  uniform(((((designer*4.5) + (cto*2.5) + (aerodynamicst*4.5))/50))-5.5,((((designer*4.5) + (cto*2.5) + (aerodynamicst*4.5))/50))+5.5) + RW_R
        CHASSIS = 45 + phase_1 + phase_3 +  uniform(((((designer*3.5) + (cto*3.5) + (aerodynamicst*1.5))/50))-5.5,((((designer*3.5) + (cto*3.5) + (aerodynamicst*1.5))/50))+5.5) + chassis_R
        BASE = 45 + phase_1 + phase_3 +  uniform(((((designer*4) + (cto*3) + (aerodynamicst*3))/50))-5.5,((((designer*4) + (cto*3) + (aerodynamicst*3))/50))+5.5) + base_R
        SIDEPOD = 45 + phase_1 + phase_3 +  uniform(((((designer*5) + (cto*3) + (aerodynamicst*2))/50))-5.5,((((designer*5) + (cto*3) + (aerodynamicst*2))/50))+5.5) + sidepod_R
        SUSPENSION = 45 + phase_1 + phase_3 +  uniform(((((designer*3.5) + (cto*5.5) + (aerodynamicst*2.5))/50))-5.5,((((designer*3.5) + (cto*5.5) + (aerodynamicst*2.5))/50))+5.5) + suspension_R
        dlung = choice([-1,0,1,1,1])
        if dlung == 1:
            WEIGHT = f'+{uniform(1.01,4.98)}'
        elif dlung == -1:
            WEIGHT = f'-{uniform(1.01,4.98)}'
        else:
            WEIGHT = f'Optimal Weight'
    elif focus == 'Balanced' or 'Unbalanced':
        FW = 45 + phase_1 + phase_3 +  uniform(((((designer*4) + (cto*2) + (aerodynamicst*4))/50))-5.5,((((designer*4) + (cto*2) + (aerodynamicst*4))/50))+5.5) + FW_R
        RW = 45 + phase_1 + phase_3 +  uniform(((((designer*4) + (cto*2) + (aerodynamicst*4))/50))-5.5,((((designer*4) + (cto*2) + (aerodynamicst*4))/50))+5.5) + RW_R
        CHASSIS = 45 + phase_1 + phase_3 +  uniform(((((designer*4) + (cto*4) + (aerodynamicst*2))/50))-5.5,((((designer*4) + (cto*4) + (aerodynamicst*2))/50))+5.5) + chassis_R
        BASE = 45 + phase_1 + phase_3 +  uniform(((((designer*4) + (cto*3) + (aerodynamicst*3))/50))-5.5,((((designer*4) + (cto*3) + (aerodynamicst*3))/50))+5.5) + base_R
        SIDEPOD = 45 + phase_1 + phase_3 +  uniform(((((designer*5) + (cto*3) + (aerodynamicst*2))/50))-5.5,((((designer*5) + (cto*3) + (aerodynamicst*2))/50))+5.5) + sidepod_R
        SUSPENSION = 45 + phase_1 + phase_3 +  uniform(((((designer*3) + (cto*5) + (aerodynamicst*2))/50))-5.5,((((designer*3) + (cto*5) + (aerodynamicst*2))/50))+5.5) + suspension_R
        dlung = choice([-1,1,0,0,0])
        if dlung == 1:
            WEIGHT = f'+{uniform(1.01,4.98)}'
        elif dlung == -1:
            WEIGHT = f'-{uniform(1.01,4.98)}'
        else:
            WEIGHT = f'Optimal Weight'

    
    if focus_r == 'Balanced Reliability':
        RELIABILITY = uniform(72,84)
    elif focus_r == 'Low Reliability':
        FW += uniform(1.5,4.5)
        CHASSIS += uniform(1.5,4.5) 
        SIDEPOD += uniform(1.5,4.5)
        SUSPENSION += uniform(1.5,4.5)
        RELIABILITY = uniform(56,72)
    elif focus_r == 'High Reliability':
        FW -= uniform(1.5,4.5)
        CHASSIS -= uniform(1.5,4.5) 
        SIDEPOD -= uniform(1.5,4.5)
        SUSPENSION -= uniform(1.5,4.5)
        RELIABILITY = uniform(84,94)

    if pit_package == 1.0:
        CREW = choice(['Good','Average','Average','Average','Average','Bad','Bad','Bad','Bad'])
    elif pit_package == 3.0:
        CREW = choice(['Perfect','Good','Good','Good','Average','Average','Average','Bad','Bad'])
    elif pit_package == 5.0:
        CREW = choice(['Perfect','Perfect','Perfect','Good','Good','Good','Average','Average','Bad'])
    elif pit_package == 7.0:
        CREW = choice(['Perfect','Perfect','Perfect','Perfect','Perfect','Good','Good','Good','Average'])

    if designer_name == 'Adrian Newey':
        BASE += uniform(4.011,8.01)
    elif designer_name == 'Dan Fallows':
        BASE += uniform(2.011,5.01)
    elif designer_name == 'Aldo Costa':
        FW += uniform(1.011,3.01)
        RW += uniform(1.011,3.01)
        CHASSIS += uniform(1.011,3.01)
        BASE += uniform(1.011,3.01)
        SIDEPOD += uniform(1.011,3.01)
        SUSPENSION += uniform(1.011,3.01)
    elif designer_name == 'John Barnard':
        CHASSIS += uniform(4.011,8.01)
    elif designer_name == 'James Allison':
        FW += uniform(2.011,5.01)
        SIDEPOD += uniform(4.011,8.01)
    elif designer_name == 'Gordon Murray':
        FW += uniform(2.011,5.01)
        CHASSIS += uniform(2.011,5.01)

    print(f'Front Wing: {round(FW,3)}')
    print(f'Rear Wing: {round(RW,3)}')
    print(f'Chassis: {round(CHASSIS,3)}')
    print(f'Base: {round(BASE,3)}')
    print(f'Sidepod: {round(SIDEPOD,3)}')
    print(f'Suspension: {round(SUSPENSION,3)}')
    print(f'Reliability: {round(RELIABILITY,3)}')
    print(f'Weight: {WEIGHT}')
    print(f'Pit Crew: {CREW}')

def driver(automated, status, quality, style, char, preferences):
    if status != 'Rookie':
        P1 = 14
        unique = ['Balanced','Balanced','Balanced','Balanced','Balanced'
                  'Rear Stiff','Rear Stiff',
                  'Front Stiff','Front Stiff'
                  'Unbalanced']
    else:
        P1 = 4
        unique = [None]

    from random import choice, randint
    if automated == True:
        quality = choice(['Generational',
                          'Elite','Elite',
                          'Superstar','Superstar','Superstar',
                          'Talanted','Talanted','Talanted','Talanted','Talanted','Talanted','Talanted',
                          'Good','Good','Good','Good','Good','Good','Good','Good','Good','Good','Good','Good','Good','Good','Good','Good',
                          'Average','Average','Average','Average','Average','Average','Average','Average','Average','Average','Average','Average','Average',
                          'Average','Average','Average','Average','Average','Average','Average','Average','Average','Average','Average','Average','Average',
                          'Bad','Bad','Bad','Bad','Bad','Bad','Bad','Bad','Bad','Bad','Bad','Bad'])
        style = choice(['Smooth','Sharp',
                        'Balanced','Balanced','Balanced','Balanced','Balanced',])
        char = choice(['RP','RC','Balanced'])
        preferences = choice(['Attacker','Defender','Consister'])
    else:
        pass

    if quality == 'Generational':
        P2 = randint(28,34)
    elif quality == 'Elite':
        P2 = randint(24,30)
    elif quality == 'Superstar':
        P2 = randint(20,26)
    elif quality == 'Talanted':
        P2 = randint(16,22)
    elif quality == 'Good':
        P2 = randint(14,20)
    elif quality == 'Average':
        P2 = randint(10,16)
    elif quality == 'Bad':
        P2 = randint(4,10)

    if style == 'Smooth':
        P3 = randint(2,6)
        P4 = 0
    elif style == 'Sharp':
        P3 = 0
        P4 = randint(2,6)
    elif style == 'Balanced':
        P3 = 0
        P4 = 0

    if char == 'RP':
        P5 = randint(2,6)
        P6 = 0
    elif char == 'RC':
        P5 = 0
        P6 = randint(2,6)
    elif char == 'Balanced':
        P5 = 0
        P6 = 0

    if preferences == 'Attacker':
        P7 = randint(2,6)
        P8 = 0
        P9 = 0
    elif preferences == 'Defender':
        P7 = 0
        P8 = randint(2,6)
        P9 = 0
    elif preferences == 'Consister':
        P7 = 0
        P8 = 0
        P9 = randint(2,6)

    pace = 50 + P1 + (P2 + randint(-3,3)) + (P4 - P3) + (P5 - P6)
    braking = 50 + P1 + (P2 + randint(-3,3)) + (P5 - P6)
    smoothness = 50 + P1 + (P2 + randint(-3,3)) + (P3 - P4)
    adaptability = 50 + P1 + (P2 + randint(-3,3)) + (P6 - P5)
    consistency = 50 + P1 + (P2 + randint(-3,3)) + P9
    fitness = 50 + P1 + (P2 + randint(-3,3)) + (P6 - P5)
    aggression = 50 + P1 + (P2 + randint(-3,3))
    attack = 50 + P1 + (P2 + randint(-3,3)) + P7
    defence = 50 + P1 + (P2 + randint(-3,3)) + P8
    start = 50 + P1 + (P2 + randint(-3,3))
    wet = 50 + P1 + (P2 + randint(-3,3))

    print(f'{quality} driver.\n')
    print(f'Pace: {pace}')
    print(f'Braking: {braking}')
    print(f'Smoothness: {smoothness}')
    print(f'Adaptability: {adaptability}')
    print(f'Consistency: {consistency}')
    print(f'Fitness: {fitness}')
    print(f'Aggression: {aggression}')
    print(f'Attack: {attack}')
    print(f'Defence: {defence}')
    print(f'Start: {start}')
    print(f'Wet: {wet}')

    print(f'\nDriver(None,None,None,None,{pace},{braking},{smoothness},{adaptability},{consistency},{fitness},{aggression},{attack},{defence},{start},None,{choice(unique)})')

driver(True,'Rookie',0,0,0,0)