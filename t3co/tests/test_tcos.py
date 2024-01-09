"""
Testing module for TCO to ensure the TCO related results remain consistent over time

Flow:
code reads TCO tests vehicles and scenarios one at a time. Generates TCO output dictionaries
and compares the results with the hard coded dictionaries below in comparison_dict.
"""
import math
import unittest
import pprint
from pathlib import Path

from t3co import run_scenario
from t3co import Global as gl

c8_long_haul_control_values = {
'tot_cost':623988.9138875754,
'disc_cost': 569899.8836666911,
'mpgge': {'mpgge': 7.498430055950212, 'grid_mpgge': 6.448649848117184, 'mpgde': 8.45369792102617, 'kwh_per_mi': 4.494274101184436},
'primary_fuel_range_mi': 879.6248481947598,
'veh_msrp_set': {
    'Glider': 121918.9997, 
    'Fuel converter': 24122.324999999997, 
    'Fuel Storage': 415.0938932700001, 
    'Motor & power electronics': 0, 
    'Plug': 0.0, 
    'Battery': 0.0, 
    'Battery replacement': 0, 
    'Purchase tax': 0.0, 
    'msrp': 146456.41859327
    },
'vehicle_mass': {
    'glider_kg': 11776, 
    'cargo_kg': 16329.34474, 
    'transKg': 360.0, 
    'ess_mass_kg': 0.0, 
    'mc_mass_kg': 0.0, 
    'fc_mass_kg': 1486.3387978142077, 
    'fs_mass_kg': 480.36703606292315, 
    'veh_kg': 30432.05057387713, 
    'gliderLb': 25961.605119999997, 
    'cargoLb': 36000.0000006988, 
    'transLb': 793.6632, 
    'essMasLb': 0.0, 
    'mcMassLb': 0.0, 
    'fcMassLb': 3276.8122404371584, 
    'fsMassLb': 1059.0267750450416, 
    'vehLb': 67091.107336181
    },
'zero_to_60': 45.432889231203845,
'zero_to_30': 11.778581178654205,
'zero_to_60_loaded': 54.88059369172835,
'zero_to_30_loaded': 13.635790151751975,
'grade_6_mph_ach': 29.99535831436837,
'grade_1_25_mph_ach': 69.81620,
}

cng_2020_values = {'tot_cost': 693170.6481473122,
'disc_cost': 640179.8187983447,
'mpgge': {'mpgge': 5.341163281863401, 'grid_mpgge': 4.593400422402524, 'mpgde': 6.021604601875311, 'kwh_per_mi': 6.309486945368744},
'primary_fuel_range_mi': 887.5645109481588,
'veh_msrp_set': {'Glider': 121918.9997,
'Fuel converter': 28049.324999999997,
'Fuel Storage': 62729.83733216161,
'Motor & power electronics': 0,
'Plug': 0.0,
'Battery': 0.0,
'Battery replacement': 0,
'Purchase tax': 0.0,
'msrp': 212698.1620321616},
'vehicle_mass': {'glider_kg': 11776,
'cargo_kg': 16329.34474,
'transKg': 360.0,
'ess_mass_kg': 0.0,
'mc_mass_kg': 0.0,
'fc_mass_kg': 1457.142857142857,
'fs_mass_kg': 1594.4035384834394,
'veh_kg': 31516.891135626298,
'gliderLb': 25961.605119999997,
'cargoLb': 36000.0000006988,
'transLb': 793.6632,
'essMasLb': 0.0,
'mcMassLb': 0.0,
'fcMassLb': 3212.4462857142853,
'fsMassLb': 3515.0539290113597,
'vehLb': 69482.76853542445},
'zero_to_60': 47.143699127990274,
'zero_to_30': 12.117136468212376,
'zero_to_60_loaded': 54.88059369172835,
'zero_to_30_loaded': 13.635790151751975,
'grade_6_mph_ach': 29.970940455235045,
'grade_1_25_mph_ach': 69.81620772521556}

hev_2020_values = {   'disc_cost': 713613.1257162548,
    'mpgge': {   'grid_mpgge': 6.710677269764461,
                 'kwh_per_mi': 4.318787773240858,
                 'mpgde': 8.797199033745098,
                 'mpgge': 7.803115542931902},
    'primary_fuel_range_mi': 846.7046823067088,
    'tot_cost': 785246.4080251309,
    'veh_msrp_set': {   'Battery': 7309.147060965,
                        'Battery replacement': 0,
                        'Fuel Storage': 382.918608555,
                        'Fuel converter': 18554.678768654998,
                        'Glider': 121918.9997,
                        'Motor & power electronics': 627.78252096,
                        'Plug': 0.0,
                        'Purchase tax': 0.0,
                        'msrp': 148793.526659135},
    'vehicle_mass': {   'cargo_kg': 16329.34474,
                        'cargoLb': 36000.0000006988,
                        'essMasLb': 505.97028296308577,
                        'ess_mass_kg': 229.50453273719998,
                        'fc_mass_kg': 1143.2882399999999,
                        'fcMassLb': 2520.5161196687995,
                        'fs_mass_kg': 443.13221665551777,
                        'fsMassLb': 976.9381474830875,
                        'glider_kg': 11776,
                        'gliderLb': 25961.605119999997,
                        'mc_mass_kg': 31.389126016610877,
                        'mcMassLb': 69.20109499874067,
                        'transKg': 360.0,
                        'transLb': 793.6632,
                        'veh_kg': 30312.658855409325,
                        'vehLb': 66827.8939658125},
    'zero_to_30': 11.508810449993108,
    'zero_to_30_loaded': 13.401009112541246,
    'zero_to_60': 45.00857022902052,
    'zero_to_60_loaded': 54.64676123984683,
    'grade_1_25_mph_ach': 61.711499873574,
    'grade_6_mph_ach': 23.309451039405502,
    }

ev_2020_values = {   'disc_cost': 1254634.9894996588,
    'grade_1_25_mph_ach': 65.7022591686863,
    'grade_6_mph_ach': 26.223181278473408,
    'mpgge': {   'grid_mpgge': 12.1925550250942,
                 'kwh_per_mi': 2.377024334961005,
                 'mpgde': 15.983528257117273,
                 'mpgge': 14.177389564063022},
    'primary_fuel_range_mi': 766.963913846472,
    'tot_cost': 1305464.5441249725,
    'veh_msrp_set': {   'Battery': 718298.2035765,
                        'Battery replacement': 0,
                        'Fuel Storage': 0.0,
                        'Fuel converter': 0.0,
                        'Glider': 121918.9997,
                        'Motor & power electronics': 2421.3612312,
                        'Plug': 187.5,
                        'Purchase tax': 0.0,
                        'msrp': 842826.0645076999},
    'vehicle_mass': {   'cargo_kg': 16329.34474,
                        'cargoLb': 36000.0000006988,
                        'essMasLb': 30422.98657024759,
                        'ess_mass_kg': 13799.65099212,
                        'fc_mass_kg': 0.0,
                        'fcMassLb': 0.0,
                        'fs_mass_kg': 0.0,
                        'fsMassLb': 0.0,
                        'glider_kg': 11776,
                        'gliderLb': 25961.605119999997,
                        'mc_mass_kg': 121.06806143893193,
                        'mcMassLb': 266.9090696094981,
                        'transKg': 360.0,
                        'transLb': 793.6632,
                        'veh_kg': 42386.06379355893,
                        'vehLb': 93445.16396055589},
    'zero_to_30': 16.361635654318608,
    'zero_to_30_loaded': 14.432964518255655,
    'zero_to_60': 75.08583117972121,
    'zero_to_60_loaded': 64.34575142966628}

fcev_2020_values = {   'disc_cost': 1158299.4350269649,
    'grade_1_25_mph_ach': 67.54018387733916,
    'grade_6_mph_ach': 27.98070929403741,
    'mpgge': {   'grid_mpgge': 8.274583590070177,
                 'kwh_per_mi': 3.5025327479103345,
                 'mpgde': 10.847360570082298,
                 'mpgge': 9.621608825662998},
    'primary_fuel_range_mi': 868.2288557519636,
    'tot_cost': 1248968.930223777,
    'veh_msrp_set': {   'Battery': 5910.0,
                        'Battery replacement': 0,
                        'Fuel Storage': 163782.0,
                        'Fuel converter': 96900.0,
                        'Glider': 121918.9997,
                        'Motor & power electronics': 2720.0,
                        'Plug': 0.0,
                        'Purchase tax': 0.0,
                        'msrp': 391230.9997},
    'vehicle_mass': {   'cargoLb': 36000.0000006988,
                        'cargo_kg': 16329.34474,
                        'essMasLb': 447.0969359999999,
                        'ess_mass_kg': 202.79999999999998,
                        'fcMassLb': 936.9635,
                        'fc_mass_kg': 425.0,
                        'fsMassLb': 5421.577670270269,
                        'fs_mass_kg': 2459.1891891891887,
                        'gliderLb': 25961.605119999997,
                        'glider_kg': 11776.0,
                        'mcMassLb': 299.8283197001716,
                        'mc_mass_kg': 135.999999864,
                        'transKg': 360.0,
                        'transLb': 793.6632,
                        'vehLb': 69860.73474666924,
                        'veh_kg': 31688.33392905319},
    'zero_to_30': 11.149442559481507,
    'zero_to_30_loaded': 12.612189835351128,
    'zero_to_60': 46.39458655724283,
    'zero_to_60_loaded': 53.85700346336351}

phev_2020_values = {   'disc_cost': 690812.6117100735,
    'grade_1_25_mph_ach': 69.88245922406252,
    'grade_6_mph_ach': 29.974993791657326,
    'mpgge': {   'ave_combined_kwh__mile': 4.018149686493237,
                 'cd_electric_kwh__mi': 0.6053378585491833,
                 'cd_electric_mpgge': 55.67138999164697,
                 'cd_fuel_kwh__mi': 2.889829734337671,
                 'cd_fuel_mpgde': 13.147222887999002,
                 'cd_fuel_mpgge': 11.661586701655114,
                 'cd_grid_electric_mpgge': 47.87739539281639,
                 'cs_fuel_kwh__mi': 4.186942848979943,
                 'cs_fuel_mpgde': 9.074218826502694,
                 'cs_fuel_mpgge': 8.048832099107889},
    'cd_aer_phev_range_mi' : 97.74195204774678,
    'cs_phev_range_mi' : 656.9333520638623,
    'true_phev_range_mi': 754.6753041116091,
    'tot_cost': 717195.7658084419,
    'veh_msrp_set': {   'Battery': 24976.885878795,
                        'Battery replacement': 0,
                        'Fuel Storage': 318.46500000000003,
                        'Fuel converter': 14211.549775319996,
                        'Glider': 121918.9997,
                        'Motor & power electronics': 1117.4940352,
                        'Plug': 187.5,
                        'Purchase tax': 0.0,
                        'msrp': 162730.894389315},
    'vehicle_mass': {   'cargoLb': 36000.0000006988,
                        'cargo_kg': 16329.34474,
                        'essMasLb': 1249.393863296294,
                        'ess_mass_kg': 566.7161974836,
                        'fcMassLb': 2091.9337578346313,
                        'fc_mass_kg': 948.8863195628414,
                        'fsMassLb': 812.4980092042566,
                        'fs_mass_kg': 368.54333590562396,
                        'gliderLb': 25961.605119999997,
                        'glider_kg': 11776.0,
                        'mcMassLb': 123.18248487094873,
                        'mc_mass_kg': 55.87470170412531,
                        'transKg': 360.0,
                        'transLb': 793.6632,
                        'vehLb': 67032.27643590492,
                        'veh_kg': 30405.36529465619},
    'zero_to_30': 11.353558185237757,
    'zero_to_30_loaded': 13.21530702927626,
    'zero_to_60': 44.97071140096316,
    'zero_to_60_loaded': 54.46309121515837}

CONV, CNG, HEV, EV, FCEV = 1, 8, 15, 22, 29
# Next, ensure TCO calculations still work based on UF modified CD CS fuel usages
# using tco_conv_test module, add PHEV, us gl.write_files and gl.TCO_INTERMEDIATES
PHEV = 36
comparison_dict = {
    '1': c8_long_haul_control_values,
    '8': cng_2020_values,
    '15': hev_2020_values,
    '22': ev_2020_values,
    '29': fcev_2020_values,
    str(PHEV): phev_2020_values,
}

def remove(out):
    """
    removes key-values from output dict that can't be compared very easily
    """
    del out['design_cycle_sim_drive_record']
    del out['accel_sim_drive_record']
    del out['accel_loaded_sim_drive_record']
    del out['grade_6_sim_drive_record']
    del out['grade_125_sim_drive_record']
    del out['vehicle']
    del out['discounted_costs_df']
    del out['scenario']
    del out['payload_cap_cost_multiplier']

class RunCONVTCOTests(unittest.TestCase):

    def setUp(self):
        print(f'Vehicle file: {gl.TESTVEHICLEINPUTS}')
        print(f'Scenario file: {gl.TESTSCENARIOINPUTS}\n')
        pass

    def compare(self, runresults, staticresults):
        """
        Check all key-value pairs between dicts for equality
        :param runresults: dict of results from generated vehicle results
        :param staticresults: dict of results from static comparison dict
        :return: None
        """
        for k, v in runresults.items():
            if type(v) is dict:
                self.compare(v, staticresults[k])
            else:
                try:
                    print(k.rjust(25, ' '), str(round(v, 3)).rjust(15, ' '), str(round(staticresults[k], 3)).rjust(15, ' '))
                    self.assertTrue(math.isclose(v, staticresults[k], rel_tol = 0.01, abs_tol = 0.01),  f"{k} fails, new value: {v} static value: {staticresults[k]}")
                except KeyError:
                    print(k, "not in static dict, run result value:", v)
                except TypeError:
                    print(k, v, staticresults[k], "fails to compare")


    def test_conv_tco_consitent(self):

        def runscenario(vnum):

            # if vnum == PHEV:
            #     gl.write_files = True

            vocscenario = str(vnum)
        
            out = run_scenario.run(vnum, str(vocscenario),
                                   vehicle_input_path=gl.TESTSDIR / gl.TESTVEHICLEINPUTS,
                                   scenario_inputs_path=gl.TESTSDIR / gl.TESTSCENARIOINPUTS,
                                   )
            # print('writing to', gl.TCO_INTERMEDIATES)
            remove(out)
            # pp = pprint.PrettyPrinter(indent=4)
            # pp.pprint(out)
            print("Comparing Vehicle:", vocscenario)

            # if vnum == PHEV:
            #     return

            self.compare(out, comparison_dict[vocscenario])

        for vnum in [FCEV, CONV, HEV, EV, PHEV]:
            runscenario(vnum)


    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
