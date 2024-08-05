"""Module for simulating acceleration performance."""
# %%
import time
from pathlib import Path

import numpy as np
from fastsim import cycle
from fastsim import parameters as params

from t3co.run import Global as gl
from t3co.run import run_scenario


def get_accel(
    analysis_vehicle,
    scenario=None,
    set_weight_to_max_kg=True,
    verbose=False,
    ess_init_soc=None,
):
    """
    This function runs a simdrive for getting 0-to-60 and 0-30 mph time with fully laden weight at GVWR (plus gvwr_credit_kg?)


    Args:
        analysis_vehicle (fastsim.vehicle.Vehicle): FASTSim vehicle object for analysis vehicle
        scenario (run_scenario.Scenario, optional): Scenario object for current selection. Defaults to None.
        set_weight_to_max_kg (bool, optional): if True, runs run_scenario.set_test_weight(). Defaults to True.
        verbose (bool, optional): if True, prints the process steps. Defaults to False.
        ess_init_soc (float, optional): ESS initial SOC override. Defaults to None.

    Returns:
        zero_to_sixty (float): 0-60 mph acceleration time in sec
        zero_to_thirty (float): 0-30 mph acceleration time in sec
        accel_simdrive (fastsim.simdrive.SimDrive): FASTSim.simdrive.SimDrive object for running the acceleration drivecycle

    """
    CYC_MPH = 90

    kg_before = None
    if set_weight_to_max_kg and scenario is not None:
        kg_before = analysis_vehicle.veh_kg
        run_scenario.set_test_weight(analysis_vehicle, scenario)

    # load the vehicle
    t0 = time.time()

    if verbose:
        print(f"f'{Path(__file__).name}:: Vehicle load time: {time.time() - t0:.3f} s")
    # load the cycles
    t0 = time.time()
    accel_cyc_secs = np.arange(300)
    cyc_dict = {
        "time_s": accel_cyc_secs,
        "mps": np.append(
            [0], np.ones(len(accel_cyc_secs) - 1) * CYC_MPH / params.MPH_PER_MPS
        ),
        "cycGrade": np.zeros(len(accel_cyc_secs)),
    }

    cyc_accel = cycle.Cycle.from_dict(cyc_dict)

    accel_simdrive = run_scenario.get_objective_simdrive(analysis_vehicle, cyc_accel)

    run_scenario.run_grade_or_accel(
        "accel", analysis_vehicle, accel_simdrive, ess_init_soc
    )
    # print(f'accel:get_accel::>>> {type(accel_simdrive.sim_params)} accel_simdrive.sim_params.trace_miss_dist_tol', accel_simdrive.sim_params.trace_miss_dist_tol)
    # print(f'accel:get_accel::>>> {type(accel_simdrive.sim_params)} accel_simdrive.sim_params.trace_miss_speed_mps_tol ', accel_simdrive.sim_params.trace_miss_speed_mps_tol )
    assert (
        accel_simdrive.trace_miss_dist_frac
        <= accel_simdrive.sim_params.trace_miss_dist_tol
    )

    def test_accel(speed_mph_target):
        """
        This function gets the time it takes to reach target speed

        Args:
            speed_mph_target (float): Target speed for acceleration time

        Returns:
            zero_to_target_mph_s (float): Time taken to reach target speed
        """
        # seconds to target mph test
        if (np.array(accel_simdrive.mph_ach) >= speed_mph_target).any():
            zero_to_target_mph_s = np.interp(
                x=speed_mph_target,
                xp=np.array(accel_simdrive.mph_ach),
                fp=cyc_accel.time_s,
            )
        else:
            # in case vehicle never exceeds speed_mph_target mph, penalize it a lot with a high number
            # print(analysis_vehicle.scenario_name + f' did not achieve {speed_mph_target} mph during the accel test')
            zero_to_target_mph_s = -accel_simdrive.mph_ach[-1]

        return zero_to_target_mph_s

    # seconds to 60 test
    zero_to_sixty = test_accel(60)
    # seconds to 30 test
    zero_to_thirty = test_accel(30)

    #  an assert to ensure that vehicle weight is reset correctly
    if set_weight_to_max_kg and scenario is not None:
        run_scenario.reset_vehicle_weight(analysis_vehicle)
        kg_after = analysis_vehicle.veh_kg
        assert (
            kg_after == kg_before
        ), f"total vehicle kg (veh_kg) kg_after must be to kg_before, {kg_after} != {kg_before}"

    return zero_to_sixty, zero_to_thirty, accel_simdrive


# %%

if __name__ == "__main__":
    # PHEV DEBUGGING
    vehicle_input_path = Path(
        gl.T3CO_INPUTS_DIR / "tda_example/TDA_FY22_vehicle_model_assumptions.csv"
    ).resolve()
    scenario_inputs_path = Path(
        gl.T3CO_INPUTS_DIR / "tda_example/TDA_FY22_scenario_assumptions.csv"
    ).resolve()
    # load the generated file of vehicles, drive cycles, and tech targets
    PHEV = 365
    v = run_scenario.get_vehicle(PHEV, vehicle_input_path)
    scenario, _ = run_scenario.get_scenario_and_cycle(PHEV, scenario_inputs_path)
    zero_to_sixty, zero_to_thirty, accel_simdrive = get_accel(
        v,
        scenario=scenario,
        set_weight_to_max_kg=False,
        verbose=False,
        ess_init_soc=None,
    )
    # %%
    init_socs = [i for i in np.linspace(v.min_soc, v.max_soc, 10)]
    zero_to_sixties = []
    for insoc in init_socs:
        zero_to_sixty, zero_to_thirty, accel_simdrive = get_accel(
            v,
            scenario=scenario,
            set_weight_to_max_kg=False,
            verbose=False,
            ess_init_soc=insoc,
        )
        zero_to_sixties.append(zero_to_sixty)
    # %%
