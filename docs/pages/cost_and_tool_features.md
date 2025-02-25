# T3CO Cost and Tool Features

## Cost Features

### Capital Cost Components

- *MSRP Breakdown:* Glider, Fuel Converter, Fuel Storage, Battery, Motor Controller and Power Electronics, Plugin
- *Purchase or Sales Tax*
- *Purchasing Downpayment:* For loan or lease purchasing method
- *Residual Cost:* Salvage value at end of life of vehicle

### Operating Cost Components

- *Fuel Expense*: Total cost of fuel or energy consumed
- *Maintenance Cost*
- *Purchasing Cost:* Recurring payments for loan or lease purchasing method
- *Insurance Cost*
- *Fueling Dwell Labor cost*
- All operating costs are discounted year over year to account for time value of money

### Opportunity Cost Components

- *Lost Payload Capacity Cost*: Cost of fractionally additional advanced powertrain vehicles needed to carry the same payload as a conventional one (only for Class 8)
- *Fueling/Charging Dwell Time Opportunity Cost*: Cost of unproductive dwell time while charging or fueling a vehicle
- *Maintenance & Repair Downtime Opportunity Cost*: Cost of planned and unplanned vehicle downtime due to M&R
- All opportunity costs are discounted year over year to account for time value of money

### Total Cost of Ownership

- *Two methods of estimating discounted TCO:* 'DIRECT' and 'EFFICIENCY'
- *Annualized total costs:* And 
- *Total cost per mile and levelized cost per mile*

## Tool Features

- Ability to generate individual Ledger and TCO Per Year reports exported as CSV or JSON files
- Ability to run multiple Vehicle-Scenario-Energy selections from input files and export results to CSV
- Option to run FASTSim simulations for energy calculations
- Option to provide exogenous MPGGE and vehicle range inputs instead of running a powertrain simulation
- BatchMode to run a folder of drivecycles through FASTSim and generate multiple scenarios per selection
- Multiprocessing/Parallelization to reduce runtime for large selections. Can be clubbed with BatchMode to run 1000s of drivecycles on a local machine
- Dynamic Wireless Power Transfer - Analyze on-road charging technologies and its impact on cost

## Features Roadmap

- Charts Module to visualize Ledgers and large sets of T3CO results
- Optimization Toolbox to size the future or advanced vehicle parameters for minimizing TCO and other objectives
- Labor Cost as an operating cost component
- Grants incentives, registration, title, and recurring fees added as Capital and Operating Cost components
- Battery replacement and battery degradation accounted for in Operating Costs and Energy calculations
- Regionalized fuel, registration, and labor cost inputs
- Option to run RouteE for Energy calculations
