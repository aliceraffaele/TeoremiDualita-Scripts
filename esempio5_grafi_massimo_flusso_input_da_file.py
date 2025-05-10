#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 11:10:03 2025

@author: Alice Raffaele
"""

from pulp import *

def leggi_istanza(filename):
    f = open(filename, "r")
    row = f.readline()
    # La prima riga contiene il numero di nodi e il numero di archi da leggere
    nb_nodes = int(row.split()[0])
    nb_arcs = int(row.split()[1])
    # Lettura dei nodi
    row = f.readline()
    V = [v.replace("\n", "") for v in row.split()]
    source = V[0]
    dest = V[1]
    # Lettura degli archi
    A = {}
    for i in range(nb_arcs):
        row = f.readline()
        endpoint1 = row.split()[0]
        endpoint2 = row.split()[1]
        weight = int(row.split()[2])
        assert(endpoint1 in V and endpoint2 in V)
        A[(endpoint1, endpoint2)] = weight
    f.close()
    return V, A, source, dest

def risolvi_modello(V, A, source, dest):
    # Inizializzazione
    model = LpProblem("MassimoFlusso", LpMaximize)
    
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
        

V, A, source, dest = leggi_istanza("esempio5_revisione_pari.txt")
risolvi_modello(V, A, source, dest)
