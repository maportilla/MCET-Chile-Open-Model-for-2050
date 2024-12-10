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
    mod.TX_BUDGET_DUMMY_SET = Set(initialize=[0])

#   Parameters
    mod.max_tx_budget = Param(
        mod.TX_BUDGET_DUMMY_SET,
        within=NonNegativeReals,
        default=50000)

    
#   Thermal power balance equation
    def Tx_budget_rule(m):
        return sum(m.BuildTx[tx,p] for tx,p in m.TRANS_BLD_YRS) <= m.max_tx_budget[0]

    mod.Tx_Budget_Constraint = Constraint(
        rule=Tx_budget_rule)

        

def load_inputs(mod, switch_data, inputs_dir):
    switch_data.load_aug(
        filename=os.path.join(inputs_dir, 'tx_budget.csv'),
        select=(
            "TX_BUDGET_DUMMY_SET", "max_tx_budget"
        ),
        index=mod.TX_BUDGET_DUMMY_SET,
        param=(mod.max_tx_budget))



def post_solve(instance, outdir):
    pass