#!/usr/bin/env python

# script to output useful geometry optimisation data from .castep file to a more readable format


import sys

# file management for input file
filename = sys.argv[1]
file = open(filename, 'r')
contents = file.readlines()

OptDataList = []

# finds tolerances
x=0
y=0
while x == 0:
    line = contents[y]
    if "dE/ion" in line:
        dELine = line.split()
        dETol = dELine[5]               # pulls out dE/ion tolerance
    if "|F|max" in line:
        FLine = line.split()
        FTol = FLine[5]                 # pulls out Fmax Tol
    if "|dR|max" in line:
        dRLine = line.split()
        RTol = dRLine[5]                # pulls out dR tol
    if "Smax" in line:
        SLine = line.split()
        STol = SLine[5]                 # pulls out Smax tol
        x = 1
    y = y + 1

tolerance = ''.join(['Tol', '                  ', dETol, '  ', FTol, '  ', RTol, '  ', STol])


# iterates through document to find geometry optimisation data
for line in contents:
    if "with enthalpy=" in line:
        enthalpyLine = line.split()
        Iteration = enthalpyLine[3]     # pulls out the iteration number
        Enthalpy = enthalpyLine[6]      # pulls out the enthalpy
    if "dE/ion" in line:
        dELine = line.split()
        dEIon = dELine[3]               # pulls out dE/ion
        dEOK = dELine[9]                # pulls out whether dE/ion is optimised
    if "|F|max" in line:
        FLine = line.split()
        Fmax = FLine[3]                 # pulls out Fmax
        FOK = FLine[9]                  # pulls out whether Fmax is optimised
    if "|dR|max" in line:
        dRLine = line.split()
        dRmax = dRLine[3]               # pulls out dRmax
        dROK = dRLine[9]                # pulls out whether dRmax is optimised
    if "Smax" in line:
        SLine = line.split()
        Smax = SLine[3]                 # pulls out Smax
        SOK = SLine[9]                  # pulls out whether Smax is optimised

        OK_Stat_List = []
        if dEOK == "Yes":               # checks if optimisation was successful
            OK_Stat_List.append('E')
        if FOK == "Yes":
            OK_Stat_List.append('F')
        if dROK == "Yes":
            OK_Stat_List.append('R')
        if SOK == "Yes":
            OK_Stat_List.append('S')
        OK_Stat = "Yes"
        if len(OK_Stat_List) == 0:
            OK_Stat = ''
        else:
            if len(OK_Stat_List) == 4:
                OK_Stat = '[Yes!]'
            else:
                OK_Stat = ','.join(OK_Stat_List)



        if int(Iteration) >= 100:            # just a formatting thing
            spacer = ' '
        else:
            if int(Iteration) >= 10:
                spacer = '  '
            else:
                spacer = '   '


        OptData = ''.join([Iteration, spacer, Enthalpy, ' ', dEIon, '  ', Fmax, '  ', dRmax, '  ', Smax, '  ', OK_Stat]) # strings optimisation data together in convenient format
        OptDataList.append(OptData)

file.close()

# file management for output file
filePrefix = filename.split(".")[0]
outputFileName = "".join([filePrefix, '.ezGeom'])
outputFileOpen = open(outputFileName, 'w')

outputFileOpen.write("Iteration Enthalpy   dE/ion         |F|max         |dR|max        Smax         OK?" + '\n')
outputFileOpen.write(tolerance + '\n')

for dataSet in OptDataList:
    outputFileOpen.write(dataSet + '\n')

outputFileOpen.close()
