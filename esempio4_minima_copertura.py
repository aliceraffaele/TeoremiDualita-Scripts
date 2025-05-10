#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 12:55:35 2025

@author: Alice Raffaele
"""

from pulp import *

# Inizializzazione
model = LpProblem("MinimaCopertura", LpMinimize)

# Set e parametri
V = ["U1", "U2", "U3", "U4", "U5", "W1", "W2", "W3", "W4"]
E = [("U1", "W1"), ("U2", "W1"), ("U2", "W2"), ("U3", "W3"), ("U3", "W4"), ("U4", "W2"), ("U5", "W1"), ("U5", "W4")]

# Variabili decisionali
x = LpVariable.dicts("x", V, 0, None, LpContinuous)

# Funzione obiettivo
model += lpSum(x[v] for v in V) 

# Vincoli
for e in E:
    model += lpSum(x[v] for v in V if v in e) >= 1

# Chiamata al solver
model.solve()

# Stampa soluzione ottima se trovata
if LpStatus[model.status] == "Optimal":
    print("Soluzione ottima:")
    for v in model.variables():
        if v.varValue > 0:
            print(v.name, " = ", v.varValue)
        
    # Valore della funzione obiettivo
    print("\nMinimo numero di vertici di copertura = {}".format(round(value(model.objective),2)))

elif LpStatus[model.status] == "Infeasible":
    print("Istanza non ammissibile")