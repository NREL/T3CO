import numpy as np
from multiprocessing import Pool
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import ElementwiseProblem, StarmapParallelization
from pymoo.optimize import minimize
from pymoo.termination.default import DefaultSingleObjectiveTermination

from t3co.energy_models.energy import Energy
from t3co.input_data.config import Config
from t3co.input_data.scenario import Scenario
from t3co.input_data.vehicle import Vehicle
import t3co.constants.Global as gl

# Import Ledger from ledger.py.
from t3co.tco.ledger import Ledger
import argparse


class VehicleDesignOpt(ElementwiseProblem):
    """
    Decision variables:
      x[0]: Battery size (kWh)
      x[1]: Fuel converter peak power (kW)
      x[2]: Fuel storage energy (kWh equivalent)
      x[3]: Motor peak power (kW)

    Objective:
      Minimize Ledger.discounted_tco_dol.
    """

    def __init__(
        self,
        vehicle: Vehicle,
        scenario: Scenario,
        config: Config,
        runner=None,
    ):
        self.vehicle = vehicle
        self.scenario = scenario
        self.config = config

        xl = []
        xu = []
        x = {}
        # Define decision variables based on powertrain type
        if vehicle.veh_pt_type == gl.CONV:
            # x[0]: Fuel converter peak power (kW)
            xl.append(scenario.knob_min_fc_kw)
            xu.append(scenario.knob_max_fc_kw)
            x["knob_min_fc_kw"] = scenario.knob_min_fc_kw
            x["knob_max_fc_kw"] = scenario.knob_max_fc_kw

            # x[1]: Fuel storage energy (kWh equivalent)
            if (
                scenario.knob_min_fs_kwh is not None
                and scenario.knob_max_fs_kwh is not None
            ):
                xl.append(scenario.knob_min_fs_kwh)
                xu.append(scenario.knob_max_fs_kwh)
                x["knob_min_fs_kwh"] = scenario.knob_min_fs_kwh
                x["knob_max_fs_kwh"] = scenario.knob_max_fs_kwh

        elif vehicle.veh_pt_type == gl.BEV:
            # x[0]: Battery size (kWh)
            xl.append(scenario.knob_min_ess_kwh)
            xu.append(scenario.knob_max_ess_kwh)
            x["knob_min_ess_kwh"] = scenario.knob_min_ess_kwh
            x["knob_max_ess_kwh"] = scenario.knob_max_ess_kwh

            # x[1]: Motor peak power (kW)
            xl.append(scenario.knob_min_motor_kw)
            xu.append(scenario.knob_max_motor_kw)
            x["knob_min_motor_kw"] = scenario.knob_min_motor_kw
            x["knob_max_motor_kw"] = scenario.knob_max_motor_kw

        elif vehicle.veh_pt_type == gl.HEV:
            # x[0]: Battery size (kWh)
            xl.append(scenario.knob_min_ess_kwh)
            xu.append(scenario.knob_max_ess_kwh)
            # x[1]: Fuel converter peak power (kW)
            xl.append(scenario.knob_min_fc_kw)
            xu.append(scenario.knob_max_fc_kw)
            # x[2]: Fuel storage energy (kWh equivalent)
            xl.append(scenario.knob_min_fs_kwh)
            xu.append(scenario.knob_max_fs_kwh)
            # x[3]: Motor peak power (kW)
            xl.append(scenario.knob_min_motor_kw)
            xu.append(scenario.knob_max_motor_kw)

            x["knob_min_ess_kwh"] = scenario.knob_min_ess_kwh
            x["knob_max_ess_kwh"] = scenario.knob_max_ess_kwh
            x["knob_min_fc_kw"] = scenario.knob_min_fc_kw
            x["knob_max_fc_kw"] = scenario.knob_max_fc_kw
            x["knob_min_fs_kwh"] = scenario.knob_min_fs_kwh
            x["knob_max_fs_kwh"] = scenario.knob_max_fs_kwh
            x["knob_min_motor_kw"] = scenario.knob_min_motor_kw
            x["knob_max_motor_kw"] = scenario.knob_max_motor_kw
        else:
            raise ValueError(f"Unknown vehicle type: {vehicle.veh_pt_type}")

        xl = np.array(xl)
        xu = np.array(xu)
        n_var = len(xl)
        print("Knobs:")
        for key, value in x.items():
            print(f" {key}: {value}")

        # Determine number of inequality constraints
        n_ieq_constr = 0
        if scenario.constraint_accel:
            # 0-60 mph and 0-30 mph
            if scenario.max_time_0_to_60mph_at_gvwr_s > 0:
                n_ieq_constr += 1
            if scenario.max_time_0_to_30mph_at_gvwr_s > 0:
                n_ieq_constr += 1

        if scenario.constraint_grade:
            # 6% and 1.25% grade
            if scenario.min_speed_at_6pct_grade_in_5min_mph > 0:
                n_ieq_constr += 1
            if scenario.min_speed_at_1p25pct_grade_in_5min_mph > 0:
                n_ieq_constr += 1

        super().__init__(
            n_var=n_var,
            n_obj=1,
            n_ieq_constr=n_ieq_constr,
            xl=xl,
            xu=xu,
            elementwise_runner=runner,
        )

    def apply_design_variables(self, x, vehicle=None):
        target_vehicle = self.vehicle if vehicle is None else vehicle

        if target_vehicle.veh_pt_type == gl.CONV:
            target_vehicle.fc_max_kw = x[0]
            if len(x) > 1:
                target_vehicle.fs_kwh = x[1]
        elif target_vehicle.veh_pt_type == gl.BEV:
            target_vehicle.ess_max_kwh = x[0]
            target_vehicle.mc_max_kw = x[1]
        elif target_vehicle.veh_pt_type == gl.HEV:
            target_vehicle.ess_max_kwh = x[0]
            target_vehicle.fc_max_kw = x[1]
            target_vehicle.fs_kwh = x[2]
            target_vehicle.mc_max_kw = x[3]
        else:
            raise ValueError(f"Unknown vehicle type: {target_vehicle.veh_pt_type}")

        return target_vehicle

    def evaluate_solution(self, x):
        vehicle = self.apply_design_variables(x)

        energy = Energy()
        energy.run_fastsim_model(
            veh_no=vehicle.selection,
            scenario=self.scenario,
            vehicle_df=self.config.vehicle_df,
            t3co_vehicle=vehicle,
        )

        if self.scenario.constraint_accel:
            energy.run_acceleration_test(vehicle, self.scenario)
        if self.scenario.constraint_grade:
            energy.run_gradeability_test(vehicle, self.scenario)
        if self.scenario.constraint_range:
            energy.run_range_test(vehicle, self.scenario)

        ledger = Ledger(vehicle, self.scenario, energy, self.config)
        return vehicle, energy, ledger

    def _evaluate(self, x, out, *args, **kwargs):
        vehicle, energy, ledger = self.evaluate_solution(x)

        # Objective: minimize the discounted total cost of ownership
        out["F"] = [ledger.discounted_tco_dol]

        # Constraints
        # G <= 0
        g = []

        if self.scenario.constraint_accel:
            # 0-60 mph time constraint
            if self.scenario.max_time_0_to_60mph_at_gvwr_s > 0:
                g.append(
                    energy.zero_to_sixty_loaded
                    - self.scenario.max_time_0_to_60mph_at_gvwr_s
                )

            # 0-30 mph time constraint
            if self.scenario.max_time_0_to_30mph_at_gvwr_s > 0:
                g.append(
                    energy.zero_to_thirty_loaded
                    - self.scenario.max_time_0_to_30mph_at_gvwr_s
                )

        if self.scenario.constraint_grade:
            # Gradeability 6% constraint (min speed)
            if self.scenario.min_speed_at_6pct_grade_in_5min_mph > 0:
                # We want achieved speed >= target speed => target - achieved <= 0
                g.append(
                    self.scenario.min_speed_at_6pct_grade_in_5min_mph
                    - energy.grade_6_mph_ach
                )

            # Gradeability 1.25% constraint (min speed)
            if self.scenario.min_speed_at_1p25pct_grade_in_5min_mph > 0:
                g.append(
                    self.scenario.min_speed_at_1p25pct_grade_in_5min_mph
                    - energy.grade_1_25_mph_ach
                )

        if self.scenario.constraint_range:
            if self.scenario.target_range_mi > 0:
                g.append(self.scenario.target_range_mi - energy.primary_fuel_range_mi)

        if g:
            out["G"] = g


def run_optimization(selection, parallel=True, n_processes=4):
    # Create default instances for vehicle, scenario, and config
    config = Config()
    config.skip_all_opt = False
    config.selections = [selection]
    # print(f"config year: {config.vehicle_life_yr}")
    vehicle = Vehicle().from_config(selection=selection, config=config)
    vehicle.set_veh_kg()
    scenario = Scenario().from_csv(
        selection=selection, scenario_file=config.scenario_file
    )
    config.vehicle_life_yr = scenario.vehicle_life_yr

    # scenario.override_from_config(config=config)

    # print(f"vehicle: {vehicle}")
    # print(f"scenario: {scenario}")

    pool = None
    runner = None
    if parallel:
        pool = Pool(n_processes)
        runner = StarmapParallelization(pool.starmap)

    try:
        problem = VehicleDesignOpt(vehicle, scenario, config, runner=runner)
        algorithm = NSGA2(pop_size=config.pop_size, eliminate_duplicates=True)

        res = minimize(
            problem,
            algorithm,
            termination=DefaultSingleObjectiveTermination(
                xtol=config.x_tol,
                ftol=config.f_tol,
                period=max(config.nth_gen, config.n_last),
                n_max_gen=config.n_max_gen,
            ),
            seed=1,
            verbose=True,
        )
    finally:
        if pool:
            pool.close()
            pool.join()

    vehicle, energy, ledger = problem.evaluate_solution(res.X)

    print("Best solution:")
    if vehicle.veh_pt_type == gl.CONV:
        print("  Fuel Converter Peak Power (kW): {:.2f}".format(res.X[0]))
        if len(res.X) > 1:
            print("  Fuel Storage Energy (kWh eq.):  {:.2f}".format(res.X[1]))

    elif vehicle.veh_pt_type == gl.BEV:
        print("  Battery Size (kWh):          {:.2f}".format(res.X[0]))
        print("  Motor Peak Power (kW):          {:.2f}".format(res.X[1]))
    elif vehicle.veh_pt_type == gl.HEV:
        print("  Battery Size (kWh):          {:.2f}".format(res.X[0]))
        print("  Fuel Converter Peak Power (kW): {:.2f}".format(res.X[1]))
        print("  Fuel Storage Energy (kWh eq.):  {:.2f}".format(res.X[2]))
        print("  Motor Peak Power (kW):          {:.2f}".format(res.X[3]))
    print("Minimum Discounted TCO:           ${:.2f}".format(ledger.discounted_tco_dol))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Optimize vehicle design parameters for minimum discounted TCO using Ledger and fastsim."
    )
    parser.add_argument(
        "--selection", type=int, default=1, help="Vehicle and Scenario selection number"
    )
    parser.add_argument(
        "--no-parallel", action="store_true", help="Disable parallel evaluation."
    )
    parser.add_argument(
        "--n-processes", type=int, default=9, help="Number of processes."
    )
    args = parser.parse_args()

    run_optimization(
        selection=args.selection,
        parallel=not args.no_parallel,
        n_processes=args.n_processes,
    )
