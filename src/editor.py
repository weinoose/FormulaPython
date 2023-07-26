from random import uniform, choice, randint
import pandas as pd

def upgrade(part,regulation,spent,engineers,designer,cto,aerodynamicst):
    
    # Part Development
    if part == 'Front Wing':
        min_budget = 3.0
        max_budget = 6.0
    elif part == 'Rear Wing':
        min_budget = 3.0
        max_budget = 6.0
    elif part == 'Chassis':
        min_budget = 3.0
        max_budget = 6.0
    elif part == 'Base':
        min_budget = 4.0
        max_budget = 8.0
    elif part == 'Sidepod':
        min_budget = 1.0
        max_budget = 2.0
    elif part == 'Suspension':
        min_budget = 1.0
        max_budget = 2.0

    min_point = ((((designer*5) + (cto*3) + (aerodynamicst*2))/10)/110)
    max_point = ((((designer*5) + (cto*3) + (aerodynamicst*2))/10)/90)
    
    limit = max_budget - min_budget
    spentx = (spent + 0.1) - min_budget

    phase_1 = uniform(min_point,max_point)    
    phase_2 = (spentx/limit) + 0.5

    if engineers == 'Perfect':
        phase_3 = uniform(0.35,0.75)
    elif engineers == 'Good':
        phase_3 = uniform(0.10,0.50)
    elif engineers == 'Average':
        phase_3 = uniform(-0.15,0.25)
    elif engineers == 'Bad':
        phase_3 = uniform(0.00,0.40)*(-1.0)
    elif engineers == 'Very Bad':
        phase_3 = uniform(0.25,0.60)*(-1.0)
    
    # x0.666 +4 0.4 saniye
    # x1.000 +6 0.6 saniye
    # x1.500 +9 1.0 saniye
    # x2.000 +12 1.5 saniye

    regulation = int(regulation)
    if regulation == 1998:
        svv = 1.500
    elif regulation == 2005:
        svv = 1.333
    elif regulation == 2006:
        svv = 0.666
    elif regulation == 2009:
        svv = 2.000
    elif regulation == 2011:
        svv = 0.666
    elif regulation == 2014:
        svv = 1.333
    elif regulation == 2016:
        svv = 1.333
    elif regulation == 2017:
        svv = 1.333
    elif regulation == 2018:
        svv = 0.666
    elif regulation == 2021:
        svv = 1.333
    elif regulation == 2022:
        svv = 1.333

    final = round((round((round((phase_1 + phase_2 + phase_3)*10))//uniform(4.25,5.75)))*(svv))

    pb1 = randint(1,106) >= designer
    pb2 = randint(1,106) >= cto
    pb3 = randint(1,106) >= aerodynamicst
    
    if (pb1 and pb2 and pb3) == True:
        FAIL = uniform(final-3.75,final+1.25)*(-1.0)
        iffail = 'However, there were problems which negatively affected the development process.'
    else:
        if (pb1 and pb2) == True:
            FAIL = uniform(final-3.75,final+1.25)*(-1.0)
            iffail = 'However, there were problems which negatively affected the development process.'
        else:
            if (pb1 and pb3) == True:
                FAIL = uniform(final-3.75,final+1.25)*(-1.0)
                iffail = 'However, there were problems which negatively affected the development process.'
            else: 
                if (pb2 and pb3) == True:
                    FAIL = uniform(final-3.75,final+1.25)*(-1.0)
                    iffail = 'However, there were problems which negatively affected the development process.'
                else:
                    FAIL = 0
                    iffail = 'There were no issues to concern.'

    final = round(final) + round(FAIL)
    if FAIL == 0:
        return f'{part} has upgraded by +{final}.\n{iffail}'
    else:
        if final >= 0:
            return f'{part} has upgraded by +{final}.\n{iffail}'
        else:
            return f'{part} has upgraded by {final}.\n{iffail}'

def design(engineers,head,designer,cto,aerodynamicst,concept,durability,spent,box,regulation,title,engine):

    # Money Talks
    spentx = (spent - 0.1) - 13.0
    phase_1 = ((spentx/(33.0-13.0)) + 0.5)*13.75

    if engineers == 'Perfect':
        phase_3 = uniform(2.50,5.00)
    elif engineers == 'Good':
        phase_3 = uniform(0.50,2.49)
    elif engineers == 'Average':
        phase_3 = uniform(0.00,0.49)
    elif engineers == 'Bad':
        phase_3 = uniform(0.50,2.49)*(-1.0)
    elif engineers == 'Very Bad':
        phase_3 = uniform(2.50,5.00)*(-1.0)

    if concept == 'Front Stiff': 
        FW = 45 + phase_1 + phase_3 +  uniform(((((designer*4.5) + (cto*2.5) + (aerodynamicst*4.5))/50))-5.5,((((designer*4.5) + (cto*2.5) + (aerodynamicst*4.5))/50))+5.5)
        RW = 45 + phase_1 + phase_3 +  uniform(((((designer*3.5) + (cto*1.5) + (aerodynamicst*3.5))/50))-5.5,((((designer*3.5) + (cto*1.5) + (aerodynamicst*3.5))/50))+5.5)
        CHASSIS = 45 + phase_1 + phase_3 +  uniform(((((designer*4.5) + (cto*4.5) + (aerodynamicst*2.5))/50))-5.5,((((designer*4.5) + (cto*4.5) + (aerodynamicst*2.5))/50))+5.5)
        BASE = 45 + phase_1 + phase_3 +  uniform(((((designer*4) + (cto*3) + (aerodynamicst*3))/50))-5.5,((((designer*4) + (cto*3) + (aerodynamicst*3))/50))+5.5)
        SIDEPOD = 45 + phase_1 + phase_3 +  uniform(((((designer*5) + (cto*3) + (aerodynamicst*2))/50))-5.5,((((designer*5) + (cto*3) + (aerodynamicst*2))/50))+5.5)
        SUSPENSION = 45 + phase_1 + phase_3 +  uniform(((((designer*2.5) + (cto*4.5) + (aerodynamicst*1.5))/50))-5.5,((((designer*2.5) + (cto*4.5) + (aerodynamicst*1.5))/50))+5.5)
        w = choice([1,0,-1,-1,-1])
        if w == 1:
            WEIGHT = f'+{round(uniform(1.01,4.98),2)}'
        elif w == -1:
            WEIGHT = f'-{round(uniform(1.01,4.98),2)}'
        else:
            WEIGHT = 0.00
    elif concept == 'Rear Stiff':
        FW = 45 + phase_1 + phase_3 +  uniform(((((designer*3.5) + (cto*1.5) + (aerodynamicst*3.5))/50))-5.5,((((designer*3.5) + (cto*1.5) + (aerodynamicst*3.5))/50))+5.5)
        RW = 45 + phase_1 + phase_3 +  uniform(((((designer*4.5) + (cto*2.5) + (aerodynamicst*4.5))/50))-5.5,((((designer*4.5) + (cto*2.5) + (aerodynamicst*4.5))/50))+5.5)
        CHASSIS = 45 + phase_1 + phase_3 +  uniform(((((designer*3.5) + (cto*3.5) + (aerodynamicst*1.5))/50))-5.5,((((designer*3.5) + (cto*3.5) + (aerodynamicst*1.5))/50))+5.5)
        BASE = 45 + phase_1 + phase_3 +  uniform(((((designer*4) + (cto*3) + (aerodynamicst*3))/50))-5.5,((((designer*4) + (cto*3) + (aerodynamicst*3))/50))+5.5)
        SIDEPOD = 45 + phase_1 + phase_3 +  uniform(((((designer*5) + (cto*3) + (aerodynamicst*2))/50))-5.5,((((designer*5) + (cto*3) + (aerodynamicst*2))/50))+5.5)
        SUSPENSION = 45 + phase_1 + phase_3 +  uniform(((((designer*3.5) + (cto*5.5) + (aerodynamicst*2.5))/50))-5.5,((((designer*3.5) + (cto*5.5) + (aerodynamicst*2.5))/50))+5.5)
        w = choice([-1,0,1,1,1])
        if w == 1:
            WEIGHT = f'+{round(uniform(1.01,4.98),2)}'
        elif w == -1:
            WEIGHT = f'-{round(uniform(1.01,4.98),2)}'
        else:
            WEIGHT = 0.00
    elif concept == 'Balanced':
        FW = 45 + phase_1 + phase_3 +  uniform(((((designer*4) + (cto*2) + (aerodynamicst*4))/50))-5.5,((((designer*4) + (cto*2) + (aerodynamicst*4))/50))+5.5)
        RW = 45 + phase_1 + phase_3 +  uniform(((((designer*4) + (cto*2) + (aerodynamicst*4))/50))-5.5,((((designer*4) + (cto*2) + (aerodynamicst*4))/50))+5.5)
        CHASSIS = 45 + phase_1 + phase_3 +  uniform(((((designer*4) + (cto*4) + (aerodynamicst*2))/50))-5.5,((((designer*4) + (cto*4) + (aerodynamicst*2))/50))+5.5)
        BASE = 45 + phase_1 + phase_3 +  uniform(((((designer*4) + (cto*3) + (aerodynamicst*3))/50))-5.5,((((designer*4) + (cto*3) + (aerodynamicst*3))/50))+5.5)
        SIDEPOD = 45 + phase_1 + phase_3 +  uniform(((((designer*5) + (cto*3) + (aerodynamicst*2))/50))-5.5,((((designer*5) + (cto*3) + (aerodynamicst*2))/50))+5.5)
        SUSPENSION = 45 + phase_1 + phase_3 +  uniform(((((designer*3) + (cto*5) + (aerodynamicst*2))/50))-5.5,((((designer*3) + (cto*5) + (aerodynamicst*2))/50))+5.5)
        w = choice([-1,1,0,0,0])
        if w == 1:
            WEIGHT = f'{round(uniform(1.01,4.98),2)}'
        elif w == -1:
            WEIGHT = f'-{round(uniform(1.01,4.98),2)}'
        else:
            WEIGHT = 0.00

    if durability == 'Balanced':
        RELIABILITY = uniform(72,84)
    elif durability == 'Low':
        FW += uniform(1.5,4.5)
        CHASSIS += uniform(1.5,4.5) 
        SIDEPOD += uniform(1.5,4.5)
        SUSPENSION += uniform(1.5,4.5)
        RELIABILITY = uniform(56,72)
    elif durability == 'High':
        FW -= uniform(1.5,4.5)
        CHASSIS -= uniform(1.5,4.5) 
        SIDEPOD -= uniform(1.5,4.5)
        SUSPENSION -= uniform(1.5,4.5)
        RELIABILITY = uniform(84,94)

    if box == 1.0:
        CREW = choice(['Good','Average','Average','Average','Average','Bad','Bad','Bad','Bad'])
    elif box == 3.0:
        CREW = choice(['Perfect','Good','Good','Good','Average','Average','Average','Bad','Bad'])
    elif box == 5.0:
        CREW = choice(['Perfect','Perfect','Perfect','Good','Good','Good','Average','Average','Bad'])
    elif box == 7.0:
        CREW = choice(['Perfect','Perfect','Perfect','Perfect','Perfect','Good','Good','Good','Average'])

    if head == 'Adrian Newey':
        BASE += uniform(4.011,8.01)
    elif head == 'Dan Fallows':
        BASE += uniform(2.011,5.01)
    elif head == 'Aldo Costa':
        FW += uniform(1.011,3.01)
        RW += uniform(1.011,3.01)
        CHASSIS += uniform(1.011,3.01)
        BASE += uniform(1.011,3.01)
        SIDEPOD += uniform(1.011,3.01)
        SUSPENSION += uniform(1.011,3.01)
    elif head == 'John Barnard':
        CHASSIS += uniform(4.011,8.01)
    elif head == 'James Allison':
        FW += uniform(2.011,5.01)
        SIDEPOD += uniform(4.011,8.01)
    elif head == 'Gordon Murray':
        FW += uniform(2.011,5.01)
        CHASSIS += uniform(2.011,5.01)

    regulation = int(regulation)
    if 2004 >= regulation >= 1998:
        RELIABILITY -= 14
    elif 2008 >= regulation >= 2005:
        RELIABILITY -= 9
    elif 2012 >= regulation >= 2009:
        RELIABILITY -= 6
    elif 2018 >= regulation >= 2013:
        RELIABILITY -= 2
    elif 2021 >= regulation >= 2019:
        RELIABILITY += 2
    elif regulation >= 2022:
        RELIABILITY += 6
    
    return f"Manufacturer('{title}','{CREW}',{engine},{round(CHASSIS)},{round(FW)},{round(RW)},{round(BASE)},{round(SIDEPOD)},{round(SUSPENSION)},{round(RELIABILITY)},{WEIGHT})"

def driver(automated,status,quality,talent,style):
    if status != 'Rookie':
        P1 = 16
    elif status == 'Rookie':
        P1 = 8
    
    if automated == True:
        quality = choice(['Elite',
                          'Superstar','Superstar','Superstar',
                          'Talanted','Talanted','Talanted','Talanted','Talanted',
                          'Good','Good','Good','Good','Good','Good','Good','Good','Good','Good','Good','Good','Good','Good',
                          'Average','Average','Average','Average','Average','Average','Average','Average','Average',
                          'Average','Average','Average','Average','Average','Average','Average','Average','Average',
                          'Bad','Bad','Bad','Bad','Bad','Bad','Bad'])
        
        talent = choice(['RP','RC','Balanced','Balanced','Balanced'])

        style = choice(['Smooth','Smooth',
                        'Sharp','Sharp',
                        'Balanced','Balanced','Balanced','Balanced','Balanced',])
        
        like = choice(['Balanced','Balanced','Balanced','Balanced','Balanced','Balanced','Balanced',
                    'Stiff Rear','Stiff Rear','Stiff Rear',
                    'Stiff Front','Stiff Front',
                    'Unbalanced','Unbalanced'])
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

    if talent == 'RP':
        P5 = randint(2,6)
        P6 = 0
    elif talent == 'RC':
        P5 = 0
        P6 = randint(2,6)
    elif talent == 'Balanced':
        P5 = 0
        P6 = 0

    if style == 'Smooth':
        P3 = randint(2,6)
        P4 = 0
    elif style == 'Sharp':
        P3 = 0
        P4 = randint(2,6)
    elif style == 'Balanced':
        P3 = 0
        P4 = 0

    pace = round(50 + P1 + (P2 + randint(-3,3)) + (P4 - P3) + (P5 - P6))
    braking = round(50 + P1 + (P2 + randint(-3,3)) + (P5 - P6))
    smoothness = round(50 + P1 + (P2 + randint(-3,3)) + (P3 - P4))
    adaptability = round(50 + P1 + (P2 + randint(-3,3)) + ((P6 - P5)*1.5))
    consistency = round(50 + P1 + (P2 + randint(-3,3)) + (P5 - P6))
    fitness = round(50 + P1 + (P2 + randint(-3,3)) + ((P6 - P5)*1.5))
    aggression = round(50 + P1 + (P2 + randint(-3,3)))
    attack = round(50 + P1 + (P2 + randint(-3,3)))
    defence = round(50 + P1 + (P2 + randint(-3,3)))
    start = round(50 + P1 + (P2 + randint(-3,3)))
    wet = round(50 + P1 + (P2 + randint(-3,3)))

    likes = [None, None, None, None, None, None, None, None,
            'Wild','Wild',
            'Calm','Calm']
    
    bales = [None, None, None, None, None, None, None, None,
            'Weak Rear','Weak Rear',
            'Weak Front','Weak Front']
    
    like = [choice(likes),choice(bales)]

    return f"Driver('Team','Name','Nationality','Number',{pace},{braking},{smoothness},{adaptability},{consistency},{fitness},{aggression},{attack},{defence},{start},{wet},[None],['{like[0]}','{like[1]}'])"