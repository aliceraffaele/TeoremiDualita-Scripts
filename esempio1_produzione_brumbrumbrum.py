#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 15:39:03 2025

@author: Alice Raffaele
"""

from pulp import *

# Inizializzazione del problema
model = LpProblem("BrumBrumBrum", LpMaximize)

# Set e parametri
auto = ["Utilitaria", "Minicar"]
ricavi = {"Utilitaria": 16000, "Minicar": 10000}
macchine = ["M1", "M2"]
capacità = {"M1": 40, "M2": 60}
tempi = {"M1": {"Utilitaria": 1, "Minicar": 2}, "M2": {"Utilitaria": 3, "Minicar": 2}}
nb_max_utilitarie = 13

# Variabili
vars = LpVariable.dicts("x", auto, 0, None, LpContinuous)

# Funzione obiettivo
model += lpSum(vars[i] * ricavi[i] for i in auto)

# Vincoli
for m in macchine:
    model += lpSum(vars[i]*tempi[m][i] for i in auto) <= capacità[m]
model += vars["Utilitaria"] <= nb_max_utilitarie
# Chiamata al solver
model.solve()

# Stampa soluzione ottima trovata
for v in model.variables():
    if v.varValue > 0:
        print(v.name, " = ", v.varValue)

# Valore della funzione obiettivo
print("Ricavo massimo = {}".format(round(value(model.objective),2)))
