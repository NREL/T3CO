from t3co.cost_models.capital_costs import CapitalCosts
from t3co.cost_models.operating_costs import OperatingCosts
from t3co.cost_models.opportunity_costs import OpportunityCosts
from t3co.energy_models.energy import Energy
from t3co.input_data.config import Config
from t3co.input_data.scenario import Scenario
from t3co.input_data.vehicle import Vehicle
from t3co.utils.print_class_objects import obj_to_string

class TCOCalc():
    year_index: int = None
    total_cost_dol_per_yr: float = None
    disc_total_cost_dol_per_yr: float = None
    cap_costs_dol: CapitalCosts = None
    oper_costs_dol: OperatingCosts = None
    oppy_costs_dol: OpportunityCosts = None

    def __init__(self, year_index: int, vehicle:Vehicle, scenario: Scenario, energy: Energy, cap_costs: CapitalCosts = None):
        if year_index==0:
            self.calculate_capital_costs(vehicle=vehicle, scenario=scenario)
        
        if cap_costs:
            self.cap_costs_dol = cap_costs
        else:
            self.calculate_capital_costs(vehicle=vehicle, scenario=scenario)
        self.calculate_opportunity_costs(year_number=year_index, vehicle=vehicle, scenario=scenario, energy=energy)
        self.calculate_operating_costs(year_number=year_index, vehicle=vehicle, scenario=scenario,energy=energy)
    
    
    def calculate_capital_costs(self, vehicle: Vehicle, scenario: Scenario):
        self.cap_costs_dol = CapitalCosts(vehicle=vehicle, scenario=scenario)

    def calculate_opportunity_costs(self, year_number:int , vehicle: Vehicle, scenario: Scenario, energy: Energy):
        self.oppy_costs_dol =  OpportunityCosts(year_number=year_number, vehicle=vehicle, scenario=scenario, energy=energy)

    def calculate_operating_costs(self, year_number, vehicle: Vehicle, scenario: Scenario, energy: Energy):
        self.oper_costs_dol =  OperatingCosts(year_number=year_number, cap_costs=self.cap_costs_dol, vehicle=vehicle, scenario=scenario, energy=energy, oppy_costs=self.oppy_costs_dol)
    
    def set_total_cost(self, year_number: int, scenario: Scenario):
        self.total_cost_dol_per_yr = (
            (self.cap_costs_dol.net_capital_cost_dol if year_number==0 else 0) 
            + self.oper_costs_dol.net_oper_cost_dol_per_yr
            + self.oppy_costs_dol
            + (self.cap_costs_dol.residual_cost_dol if year_number==scenario.vehicle_life_yr-1 else 0)
        )
    
    
        
    def __str__(self):
        return obj_to_string(self)
