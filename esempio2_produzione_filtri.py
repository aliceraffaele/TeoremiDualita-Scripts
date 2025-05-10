#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 19:39:03 2025

@author: Alice Raffaele
"""

from pulp import *

# Inizializzazione del problema
model = LpProblem("Filtri", LpMaximize)

# Set e parametri
num_giorni = 6
prodotti = {"F1": 55, "F2": 60, "F3": 35, "F4": 40, "F5": 20}
fasi = {"Taglio": {"num": 3, "capacità": 16*60, "tempi": {"F1": 12, "F2": 20, "F3": 0, "F4": 25, "F5": 15}},
        "Plissettatura": {"num": 2, "capacità": 16*60, "tempi": {"F1": 10, "F2": 8, "F3": 16, "F4": 0, "F5": 0}},
        "Assemblaggio": {"num": 5, "capacità": 8*60, "tempi": {"F1": 15, "F2": 15, "F3": 18, "F4": 18, "F5": 18}}}

# Variabili
vars = LpVariable.dicts("x", prodotti.keys(), 0, None, LpContinuous)

# Funzione obiettivo
model += lpSum(vars[p] * prodotti[p] for p in prodotti.keys())

# Vincoli
for f in fasi:
    model += lpSum(vars[p]*fasi[f]["tempi"][p] for p in prodotti) <= fasi[f]["num"]*fasi[f]["capacità"]*num_giorni
    
# Chiamata al solver
model.solve()

# Stampa soluzione ottima trovata
for v in model.variables():
    if v.varValue > 0:
        print(v.name, " = ", v.varValue)

# Valore della funzione obiettivo
print("Profitto massimo = {}".format(round(value(model.objective),2)))