#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 10 12:41:29 2025

@author: Alice Raffaele
"""

from pulp import *

# Set e parametri
I = [x for x in range(10)]
durata_min = [20, 120, 60, 45, 15, 40, 100, 40, 30, 10]
durata_max = [30, 180, 75, 60, 25, 60, 150, 70, 45, 40]
priorità = [3, 4, 5, 3, 1, 7, 8, 7, 6, 2]
B = 300

for Gamma in range(len(I)+1):
    # Inizializzazione
    model = LpProblem("SalaOperatoria-ControparteRobusta", LpMaximize)
    
    # Variabili decisionali
    x = LpVariable.dicts("x", I, 0, None, LpBinary)
    q = LpVariable.dicts("q", I, 0, None, LpContinuous)
    s = LpVariable("s", 0, None, LpContinuous)
    
    # Funzione obiettivo
    model += lpSum(priorità[i] * x[i] for i in I)
    
    # Vincoli
    model += lpSum(durata_min[i] * x[i] for i in I) + Gamma * s + lpSum( q[i] for i in I) <= B
    
    for i in I:
        model += s + q[i] >= (durata_max[i] - durata_min[i]) * x[i]
    # Chiamata al solver
    model.solve()
    
    # Stampa soluzione ottima se trovata
    if LpStatus[model.status] == "Optimal":
        print("Soluzione ottima con Gamma = " + str(Gamma) + " - Interventi selezionati:")
        for v in model.variables():
            if v.varValue > 0:
                print(v.name, " = ", v.varValue)
            
        # Valore della funzione obiettivo
        print("\nMassima priorità totale = {}".format(round(value(model.objective),2)))
    
    elif LpStatus[model.status] == "Infeasible":
        print("Istanza non ammissibile")
    input()
    