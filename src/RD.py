def upgrade(designer,cto,aerodynamicst,min_budget,max_budget,spent_budget,engineer_crew):
    # budget unit is million.
    min_point = ((((designer*5) + (cto*3) + (aerodynamicst*2))/10)/110)
    max_point = ((((designer*5) + (cto*3) + (aerodynamicst*2))/10)/90)
    
    limit = max_budget - min_budget
    spent = (spent_budget + 0.1) - min_budget

    from random import uniform
    phase_1 = uniform(min_point,max_point)    
    phase_2 = (spent/limit) + 0.5

    if engineer_crew == 'Perfect':
        phase_3 = +0.50
    elif engineer_crew == 'Good':
        phase_3 = +0.25
    elif engineer_crew == 'Average':
        phase_3 = +0.00
    elif engineer_crew == 'Bad':
        phase_3 = -0.25
    elif engineer_crew == 'Very Bad':
        phase_3 = -0.50

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

    print(f'Front Wing: {round(FW,3)}')
    print(f'Rear Wing: {round(RW,3)}')
    print(f'Chassis: {round(CHASSIS,3)}')
    print(f'Base: {round(BASE,3)}')
    print(f'Sidepod: {round(SIDEPOD,3)}')
    print(f'Suspension: {round(SUSPENSION,3)}')
    print(f'Reliability: {round(RELIABILITY,3)}')
    print(f'Weight: {WEIGHT}')
    print(f'Pit Crew: {CREW}')