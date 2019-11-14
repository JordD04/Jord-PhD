#!/usr/bin/env python

# LZCT = LaZy Convergence Testing
# script for automating CASTEP convergence testing

import sys
import os
import subprocess
import math

# imports data from command line
seed = sys.argv[1]                              # filename seed
DFTvariable = sys.argv[2]                       # c to vary cutoff, k to vary kpoints
variableMin = float(sys.argv[3])                # minimum value of variable
variableMax = float(sys.argv[4])                # maximum value of variable
varStep = float(sys.argv[5])                    # change in variable per step

#seed = 'Si'                         # filename seed
#DFTvariable = 'c'                   # c to vary cutoff, k to vary kpoints
#variableMin = 300                   # minimum value of variable
#variableMax = 500                   # maximum value of variable
#varStep = 100                       # change in variable per step

# finds path and works out whether path uses / or \
path = os.getcwd()
backslashCount = path.count("\\")
forwardslashCount = path.count("/")
if forwardslashCount > backslashCount:
    dirChar = "/"                        # variable used for navigating directories
else:
    dirChar = "\\"
path = path + dirChar


# finds all the variables
variableList = []
nextVariable = variableMin
while nextVariable <= variableMax:
    variableList.append(str(nextVariable))
    nextVariable = round(nextVariable + varStep, 4)
print(variableList)

# saves contents of job file
jobFileName = ''.join([seed, '.job'])
with (open(jobFileName, 'r')) as jobFile:
    jobFileContents = jobFile.read()
jobFile.close()


def jobScriptMaker(path, directoryName, seed, i):
    # makes job scrips and creates initial directory
    dirPath = path + directoryName
    jobFileName = ''.join([dirPath, seed, '_', i, '.job'])
    os.mkdir(dirPath)
    open(jobFileName, 'w').write(jobFileContents)
    (open(jobFileName, 'r')).close()

    return dirPath, jobFileName;

# saves cell and param files when cutoff is changing
def varCutoffInput(seed):
    #saves cell file and finds kpoint line
    cellFileName = ''.join([seed, '.cell'])
    cellFile = (open(cellFileName, 'r'))
    for line in cellFile:
        if "kpoint_mp_spacing" in line or "KPOINT_MP_SPACING" in line:
            kpointSplit = line.split()
            kpoint = kpointSplit[len(kpointSplit)-1]
        else:
            pass
    cellFileContents = (open(cellFileName, 'r')).read()
    cellFile.close()

    #saves param file and finds cutoff line
    paramFileName = ''.join([seed, '.param'])
    paramFile = (open(paramFileName, 'r'))
    paramFileContents1 = []                     #first half of param file
    paramFileContents2 = []                     #second half of param file
    cutoff_position = -1
    lineCount = 0
    for line in paramFile:
        if "cut_off_energy" in line or "CUT_OFF_ENERGY" in line:
            cutoff_position = lineCount
        else:
            if cutoff_position > -1:            #tests if cut_off_energy line has been found
                paramFileContents2.append(line)
            else:
                paramFileContents1.append(line)
            lineCount + 1

    paramFile.close()

    return kpoint, cellFileContents, paramFileContents1, paramFileContents2;

# creates cell and param files with cutoff is varying
def varCutoffOutput(seed, dirPath, cellFileContents, paramFileContents1, paramFileContents2, i):
    #prints cell file to directory
    cellFileName = ''.join([dirPath, seed, ".cell"])
    open(cellFileName, 'w').write(cellFileContents)
    (open(cellFileName, 'r')).close()

    #prints param file to directory
    paramFileName = ''.join([dirPath, seed, ".param"])
    cutoff_line =  ''.join(["cut_off_energy : ", i, "\n"])
    paramFileContents0 = []
    for line in paramFileContents1:
        paramFileContents0.append(line)
    paramFileContents0.append(cutoff_line)
    for line in paramFileContents2:
        paramFileContents0.append(line)
    paramFileContents0 = ''.join(paramFileContents0)
    open(paramFileName, 'w').write(paramFileContents0)
    (open(paramFileName, 'r')).close()

def varKpointInput(seed):
    #saves cell file and finds kpoint line
    paramFileName = ''.join([seed, '.param'])
    paramFile = (open(paramFileName, 'r'))
    for line in paramFile:
        if "cut_off_energy" in line or "CUT_OFF_ENERGY" in line:
            cutoffSplit = line.split()
            cutoff = cutoffSplit[len(cutoffSplit)-1]
        else:
            pass
    paramFileContents = (open(paramFileName, 'r')).read()
    paramFile.close()

    #saves param file and finds cutoff line
    cellFileName = ''.join([seed, '.cell'])
    cellFile = (open(cellFileName, 'r'))
    cellFileContents1 = []                      #first half of cell file
    cellFileContents2 = []                      #second half of cell file
    kpoint_position = -1
    lineCount = 0
    for line in cellFile:
        if "kpoint_mp_spacing" in line or "KPOINT_MP_SPACING" in line:
            kpoint_position = lineCount
        else:
            if kpoint_position > -1:            #tests if kpoint_energy line has been found
                cellFileContents2.append(line)
            else:
                cellFileContents1.append(line)
            lineCount + 1

    paramFile.close()

    return cutoff, paramFileContents, cellFileContents1, cellFileContents2;

def varKpointOutput(seed, dirPath, paramFileContents, cellFileContents1, cellFileContents2, i):
    #prints cell file to directory
    paramFileName = ''.join([dirPath, seed, ".param"])
    open(paramFileName, 'w').write(paramFileContents)
    (open(paramFileName, 'r')).close()

    #prints param file to directory
    cellFileName = ''.join([dirPath, seed, ".cell"])
    cutoff_line =  ''.join(["kpoint_mp_spacing ", i, "\n"])
    cellFileContents0 = []
    for line in cellFileContents1:
        cellFileContents0.append(line)
    cellFileContents0.append(cutoff_line)
    for line in cellFileContents2:
        cellFileContents0.append(line)
    cellFileContents0 = ''.join(cellFileContents1)
    open(cellFileName, 'w').write(cellFileContents0)
    (open(cellFileName, 'r')).close()



# sets up convergence testing with variable cutoff
if DFTvariable == "c":
    kpoint, cellFileContents, paramFileContents1, paramFileContents2 = varCutoffInput(seed)
    for i in variableList:
        directoryName = ''.join([seed, "-", str(math.trunc(float(i))), "-", kpoint, dirChar])  # determines name of new directory for const kpoint
        dirPath, jobFileName = jobScriptMaker(path, directoryName, seed, i)
        varCutoffOutput(seed, dirPath, cellFileContents, paramFileContents1, paramFileContents2, i)
        subprocess.run(["sbatch", "-D", dirPath, jobFileName])

# sets up convergence testing with variable kpoint spacing
if DFTvariable == "k":
    cutoff, paramFileContents, cellFileContents1, cellFileContents2 = varKpointInput(seed)
    for i in variableList:
        directoryName = ''.join([seed, "-", cutoff, "-", i, dirChar])                           # determines name of new directory for const cutoff
        dirPath = jobScriptMaker(path, directoryName, seed, i)
        varKpointOutput(seed, dirPath, paramFileContents, cellFileContents1, cellFileContents2, i)
        subprocess.run(["sbatch", "-D", dirPath, jobFileName])