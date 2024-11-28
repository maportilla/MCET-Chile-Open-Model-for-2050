# MCET-Chile-Open-Model-for-2050# MCET Chile - Switch Open Model for 2050

This repository contains the modules and inputs used by the Chilean Team for the MCET Project scenario simulations.

## Overview

As a continuation of the work performed in the Open Decarbonization Planning Project (ODPP), the MCET Project extended the modeling of various scenarios. The objective was to simulate the operation of the electric system under conditions where nearly all generation comes from renewable energy resources, with no generation from high carbon-intensive fuels. For both ODPP and MCET, the Chilean team decided to work with Switch, particularly version 2.0.6, using mainly the core modules defined in the platform along with some additional and adapted modules.

All the defined scenarios in this study consists of one year of operation, specifically 2050, with hourly resolution (the entire 8760 hours of the year), to represent the operation of the system. Among the main assumptions considered to define the scenarios inputs are the following:

- Power system structure: For the topology of the electrical network, 26 electrical nodes and 28 transmission lines were considered. These were defined in the LTEP database, integrating the candidate nodes outlined therein.

- Initial generation capacity: Information on identified existing generators was used, including operational parameters, installed capacity, location, and connection dates.

- Load profile: The 2022 demand profile used by the Chilean ISO was projected to 2050 using data from the Long-Term Energy Planning (LTEP) database.

- Hydro system: An approximate model of Chile’s water network was used to describe water availability and energy generation.

- Carbon tax: A carbon price of $35 USD/tCO₂ was used, aligned with the Carbon Neutrality 2050 LTEP scenario.

- Candidate projects: Parameters were based on LTEP data, the NREL Annual Technology Baseline 2023, and other technical references. This includes overnight costs, fixed O&M costs, and variable costs.

- Predetermined generating park: This primarily consists of non-conventional renewable generation, including technologies such as Biogas, Biomass, CAES, CSP-TES, Gas CCS, Geothermal, Reservoir and run-of-river Hydro, Hydrogen Storage PEM, PHS, Solar, Storage, and Wind.

The available scenarios were defined to represent various potential contexts of the power system in 2050. Eleven scenarios were developed, all assuming a system with minimal emissions, enabling prescriptive analyses across different technological developments. The modeled scenarios are:

- Reference: Includes candidate generation projects for Solar, Wind, Gas with CCS, Geothermal, Biomass, BESS, CSP-TES, PHS, CAES, and Hydrogen Storage technologies.

- Only Renewables with Storage (Renewables Only): The same existing and candidate plants are considered as in the Reference scenario, except for Gas with CCS and Hydrogen.

- Only Renewables with Storage and Hydrogen (Renewables Only + H₂): Same as the previous scenario, but with Hydrogen-based storage.

- Restricted Transmission Expansion (X% Transmission): Four scenarios where the transmission expansion is restricted to 75%, 50%, 25%, and 0% of the expanded capacity in the Reference scenario.

- Reference with Zonal Flexible Loads: The same inputs as the Reference scenario, but loads can be optimally shifted between all nodes.

- Reference with Non-Zonal Flexible Loads: Based on the Reference scenario, but flexible loads cannot shift between nodes, and daily, annual, and baseload DSF are shifted within each node separately.

- Renewables with Zonal Flexible Loads: Uses the same inputs as the Renewables Only scenario, allowing all nodes to be grouped into one zone where loads can be optimally shifted between nodes.

- Renewables with Non-Zonal Flexible Loads: Uses the same inputs as the Renewables Only scenario but ensures flexible loads cannot shift between nodes.

## Usage

On the ```inputs``` folder, we have uploaded the folder associated to each of the scenarios medeled on the MCET project. To run each of them, you can either use ```switch solve-scenarios``` (to solve all the scenarios defined inside the ```inputs``` folder) or ```switch solve``` to solve one of the particular scenarios as a single simulation.

We have included a the ```switch_model``` folder containing the scripts used for the simulations.

## Acknowledgements

We would like to express our gratitude to everyone who contributed to the development of this project. This includes developers, researchers, testers, and collaborators who generously shared their time, expertise, and insights. In particular, we want to thank Lucas Maulén, Matías Aguad, Patricio Castillo, Manuel Portilla, and Nicolás Lobos, who worked on the preparation of inputs and simulation of the different scenarios.
