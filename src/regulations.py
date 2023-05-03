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

def design(designer,cto,aerodynamicst,focus,FW_R,RW_R,chassis_R,base_R,sidepod_R,suspension_R,min_budget,max_budget,spent_budget,engineer_crew): 
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
    else:
        FW = 47 + phase_1 + phase_3 +  uniform(((((designer*4) + (cto*2) + (aerodynamicst*4))/50))-5.5,((((designer*4) + (cto*2) + (aerodynamicst*4))/50))+5.5) + FW_R
        RW = 47 + phase_1 + phase_3 +  uniform(((((designer*4) + (cto*2) + (aerodynamicst*4))/50))-5.5,((((designer*4) + (cto*2) + (aerodynamicst*4))/50))+5.5) + RW_R
        CHASSIS = 47 + phase_1 + phase_3 +  uniform(((((designer*4) + (cto*4) + (aerodynamicst*2))/50))-5.5,((((designer*4) + (cto*4) + (aerodynamicst*2))/50))+5.5) + chassis_R
        BASE = 47 + phase_1 + phase_3 +  uniform(((((designer*4) + (cto*3) + (aerodynamicst*3))/50))-5.5,((((designer*4) + (cto*3) + (aerodynamicst*3))/50))+5.5) + base_R
        SIDEPOD = 47 + phase_1 + phase_3 +  uniform(((((designer*5) + (cto*3) + (aerodynamicst*2))/50))-5.5,((((designer*5) + (cto*3) + (aerodynamicst*2))/50))+5.5) + sidepod_R
        SUSPENSION = 47 + phase_1 + phase_3 +  uniform(((((designer*3) + (cto*5) + (aerodynamicst*2))/50))-5.5,((((designer*3) + (cto*5) + (aerodynamicst*2))/50))+5.5) + suspension_R
        if focus == 'Balanced':
            TIRE_DEG = 0.05 + (phase_1/250) + uniform(0.042, 0.095)
        elif focus == 'Quali Performance':
            TIRE_DEG = 0.05 + (phase_1/250) + uniform(0.015, 0.041)
        elif focus == 'Race Performance':
            TIRE_DEG = 0.05 + (phase_1/250) + uniform(0.065, 0.095)

    print(f'Front Wing: {round(FW,3)}')
    print(f'Rear Wing: {round(RW,3)}')
    print(f'Chassis: {round(CHASSIS,3)}')
    print(f'Base: {round(BASE,3)}')
    print(f'Sidepod: {round(SIDEPOD,3)}')
    print(f'Suspension: {round(SUSPENSION,3)}')
    print(f'Tire Degredation: {round(TIRE_DEG,3)}')