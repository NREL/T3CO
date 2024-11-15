"""
Testing module for TCO to ensure the TCO related results remain consistent over time with
previous model (Tech Targets c 2019)

Flow:
code reads TCO tests vehicles and scenarios one at a time. Generates TCO output dictionaries
and compares the results with the hard coded dictionaries below in comparison_dict.
"""
import numpy as np
import ast

# generated using Notebook from: https://github.nrel.gov/AVCI/FASTSim_TCO_Truck/blob/master/get_BEV_mpgge_t3co_baselining.ipynb
# and pasting attributes dict here
t2vehicle="""
{
    'selection': 4.0,
    'scenario_name': 'EV 2025 tech,  750 mi range',
    'veh_pt_type': 4.0,
    'drag_coef': 0.5026666670000001,
    'frontalAreaM2': 10.18,
    'glider_kg': 11776.0,
    'vehCgM': 0.46,
    'driveAxleWeightFrac': 0.8,
    'wheelBaseM': 2.28,
    'cargo_kg': 16329.34474,
    'vehOverrideKg': 0.0,
    'fs_max_kw': 5000.0,
    'fuelStorSecsToPeakPwr': 1.0,
    'fs_kwh': 0.0,
    'fs_kwhPerKg': 9.875636446,
    'fc_max_kw': 0.0,
    'fc_eff_map': [0.1, 0.14, 0.2, 0.26, 0.32, 0.39, 0.41, 0.42, 0.41, 0.38, 0.36, 0.34],
    'fc_eff_type': 3.0,
    'fcAbsEffImpr': 0.0,
    'fuelConvSecsToPeakPwr': 6.0,
    'fuelConvBaseKg': 0.0,
    'fuelConvKwPerKg': 0.0,
    'mcPwrOutPerc': [0.00, 0.02, 0.04, 0.06, 0.08, 0.10, 0.20, 0.40, 0.60, 0.80, 1.00],
    'largeBaselineEff': [0.83, 0.85, 0.87, 0.89, 0.90, 0.91, 0.93, 0.94, 0.94, 0.93, 0.92],
    'smallBaselineEff': [0.12, 0.16, 0.21, 0.29, 0.35, 0.42, 0.75, 0.92, 0.93, 0.93, 0.92],
    'modernMax': 0.95,
    'mc_max_kw': 295.00825069999996,
    'motorPeakEff': 0.939526407,
    'motorSecsToPeakPwr': 4.0,
    'stopStart': False,
    'mcPeKgPerKw': 0.266344418,
    'mcPeBaseKg': 0.0,
    'ess_max_kw': 324.5090758,
    'ess_max_kwh': 2430.789183,
    'essKgPerKwh': 4.03,
    'essBaseKg': 75.0,
    'essRoundTripEff': 0.97,
    'essLifeCoefA': 110.0,
    'essLifeCoefB': -0.6811,
    'wheelInertiaKgM2': 10.0,
    'numWheels': 18.0,
    'wheelRrCoef': 0.005966666999999999,
    'wheelRadiusM': 0.506,
    'wheelCoefOfFric': 0.6,
    'min_soc': 0.03,
    'max_soc': 0.8148564220000001,
    'essDischgToFcMaxEffPerc': 0.0,
    'essChgToFcMaxEffPerc': 0.0,
    'maxAccelBufferMph': 60.0,
    'maxAccelBufferPercOfUseableSoc': 0.2,
    'percHighAccBuf': 0.0,
    'mphFcOn': 1.0,
    'kwDemandFcOn': 100.0,
    'altEff': 1.0,
    'chgEff': 0.8766446609999999,
    'auxKw': 3.233333333,
    'forceAuxOnFC': 0.0,
    'transKg': 300.0,
    'transEff': 0.95,
    'comp_mass_multiplier': 1.2,
    'essToFuelOkError': 0.005,
    'maxRegen': 0.9,
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
    'noElecSys': False,
    'noElecAux': False,
    'vehTypeSelection': np.array(4.),
    'maxFcEffKw': 0,
    'fc_max_kw': 0,
    'mcKwInArray': np.array([  0.        ,   3.4706853 ,   6.86065699,  10.1726983 ,
          13.40946594,  16.57349723,  19.66721671,  22.81831773,
          25.93479127,  29.01720499,  32.06611421,  35.19621212,
          38.31275983,  41.41584513,  44.50555506,  47.58197592,
          50.64519325,  53.69529188,  56.7323559 ,  59.75646869,
          62.76771291,  65.87106076,  68.97111068,  72.06786794,
          75.16133776,  78.25152538,  81.33843604,  84.42207492,
          87.50244724,  90.57955818,  93.65341292,  96.72401662,
          99.79137444, 102.85549153, 105.91637301, 108.97402401,
         112.02844963, 115.07965499, 118.12764517, 121.17242525,
         124.21400029, 127.3193503 , 130.42470031, 133.53005032,
         136.63540032, 139.74075033, 142.84610034, 145.95145035,
         149.05680035, 152.16215036, 155.26750037, 158.37285038,
         161.47820038, 164.58355039, 167.6889004 , 170.79425041,
         173.89960041, 177.00495042, 180.11030043, 183.21565043,
         186.32100044, 189.52610103, 192.73457896, 195.94643958,
         199.16168824, 202.3803303 , 205.60237113, 208.82781613,
         212.05667069, 215.28894023, 218.52463015, 221.76374589,
         225.00629291, 228.25227664, 231.50170256, 234.75457615,
         238.0109029 , 241.2706883 , 244.53393788, 247.80065715,
         251.07085166, 254.34452695, 257.62168858, 260.90234212,
         264.18649316, 267.4741473 , 270.76531014, 274.0599873 ,
         277.35818442, 280.65990713, 283.9651611 , 287.27395199,
         290.58628549, 293.90216727, 297.22160306, 300.54459857,
         303.87115952, 307.20129166, 310.53500074, 313.87229252,
         317.2131728 ]),
    'mcKwOutArray': np.array([  0.        ,   2.95008251,   5.90016501,   8.85024752,
          11.80033003,  14.75041253,  17.70049504,  20.65057755,
          23.60066006,  26.55074256,  29.50082507,  32.45090758,
          35.40099008,  38.35107259,  41.3011551 ,  44.2512376 ,
          47.20132011,  50.15140262,  53.10148513,  56.05156763,
          59.00165014,  61.95173265,  64.90181515,  67.85189766,
          70.80198017,  73.75206267,  76.70214518,  79.65222769,
          82.6023102 ,  85.5523927 ,  88.50247521,  91.45255772,
          94.40264022,  97.35272273, 100.30280524, 103.25288774,
         106.20297025, 109.15305276, 112.10313527, 115.05321777,
         118.00330028, 120.95338279, 123.90346529, 126.8535478 ,
         129.80363031, 132.75371282, 135.70379532, 138.65387783,
         141.60396034, 144.55404284, 147.50412535, 150.45420786,
         153.40429036, 156.35437287, 159.30445538, 162.25453788,
         165.20462039, 168.1547029 , 171.10478541, 174.05486791,
         177.00495042, 179.95503293, 182.90511543, 185.85519794,
         188.80528045, 191.75536295, 194.70544546, 197.65552797,
         200.60561048, 203.55569298, 206.50577549, 209.455858  ,
         212.4059405 , 215.35602301, 218.30610552, 221.25618802,
         224.20627053, 227.15635304, 230.10643555, 233.05651805,
         236.00660056, 238.95668307, 241.90676557, 244.85684808,
         247.80693059, 250.75701309, 253.7070956 , 256.65717811,
         259.60726062, 262.55734312, 265.50742563, 268.45750814,
         271.40759064, 274.35767315, 277.30775566, 280.25783817,
         283.20792067, 286.15800318, 289.10808569, 292.05816819,
         295.0082507 ]),
    'mcMaxElecInKw': 317.2131727956989,
    'mcFullEffArray': np.array([0.    , 0.85  , 0.86  , 0.87  , 0.88  , 0.89  , 0.9   , 0.905 ,
         0.91  , 0.915 , 0.92  , 0.922 , 0.924 , 0.926 , 0.928 , 0.93  ,
         0.932 , 0.934 , 0.936 , 0.938 , 0.94  , 0.9405, 0.941 , 0.9415,
         0.942 , 0.9425, 0.943 , 0.9435, 0.944 , 0.9445, 0.945 , 0.9455,
         0.946 , 0.9465, 0.947 , 0.9475, 0.948 , 0.9485, 0.949 , 0.9495,
         0.95  , 0.95  , 0.95  , 0.95  , 0.95  , 0.95  , 0.95  , 0.95  ,
         0.95  , 0.95  , 0.95  , 0.95  , 0.95  , 0.95  , 0.95  , 0.95  ,
         0.95  , 0.95  , 0.95  , 0.95  , 0.95  , 0.9495, 0.949 , 0.9485,
         0.948 , 0.9475, 0.947 , 0.9465, 0.946 , 0.9455, 0.945 , 0.9445,
         0.944 , 0.9435, 0.943 , 0.9425, 0.942 , 0.9415, 0.941 , 0.9405,
         0.94  , 0.9395, 0.939 , 0.9385, 0.938 , 0.9375, 0.937 , 0.9365,
         0.936 , 0.9355, 0.935 , 0.9345, 0.934 , 0.9335, 0.933 , 0.9325,
         0.932 , 0.9315, 0.931 , 0.9305, 0.93  ]),
    'mcEffArray': np.array([0.84, 0.86, 0.88, 0.9 , 0.91, 0.92, 0.94, 0.95, 0.95, 0.94, 0.93]),
    'regenA': 500.0,
    'regenB': 0.99,
    'veh_kg': 40404.92978999347,
    'cargoMassKg': 16329.34474,
    'curbMassKg': 24075.585049993468,
    'gvwrMassKg': 40404.92978999347,
    'ess_mass_kg': 11845.296488988,
    'mc_mass_kg': 94.28856100546751,
    'fc_mass_kg': 0.0,
    'fs_mass_kg': 0.0,
    'mpgge': 13.330364402123372,
    'is_base': False,
    'fuel_type': 'electricity',
}
"""

t2vehicle = ast.literal_eval(t2vehicle)

from t3co import run_scenario
from t3co import Global as gl

veh_no = 4  #
vocation = "EV 2025 tech,  750 mi range"

gl.vocation_scenario = vocation


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
            except ValueError:
                pass
    assert notmatch == {}, notmatch


# load the generated file of vehicles, drive cycles, and tech targets
t3vehicle = run_scenario.get_vehicle(veh_no, gl.T2COBENCHMARKDATADIR / 't3cobenchmarkFASTSimInputs.csv', use_jit=False)

assert t3vehicle.veh_pt_type == gl.BEV

scenario, range_cyc = run_scenario.get_scenario_and_cycle(veh_no, gl.T2COBENCHMARKDATADIR / 't3cobenchmarkOtherInputs.csv', use_jit=False)

out = run_scenario.rerun(t3vehicle, vocation, scenario, use_jit=False)

t2mpgge = t2vehicle['mpgge']
t3mpgge = out['mpgge']
print(f"t3co BEV mpgge {t3mpgge} \nt2co BEV mpgge {t2mpgge}")
print(t3vehicle)
benchmark_vehicles()
