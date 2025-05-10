#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 10 10:14:30 2025

@author: Alice Raffaele
"""

from pulp import *

# Inizializzazione
model = LpProblem("SalaOperatoria-DurataMassima", LpMaximize)

# Set e parametri
I = [x for x in range(10)]
durata_min = [20, 120, 60, 45, 15, 40, 100, 40, 30, 10]
durata_max = [30, 180, 75, 60, 25, 60, 150, 70, 45, 40]
priorità = [3, 4, 5, 3, 1, 7, 8, 7, 6, 2]
B = 300

# Variabili decisionali
x = LpVariable.dicts("x", I, 0, None, LpBinary)

# Funzione obiettivo
model += lpSum(priorità[i] * x[i] for i in I)

# Vincoli
model += lpSum(durata_max[i] * x[i] for i in I) <= B

# Chiamata al solver
model.solve()

# Stampa soluzione ottima se trovata
if LpStatus[model.status] == "Optimal":
    print("Soluzione ottima - Interventi selezionati:")
    for v in model.variables():
        if v.varValue > 0.5:
            print(v.name, " = ", v.varValue)
        
    # Valore della funzione obiettivo
    print("\nMassima priorità totale = {}".format(round(value(model.objective),2)))

elif LpStatus[model.status] == "Infeasible":
    print("Istanza non ammissibile")