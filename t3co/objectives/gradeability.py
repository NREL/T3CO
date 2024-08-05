# %%

import time
from pathlib import Path

import numpy as np
from fastsim import cycle
from fastsim import parameters as params

from t3co.run import Global as gl
from t3co.run import run_scenario


def get_gradeability(
    analysis_vehicle,
    scenario=None,
    verbose=False,
    ess_init_soc=None,
    set_weight_to_max_kg=True,
):
    """
    This function runs SimDrives to determine the gradeability at given speed and the grade vehicle is
    evaluated at how much it meets or exceeds target speed at the target grade.

    Args:
        analysis_vehicle (fastsim.vehicle.Vehicle): FASTSim vehicle object for analysis vehicle
        scenario (run_scenario.Scenario, optional): Scenario object for current selection. Defaults to None.
        verbose (bool, optional): if True, prints process steps. Defaults to False.
        ess_init_soc (float, optional): ESS Initial SOC override. Defaults to None.
        set_weight_to_max_kg (bool, optional): if True, run_scenario.set_test_weight() overrides vehice weight to GVWR. Defaults to True.

    Returns:
        grade_6percent_mph_ach (float): Achieved speed on 6% grade test
        grade_1pt25percent_mph_ach (float): Achieved speed on 1.25% grade test
        grade_6_simdrive (fastsim.simdrive.SimDrive): FASTSim SimDrive for gradeability test of 6% grade
        grade_125_simdrive (fastsim.simdrive.SimDrive): FASTSim SimDrive for gradeability test of 1.25% grade
    """
    SIX_GRADE = 0.06
    ONE_POINT_TWENTY_FIVE_GRADE = 0.0125
    CYC_SECONDS = 100
    CYC_MPH = 90

    t0 = time.time()

    if scenario is not None and set_weight_to_max_kg:
        kg_before = analysis_vehicle.veh_kg
        run_scenario.set_test_weight(analysis_vehicle, scenario)

    if verbose:
        print(f"f'{Path(__file__).name}:: Vehicle load time: {time.time() - t0:.3f} s")
    # load the cycles

    def get_grade_perf(target_grade):
        """
        This function obtains the maximum speed achieved on gradeability test for target grade

        Args:
            target_grade (float): Input constant grade for gradeability test

        Returns:
            target_grade_mph_ach (float): Achieved maximum speed mph on gradeability test
            grade_simdrive (fastsim.simdrive.SimDrive): FASTSim SimDrive object for constant grade cycle
        """
        # Test speed achieved at end of 5 minutes at 6% grade (default)
        first_time_step_mph = 0
        if scenario is not None:
            if target_grade == SIX_GRADE:
                first_time_step_mph = scenario.min_speed_at_6pct_grade_in_5min_mph
                if verbose:
                    print(
                        f"f'{Path(__file__).name}:: scenario.min_speed_at_6pct_grade_in_5min_mph: {scenario.min_speed_at_6pct_grade_in_5min_mph}"
                    )
            if target_grade == ONE_POINT_TWENTY_FIVE_GRADE:
                first_time_step_mph = scenario.min_speed_at_125pct_grade_in_5min_mph
                if verbose:
                    print(
                        f"f'{Path(__file__).name}:: scenario.min_speed_at_125pct_grade_in_5min_mph: {scenario.min_speed_at_125pct_grade_in_5min_mph}"
                    )
        if verbose:
            print(
                f"f'{Path(__file__).name}:: first_time_step_mph: {first_time_step_mph}"
            )
        target_grade_cyc_secs = np.arange(CYC_SECONDS)
        cyc_dict = {
            "cycSecs": target_grade_cyc_secs,
            "cycMps": np.append(
                [first_time_step_mph], np.ones(CYC_SECONDS - 1) * CYC_MPH
            )
            / params.MPH_PER_MPS,
            "cycGrade": np.ones(CYC_SECONDS) * target_grade,
        }

        grade_cycle = cycle.Cycle.from_dict(cyc_dict)

        if verbose:
            print(
                f"f'{Path(__file__).name}:: Cycle load time: {time.time() - t0:.3f} s"
            )

        grade_simdrive = run_scenario.get_objective_simdrive(
            analysis_vehicle, grade_cycle
        )

        run_scenario.run_grade_or_accel(
            "grade", analysis_vehicle, grade_simdrive, ess_init_soc
        )

        assert (
            grade_simdrive.trace_miss_dist_frac
            <= grade_simdrive.sim_params.trace_miss_dist_tol
        )

        target_grade_mph_ach = grade_simdrive.mph_ach[-1]
        return target_grade_mph_ach, grade_simdrive

    grade_6percent_mph_ach, grade_6_simdrive = get_grade_perf(SIX_GRADE)
    grade_1pt25percent_mph_ach, grade_125_simdrive = get_grade_perf(
        ONE_POINT_TWENTY_FIVE_GRADE
    )
    if scenario is not None and set_weight_to_max_kg:
        run_scenario.reset_vehicle_weight(analysis_vehicle)
        kg_after = analysis_vehicle.veh_kg
        assert (
            kg_after == kg_before
        ), f"total vehicle kg (veh_kg) kg_after must be equal to kg_before: kg_after/kg_before {round(kg_after,4)}/{round(kg_before, 4)}"

    return (
        grade_6percent_mph_ach,
        grade_1pt25percent_mph_ach,
        grade_6_simdrive,
        grade_125_simdrive,
    )


# %%

if __name__ == "__main__":
    vehicle_input_path = Path(
        gl.T3CO_INPUTS_DIR / "phev-testing/TDA_FY22_vehicle_model_assumptions.csv"
    ).resolve()
    scenario_inputs_path = Path(
        gl.T3CO_INPUTS_DIR / "phev-testing/TDA_FY22_scenario_assumptions.csv"
    ).resolve()
    # load the generated file of vehicles, drive cycles, and tech targets
    PHEV = 365

    analysis_vehicle = run_scenario.get_vehicle(PHEV, vehicle_input_path)

    scenario, _ = run_scenario.get_scenario_and_cycle(PHEV, scenario_inputs_path)
    (
        grade_6percent_mph_ach,
        grade_1pt25percent_mph_ach,
        grade_6_simdrive,
        grade_125_simdrive,
    ) = get_gradeability(
        analysis_vehicle,
        scenario=scenario,
        verbose=True,
        ess_init_soc=None,
        set_weight_to_max_kg=True,
    )
    print(grade_6percent_mph_ach, grade_1pt25percent_mph_ach)
    # %%
    v = analysis_vehicle
    init_socs = [i for i in np.linspace(v.min_soc, v.max_soc, 10)]
    g6mphachs = []
    soc_used = []
    print(f"ess kwh size {v.ess_max_kwh}")
    print(f"max motor kw {v.mc_max_kw}")
    print(f"max fc kw {v.fc_max_kw}")
    for insoc in init_socs:
        g6mphach, g125mphach, g6sd, g125sd = get_gradeability(
            analysis_vehicle,
            scenario=None,
            verbose=False,
            ess_init_soc=insoc,
            set_weight_to_max_kg=False,
        )

        soc_used.append((g6sd.soc[0], g6sd.soc[-1]))

        print(
            "init soc: ",
            round(insoc, 3),
            r"max speed at 6% grade achvd",
            round(g6mphach, 3),
        )

        g6mphachs.append(g6mphach)
# %%
