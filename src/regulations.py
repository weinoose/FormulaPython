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

    return (round(((phase_1) + (phase_2) + (phase_3)),3))

def design(designer_name,designer,cto,aerodynamicst,focus,FW_R,RW_R,chassis_R,base_R,sidepod_R,suspension_R,min_budget,max_budget,spent_budget,engineer_crew): 
    # budgest unit is million.
    
    from random import uniform
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

    if focus == 'Top Speed': 
        FW = 47 + phase_1 + phase_3 + uniform(((((designer*3) + (cto*1) + (aerodynamicst*3))/50))-5.5,((((designer*3) + (cto*1) + (aerodynamicst*3))/50))+5.5) + FW_R
        RW = 47 + phase_1 + phase_3 +  uniform(((((designer*5) + (cto*3) + (aerodynamicst*5))/50))-5.5,((((designer*5) + (cto*3) + (aerodynamicst*5))/50))+5.5) + RW_R
        CHASSIS = 47 + phase_1 + phase_3 +  uniform(((((designer*5) + (cto*5) + (aerodynamicst*3))/50))-5.5,((((designer*5) + (cto*5) + (aerodynamicst*3))/50))+5.5) + chassis_R
        BASE = 47 + phase_1 + phase_3 +  uniform(((((designer*3) + (cto*2) + (aerodynamicst*2))/50))-5.5,((((designer*3) + (cto*2) + (aerodynamicst*2))/50))+5.5) + base_R
        SIDEPOD = 47 + phase_1 + phase_3 +  uniform(((((designer*4) + (cto*2) + (aerodynamicst*1))/50))-5.5,((((designer*4) + (cto*2) + (aerodynamicst*1))/50))+5.5) + sidepod_R
        SUSPENSION = 47 + phase_1 + phase_3 +  uniform(((((designer*4) + (cto*6) + (aerodynamicst*3))/50))-5.5,((((designer*4) + (cto*6) + (aerodynamicst*3))/50))+5.5) + suspension_R
        TIRE_DEG = 0.05 + (phase_1/250) + uniform(0.065, 0.095)
    elif focus == 'Downforce':
        FW = 47 + phase_1 + phase_3 +  uniform(((((designer*5) + (cto*3) + (aerodynamicst*5))/50))-5.5,((((designer*5) + (cto*3) + (aerodynamicst*5))/50))+5.5) + FW_R
        RW = 47 + phase_1 + phase_3 +  uniform(((((designer*5) + (cto*3) + (aerodynamicst*5))/50))-5.5,((((designer*5) + (cto*3) + (aerodynamicst*5))/50))+5.5) + RW_R
        CHASSIS = 47 + phase_1 + phase_3 +  uniform(((((designer*3) + (cto*3) + (aerodynamicst*1))/50))-5.5,((((designer*3) + (cto*3) + (aerodynamicst*1))/50))+5.5) + chassis_R
        BASE = 47 + phase_1 + phase_3 +  uniform(((((designer*5) + (cto*4) + (aerodynamicst*4))/50))-5.5,((((designer*5) + (cto*4) + (aerodynamicst*4))/50))+5.5) + base_R
        SIDEPOD = 47 + phase_1 + phase_3 +  uniform(((((designer*4) + (cto*2) + (aerodynamicst*1))/50))-5.5,((((designer*4) + (cto*2) + (aerodynamicst*1))/50))+5.5) + sidepod_R
        SUSPENSION = 47 + phase_1 + phase_3 +  uniform(((((designer*2) + (cto*4) + (aerodynamicst*1))/50))-5.5,((((designer*2) + (cto*4) + (aerodynamicst*1))/50))+5.5) + suspension_R
        TIRE_DEG = 0.05 + (phase_1/250) + uniform(0.042, 0.064)
    elif focus == 'Balanced':
        FW = 47 + phase_1 + phase_3 +  uniform(((((designer*4) + (cto*2) + (aerodynamicst*4))/50))-5.5,((((designer*4) + (cto*2) + (aerodynamicst*4))/50))+5.5) + FW_R
        RW = 47 + phase_1 + phase_3 +  uniform(((((designer*4) + (cto*2) + (aerodynamicst*4))/50))-5.5,((((designer*4) + (cto*2) + (aerodynamicst*4))/50))+5.5) + RW_R
        CHASSIS = 47 + phase_1 + phase_3 +  uniform(((((designer*4) + (cto*4) + (aerodynamicst*2))/50))-5.5,((((designer*4) + (cto*4) + (aerodynamicst*2))/50))+5.5) + chassis_R
        BASE = 47 + phase_1 + phase_3 +  uniform(((((designer*4) + (cto*3) + (aerodynamicst*3))/50))-5.5,((((designer*4) + (cto*3) + (aerodynamicst*3))/50))+5.5) + base_R
        SIDEPOD = 47 + phase_1 + phase_3 +  uniform(((((designer*5) + (cto*3) + (aerodynamicst*2))/50))-5.5,((((designer*5) + (cto*3) + (aerodynamicst*2))/50))+5.5) + sidepod_R
        SUSPENSION = 47 + phase_1 + phase_3 +  uniform(((((designer*3) + (cto*5) + (aerodynamicst*2))/50))-5.5,((((designer*3) + (cto*5) + (aerodynamicst*2))/50))+5.5) + suspension_R
        TIRE_DEG = 0.05 + (phase_1/250) + uniform(0.042, 0.095)
    elif focus == 'Unbalanced':
        FW = 47 + phase_1 + phase_3 +  uniform(((((designer*4) + (cto*2) + (aerodynamicst*4))/50))-5.5,((((designer*4) + (cto*2) + (aerodynamicst*4))/50))+5.5) + FW_R
        RW = 47 + phase_1 + phase_3 +  uniform(((((designer*4) + (cto*2) + (aerodynamicst*4))/50))-5.5,((((designer*4) + (cto*2) + (aerodynamicst*4))/50))+5.5) + RW_R
        CHASSIS = 47 + phase_1 + phase_3 +  uniform(((((designer*4) + (cto*4) + (aerodynamicst*2))/50))-5.5,((((designer*4) + (cto*4) + (aerodynamicst*2))/50))+5.5) + chassis_R
        BASE = 47 + phase_1 + phase_3 +  uniform(((((designer*4) + (cto*3) + (aerodynamicst*3))/50))-5.5,((((designer*4) + (cto*3) + (aerodynamicst*3))/50))+5.5) + base_R
        SIDEPOD = 47 + phase_1 + phase_3 +  uniform(((((designer*5) + (cto*3) + (aerodynamicst*2))/50))-5.5,((((designer*5) + (cto*3) + (aerodynamicst*2))/50))+5.5) + sidepod_R
        SUSPENSION = 47 + phase_1 + phase_3 +  uniform(((((designer*3) + (cto*5) + (aerodynamicst*2))/50))-5.5,((((designer*3) + (cto*5) + (aerodynamicst*2))/50))+5.5) + suspension_R
        TIRE_DEG = 0.05 + (phase_1/250) + uniform(0.042, 0.095)
    elif focus == 'Quali Performance':
        FW = 47 + phase_1 + phase_3 +  uniform(((((designer*4) + (cto*2) + (aerodynamicst*4))/50))-5.5,((((designer*4) + (cto*2) + (aerodynamicst*4))/50))+5.5) + FW_R + 1
        RW = 47 + phase_1 + phase_3 +  uniform(((((designer*4) + (cto*2) + (aerodynamicst*4))/50))-5.5,((((designer*4) + (cto*2) + (aerodynamicst*4))/50))+5.5) + RW_R + 1
        CHASSIS = 47 + phase_1 + phase_3 +  uniform(((((designer*4) + (cto*4) + (aerodynamicst*2))/50))-5.5,((((designer*4) + (cto*4) + (aerodynamicst*2))/50))+5.5) + chassis_R + 1
        BASE = 47 + phase_1 + phase_3 +  uniform(((((designer*4) + (cto*3) + (aerodynamicst*3))/50))-5.5,((((designer*4) + (cto*3) + (aerodynamicst*3))/50))+5.5) + base_R + 1
        SIDEPOD = 47 + phase_1 + phase_3 +  uniform(((((designer*5) + (cto*3) + (aerodynamicst*2))/50))-5.5,((((designer*5) + (cto*3) + (aerodynamicst*2))/50))+5.5) + sidepod_R + 1
        SUSPENSION = 47 + phase_1 + phase_3 +  uniform(((((designer*3) + (cto*5) + (aerodynamicst*2))/50))-5.5,((((designer*3) + (cto*5) + (aerodynamicst*2))/50))+5.5) + suspension_R + 1
        TIRE_DEG = 0.05 + (phase_1/250) + uniform(0.015, 0.041)
    elif focus == 'Race Performance':
        FW = 47 + phase_1 + phase_3 +  uniform(((((designer*4) + (cto*2) + (aerodynamicst*4))/50))-5.5,((((designer*4) + (cto*2) + (aerodynamicst*4))/50))+5.5) + FW_R
        RW = 47 + phase_1 + phase_3 +  uniform(((((designer*4) + (cto*2) + (aerodynamicst*4))/50))-5.5,((((designer*4) + (cto*2) + (aerodynamicst*4))/50))+5.5) + RW_R
        CHASSIS = 47 + phase_1 + phase_3 +  uniform(((((designer*4) + (cto*4) + (aerodynamicst*2))/50))-5.5,((((designer*4) + (cto*4) + (aerodynamicst*2))/50))+5.5) + chassis_R
        BASE = 47 + phase_1 + phase_3 +  uniform(((((designer*4) + (cto*3) + (aerodynamicst*3))/50))-5.5,((((designer*4) + (cto*3) + (aerodynamicst*3))/50))+5.5) + base_R
        SIDEPOD = 47 + phase_1 + phase_3 +  uniform(((((designer*5) + (cto*3) + (aerodynamicst*2))/50))-5.5,((((designer*5) + (cto*3) + (aerodynamicst*2))/50))+5.5) + sidepod_R
        SUSPENSION = 47 + phase_1 + phase_3 +  uniform(((((designer*3) + (cto*5) + (aerodynamicst*2))/50))-5.5,((((designer*3) + (cto*5) + (aerodynamicst*2))/50))+5.5) + suspension_R
        TIRE_DEG = 0.05 + (phase_1/250) + uniform(0.065, 0.095)

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

    from random import choice
    if focus == 'Top Speed':
        dlist = ['Front Stiff','Front Stiff','Rear Stiff','Rear Stiff','Balanced','Unbalanced','Unbalanced','Unbalanced']
        CHAR = choice(dlist)
        dlung = choice([1,1,-1,-1,-1,-1,-1,0,0,0])
        if dlung == 1:
            WEIGHT = f'+{choice(3.01,7.98)}'
        elif dlung == -1:
            WEIGHT = f'-{choice(1.01,4.98)}'
        else:
            WEIGHT = f'Optimal Weight'
    elif focus == 'Downforce':
        dlist = ['Rear Stiff','Rear Stiff','Rear Stiff','Front Stiff','Unbalanced','Balanced','Balanced','Balanced']
        CHAR = choice(dlist)
        dlung = choice([-1,-1,1,1,1,1,1,0,0,0])
        if dlung == 1:
            WEIGHT = f'+{choice(3.01,7.98)}'
        elif dlung == -1:
            WEIGHT = f'-{choice(1.01,4.98)}'
        else:
            WEIGHT = f'Optimal Weight'
    elif focus == 'Balanced':
        dlist = ['Rear Stiff','Front Stiff','Unbalanced','Balanced','Balanced']
        CHAR = choice(dlist)
        WEIGHT = f''
        WEIGHT = f'Optimal Weight'
    elif focus == 'Quali Performance':
        dlist = ['Rear Stiff','Front Stiff','Unbalanced','Balanced','Balanced']
        CHAR = choice(dlist)
        WEIGHT = f''
        WEIGHT = f'Optimal Weight'
    elif focus == 'Race Performance':
        dlist = ['Rear Stiff','Front Stiff','Unbalanced','Balanced','Balanced']
        CHAR = choice(dlist)
        WEIGHT = f''
        WEIGHT = f'Optimal Weight'
    elif focus == 'Unbalanced':
        dlist = ['Rear Stiff','Rear Stiff','Front Stiff','Front Stiff','Unbalanced','Unbalanced','Unbalanced','Unbalanced','Unbalanced']
        CHAR = choice(dlist)
        WEIGHT = f''
        WEIGHT = f'Optimal Weight'

    print(f'Front Wing: {round(FW,3)}')
    print(f'Rear Wing: {round(RW,3)}')
    print(f'Chassis: {round(CHASSIS,3)}')
    print(f'Base: {round(BASE,3)}')
    print(f'Sidepod: {round(SIDEPOD,3)}')
    print(f'Suspension: {round(SUSPENSION,3)}')
    print(f'Tire Degredation: {round(TIRE_DEG,3)}')
    print(f'Car Charasteric: {CHAR}')
    print(f'WEIGHT: {WEIGHT}')