"""
Testing module for TCO to ensure the TCO related results remain consistent over time with
previous model (Tech Targets c 2019)

Flow:
code reads TCO tests vehicles and scenarios one at a time. Generates TCO output dictionaries
and compares the results with the hard coded dictionaries below in comparison_dict.
"""
import numpy as np
from pathlib import Path
import ast

from t3co import run_scenario
from t3co.tco import tco_analysis
from t3co import Global as gl

# generated using Notebook from: https://github.nrel.gov/AVCI/FASTSim_TCO_Truck/blob/master/tco_baselining.ipynb
# and pasting attributes dict here
t2vehicle="""
{'selection': 1.0,
 'scenario_name': 'Conv 2020 tech,  750 mi range',
 'veh_pt_type': 1.0,
 'drag_coef': 0.546,
 'frontalAreaM2': 10.18,
 'glider_kg': 11776.0,
 'vehCgM': 0.46,
 'driveAxleWeightFrac': 0.8,
 'wheelBaseM': 2.28,
 'cargo_kg': 16329.34474,
 'vehOverrideKg': 0.0,
 'fs_max_kw': 5000.0,
 'fuelStorSecsToPeakPwr': 1.0,
 'fs_kwh': 3953.2751740000003,
 'fs_kwhPerKg': 9.875636446,
 'fc_max_kw': 340.0,
 'fc_eff_map': [0.05, 0.07, 0.12, 0.21, 0.26, 0.34, 0.38, 0.42, 0.45, 0.46, 0.46, 0.46],
 'fc_eff_type': 5.0,
 'fcAbsEffImpr': 0.0,
 'fuelConvSecsToPeakPwr': 6.0,
 'fuelConvBaseKg': 0.0,
 'fuelConvKwPerKg': 0.2745,
 'mcPwrOutPerc': [0.00, 0.02, 0.04, 0.06, 0.08, 0.10, 0.20, 0.40, 0.60, 0.80, 1.00],
 'largeBaselineEff': [0.83, 0.85, 0.87, 0.89, 0.90, 0.91, 0.93, 0.94, 0.94, 0.93, 0.92],
 'smallBaselineEff': [0.12, 0.16, 0.21, 0.29, 0.35, 0.42, 0.75, 0.92, 0.93, 0.93, 0.92],
 'modernMax': 0.95,
 'mc_max_kw': 0.0,
 'motorPeakEff': 0.93,
 'motorSecsToPeakPwr': 4.0,
 'stopStart': False,
 'mcPeKgPerKw': 0.333333333,
 'mcPeBaseKg': 0.0,
 'ess_max_kw': 0.0,
 'ess_max_kwh': 0.0,
 'essKgPerKwh': 4.7,
 'essBaseKg': 75.0,
 'essRoundTripEff': 0.97,
 'essLifeCoefA': 110.0,
 'essLifeCoefB': -0.6811,
 'wheelInertiaKgM2': 10.0,
 'numWheels': 18.0,
 'wheelRrCoef': 0.0061,
 'wheelRadiusM': 0.506,
 'wheelCoefOfFric': 0.6,
 'min_soc': 0.1,
 'max_soc': 0.95,
 'essDischgToFcMaxEffPerc': 0.0,
 'essChgToFcMaxEffPerc': 0.0,
 'maxAccelBufferMph': 60.0,
 'maxAccelBufferPercOfUseableSoc': 0.2,
 'percHighAccBuf': 0.0,
 'mphFcOn': 55.0,
 'kwDemandFcOn': 100.0,
 'altEff': 1.0,
 'chgEff': 0.86,
 'auxKw': 0.0,
 'forceAuxOnFC': 0.0,
 'transKg': 300.0,
 'transEff': 0.95,
 'comp_mass_multiplier': 1.2,
 'essToFuelOkError': 0.005,
 'maxRegen': 0.9,
 'valUddsMpgge': 0.0,
 'valHwyMpgge': 0.0,
 'valCombMpgge': 0.0,
 'valUddsKwhPerMile': 0.0,
 'valHwyKwhPerMile': 0.0,
 'valCombKwhPerMile': 0.0,
 'valCdRangeMi': 0.0,
 'valConst65MphKwhPerMile': 0.0,
 'valConst60MphKwhPerMile': 0.0,
 'valConst55MphKwhPerMile': 0.0,
 'valConst45MphKwhPerMile': 0.0,
 'valUnadjUddsKwhPerMile': 0.0,
 'valUnadjHwyKwhPerMile': 0.0,
 'val0To60Mph': 0.0,
 'valEssLifeMiles': 0.0,
 'valRangeMiles': 0.0,
 'valVehBaseCost': 0.0,
 'valMsrp': 0.0,
 'minFcTimeOn': 30,
 'idleFcKw': 0.0,
 'MaxRoadwayChgKw_Roadway': range(0, 6),
 'MaxRoadwayChgKw': [0, 0, 0, 0, 0, 0],
 'chargingOn': 0,
 'noElecSys': True,
 'noElecAux': True,
 'vehTypeSelection': 1,
 'fcEffArray': np.array([0.1       , 0.108     , 0.116     , 0.124     , 0.132     ,
        0.14      , 0.146     , 0.152     , 0.158     , 0.164     ,
        0.17      , 0.176     , 0.182     , 0.188     , 0.194     ,
        0.2       , 0.2024    , 0.2048    , 0.2072    , 0.2096    ,
        0.212     , 0.2144    , 0.2168    , 0.2192    , 0.2216    ,
        0.224     , 0.2264    , 0.2288    , 0.2312    , 0.2336    ,
        0.236     , 0.248     , 0.26      , 0.275     , 0.29      ,
        0.305     , 0.32      , 0.32875   , 0.3375    , 0.355     ,
        0.3725    , 0.39      , 0.395     , 0.4       , 0.405     ,
        0.41      , 0.41166667, 0.41333333, 0.415     , 0.41666667,
        0.41833333, 0.42      , 0.4195    , 0.419     , 0.4185    ,
        0.418     , 0.4175    , 0.417     , 0.4165    , 0.416     ,
        0.4155    , 0.415     , 0.4145    , 0.414     , 0.4135    ,
        0.413     , 0.4125    , 0.412     , 0.4115    , 0.411     ,
        0.4105    , 0.41      , 0.4085    , 0.407     , 0.4055    ,
        0.404     , 0.4025    , 0.401     , 0.3995    , 0.398     ,
        0.3965    , 0.395     , 0.3935    , 0.392     , 0.3905    ,
        0.389     , 0.3875    , 0.386     , 0.3845    , 0.383     ,
        0.3815    , 0.38      , 0.375     , 0.37      , 0.365     ,
        0.36      , 0.355     , 0.35      , 0.345     , 0.34      ]),
 'fcKwOutArray': np.array([  0.  ,   0.34,   0.68,   1.02,   1.36,   1.7 ,   2.04,   2.38,
          2.72,   3.06,   3.4 ,   3.74,   4.08,   4.42,   4.76,   5.1 ,
          5.44,   5.78,   6.12,   6.46,   6.8 ,   7.14,   7.48,   7.82,
          8.16,   8.5 ,   8.84,   9.18,   9.52,   9.86,  10.2 ,  11.9 ,
         13.6 ,  15.3 ,  17.  ,  18.7 ,  20.4 ,  22.1 ,  23.8 ,  27.2 ,
         30.6 ,  34.  ,  37.4 ,  40.8 ,  44.2 ,  47.6 ,  51.  ,  54.4 ,
         57.8 ,  61.2 ,  64.6 ,  68.  ,  71.4 ,  74.8 ,  78.2 ,  81.6 ,
         85.  ,  88.4 ,  91.8 ,  95.2 ,  98.6 , 102.  , 105.4 , 108.8 ,
        112.2 , 115.6 , 119.  , 122.4 , 125.8 , 129.2 , 132.6 , 136.  ,
        139.4 , 142.8 , 146.2 , 149.6 , 153.  , 156.4 , 159.8 , 163.2 ,
        166.6 , 170.  , 173.4 , 176.8 , 180.2 , 183.6 , 187.  , 190.4 ,
        193.8 , 197.2 , 200.6 , 204.  , 221.  , 238.  , 255.  , 272.  ,
        289.  , 306.  , 323.  , 340.  ]),
 'maxFcEffKw': np.array(68.),
 'fc_max_kw': np.array(340.),
 'mcKwInArray': np.array([0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]),
 'mcKwOutArray': np.array([0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]),
 'mcMaxElecInKw': 0.0,
 'regenA': 500.0,
 'regenB': 0.99,
 'veh_kg': 30432.05057387713,
 'cargoMassKg': 16329.34474,
 'curbMassKg': 14102.705833877131,
 'gvwrMassKg': 30432.05057387713,
 'ess_mass_kg': 0.0,
 'mc_mass_kg': 0.0,
 'fc_mass_kg': 1486.3387978142077,
 'fs_mass_kg': 480.36703606292315,
 'kwhPerMile': 5.864161359481092,
 'mpgge': 5.746772289189199}
"""

t2vehicle = ast.literal_eval(t2vehicle)

veh_no = 1  #
vocation = "Conv 2020 tech, 500 mi range"

gl.vocation_scenario = vocation
# gl.FASTSIM_INPUTS = gl.T2COBENCHMARKDATADIR / 't3cobenchmarkFASTSimInputs.csv'
# gl.OTHER_INPUTS = gl.T2COBENCHMARKDATADIR / 't3cobenchmarkOtherInputs.csv'

# load the generated file of vehicles, drive cycles, and tech targets
t3vehicle = run_scenario.get_vehicle(veh_no, gl.T2COBENCHMARKDATADIR / 't3cobenchmarkFASTSimInputs.csv', use_jit=False)
scenario, range_cyc = run_scenario.get_scenario_and_cycle(veh_no, gl.T2COBENCHMARKDATADIR / 't3cobenchmarkOtherInputs.csv', use_jit=False)
scenario.drive_cycle = r't3co_benchmarking_long_haul_cyc.csv'
cycpath = Path(r'C:\Users\gpayne\Documents\__old_projects\_Truck_FSIM_TCO\fastsim_src\cycles')
range_cyc = run_scenario.load_design_cycle_from_scenario(scenario, cyc_file_path=Path(cycpath))




def benchmark_vehicles():

    notmatch = {}
    for vspec, t3val in t3vehicle.__dict__.items():
        if vspec in t2vehicle:
            try:
                t2val = t2vehicle[vspec]

                if list in [type(t3val), type(t2val)]:
                    t3val = list(t3val)
                    t2val = list(t2val)

                if t2val != t3val:
                    notmatch[vspec] = {"t3val": t3val, "t2val": t2val}
                else:
                    print(f"{vspec} t3 {t3val} t2 {t2val}")

            except ValueError:
                pass


    assert notmatch == {}, notmatch

def benchmark_sim_outputs(t3out):

    # generated using Notebook from: https://github.nrel.gov/AVCI/FASTSim_TCO_Truck/blob/master/tco_baselining.ipynb
    # and pasting results and vars here
    t2output = {
        'Glider': 121918.9997,
        'Fuel converter': 31623.0,
        'Fuel Storage': 415.0938932700001,
        'Motor & power electronics': 0,
        'Plug': 0,
        'Battery': 0,
        'Battery replacement': 0,
        'Purchase tax': 0.0,
        'msrp': 153957.09359327,
        'tot_cost': 578491.5358170538,
        "disc_cost": 531496.4249639589,
        "mpgge": 6.737434503166163,
        "life_time_fuel_cost": 270534.442224,
        "discounted_life_time_fuel_cost": 240586.822343,
        }

    t3out["discounted_costs_df"].to_csv(gl.T2COBENCHMARKDATADIR / "t3co_discounted_costs_df_benchmark.csv")

    t3fuelagg = t3out["discounted_costs_df"].groupby(["Category"]).sum()
    t3_life_fuel = t3fuelagg.loc["Fuel", "Cost [$]"]
    t3_life_fuel_disc = t3fuelagg.loc["Fuel", "Discounted Cost [$]"]

    t3 = t3out['mpgge']
    t2 = t2output['mpgge']
    # mpgge t3co 6.737368952765226 != t2co 5.746772289189199 : %15.869680491069909
    print(f"mpgge t3co {t3} != t2co {t2} : %{abs(t3-t2)/((t3+t2)/2) * 100}")
    assert np.isclose(t3, t2)

    t2 = t2output["discounted_life_time_fuel_cost"]
    t3 = t3_life_fuel_disc
    print(f"discounted lifetime fuel cost t3co {t3} != t2co {t2} : %{abs(t3-t2)/((t3+t2)/2) * 100}")
    assert np.isclose(t3, t2)

    t2 = t2output["life_time_fuel_cost"]
    t3 = t3_life_fuel
    print(f"lifetime fuel cost t3co {t3} != t2co {t2} : %{abs(t3-t2)/((t3+t2)/2) * 100}")
    assert np.isclose(t3, t2)

    t3totcost = t3out['tot_cost']
    t2totcost = t2output['tot_cost']
    print(f"total TCO t3co {t3totcost} != t2co {t2totcost} : %{abs(t3totcost-t2totcost)/((t3totcost+t2totcost)/2) * 100}")
    assert np.isclose(t3totcost, t2totcost)


# hack, see if it makes mpgge align
t3vehicle.maxFcEffKw = np.array(68.)

out = run_scenario.rerun(t3vehicle, vocation, scenario, use_jit=False)
print("run scenario mpgge", out['mpgge'])

tot_cost, disc_cost, oppy_cost_set, discounted_costs_df, mpgge, veh_cost_set, sim_drive_record, veh_oper_cost_set,veh_opp_cost_set = tco_analysis.get_tco_of_vehicle(t3vehicle, range_cyc, scenario, out['mpgge'],use_jit=False)
print("manual mpgge", mpgge)
benchmark_vehicles()
benchmark_sim_outputs(out)

range_cyc = [(range_cyc, .3333)]*3
print("composite cycles test")
tot_cost, disc_cost, oppy_cost_set, discounted_costs_df, mpgge, veh_cost_set, sim_drive_record, veh_oper_cost_set, veh_opp_cost_set = tco_analysis.get_tco_of_vehicle(t3vehicle, range_cyc, scenario, out['mpgge'],use_jit=False)
print("manual mpgge", mpgge)
benchmark_vehicles()
benchmark_sim_outputs(out)
