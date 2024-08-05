import time
import pandas as pd
from dataclasses import asdict
from fastsim import vehicle

from t3co import Global as gl
from t3co import moo
from t3co.run_scenario import rerun, limit_cargo_kg_for_moo_hev_bev, set_max_battery_kwh, set_max_motor_kw

RANGE, ACCEL, GRADE, TCO = moo.RANGE, moo.ACCEL, moo.GRADE, moo.TCO

if __name__ == '__main__':

    # optimization scenario parameters where we get our baseline vehicle and scenario
    # eventually needs parameterization
    vnum = 1  #
    vocation = "Conv 2020 tech,  750 mi range"
    gl.vocation_scenario = vocation
    gl.FASTSIM_INPUTS = gl.T2COBENCHMARKDATADIR / 't3cobenchmarkFASTSimInputs.csv'
    gl.OTHER_INPUTS = gl.T2COBENCHMARKDATADIR / 't3cobenchmarkOtherInputs.csv'

    # can adjust this if we don't get good benchmark/viable results

    # sol not found
    pop_size = 10
    n_max_gen = 15
    tol = 0.01

    knobs_bounds = {
        'CdA_perc_imp': (5.0, 25.0),
        'ess_max_kwh': (500, 2_000),
        'mc_max_kw': (100, 390),
        'wt_delta_perc': (0, 25),
    }

    t0 = time.time()

    res, problem, solutions, solution = moo.run_optimization(
        pop_size, n_max_gen, knobs_bounds, vnum,
        optimize_pt=gl.BEV, skip_optimization=False, obj_list=[RANGE, ACCEL, GRADE, TCO],
        use_jit=True
    )
    if type(solution) is str and solution == 'solution not found':
        print("ALERT", solution)
    # cProfile.run('res, resd = run_optimization(pop_size, n_max_gen, knobs, knobs_bounds, vnum)',
    #              sort=SortKey.CUMULATIVE
    #              )
    t1 = time.time()

    res_df = solutions
    res_df.to_csv(gl.T2COBENCHMARKDATADIR / "moo_res_df_benchmark_bev.csv")

    def run_veh_for_sweep(i, kwh, motor, conv=False):
        if not conv:
            sweep_vehicle = vehicle.copy_vehicle(problem.mooadvancedvehicle)
            set_max_battery_kwh(sweep_vehicle, kwh)
            set_max_motor_kw(sweep_vehicle, motor)
            limit_cargo_kg_for_moo_hev_bev(problem.opt_scenario, sweep_vehicle)
            problem.opt_scenario.fuel_type = "electricity"
        else:
            problem.opt_scenario.fuel_type = "diesel"
            sweep_vehicle = problem.moobasevehicle
        outdf = rerun(sweep_vehicle, vocation, problem.opt_scenario, use_jit=True)
        outdf["CONV"] = conv
        outdf.update(outdf['veh_msrp_set'])
        outdf.update(outdf['vehicle_mass'])
        if not conv:
            outdf["mpgge"] = outdf["mpgge"]["mpgge"]
        del outdf['veh_msrp_set']
        del outdf['vehicle_mass']
        del outdf['discounted_costs_df']
        del outdf['sim_drive_record']
        del outdf['vehicle']
        del outdf['scenario']
        outdf = pd.DataFrame(outdf, index=[i])
        outdf['vehicle'] = i
        outdf['battery_kwh'] = kwh
        outdf['motor_kw'] = motor
        outdf.set_index('vehicle', inplace=True)
        return outdf

    # for each solution run its results for motor and battery
    # store each vehicle + mpgge results
    sweep_results = []
    for i, kwh, motor in zip(res_df.index, res_df['knob_ess_max_kwh'], res_df['knob_mc_max_kw']):
        outdf = run_veh_for_sweep(i, kwh, motor)
        sweep_results.append(outdf)
    outdf = run_veh_for_sweep(max(res_df.index) + 1, None, None, True)
    sweep_results.append(outdf)

    scenario = problem.opt_scenario
    # pd.DataFrame(asdict(scenario), index=[0]).to_csv(gl.T2COBENCHMARKDATADIR / "t3co_benchmark_scenario.csv")
    sweep_df = pd.concat(sweep_results)
    sweep_df.sort_values(inplace=True, by='tot_cost')
    sweep_df['GVWRLb'] = gl.kg_to_lbs(scenario.gvwr_kg)
    sweep_df['GVWRCreditLb'] = gl.kg_to_lbs(scenario.gvwr_credit_kg)
    sweep_df['GVWRMaxLb'] = gl.kg_to_lbs(scenario.gvwr_credit_kg) + gl.kg_to_lbs(scenario.gvwr_kg)
    sweep_df.to_csv(gl.T2COBENCHMARKDATADIR / "t2co_moo_sweep_solution_set.csv")


