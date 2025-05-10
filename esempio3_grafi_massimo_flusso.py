#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 11:10:03 2025

@author: Alice Raffaele
"""

from pulp import *

# Inizializzazione
model = LpProblem("MassimoFlusso", LpMaximize)

# Set e parametri
V = ['S', 'A', 'B', 'C', 'D', 'E', 'T']
A = {
     ('S', 'A'): 14,
     ('S', 'B'): 15,
     ('A', 'B'): 3,
     ('A', 'C'): 4,
     ('A', 'D'): 8,
     ('B', 'C'): 7,
     ('B', 'E'): 9,
     ('C', 'D'): 6,
     ('C', 'E'): 5,
     ('D', 'T'): 11,
     ('E', 'T'): 16}

source = 'S'
dest = 'T'

# Variabili decisionali
x = LpVariable.dicts("x", A.keys(), 0, None, LpContinuous)
phi = LpVariable("phi", 0, None, LpContinuous)

# Funzione obiettivo
model += phi 

# Vincoli
for i,j in A.keys():
    model += x[i,j] <= A[i,j]
    
model += lpSum(x[i,j] for i,j in A.keys() if i == source) == phi
model += lpSum(x[i,j] for i,j in A.keys() if j == dest) == phi

for v in V:
    if v not in [source, dest]:
        model += lpSum(x[i,j] for i,j in A.keys() if j == v) == lpSum(x[i,j] for i,j in A.keys() if i == v)

# Chiamata al solver
model.solve()

# Stampa soluzione ottima se trovata
if LpStatus[model.status] == "Optimal":
    print("Soluzione ottima:")
    for v in model.variables():
        if v.varValue > 0:
            print(v.name, " = ", v.varValue)
        
    # Valore della funzione obiettivo
    print("\nMassimo flusso = {}".format(round(value(model.objective),2)))

elif LpStatus[model.status] == "Infeasible":
    print("Istanza non ammissibile")