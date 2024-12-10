# Copyright (c) 2016-2017 The Switch Authors. All rights reserved.
# Licensed under the Apache License, Version 2.0, which is in the LICENSE file.

"""
This module defines CSP+TES technologies. It builds on top of generic
generators, adding components for deciding how much to build, when to 
charge and discharge, energy accounting, etc.
"""

from pyomo.environ import *
import os, collections
from switch_model.financials import capital_recovery_factor as crf

dependencies = 'switch_model.timescales', 'switch_model.balancing.load_zones',\
    'switch_model.financials', 'switch_model.energy_sources.properties', \
    'switch_model.generators.core.build', 'switch_model.generators.core.dispatch'

def define_components(mod):
    """

    CSP_GENS is the subset of CSP+TES projects that can provide power and
    storage thermal energy.

    csp_sf_tes_efficiency[CSP_GENS] describes the efficiency of the heat exchager 
    between the solar field (SF) and the thermal energy storage (TES) for 
    parabolic trough CSP technology. In the case of central tower CSP technology,
    this efficiency is equivalent to 1 (dafault value).

    csp_tes_efficiency[CSP_GENS] efficiency of the TES associated to heat losses.

    csp_tes_pb_efficiency[CSP_GENS] efficiency of the heat exchager between the TES
    and the oil circuit before the power block (PB) for parabolic trough CSP technology.
    In the case of central tower CSP technology, this efficiency is equivalent to 1 
    (dafault value).

    csp_sf_tes_pb_efficiency[CSP_GENS] efficiency of the heat exchager between the 
    molten salts/oil circuit and the PB.

    csp_pb_efficiency[CSP_GENS] efficiency of the PB.

    csp_tes_capacity_h[CSP_GENS] TES energy storage capacity (in hours).
    
    CSP_GEN_TPS is the subset of GEN_TPS, restricted to CSP projects.

    csp_sf_power_output_mwt[CSP_GEN_TPS] thermal power delivered by the solar field 
    (in thermal mw).

    ChargeTES[(g, t) in CSP_GEN_TPS] is a dispatch decision of how much to charge 
    the TES in each timepoint.

    DischargeTES[(g, t) in CSP_GEN_TPS] is a dispatch decision of how much to discharge 
    the TES in each timepoint.

    ExcessPower[(g, t) in CSP_GEN_TPS] is a dispatch decision of how much to defocuse
    the mirrors of the solar field. If solar radiation is high, the TES is fully charged
    and the PB is generating at maximum capacity, then, some mirrors are needed to be
    defocused to maintain the thermal power balance. This defocusing is described as
    an excess of thermal power, neither used nor stored and, therefore, lost.
    
    TES_StateOfCharge[(g, t) in CSP_GEN_TPS] is a variable for tracking state of charge.
    This value stores the TES state of charge at the end of each timepoint.

    Charge_TES_Upper_Limit[(g, t) in CSP_GEN_TPS] constrains ChargeTES to the available 
    thermal power delivered by the solar field, csp_sf_power_output_mwt[CSP_GEN_TPS].
    
    Discharge_TES_Upper_Limit[(g, t) in CSP_GEN_TPS] constrains DischargeTES to be, at
    most. the dispatch requirements.

    Thermal_Power_Balance[(g, t) in CSP_GEN_TPS] constrains the inner thermal power 
    balance of the CSP project.

    Track_TES_State_Of_Charge[(g, t) in CSP_GEN_TPS] constrains TES_StateOfCharge based 
    on the TES_StateOfCharge in the previous timepoint, ChargeTES and DischargeTES.
    
    TES_State_Of_Charge_Upper_Limit[(g, t) in CESP_GEN_TPS] constrains TES_StateOfCharge 
    based on TES capacity of the CSP project.

    """
    mod.CSP_GENS = Set(within=mod.GENERATION_PROJECTS)

#   Parameters
    mod.csp_sf_tes_efficiency = Param(
        mod.CSP_GENS,
        within=PercentFraction,
        default=1.0)

    mod.csp_tes_efficiency = Param(
        mod.CSP_GENS,
        within=PercentFraction)
 
    mod.csp_tes_pb_efficiency = Param(
        mod.CSP_GENS,
        within=PercentFraction,
        default=1.0)    

    mod.csp_sf_tes_pb_efficiency = Param(
        mod.CSP_GENS,
        within=PercentFraction)

    mod.csp_pb_efficiency = Param(
        mod.CSP_GENS,
        within=PercentFraction)

    mod.csp_tes_capacity_h = Param(
        mod.CSP_GENS,
        within=NonNegativeReals)

    mod.CSP_GEN_TPS = Set(
        dimen=2,
        initialize=lambda m: (
            (g, tp) 
                for g in m.CSP_GENS
                    for tp in m.TPS_FOR_GEN[g]))

    mod.csp_sf_power_output_mwt = Param(
        mod.CSP_GEN_TPS,
        within=NonNegativeReals)
    mod.min_data_check('csp_sf_power_output_mwt')

#   Variables
    mod.ChargeTES = Var(
        mod.CSP_GEN_TPS,
        within=NonNegativeReals)

    def Charge_TES_Upper_Limit_rule(m, g, t):
        return m.ChargeTES[g, t] <= \
            m.csp_sf_power_output_mwt[g, t] * (m.GenCapacity[g, m.tp_period[t]])

    mod.Charge_TES_Upper_Limit = Constraint(
        mod.CSP_GEN_TPS,
        rule=Charge_TES_Upper_Limit_rule)

#   Discharge TES
    mod.DischargeTES = Var(
        mod.CSP_GEN_TPS,
        within=NonNegativeReals)

    #   State of charge      
    mod.TES_StateOfCharge = Var(
        mod.CSP_GEN_TPS,
        within=NonNegativeReals)

    def Discharge_TES_Upper_Limit_rule(m, g, t):
        # at the last timepoint, impose DischargeTES <= TES_State_Of_Charge/dt
#        if t == m.TPS_IN_PERIOD[m.PERIODS.last()].last():
#        	return m.DischargeTES[g, t] <= m.TES_StateOfCharge[g, t]/m.tp_duration_hrs[t]
#        else:
       	return m.DischargeTES[g, t] <= \
       		m.DispatchGen[g, t]/(m.csp_pb_efficiency[g]*m.csp_sf_tes_pb_efficiency[g])

    mod.Discharge_TES_Upper_Limit = Constraint(
        mod.CSP_GEN_TPS,
        rule=Discharge_TES_Upper_Limit_rule)
    
#   Thermal power balance equation
    mod.ExcessPower = Var(
        mod.CSP_GEN_TPS,
        within=NonNegativeReals)

    def Thermal_Power_Balance_rule(m, g, t):
        return m.csp_sf_power_output_mwt[g, t] * (m.GenCapacity[g, m.tp_period[t]]) == \
            m.DispatchGen[g, t]/(m.csp_pb_efficiency[g]*m.csp_sf_tes_pb_efficiency[g]) + \
            m.ChargeTES[g, t]/m.csp_sf_tes_efficiency[g] - \
            m.DischargeTES[g, t]*m.csp_tes_pb_efficiency[g] + \
            m.ExcessPower[g, t]

    mod.Thermal_Power_Balance = Constraint(
        mod.CSP_GEN_TPS,
        rule=Thermal_Power_Balance_rule)

##   State of charge      
#    mod.TES_StateOfCharge = Var(
#        mod.CSP_GEN_TPS,
#        within=NonNegativeReals)

    def Track_TES_State_Of_Charge_rule(m, g, t):
        return m.TES_StateOfCharge[g, t] == \
            m.TES_StateOfCharge[g, m.tp_previous[t]]*m.csp_tes_efficiency[g] + \
            (m.ChargeTES[g, t] -
            m.DischargeTES[g, t]) * m.tp_duration_hrs[t]

        # # impose TES_State_Of_Charge at the first timepoint of a period = 
        # # TES_State_Of_Charge at the last timepoint of the the same period
        # if t == m.TPS_IN_PERIOD[m.tp_period[t]].first():
        # 	tp_last = m.TPS_IN_PERIOD[m.tp_period[t]].last()
        # 	return m.TES_StateOfCharge[g, t] == \
        #         m.TES_StateOfCharge[g, tp_last]*m.csp_tes_efficiency[g] + \
        #         (m.ChargeTES[g, tp_last] - m.DischargeTES[g, tp_last]) * \
        #         m.tp_duration_hrs[t]
        # # t is the first timepoint of a timeseries
        # elif (t != m.TPS_IN_PERIOD[m.tp_period[t]].first() and \
        # 	t == m.TPS_IN_TS[m.tp_ts[t]].first()):
        #     # previous timeseries
        #     ts_prev = m.TIMESERIES.prev(m.tp_ts[t])
        #     # last timepoint of the previous timeseries
        #     tp_prev = m.TPS_IN_TS[ts_prev].last()
        #     return m.TES_StateOfCharge[g, t] == \
        #         m.TES_StateOfCharge[g, tp_prev]*m.csp_tes_efficiency[g] + \
        #         (m.ChargeTES[g, tp_prev] - m.DischargeTES[g, tp_prev]) * \
        #         m.tp_duration_hrs[t]
        # else:
        #     return m.TES_StateOfCharge[g, t] == \
        #         m.TES_StateOfCharge[g, m.tp_previous[t]]*m.csp_tes_efficiency[g] + \
        #         (m.ChargeTES[g, m.tp_previous[t]] - m.DischargeTES[g, m.tp_previous[t]]) * \
        #         m.tp_duration_hrs[t]

    mod.Track_TES_State_Of_Charge = Constraint(
        mod.CSP_GEN_TPS,
        rule=Track_TES_State_Of_Charge_rule)

    def TES_State_Of_Charge_Upper_Limit_rule(m, g, t):
        return m.TES_StateOfCharge[g, t] <= \
            (m.GenCapacity[g, m.tp_period[t]])/(m.csp_pb_efficiency[g] * \
            									m.csp_sf_tes_pb_efficiency[g] * \
            									m.csp_tes_pb_efficiency[g]) * \
            (m.csp_tes_capacity_h[g])

    mod.TES_State_Of_Charge_Upper_Limit = Constraint(
        mod.CSP_GEN_TPS,
        rule=TES_State_Of_Charge_Upper_Limit_rule)
        

def load_inputs(mod, switch_data, inputs_dir):
    """

    Import CSP parameters. Optional columns are noted with a *.

    generation_projects_info.tab
        GENERATION_PROJECT, ..., csp_tes_capacity_h

    csp_efficiencies.tab
        GENERATION_PROJECT, csp_sf_tes_efficiency*, csp_tes_efficiency,
                            csp_tes_pb_efficiency*, csp_sf_tes_pb_efficiency,
                            csp_pb_efficiency
    
    csp_sf_power_output.tab
        GENERATION_PROJECT, timepoint, csp_sf_power_output_mwt

    """
 
    switch_data.load_aug(
        filename=os.path.join(inputs_dir, 'generation_projects_info.csv'),
        auto_select=True,
        index=mod.GENERATION_PROJECTS,
        param=(mod.csp_tes_capacity_h))

    # Base the set of CSP projects on the TES capacity being specified.
    switch_data.data()['CSP_GENS'] = {
        None: switch_data.data(name='csp_tes_capacity_h').keys()}

    switch_data.load_aug(
        filename=os.path.join(inputs_dir, 'csp_efficiencies.csv'),
        auto_select=True,
        optional_params=['csp_sf_tes_efficiency', 'csp_tes_pb_efficiency'],
        index=mod.CSP_GENS,
        param=(mod.csp_sf_tes_efficiency,
               mod.csp_tes_efficiency,
               mod.csp_tes_pb_efficiency,
               mod.csp_sf_tes_pb_efficiency,
               mod.csp_pb_efficiency))

    switch_data.load_aug(
        filename=os.path.join(inputs_dir, 'csp_sf_power_output.csv'),
        auto_select=True,
        index=mod.CSP_GEN_TPS,
        param=(mod.csp_sf_power_output_mwt))


def post_solve(instance, outdir):
    """
    Export CSP dispatch info to csp_dispatch.txt
    """
    import switch_model.reporting as reporting
    reporting.write_table(
#        instance, instance.CSP_GEN_TPS,
        instance, sorted(instance.CSP_GENS), sorted(instance.TIMEPOINTS),
        output_file=os.path.join(outdir, "csp_dispatch.csv"),
        headings=("project", "timepoint", "load_zone", "Capacity", 
                  "SF_Power_Output_MWt",
                  "ChargeTES_MWt", "TES_StateOfCharge_MWht",
                  "DischargeTES_MWt", "PB_Power_MWt",
                  "Excess_Power_MWt", "E_Power_MW"),
        values=lambda m, g, t: (
            g, m.tp_timestamp[t], m.gen_load_zone[g],
			(m.GenCapacity[g, m.tp_period[t]]),
            m.csp_sf_power_output_mwt[g, t] * (m.GenCapacity[g, m.tp_period[t]]),
            m.ChargeTES[g, t], m.TES_StateOfCharge[g, t],
            m.DischargeTES[g, t], m.DispatchGen[g, t]/ \
            (m.csp_pb_efficiency[g]*m.csp_sf_tes_pb_efficiency[g]),
            m.ExcessPower[g, t], m.DispatchGen[g, t]))