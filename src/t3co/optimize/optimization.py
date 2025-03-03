import numpy as np
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.core.problem import ElementwiseProblem
from pymoo.optimize import minimize

from t3co.energy_models.energy import Energy, RunFastsim
from t3co.input_data.config import Config
from t3co.input_data.scenario import Scenario
from t3co.input_data.vehicle import Vehicle
import t3co.constants.Global as gl

# Import Ledger from ledger.py.
from t3co.tco.ledger import Ledger


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
        n_var=4,
        xl=None,
        xu=None,
    ):
        # Set lower and upper bounds for each design variable.
        self.vehicle = vehicle
        self.scenario = scenario
        self.config = config
        if self.vehicle.veh_pt_type == gl.CONV:
            n_var = 1
            xl = np.array([scenario.knob_min_fc_kw])
            xu = np.array([scenario.knob_max_fc_kw])
        elif self.vehicle.veh_pt_type == gl.BEV:
            n_var = 2
            xl = np.array([scenario.knob_min_ess_kwh, scenario.knob_min_motor_kw])
            xu = np.array([scenario.knob_max_ess_kwh, scenario.knob_max_motor_kw])
        elif self.vehicle.veh_pt_type == gl.HEV:
            n_var = 4
            xl = np.array(
                [
                    scenario.knob_min_ess_kwh,
                    scenario.knob_min_fc_kw,
                    scenario.knob_min_fs_kwh,
                    scenario.knob_min_motor_kw,
                ]
            )
            xu = np.array(
                [
                    scenario.knob_max_ess_kwh,
                    scenario.knob_max_fc_kw,
                    scenario.knob_max_fs_kwh,
                    scenario.knob_max_motor_kw,
                ]
            )
        else:
            raise ValueError(f"Unknown vehicle type: {vehicle.veh_pt_type}")

        super().__init__(n_var=n_var, n_obj=1, xl=xl, xu=xu)

    def _evaluate(self, x, out, *args, **kwargs):
        # Run fastsim simulation to obtain energy performance metrics.
        # Create default instances for the simulation.
        if self.vehicle.veh_pt_type == gl.CONV:
            self.vehicle.fc_max_kw = x[0]

        elif self.vehicle.veh_pt_type == gl.BEV:
            self.vehicle.ess_max_kwh = x[0]
            self.vehicle.mc_max_kw = x[1]

        elif self.vehicle.veh_pt_type == gl.HEV:
            self.vehicle.ess_max_kwh = x[0]
            self.vehicle.fc_max_kw = x[1]
            self.vehicle.fs_kwh = x[2]
            self.vehicle.mc_max_kw = x[3]

        # self.vehicle.ess_max_kwh = x[0]
        # self.vehicle.fc_max_kw = x[1]
        # self.vehicle.fs_kwh = x[2]
        # self.vehicle.mc_max_kw = x[3]

        self.energy = Energy()

        self.energy.run_fastsim_model(
            veh_no=self.vehicle.selection,
            scenario=self.scenario,
            vehicle_df=self.config.vehicle_df,
            t3co_vehicle=self.vehicle,
        )

        # Additional vehicle design updates could be made here if needed.
        # For instance, one might update vehicle attributes based on design variables.

        # Instantiate Ledger, which will calculate the operating costs using Energy.
        ledger = Ledger(self.vehicle, self.scenario, self.energy, self.config)

        # Objective: minimize the discounted total cost of ownership.
        out["F"] = [ledger.discounted_tco_dol]


def main(parallel=True, n_processes=4):
    problem = VehicleDesignOpt()
    algorithm = GA(pop_size=100)

    res = minimize(
        problem,
        algorithm,
        termination=("n_gen", 200),
        seed=1,
        verbose=True,
        n_processes=n_processes if parallel else None,
    )

    print("Best solution:")
    print("  Battery Size (kWh):          {:.2f}".format(res.X[0]))
    print("  Fuel Converter Peak Power (kW): {:.2f}".format(res.X[1]))
    print("  Fuel Storage Energy (kWh eq.):  {:.2f}".format(res.X[2]))
    print("  Motor Peak Power (kW):          {:.2f}".format(res.X[3]))
    print("Minimum Discounted TCO:           ${:.2f}".format(res.F[0][0]))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Optimize vehicle design parameters for minimum discounted TCO using Ledger and fastsim."
    )
    parser.add_argument(
        "--no-parallel", action="store_true", help="Disable parallel evaluation."
    )
    parser.add_argument(
        "--n-processes", type=int, default=4, help="Number of processes."
    )
    args = parser.parse_args()

    main(parallel=not args.no_parallel, n_processes=args.n_processes)
