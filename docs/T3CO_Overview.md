
- [T3CO Introduction ](#t3co-introduction)
- [Code Flow ](#code-flow)
    - [Generating TCO and performance](#generating-tco-and-performance)
- [T3CO Input Files ](#t3co-input-files)
- [Optimization Flow ](#optimization-flow)
- [Performance Constraints ](#performance-constraints)


## <a name="t3co-introduction"></a> T3CO Introduction 

[NREL's Transportation Technology Total Cost of Ownership](https://www.nrel.gov/transportation/t3co.html) (T3CO) tool enables levelized assessments of the full life cycle costs of advanced technology commercial vehicles. 

## Code Flow <a name="code-flow"></a>

Generally speaking, T3CO can be used in two ways. The first way is generating total cost of ownership (TCO) metrics and performance metrics for a vehicle. The second way is optimizing a vehicle's specifications to achieve the lowest total cost of ownership possible. Since optimization requires gathering TCO and performance metrics during each step of optimization, it essentially is an expanded version of the first way of using T3CO. So we'll look at the first way first.

### **Generating TCO and performance** <a name="generating-tco-and-performance"></a>

When generating [TCO](./models/TCO_calculations.md), there are a few main components of a vehicle's total cost of ownership:
- MSRP, the cost of the vehicle at time of purchase
- Fuel costs (based on $ per gallon of gasoline equivalent for every operational year's fuel used)
- operating costs (maintenance `[$/mile]`, opportunity cost `[\$/mile]`, etc.)
- [payload opportunity cost](./models/TCO_calculations.md#payload-opportunity-costs-)

The fuel costs are computed after determining the mile per gallone of gasoline equivalent (MPGGE) fuel efficiency of the vehicle and factoring that in with the miles driven and the cost per gallon of gasoline equivalent (GGE) for each year and region that the vehicle operates in.

The [Performance Constraints](#performance-constraints) determined for the vehicle are:
- miles of range
- acceleration, vehicle at GVWR + Weight Credits,  seconds from zero to sixty MPH and seconds from zero to thirty MPH
- gradability, vehicle at GVWR + Weight Credits, the max speed achieved at 1.5% grade and 6% grade

More on that below.

## T3CO Input Files <a name="t3co-input-files)"></a>

There are three main files that form the basis of T3CO TCO calculations and T3CO optimizations. The first is the vehicle file, which is a [Vehicle File](./vehicle_inputs_descriptions.md). The second type of file is the T3CO file, or [Scenario File](./scenario_inputs_descriptions.md), which specifies the operating conditions that make up the TCO calculation for the vehicle. These are conditions such as $ per kilowatt for engine or motor size, operating years, operating regions, whether to optimize the vehicle or not, range, grade and acceleration performance targets, etc. The third file is the [Config File](./config_inputs_descriptions.md), which provides an easier way to manage analyses with minimal command line inputs, containing overrides for major scenario input parameters.

T3CO provides some readily available Vehicle and Scenario models to run. There are demo versions of the [Vehicle file](https://github.com/NREL/T3CO/blob/264a730de942671eb2345a5afca7e1afd6d67666/t3co/resources/inputs/demo/Demo_FY22_vehicle_model_assumptions.csv) and[Scenario file](https://github.com/NREL/T3CO/blob/264a730de942671eb2345a5afca7e1afd6d67666/t3co/resources/inputs/demo/Demo_FY22_scenario_assumptions.csv) available in the  [`/t3co/resources/inputs/demo`](https://github.com/NREL/T3CO/tree/264a730de942671eb2345a5afca7e1afd6d67666/t3co/resources/inputs/demo) folder. The [Config file](https://github.com/NREL/T3CO/blob/264a730de942671eb2345a5afca7e1afd6d67666/t3co/resources/T3COConfig.csv) is available in the [`/t3co/resources/`](https://github.com/NREL/T3CO/tree/264a730de942671eb2345a5afca7e1afd6d67666/t3co/resources)

## Optimization Flow <a name="optimization-flow"></a>

The **TCO & Performance** metrics described above are the core of the [optimization loop](./models/optimization.md). T3CO has the capability to take vehicle specifications, such as engine size, motor size, battery size, area of drag, vehicle weight, etc. and modify them in order to find the set of specifications that yields the lowest TCO while still meeting minimum performance requirements in acceleration, grade and range.

Optimization is handled in the [optimization module](https://github.com/NREL/T3CO/blob/74a494bc783c1d0d5794d605584e9843b3a4cb2d/t3co/moopack/moo.py#L80), inheriting from the PyMoo module.

## Performance Constraints <a name="performance-constraints"></a>

- [Gradability](./models/acceleration_and_grade_tests.md) is the measure of the vehicle's max speed achieved at 1.25 and 6 percent grades, while the vehicle is operating at max allowable weight (including EV weight credit kilograms)
- [Acceleration](./models/acceleration_and_grade_tests.md) is the measure of the seconds the vehicle takes to reach 30 miles per hour and 60 miles per hour, which can be at max allowable weight or just current vehicle weight.
- [Range](./models/fuel_efficiency_and_range.md) is the computation of the vehicle's range in miles based on the computed fuel efficiency (mpgge) and vehicle fuel stores; mpgge is attained using a *design cycle* (cycle or cycles determined to be representative of vehicle operation). The design cycle can be a single drive cycle or a composition of weight drive cycles.

