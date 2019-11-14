# plots dE, F, dR, and S from an ezGeom file for the purposes of convergence testing

import matplotlib.pyplot as plt
import numpy as np
import sys

file = sys.argv[1]
fileOpen = open(file, 'r')

seed = file.split('.')[0]
dE_filename = ''.join([seed, '_dE.png'])
F_filename = ''.join([seed, '_F.png'])
dR_filename = ''.join([seed, '_dR.png'])
S_filename = ''.join([seed, '_dS.png'])

lines = [line.rstrip('\n') for line in fileOpen]
noLines = len(lines)

ItList = []
enthalpyList = []
dEList = []
FList = []
dRList = []
SList = []

dETolList = []
FTolList = []
dRTolList = []
STolList = []

dataList = lines[1].split()
dETol = float(dataList[1])
FTol = float(dataList[2])
dRTol = float(dataList[3])
STol = float(dataList[4])

#iterates through lines and adds all data to lists
x = 2
while x < noLines:
    dataList = lines[x].split()
    ItList.append(x-2)
    enthalpyList.append(float(dataList[1]))
    dEList.append(float(dataList[2]))
    FList.append(float(dataList[3]))
    dRList.append(float(dataList[4]))
    SList.append(float(dataList[5]))
    dETolList.append(dETol)
    FTolList.append(FTol)
    dRTolList.append(dRTol)
    STolList.append(STol)
    x = x + 1

fig, ax = plt.subplots(figsize = (14,8))
ax.plot(ItList, enthalpyList, marker='x', color='#535154', linestyle='-')
plt.ylabel('Enthalpy / eV', fontsize='12')                                                           # sets axis labels
plt.xlabel('Iteration / eV', fontsize='12')
ax.grid(axis='y', linestyle='--', color='#808080')
plt.savefig(fname=S_filename, format='png')

fig, ax = plt.subplots(figsize = (14,8))
ax.plot(ItList, dEList, marker='x', color='#396ab1', linestyle='-')
ax.plot(ItList, dETolList, marker='', color='#000000', linestyle='--')
plt.ylabel('dE per Ion / eV', fontsize='12')                                                           # sets axis labels
plt.xlabel('Iteration / eV', fontsize='12')
ax.grid(axis='y', linestyle='--', color='#808080')
plt.savefig(fname=dE_filename, format='png')

fig, ax = plt.subplots(figsize = (14,8))
ax.plot(ItList, FList, marker='x', color='#da7c30', linestyle='-')
ax.plot(ItList, FTolList, marker='', color='#000000', linestyle='--')
plt.ylabel('|F|max / eV', fontsize='12')                                                           # sets axis labels
plt.xlabel('Iteration / eV', fontsize='12')
ax.grid(axis='y', linestyle='--', color='#808080')
plt.savefig(fname=F_filename, format='png')

fig, ax = plt.subplots(figsize = (14,8))
ax.plot(ItList, dRList, marker='x', color='#3e9651', linestyle='-')
ax.plot(ItList, dRTolList, marker='', color='#000000', linestyle='--')
plt.ylabel('|dR|max / eV', fontsize='12')                                                           # sets axis labels
plt.xlabel('Iteration / eV', fontsize='12')
ax.grid(axis='y', linestyle='--', color='#808080')
plt.savefig(fname=dR_filename, format='png')

fig, ax = plt.subplots(figsize = (14,8))
ax.plot(ItList, SList, marker='x', color='#cc2529', linestyle='-')
ax.plot(ItList, STolList, marker='', color='#000000', linestyle='--')
plt.ylabel('Smax / eV', fontsize='12')                                                           # sets axis labels
plt.xlabel('Iteration / eV', fontsize='12')
ax.grid(axis='y', linestyle='--', color='#808080')
plt.savefig(fname=S_filename, format='png')

plt.show()
