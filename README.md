# MCET-Chile-Open-Model-for-2050# MCET Chile - Switch Open Model for 2050

This repository has the modules and inputs used by the Chilean Team for the MCET Project scenarios simulation.

## Overview

As a continuation of the work performed in the Open Decarbonization Planning Project (ODPP), the MCET Project consisted of continuing the different scenarios modeling exercise. The objective was to model the operation of the electric system when almost all generation is provided by renewable energy resources and no high carbon intensive fuels generation. For both ODPP and MCET the Chilean team decided to work with Switch, particularly on its version 2.0.6, using mainly the core modules defined in the platform and some extra and adapted modules.

All the defined scenarios in this study consists of one year of operation, specifically 2050, with hourly resolution (the entire 8760 hours of the year), to represent the operation of the system. Among the main assumptions considered to define the scenarios inputs are the following:

- Power system structure: For the topology of the electrical network, 26 electrical nodes and 28 transmission lines are considered. These are the ones defined in the LTEP database, also integrating the candidate nodes defined therein.

- For the initial generation capacity, we used information of identified existing generators, regarding operational parameters, installed capacity, location and connection date.

- Load profile: The 2022 demand profile used by the Chilean ISO is considered, and was projected to 2050 using the Long-Term Energy Planning ([LTEP](https://energia.gob.cl/pelp/repositorio)) database.

- For the Hydro System an approximated model of the Chilean water network is used to describe the availability and energy generation.

- For the Carbon tax a 35 $USD/tCO2 was used, associated with the Carbon neutrality on 2050 LTEP scenario carbon price.

- For the candidate projects, the parameters were built based on LTEP information, on NREL Annual Technology Baseline 2023 and other technical references. This includes the overnight, fixed O&M costs and variable costs.

- The predetermined generating park is mainly composed of non-conventional renewable generation, with Biogas, Biomass, CAES, CSP-TES, Gas CCS, Geothermal, Reservoir and run-of-river Hydro, Hydrogen Storage PEM, PHS, Solar, Storage and Wind technologies.

The available scenarios were defined  in order to represent different possible contexts of the power system in 2050. In particular, eleven scenarios were developed within a system with practically no emissions in 2050 to allow a prescriptive analysis to be carried out considering these different technological developments. The modeled scenarios are listed below:

- Reference: considers candidate generation projects of Solar, Wind, Gas with CCS, Geothermal, Biomass, BESS, CSP-TES, PHS, CAES, Hydrogen Storage technologies.

- Only Renewables with Storage (Renewable Only): The same existing and candidate plants are considered as in the previous case, with the exception of Gas with CCS and Hydrogen.

- Only renewable with storage and hydrogen (Renewable Only + H2): Same as the previous scenario, but with Hydrogen-based storage.

- Restricted transmission expansion (X% Transmission): Four scenarios in which the Tx expansion is restricted to 75, 50, 25 and 0% of the resulting expanded capacity from the Reference scenario.

- Reference with zonal flexible loads: This scenario considers the same inputs as the Reference scenario, but particularly considering that loads can be shifted optimally between all nodes. 

- Reference with non-zonal flexible loads: This scenario is also based on the Reference scenario, but the flexible loads cannot be shifted between nodes, so daily, annual and baseload DSF are shifted in each node separately.

- Renewables with zonal flexible loads: Considers the same inputs as the Renewables only scenario, that all nodes are grouped in one zone, so loads can be shifted optimally between all nodes.

- Renewables with non-zonal flexible loads: Considers the same inputs as the Renewables only scenario, considering that the flexible loads cannot be shifted between nodes.

## Usage

On the ```inputs``` folder, we have uploaded the folder associated to each of the scenarios medeled on the MCET project. To run each of them, you can either use ```switch solve-scenarios``` (to solve all the scenarios defined inside the ```inputs``` folder) or ```switch solve``` to solve one of the particular scenarios as a single simulation.

We have included a the ```switch_model``` folder containing the scripts used for the simulations.

## Acknowledgements

We would like to express our gratitude to everyone who contributed to the development of this project. This includes developers, researchers, testers, and collaborators who generously shared their time, expertise, and insights. In particular we want to thank Lucas Maulen, Matías Aguad, Patricio Castillo, Manuel Portilla and Nicolás Lobos, whom perfermed the elaboration of the inputs and the simulation of the different scenarios.
