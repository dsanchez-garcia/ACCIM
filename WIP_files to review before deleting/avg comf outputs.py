from besos.eppy_funcs import get_building
# idf_path = r'C:\Python\accim\TestModel_onlyGeometryForVRFsystem_2zones_CalcVent_V2310[CS_INT ASHRAE55[CA_80[CM_3[HM_2[VC_0[VO_0.0[MT_50.0[MW_50.0[AT_0.1[NS_X.idf'
idfpath = r'C:\Python\accim\TestModel_onlyGeometryForVRFsystem_20zones_CalcVent_V2320[CS_INT ASHRAE55[CA_80[CM_3[HM_2[VC_0[VO_0.0[MT_50.0[MW_50.0[AT_0.1[NS_X.idf'
building = get_building(idfpath)

gvs = [i.obj for i in building.idfobjects['energymanagementsystem:globalvariable']]

vars_to_avg = {
    'ComfHours': {'gvs':[]},
    'DiscomfAppHotHours': {'gvs':[]},
    'DiscomfAppColdHours': {'gvs':[]},
    'DiscomfNonAppHotHours': {'gvs':[]},
    'DiscomfNonAppColdHours': {'gvs':[]},
    'ComfHoursNoApp': {'gvs':[]},
    'OccHours': {'gvs':[]},
    'OccComfHoursNoApp': {'gvs':[]},
    'OccDiscomfHoursNoApp': {'gvs':[]},
    'VentHours': {'gvs':[]},
    }

# gvs_all = []
# for i in gvs:
#     for j in i:
#         if 'energymanagementsystem' not in j.lower():
#             gvs_all.append(j)

for i in gvs:
    for j in i:
        if 'energymanagementsystem' not in j.lower():
            for k, key in enumerate(vars_to_avg.keys()):
                if key.lower() == j.split('_')[0].lower():
                    vars_to_avg[key]['gvs'].append(j)
                    # gvs_all.append(j)

for k, key in enumerate(vars_to_avg.keys()):
    vars_to_avg[key].update({'summed_gvs': '+'.join(vars_to_avg[key]['gvs'])})

# gvs_occ_comf = [i for i in gvs_all if 'OccComfHoursNoApp' in i]
# summed_gvs = '+'.join(gvs_occ_comf)

building.newidfobject(
    'EnergyManagementSystem:GlobalVariable',
    Erl_Variable_1_Name='AvgOccComfHoursNoApp'
)

building.newidfobject(
    key='EnergyManagementSystem:ProgramCallingManager',
    Name='MakeAvgOccComfHoursNoApp',
    EnergyPlus_Model_Calling_Point='BeginTimestepBeforePredictor',
    Program_Name_1='MakeAvgOccComfHoursNoApp',
)

building.newidfobject(
    'EnergyManagementSystem:Program',
    Name='MakeAvgOccComfHoursNoApp',
    Program_Line_1='set AvgOccComfHoursNoAppNum = '+summed_gvs,
    Program_Line_2=f'set AvgOccComfHoursNoAppDen = {len(gvs_occ_comf)}',
    Program_Line_3='set AvgOccComfHoursNoApp = AvgOccComfHoursNoAppNum/AvgOccComfHoursNoAppDen'
)

building.newidfobject(
    key='EnergyManagementSystem:OutputVariable',
    Name='AvgOccComfHoursNoApp',
    EMS_Variable_Name='AvgOccComfHoursNoApp',
    Type_of_Data_in_Variable='Summed',
    Update_Frequency='ZoneTimestep',
    Units='H'
)
building.newidfobject(
    key='Output:Variable',
    Key_Value='*',
    Variable_Name='AvgOccComfHoursNoApp',
    Reporting_Frequency='Hourly'
)

building.newidfobject(
    key='Output:Variable',
    Key_Value='*',
    Variable_Name='AvgOccComfHoursNoApp',
    Reporting_Frequency='Runperiod'
)
newidfname = idfpath.split('.idf')[0]
newidfname = newidfname+'globalocccomfhours.idf'
building.savecopy(filename=newidfname)

# x = [i for i in building.idfobjects['energymanagementsystem:outputvariable']][0]
# x = [i for i in building.idfobjects['output:variable']][0]

x = [i for i in building.idfobjects['EnergyManagementSystem:Program']][0]
x = [i for i in building.idfobjects['EnergyManagementSystem:ProgramCallingManager']][0]
